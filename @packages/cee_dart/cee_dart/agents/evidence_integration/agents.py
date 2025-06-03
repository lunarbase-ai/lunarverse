from typing import List, Dict, Any, Optional
from openai import AzureOpenAI
import json
import re
from datetime import datetime
from cee_dart.utils.openai_client import client

from cee_dart.agents.evidence_integration.config import Config
from cee_dart.agents.evidence_integration.models import (UserInput, ReportComposerOutput, EvaluatorOutput, CriticOutput, 
                    DeliberationOutput, EvaluationStatus, ConsolidatedEvidence,
                    TokenUsage, AgentExecution)
from cee_dart.agents.evidence_integration.prompts import (ORCHESTRATOR_PROMPT, REPORT_COMPOSER_PROMPT, CONTENT_VALIDATOR_PROMPT, 
                        CRITICAL_REVIEWER_PROMPT, RELEVANCE_VALIDATOR_PROMPT)


class BaseAgent:
    """Base class for all agents."""
    
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        # self.client = AzureOpenAI(api_key=Config.OPENAI_API_KEY)
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
    """Orchestrator agent that coordinates the workflow and extracts evidence from consolidated files."""
    
    def __init__(self):
        super().__init__("Orchestrator", ORCHESTRATOR_PROMPT)
    
    def coordinate_workflow(self, consolidated_evidence: ConsolidatedEvidence) -> str:
        """Coordinate the overall workflow purely by routing data without LLM calls."""
        total_evidence_length = len(consolidated_evidence.combined_evidence)
        return (f"Orchestrator: routing consolidated evidence to Report Composer. "
                f"CIVIC genes: {consolidated_evidence.total_genes_civic}, "
                f"PharmGKB genes: {consolidated_evidence.total_genes_pharmgkb}, "
                f"Gene sets: {consolidated_evidence.total_gene_sets_enrichment}, "
                f"Total evidence length: {total_evidence_length} chars")
    
    def extract_evidence_from_files(self, civic_file: str, pharmgkb_file: str, 
                                   gene_enrichment_file: str) -> ConsolidatedEvidence:
        """Extract and consolidate evidence from the three analysis files."""
        civic_evidence = ""
        pharmgkb_evidence = ""
        gene_enrichment_evidence = ""
        
        total_genes_civic = 0
        total_genes_pharmgkb = 0
        total_gene_sets_enrichment = 0
        
        # Extract CIVIC evidence
        try:
            with open(civic_file, 'r', encoding='utf-8') as f:
                civic_data = json.load(f)
                total_genes_civic = civic_data.get('summary_stats', {}).get('total_genes', 0)
                
                civic_analyses = []
                for gene, analysis in civic_data.get('gene_analyses', {}).items():
                    # For consolidated analyses, use a cleaner format
                    if 'Consolidated_Analysis' in gene:
                        civic_analyses.append(analysis.get('final_analysis', ''))
                    else:
                        civic_analyses.append(f"Gene: {gene}\n{analysis.get('final_analysis', '')}")
                
                civic_evidence = "\n\n".join(civic_analyses)
        except Exception as e:
            print(f"Warning: Could not load CIVIC file {civic_file}: {e}")
        
        # Extract PharmGKB evidence
        try:
            with open(pharmgkb_file, 'r', encoding='utf-8') as f:
                pharmgkb_data = json.load(f)
                total_genes_pharmgkb = pharmgkb_data.get('summary_stats', {}).get('total_genes', 0)
                
                pharmgkb_analyses = []
                for gene, analysis in pharmgkb_data.get('gene_analyses', {}).items():
                    # For consolidated analyses, use a cleaner format
                    if 'Consolidated_Analysis' in gene:
                        pharmgkb_analyses.append(analysis.get('final_analysis', ''))
                    else:
                        pharmgkb_analyses.append(f"Gene: {gene}\n{analysis.get('final_analysis', '')}")
                
                pharmgkb_evidence = "\n\n".join(pharmgkb_analyses)
        except Exception as e:
            print(f"Warning: Could not load PharmGKB file {pharmgkb_file}: {e}")
        
        # Extract Gene Enrichment evidence
        try:
            with open(gene_enrichment_file, 'r', encoding='utf-8') as f:
                enrichment_data = json.load(f)
                total_gene_sets_enrichment = enrichment_data.get('summary_stats', {}).get('total_gene_sets', 0)
                
                enrichment_analyses = []
                for gene_set, analysis in enrichment_data.get('gene_set_analyses', {}).items():
                    # For consolidated analyses, use a cleaner format
                    if 'Consolidated_Analysis' in gene_set:
                        enrichment_analyses.append(analysis.get('final_analysis', ''))
                    else:
                        enrichment_analyses.append(f"Gene Set: {gene_set}\n{analysis.get('final_analysis', '')}")
                
                gene_enrichment_evidence = "\n\n".join(enrichment_analyses)
        except Exception as e:
            print(f"Warning: Could not load Gene Enrichment file {gene_enrichment_file}: {e}")
        
        # Combine all evidence
        evidence_sections = []
        if civic_evidence:
            evidence_sections.append(f"=== CIVIC EVIDENCE ===\n{civic_evidence}")
        if pharmgkb_evidence:
            evidence_sections.append(f"=== PHARMGKB EVIDENCE ===\n{pharmgkb_evidence}")
        if gene_enrichment_evidence:
            evidence_sections.append(f"=== GENE ENRICHMENT EVIDENCE ===\n{gene_enrichment_evidence}")
        
        combined_evidence = "\n\n".join(evidence_sections)
        
        return ConsolidatedEvidence(
            civic_evidence=civic_evidence,
            pharmgkb_evidence=pharmgkb_evidence,
            gene_enrichment_evidence=gene_enrichment_evidence,
            combined_evidence=combined_evidence,
            total_genes_civic=total_genes_civic,
            total_genes_pharmgkb=total_genes_pharmgkb,
            total_gene_sets_enrichment=total_gene_sets_enrichment
        )

