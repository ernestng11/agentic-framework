from typing import Dict, List, Optional, Any
from llm_providers.factory import LLMProviderFactory
from mcp_integration.server import MCPServerManager
from a2a_protocol.communication import A2AClient

class AgentRouter:
    def __init__(self, llm_manager: LLMProviderFactory, mcp_manager: MCPServerManager, a2a_client: A2AClient):
        self.llm_manager = llm_manager
        self.mcp_manager = mcp_manager
        self.a2a_client = a2a_client
        self.agents: Dict[str, Any] = {}
        self.routing_rules: Dict[str, List[str]] = {}
    
    async def route_task(self, task: Dict) -> str:
        """Route task to appropriate agent based on capabilities"""
        task_type = task.get("type", "general")
        required_capabilities = task.get("capabilities", [])
        
        # Analyze task requirements
        best_agent = await self._select_best_agent(task_type, required_capabilities)
        
        if not best_agent:
            return f"No suitable agent found for task type: {task_type}"
        
        # Coordinate execution
        try:
            result = await self._execute_task_with_agent(best_agent, task)
            return result
        except Exception as e:
            return f"Error executing task with agent {best_agent}: {str(e)}"
    
    async def _select_best_agent(self, task_type: str, required_capabilities: List[str]) -> Optional[str]:
        """Select best agent for the task"""
        
        # First check if we have routing rules for this task type
        if task_type in self.routing_rules:
            for agent_id in self.routing_rules[task_type]:
                if agent_id in self.agents:
                    agent = self.agents[agent_id]
                    if self._agent_has_capabilities(agent, required_capabilities):
                        return agent_id
        
        # Fallback: find any agent with required capabilities
        for agent_id, agent in self.agents.items():
            if self._agent_has_capabilities(agent, required_capabilities):
                return agent_id
        
        # Use A2A protocol to discover external agents
        if required_capabilities:
            for capability in required_capabilities:
                external_agents = await self.a2a_client.registry.discover_agents(capability)
                if external_agents:
                    return external_agents[0].agent_id
        
        return None
    
    def _agent_has_capabilities(self, agent: Any, required_capabilities: List[str]) -> bool:
        """Check if agent has required capabilities"""
        if not required_capabilities:
            return True
        
        agent_capabilities = getattr(agent, 'capabilities', [])
        return all(cap in agent_capabilities for cap in required_capabilities)
    
    async def _execute_task_with_agent(self, agent_id: str, task: Dict) -> str:
        """Execute task with selected agent"""
        if agent_id in self.agents:
            # Local agent execution
            agent = self.agents[agent_id]
            result = await agent.process_task(task)
            return f"Task completed by {agent_id}: {result}"
        else:
            # External agent execution via A2A
            result = await self.a2a_client.delegate_task(agent_id, task)
            return f"Task delegated to {agent_id}: {result}"
    
    def register_agent(self, agent_id: str, agent: Any):
        """Register an agent with the router"""
        self.agents[agent_id] = agent
        print(f"Registered agent: {agent_id}")
    
    def unregister_agent(self, agent_id: str):
        """Unregister an agent from the router"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            print(f"Unregistered agent: {agent_id}")
    
    def add_routing_rule(self, task_type: str, agent_ids: List[str]):
        """Add routing rule for specific task type"""
        self.routing_rules[task_type] = agent_ids
        print(f"Added routing rule: {task_type} -> {agent_ids}")
    
    def remove_routing_rule(self, task_type: str):
        """Remove routing rule for task type"""
        if task_type in self.routing_rules:
            del self.routing_rules[task_type]
            print(f"Removed routing rule for: {task_type}")
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all registered agents"""
        status = {}
        for agent_id, agent in self.agents.items():
            try:
                agent_status = getattr(agent, 'get_status', lambda: {"status": "unknown"})()
                status[agent_id] = agent_status
            except Exception as e:
                status[agent_id] = {"status": "error", "error": str(e)}
        
        return status
    
    async def list_capabilities(self) -> Dict[str, List[str]]:
        """List capabilities of all registered agents"""
        capabilities = {}
        for agent_id, agent in self.agents.items():
            agent_capabilities = getattr(agent, 'capabilities', [])
            capabilities[agent_id] = agent_capabilities
        
        return capabilities 