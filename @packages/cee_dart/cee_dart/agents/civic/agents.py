from typing import List, Dict, Any, Optional
from openai import AzureOpenAI
import json
from datetime import datetime
from cee_dart.agents.civic.config import Config
from cee_dart.agents.civic.models import UserInput, BioExpertOutput, EvaluatorOutput, EvaluationStatus, TokenUsage, AgentExecution
from cee_dart.agents.civic.prompts import ORCHESTRATOR_PROMPT, BIOEXPERT_PROMPT, EVALUATOR_PROMPT
import re

class BaseAgent:
    """Base class for all agents."""
    
    def __init__(self, name: str, system_prompt: str, client: AzureOpenAI):
        self.name = name
        self.system_prompt = system_prompt
        self.client = client
        self.current_execution: Optional[AgentExecution] = None
    
    def start_execution(self) -> AgentExecution:
        """Start tracking execution for this agent."""
        self.current_execution = AgentExecution(
            agent_name=self.name,
            start_time=datetime.now()
        )
        return self.current_execution
    
    def end_execution(self) -> AgentExecution:
        """End tracking execution for this agent."""
        if self.current_execution:
            self.current_execution.end_time = datetime.now()
        return self.current_execution
    
    def _call_openai(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Make a call to OpenAI API with token tracking."""
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages,
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_TOKENS,
                **kwargs
            )
            
            # Track token usage if execution is being tracked
            if self.current_execution and hasattr(response, 'usage') and response.usage:
                self.current_execution.token_usage.prompt_tokens += response.usage.prompt_tokens or 0
                self.current_execution.token_usage.completion_tokens += response.usage.completion_tokens or 0
                self.current_execution.token_usage.total_tokens += response.usage.total_tokens or 0
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {e}")

class OrchestratorAgent(BaseAgent):
    """Orchestrator agent that coordinates the workflow in pure Python routing logic."""
    
    def __init__(self, client: AzureOpenAI):
        super().__init__("Orchestrator", ORCHESTRATOR_PROMPT, client=client)
    
    def coordinate_workflow(self, user_input: UserInput) -> str:
        """Coordinate the overall workflow purely by routing data without LLM calls."""
        # Orchestrator handles routing between agents, iteration tracking, and escalation logic
        return f"Orchestrator: routing user input to BioExpert. Context length: {len(user_input.context)} chars, " \
               f"Question: '{user_input.question}', Evidence characters: {len(user_input.evidence)}"

class BioExpertAgent(BaseAgent):
    """BioExpert agent that analyzes biomedical evidence."""
    
    def __init__(self, client: AzureOpenAI):
        super().__init__("BioExpert", BIOEXPERT_PROMPT, client=client)
    
    def analyze(self, user_input: UserInput, previous_output: Optional[BioExpertOutput] = None, 
                evaluator_feedback: Optional[str] = None, iteration: int = 1) -> BioExpertOutput:
        """Analyze evidence or revise based on feedback."""
        # Handle evidence as string
        print(" BioExpertAgent user_input.evidence:\n", user_input.evidence)
        print(f" BioExpertAgent evidence length: {len(user_input.evidence) if user_input.evidence else 0}")
        print(f" BioExpertAgent evidence type: {type(user_input.evidence)}")
        evidence_text = user_input.evidence if user_input.evidence else "No evidence provided."
        
        print(" BioExpertAgent evidence_text:\n", evidence_text)
        print(f" BioExpertAgent evidence_text length: {len(evidence_text)}")
        
        # Check if evidence is meaningful (more than just gene name)
        if evidence_text and len(evidence_text.strip()) > 0:
            lines = evidence_text.split('\n')
            meaningful_lines = [line for line in lines if line.strip() and not line.startswith("Gene:")]
            print(f" BioExpertAgent meaningful evidence lines: {len(meaningful_lines)}")
            if meaningful_lines:
                print(f" BioExpertAgent first meaningful line: {meaningful_lines[0][:100]}...")
        else:
            print(" BioExpertAgent: No meaningful evidence detected")
        
        if previous_output and evaluator_feedback:
            # build a string from the structured previous output
            prev = previous_output
            prev_str = "\n".join([
                f"Relevance Explanation: {prev.relevance_explanation}",
                "Summary/Conclusion:",
                *[f"- {line}" for line in prev.summary_conclusion]
            ])
            user_message = f"""
                            Please revise your previous analysis based on the evaluator's feedback.

                            Original Context: {user_input.context}
                            Original Question: {user_input.question}

                            Evidence:
                            {evidence_text}

                            Previous Analysis (Iteration {prev.iteration}):
                            {prev_str}

                            Evaluator Feedback:
                            {evaluator_feedback}

                            Please provide an improved, structured analysis addressing each point of feedback.
                            """
        else:
            user_message = f"""
                            Context: {user_input.context}
                            Question: {user_input.question}
                            Evidence:
                            {evidence_text}

                            As the BioExpert Agent, analyze the evidence and answer the question in a structured format with relevance explanation and summary/conclusion. Cite evidence sources explicitly.
                            """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]
        raw = self._call_openai(messages)
        
        # Clean up any markdown code blocks if present
        raw = raw.strip()
        if raw.startswith('```json'):
            raw = raw[7:]  # Remove ```json
        if raw.startswith('```'):
            raw = raw[3:]  # Remove ```
        if raw.endswith('```'):
            raw = raw[:-3]  # Remove trailing ```
        raw = raw.strip()
        
        # Try to parse as JSON first
        try:
            import json
            parsed = json.loads(raw)
            return BioExpertOutput(
                relevance_explanation=parsed.get("relevance_explanation", ""),
                summary_conclusion=parsed.get("summary_conclusion", []),
                iteration=iteration
            )
        except (json.JSONDecodeError, KeyError):
            # Fallback to regex parsing if JSON parsing fails
            pass
        
        # parse into sections using regex as fallback
        m = re.search(
            r"Relevance Explanation:(.*?)Summary/Conclusion:(.*)",
            raw, re.DOTALL | re.IGNORECASE
        )
        if m:
            relevance = m.group(1).strip()
            summary_block = m.group(2).strip()
            summary_lines = [
                line.strip("- ").strip()
                for line in summary_block.splitlines()
                if line.strip().startswith("-")
            ]
        else:
            # fallback: put all in relevance explanation
            relevance, summary_lines = raw.strip(), []
        
        return BioExpertOutput(
            relevance_explanation=relevance,
            summary_conclusion=summary_lines,
            iteration=iteration
        )

class EvaluatorAgent(BaseAgent):
    """Evaluator agent that reviews BioExpert analyses."""
    
    def __init__(self, client: AzureOpenAI):
        super().__init__("Evaluator", EVALUATOR_PROMPT, client=client)
    
    def evaluate(self, user_input: UserInput, bioexpert_output: BioExpertOutput) -> EvaluatorOutput:
        """Evaluate the BioExpert's analysis."""
        # Handle evidence as string
        evidence_text = user_input.evidence if user_input.evidence else "No evidence provided."
        
        # construct analysis block from structured fields
        summary_block = "\n".join(f"- {pt}" for pt in bioexpert_output.summary_conclusion)
        user_message = f"""
Please evaluate the following biomedical evidence analysis:

Original Context: {user_input.context}
Original Question: {user_input.question}

Evidence Provided:
{evidence_text}

BioExpert Analysis (Iteration {bioexpert_output.iteration}):
Relevance Explanation:
{bioexpert_output.relevance_explanation}

Summary/Conclusion:
{summary_block}

Respond exactly with:
- "APPROVED" if the analysis meets quality standards
- Or "NOT APPROVED" followed by specific, actionable feedback
Focus on scientific accuracy, clarity, citation, and completeness.
"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]
        feedback = self._call_openai(messages).strip()
        status = EvaluationStatus.APPROVED if feedback.startswith(EvaluationStatus.APPROVED.value) \
                 else EvaluationStatus.NOT_APPROVED
        
        # extract bullet/numbered feedback points
        points: List[str] = []
        if status == EvaluationStatus.NOT_APPROVED:
            for line in feedback.splitlines()[1:]:
                if line.strip().startswith(("-", "*")) or re.match(r"\d+\.", line.strip()):
                    points.append(line.lstrip("-*0123456789. ").strip())
        
        return EvaluatorOutput(
            status=status,
            feedback_points=points
        )