class ReportComposerAgent(BaseAgent):
    """Report Composer agent that integrates evidence into structured reports."""
    
    def __init__(self):
        super().__init__("ReportComposer", REPORT_COMPOSER_PROMPT)
    
    def compose_report(self, user_input: UserInput, consolidated_evidence: ConsolidatedEvidence,
                      previous_output: Optional[ReportComposerOutput] = None, 
                      combined_feedback: Optional[str] = None, iteration: int = 1) -> ReportComposerOutput:
        """Compose a structured report or revise based on feedback."""
        
        if previous_output and combined_feedback:
            # Revision based on feedback
            prev_report = previous_output
            user_message = f"""
Please revise your previous unified report based on the feedback from all reviewing agents.

Original Context: {user_input.context}
Original Question: {user_input.question}

Consolidated Evidence:
{consolidated_evidence.combined_evidence}

Previous Report (Iteration {prev_report.iteration}):
Potential Novel Biomarkers: {prev_report.potential_novel_biomarkers}
Implications: {prev_report.implications}
Well-Known Interactions: {prev_report.well_known_interactions}
Conclusions: {prev_report.conclusions}

Combined Feedback from All Agents:
{combined_feedback}

Please provide an improved, structured report addressing all feedback points while maintaining the required sections.
"""
        else:
            # Initial report composition
            user_message = f"""
Context: {user_input.context}
Question: {user_input.question}

Consolidated Evidence from Three Analysis Systems:
{consolidated_evidence.combined_evidence}

As the Report Composer Agent, create a unified report that integrates evidence from CIVIC, PharmGKB, and Gene Enrichment analyses. Structure your response with the four required sections and provide comprehensive analysis that addresses the research question.
"""
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]
        raw = self._call_openai(messages)
        
        # Clean up any markdown code blocks if present
        raw = raw.strip()
        if raw.startswith('```json'):
            raw = raw[7:]
        if raw.startswith('```'):
            raw = raw[3:]
        if raw.endswith('```'):
            raw = raw[:-3]
        raw = raw.strip()
        
        # Try to parse as JSON first
        try:
            parsed = json.loads(raw)
            return ReportComposerOutput(
                potential_novel_biomarkers=parsed.get("potential_novel_biomarkers", ""),
                implications=parsed.get("implications", ""),
                well_known_interactions=parsed.get("well_known_interactions", ""),
                conclusions=parsed.get("conclusions", ""),
                iteration=iteration
            )
        except (json.JSONDecodeError, KeyError):
            # Fallback to regex parsing if JSON parsing fails
            pass
        
        # Parse sections using regex as fallback
        sections = {
            "potential_novel_biomarkers": "",
            "implications": "",
            "well_known_interactions": "",
            "conclusions": ""
        }
        
        # Try to extract sections from the raw text
        for section_name in sections.keys():
            pattern = rf"{section_name.replace('_', ' ').title()}[:\s]+(.*?)(?=\n\n[A-Z]|\Z)"
            match = re.search(pattern, raw, re.DOTALL | re.IGNORECASE)
            if match:
                sections[section_name] = match.group(1).strip()
        
        # If regex fails, put everything in the first section
        if not any(sections.values()):
            sections["potential_novel_biomarkers"] = raw.strip()
        
        return ReportComposerOutput(
            potential_novel_biomarkers=sections["potential_novel_biomarkers"],
            implications=sections["implications"],
            well_known_interactions=sections["well_known_interactions"],
            conclusions=sections["conclusions"],
            iteration=iteration
        )

