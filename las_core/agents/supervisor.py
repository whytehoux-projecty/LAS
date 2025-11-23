from typing import Literal
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from services.llm_service import get_llm_service
from config.settings import settings
from .state import GraphState

members = ["Planner", "WebSurfer", "Coder"]
system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers: {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)

options = ["FINISH"] + members
function_def = {
    "name": "route",
    "description": "Select the next role.",
    "parameters": {
        "title": "routeSchema",
        "type": "object",
        "properties": {
            "next": {
                "title": "Next",
                "anyOf": [
                    {"enum": options},
                ],
            }
        },
        "required": ["next"],
    },
}

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Given the conversation above, who should act next?"
            " Or should we FINISH? Select one of: {options}",
        ),
    ]
).partial(options=str(options), members=", ".join(members))

class SupervisorAgent:
    def __init__(self):
        self.llm_service = get_llm_service()
        # Note: We need an LLM that supports function calling or structured output for this to work best.
        # If using Ollama, we might need a different approach or a model that supports JSON mode well.
        self.llm = self.llm_service.provider # This needs to be a LangChain compatible LLM object
        
        # For now, assuming the provider exposes a LangChain LLM or we wrap it.
        # In Phase 1 we used a custom Provider class. We might need to adapt it to LangChain here
        # or use ChatOllama directly if settings.provider_name is ollama.
        
        # Placeholder for actual LangChain LLM instantiation based on settings
        from langchain_community.chat_models import ChatOllama
        self.llm = ChatOllama(model=settings.provider_model, base_url=settings.provider_server_address)

        self.chain = (
            prompt
            | self.llm.bind_functions(functions=[function_def], function_call="route")
            | JsonOutputFunctionsParser()
        )

    def run(self, state: GraphState):
        return self.chain.invoke(state)

def get_supervisor_chain():
    return SupervisorAgent().chain
