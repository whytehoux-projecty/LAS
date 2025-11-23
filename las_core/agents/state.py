from typing import TypedDict, Annotated, Sequence, Union
from langchain_core.messages import BaseMessage
import operator

class GraphState(TypedDict):
    """
    Represents the state of the agent graph.
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    task: str
    plan: str
    outputs: dict