class ContentValidatorAgent(BaseAgent):
    """Content Validator agent that validates structural integrity and content quality."""
    
    def __init__(self):
        super().__init__("Content Validator", CONTENT_VALIDATOR_PROMPT)
    
    def evaluate(self, user_input: UserInput, report_output: ReportComposerOutput,
                consolidated_evidence: ConsolidatedEvidence) -> EvaluatorOutput:
        """Evaluate the Report Composer's output for structural integrity and content quality."""
        
        user_message = f"""
Please evaluate the following unified biomedical report:

Original Context: {user_input.context}
Original Question: {user_input.question}

Available Evidence Summary:
- CIVIC genes analyzed: {consolidated_evidence.total_genes_civic}
- PharmGKB genes analyzed: {consolidated_evidence.total_genes_pharmgkb}
- Gene sets analyzed: {consolidated_evidence.total_gene_sets_enrichment}

Report Composer Output (Iteration {report_output.iteration}):

Potential Novel Biomarkers:
{report_output.potential_novel_biomarkers}

Implications:
{report_output.implications}

Well-Known Interactions:
{report_output.well_known_interactions}

Conclusions:
{report_output.conclusions}

Evaluate for structural integrity, content quality, and completeness. Respond with "APPROVED" or "NOT APPROVED" followed by specific feedback if needed.
"""
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]
        feedback = self._call_openai(messages).strip()
        status = EvaluationStatus.APPROVED if feedback.startswith(EvaluationStatus.APPROVED.value) \
                 else EvaluationStatus.NOT_APPROVED
        
        # Extract feedback points
        points: List[str] = []
        if status == EvaluationStatus.NOT_APPROVED:
            for line in feedback.splitlines()[1:]:
                if line.strip().startswith(("-", "*")) or re.match(r"\d+\.", line.strip()):
                    points.append(line.strip().lstrip("-*0123456789. "))
        
        return EvaluatorOutput(status=status, feedback_points=points)

