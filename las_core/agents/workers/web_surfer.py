from langchain_core.messages import HumanMessage
from services.tool_service import get_tool_service
from config.settings import settings
from langchain_community.chat_models import ChatOllama
from langchain.tools import Tool

class WebSurferAgent:
    def __init__(self):
        self.llm = ChatOllama(model=settings.provider_model, base_url=settings.provider_server_address)
        self.tool_service = get_tool_service()

    def run(self, state):
        messages = state["messages"]
        # Logic to decide if to search or browse
        # For simplicity, we'll just assume the last message contains the instruction
        last_message = messages[-1].content
        
        if "search" in last_message.lower():
            # Use search tool
            # In a real implementation, we'd use function calling to extract query
            result = self.tool_service.execute_command("web_search", query=last_message, num_results=3)
            return {"messages": [HumanMessage(content=f"Search Results: {result}")]}
        elif "browse" in last_message.lower() or "http" in last_message:
             # Use browse tool
             # Extract URL (simplified)
             import re
             url = re.search(r'(https?://\S+)', last_message)
             if url:
                 result = self.tool_service.execute_command("browse_website", url=url.group(0))
                 return {"messages": [HumanMessage(content=f"Page Content: {result[:1000]}...")]}
        
        return {"messages": [HumanMessage(content="I'm not sure what to browse. Please provide a URL or search query.")]}

def web_surfer_node(state):
    agent = WebSurferAgent()
    # Need to make this async compatible if tool service is async
    # For now, assuming synchronous execution or handling async properly in the graph
    import asyncio
    # This is a hack for the example. In production, use async nodes.
    # result = asyncio.run(agent.run(state)) 
    # But since we are in a node, we might be able to just call it if the graph runner is async
    return agent.run(state)
