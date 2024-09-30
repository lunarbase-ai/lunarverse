# SPDX-FileCopyrightText: Copyright © 2024 João Gabriel Oliveira <jgoliveira84@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import json

from typing import Any, Dict, List, Optional

from lunarcore.core.component import BaseComponent
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType

from langchain_community.tools.wikidata.tool import WikidataAPIWrapper, WikidataQueryRun
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, load_tools
from langchain_openai import OpenAI
from langchain_community.tools import ShellTool


class ReactAgent(
    BaseComponent,
    component_name="ReACT Agent",
    component_description="Implements ReACT logic.",
    input_types={
        "query": DataType.TEXT,
        "tools": DataType.LIST,
    },
    output_type=DataType.TEXT,
    component_group=ComponentGroup.GENAI,
    tools_config="{}",
    openai_api_key="",
    openai_api_version="$LUNARENV::REACT_OPENAI_API_VERSION",
    openai_api_key="$LUNARENV::REACT_OPENAI_API_KEY",
    model_name="$LUNARENV::REACT_OPENAI_MODEL_NAME",
    enable_unsupported_tools="false"

):
    DEFAULT_REACT_PROMPT = "hwchase17/react"
    CUSTOM_INSTANTIATED_TOOLS = {
        "wikidata": (lambda _opts: WikidataQueryRun(
            api_wrapper=WikidataAPIWrapper())
        ),
        "bash": (lambda _opts: ShellTool()),
    }

    DEFAULT_INSTANTIATED_TOOLS = [
        "arxiv",
        "bash",
        "wikipedia",
        "wolfram-alpha"
        "terminal",
    ]

    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)
        self._llm = OpenAI(
            temperature=0,
            openai_api_key=self.configuration.get(
                "openai_api_key", ""
            ),

        )

    def _load_tools(
        self,
        tools: List[str],
        opts: Dict[str, Any],
    ) -> List[Any]:
        
        opts_to_use = {t: opts.get(t, {}) for t in tools}

        loaded_tools = [(load_tools(
            [t],
            **opts_to_use[t]
        )[0] if t not in self.CUSTOM_INSTANTIATED_TOOLS else self.CUSTOM_INSTANTIATED_TOOLS[t](opts_to_use[t])) for t in tools]

        return loaded_tools
    
    def _validate_tools(self, tools: List[str]):
        invalid_tools = set(tools).difference(
            set(self.DEFAULT_INSTANTIATED_TOOLS + list(self.CUSTOM_INSTANTIATED_TOOLS.keys()))
        )
        if len(invalid_tools) > 0:
            raise ValueError(f"Invalid tools: {invalid_tools}")

    def run(self, query: str, tools: List):
        opts = json.loads(self.configuration.get("tools_config", "{}"))
        enable_unsupported_tools = self.configuration.get(
            "enable_unsupported_tools", "false") == "true"

        if not enable_unsupported_tools:
            self._validate_tools(tools)

        try:
            tools = self._load_tools(
                tools,
                opts,
            )
        except Exception as e:
            logging.error(f"Error loading tools: {e}")
            logging.error(
                "You may need to pass additional configurations. "
                "Example: {\"tool_name\": {\"config_name\": \"config_value\"}})"
            )
            raise e

        prompt = hub.pull(self.DEFAULT_REACT_PROMPT)

        agent = create_react_agent(
            self._llm,
            tools,
            prompt,
        )
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
        )

        return agent_executor.invoke(
            {"input": query}
        ).get("output", "")
