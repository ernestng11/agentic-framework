from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json

@dataclass
class AgentCard:
    agent_id: str
    name: str
    description: str
    capabilities: List[str]
    endpoints: Dict[str, str]
    authentication: Dict[str, str]
    metadata: Dict[str, Any]

class AgentRegistry:
    def __init__(self):
        self.agents: Dict[str, AgentCard] = {}
    
    async def register_agent(self, card: AgentCard):
        """Register agent in distributed registry"""
        self.agents[card.agent_id] = card
        print(f"Registered agent: {card.name} ({card.agent_id})")
    
    async def discover_agents(self, capability: str) -> List[AgentCard]:
        """Find agents with specific capability"""
        matching_agents = [
            agent for agent in self.agents.values() 
            if capability in agent.capabilities
        ]
        return matching_agents
    
    async def get_agent(self, agent_id: str) -> Optional[AgentCard]:
        """Get agent by ID"""
        return self.agents.get(agent_id)
    
    async def unregister_agent(self, agent_id: str):
        """Unregister agent from registry"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            print(f"Unregistered agent: {agent_id}")
    
    async def list_all_agents(self) -> List[AgentCard]:
        """List all registered agents"""
        return list(self.agents.values())
    
    async def search_agents(self, query: str) -> List[AgentCard]:
        """Search agents by name or description"""
        query_lower = query.lower()
        matching_agents = []
        
        for agent in self.agents.values():
            if (query_lower in agent.name.lower() or 
                query_lower in agent.description.lower()):
                matching_agents.append(agent)
        
        return matching_agents
    
    def to_json(self) -> str:
        """Export registry to JSON"""
        agents_dict = {
            agent_id: {
                "agent_id": card.agent_id,
                "name": card.name,
                "description": card.description,
                "capabilities": card.capabilities,
                "endpoints": card.endpoints,
                "authentication": card.authentication,
                "metadata": card.metadata
            }
            for agent_id, card in self.agents.items()
        }
        return json.dumps(agents_dict, indent=2)
    
    @classmethod
    def from_json(cls, json_data: str) -> 'AgentRegistry':
        """Load registry from JSON"""
        registry = cls()
        data = json.loads(json_data)
        
        for agent_id, agent_data in data.items():
            card = AgentCard(**agent_data)
            registry.agents[agent_id] = card
        
        return registry 