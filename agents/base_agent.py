from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from llm_providers.base import BaseLLMProvider
from mcp_integration.server import MCPServerManager
from a2a_protocol.communication import A2AClient

class BaseAgent(ABC):
    def __init__(self, agent_id: str, llm_provider: BaseLLMProvider, 
                 mcp_manager: MCPServerManager, a2a_client: A2AClient):
        self.agent_id = agent_id
        self.llm_provider = llm_provider
        self.mcp_manager = mcp_manager
        self.a2a_client = a2a_client
        self.tools: List[str] = []
        self.memory: Dict[str, Any] = {}
        self.capabilities: List[str] = []
        self.status = "idle"
    
    @abstractmethod
    async def process_task(self, task: Dict) -> Dict:
        """Process a task and return results"""
        pass
    
    async def initialize(self):
        """Initialize the agent (setup tools, register with services, etc.)"""
        await self._register_tools()
        await self._register_with_registry()
        print(f"Agent {self.agent_id} initialized with capabilities: {self.capabilities}")
    
    async def _register_tools(self):
        """Register tools with MCP server"""
        for tool_name in self.tools:
            # In a real implementation, this would register actual tool functions
            await self.mcp_manager.register_tool(
                tool_name, 
                self._get_tool_function(tool_name),
                self._get_tool_schema(tool_name)
            )
    
    async def _register_with_registry(self):
        """Register this agent with the A2A registry"""
        from a2a_protocol.agent_registry import AgentCard
        
        card = AgentCard(
            agent_id=self.agent_id,
            name=self.__class__.__name__,
            description=f"Agent specialized in {', '.join(self.capabilities)}",
            capabilities=self.capabilities,
            endpoints={"mcp": "stdio", "http": f"http://localhost:8000/agents/{self.agent_id}"},
            authentication={"type": "api_key"},
            metadata={"version": "1.0.0", "tools": self.tools}
        )
        
        await self.a2a_client.registry.register_agent(card)
    
    def _get_tool_function(self, tool_name: str):
        """Get the function for a specific tool"""
        # This would map tool names to actual functions
        # For now, return a placeholder
        async def placeholder_tool(**kwargs):
            return f"Tool {tool_name} executed with args: {kwargs}"
        return placeholder_tool
    
    def _get_tool_schema(self, tool_name: str) -> Dict:
        """Get the schema for a specific tool"""
        # Return a basic schema for each tool
        return {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": f"Execute {tool_name} tool",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
    
    async def update_memory(self, key: str, value: Any):
        """Update agent memory"""
        self.memory[key] = value
    
    async def get_memory(self, key: str) -> Any:
        """Get value from agent memory"""
        return self.memory.get(key)
    
    async def clear_memory(self):
        """Clear agent memory"""
        self.memory.clear()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "status": self.status,
            "capabilities": self.capabilities,
            "tools": self.tools,
            "memory_keys": list(self.memory.keys())
        }
    
    async def set_status(self, status: str):
        """Set agent status"""
        self.status = status
        await self.a2a_client.broadcast_status({"agent_id": self.agent_id, "status": status})
    
    async def delegate_to_other_agent(self, target_agent: str, task: Dict) -> Dict:
        """Delegate a task to another agent"""
        try:
            result = await self.a2a_client.delegate_task(target_agent, task)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def collaborate_with_agents(self, agent_ids: List[str], task: Dict) -> Dict:
        """Collaborate with multiple agents on a task"""
        results = {}
        
        for agent_id in agent_ids:
            try:
                result = await self.delegate_to_other_agent(agent_id, task)
                results[agent_id] = result
            except Exception as e:
                results[agent_id] = {"success": False, "error": str(e)}
        
        return results
    
    async def shutdown(self):
        """Shutdown the agent gracefully"""
        await self.set_status("shutting_down")
        await self.a2a_client.registry.unregister_agent(self.agent_id)
        await self.clear_memory()
        print(f"Agent {self.agent_id} shut down successfully") 