class CriticalReviewerAgent(BaseAgent):
    """Critical Reviewer agent that provides critical analysis and identifies biases."""
    
    def __init__(self):
        super().__init__("Critical Reviewer", CRITICAL_REVIEWER_PROMPT)
    
    def critique(self, user_input: UserInput, report_output: ReportComposerOutput,
                consolidated_evidence: ConsolidatedEvidence) -> CriticOutput:
        """Provide critical analysis of the Report Composer's output."""
        
        user_message = f"""
Please provide critical analysis of the following unified biomedical report:

Original Context: {user_input.context}
Original Question: {user_input.question}

Available Evidence Summary:
- CIVIC genes analyzed: {consolidated_evidence.total_genes_civic}
- PharmGKB genes analyzed: {consolidated_evidence.total_genes_pharmgkb}
- Gene sets analyzed: {consolidated_evidence.total_gene_sets_enrichment}

Report Composer Output (Iteration {report_output.iteration}):

Potential Novel Biomarkers:
{report_output.potential_novel_biomarkers}

Implications:
{report_output.implications}

Well-Known Interactions:
{report_output.well_known_interactions}

Conclusions:
{report_output.conclusions}

Analyze for potential biases, unsupported claims, and alternative interpretations. Respond with "APPROVED" or "NOT APPROVED" followed by specific critical feedback if needed.
"""
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]
        feedback = self._call_openai(messages).strip()
        status = EvaluationStatus.APPROVED if feedback.startswith(EvaluationStatus.APPROVED.value) \
                 else EvaluationStatus.NOT_APPROVED
        
        # Extract feedback points
        points: List[str] = []
        if status == EvaluationStatus.NOT_APPROVED:
            for line in feedback.splitlines()[1:]:
                if line.strip().startswith(("-", "*")) or re.match(r"\d+\.", line.strip()):
                    points.append(line.strip().lstrip("-*0123456789. "))
        
        return CriticOutput(status=status, feedback_points=points)

class RelevanceValidatorAgent(BaseAgent):
    """Relevance Validator agent that explores question alignment and validates novelty assessments."""
    
    def __init__(self):
        super().__init__("Relevance Validator", RELEVANCE_VALIDATOR_PROMPT)
    
    def deliberate(self, user_input: UserInput, report_output: ReportComposerOutput,
                  consolidated_evidence: ConsolidatedEvidence) -> DeliberationOutput:
        """Provide question alignment validation and novelty assessment analysis."""
        
        user_message = f"""
Please provide critical deliberation analysis focusing on whether this report truly answers the user's question and the basis for novelty assessments:

Original Context: {user_input.context}
Original Question: {user_input.question}

Available Evidence Summary:
- CIVIC genes analyzed: {consolidated_evidence.total_genes_civic}
- PharmGKB genes analyzed: {consolidated_evidence.total_genes_pharmgkb}
- Gene sets analyzed: {consolidated_evidence.total_gene_sets_enrichment}

Report Composer Output (Iteration {report_output.iteration}):

Potential Novel Biomarkers:
{report_output.potential_novel_biomarkers}

Implications:
{report_output.implications}

Well-Known Interactions:
{report_output.well_known_interactions}

Conclusions:
{report_output.conclusions}

CRITICAL EVALUATION FOCUS:
1. Does this report actually answer the user's specific question: "{user_input.question}"?
2. What is the basis for classifying evidence as "novel" vs "well-known"?
3. Are the conclusions logically supported by the evidence?

Respond with "APPROVED" or "NOT APPROVED" followed by specific deliberation feedback focusing on question alignment and novelty assessment basis.
"""
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]
        feedback = self._call_openai(messages).strip()
        status = EvaluationStatus.APPROVED if feedback.startswith(EvaluationStatus.APPROVED.value) \
                 else EvaluationStatus.NOT_APPROVED
        
        # Extract feedback points
        points: List[str] = []
        if status == EvaluationStatus.NOT_APPROVED:
            for line in feedback.splitlines()[1:]:
                if line.strip().startswith(("-", "*")) or re.match(r"\d+\.", line.strip()):
                    points.append(line.strip().lstrip("-*0123456789. "))
        
        return DeliberationOutput(status=status, feedback_points=points)

# Keep old names as aliases for backward compatibility
EvaluatorAgent = ContentValidatorAgent
CriticAgent = CriticalReviewerAgent
DeliberationAgent = RelevanceValidatorAgent
