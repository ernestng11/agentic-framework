from typing import Dict, Any, Optional
from .agent_registry import AgentRegistry, AgentCard
import asyncio
import json
from datetime import datetime

class A2AClient:
    def __init__(self, agent_id: str, registry: AgentRegistry):
        self.agent_id = agent_id
        self.registry = registry
        self.status_listeners = {}
        self.message_queue = asyncio.Queue()
    
    async def delegate_task(self, target_agent: str, task: Dict) -> Dict:
        """Delegate task to another agent"""
        target_card = await self.registry.get_agent(target_agent)
        if not target_card:
            raise ValueError(f"Agent {target_agent} not found in registry")
        
        # Prepare task message
        message = {
            "from": self.agent_id,
            "to": target_agent,
            "type": "task_delegation",
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "message_id": f"{self.agent_id}_{target_agent}_{datetime.now().timestamp()}"
        }
        
        try:
            # In a real implementation, this would send via the appropriate transport
            # For now, simulate the delegation
            result = await self._send_message(target_card, message)
            return result
        except Exception as e:
            raise Exception(f"Failed to delegate task to {target_agent}: {str(e)}")
    
    async def broadcast_status(self, status: Dict):
        """Broadcast status to interested agents"""
        message = {
            "from": self.agent_id,
            "type": "status_update",
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        
        # Broadcast to all agents that have registered interest
        for listener_id in self.status_listeners.keys():
            try:
                await self._send_status_update(listener_id, message)
            except Exception as e:
                print(f"Failed to send status to {listener_id}: {str(e)}")
    
    async def subscribe_to_status(self, agent_id: str):
        """Subscribe to status updates from another agent"""
        self.status_listeners[agent_id] = True
        print(f"Subscribed to status updates from {agent_id}")
    
    async def unsubscribe_from_status(self, agent_id: str):
        """Unsubscribe from status updates from another agent"""
        if agent_id in self.status_listeners:
            del self.status_listeners[agent_id]
            print(f"Unsubscribed from status updates from {agent_id}")
    
    async def send_direct_message(self, target_agent: str, message: str) -> Dict:
        """Send direct message to another agent"""
        target_card = await self.registry.get_agent(target_agent)
        if not target_card:
            raise ValueError(f"Agent {target_agent} not found in registry")
        
        message_payload = {
            "from": self.agent_id,
            "to": target_agent,
            "type": "direct_message",
            "content": message,
            "timestamp": datetime.now().isoformat(),
            "message_id": f"{self.agent_id}_{target_agent}_{datetime.now().timestamp()}"
        }
        
        try:
            result = await self._send_message(target_card, message_payload)
            return result
        except Exception as e:
            raise Exception(f"Failed to send message to {target_agent}: {str(e)}")
    
    async def _send_message(self, target_card: AgentCard, message: Dict) -> Dict:
        """Send message to target agent (implementation depends on transport)"""
        # In a real implementation, this would use the appropriate transport
        # based on the target_card.endpoints configuration
        
        # For simulation, return a mock response
        return {
            "status": "delivered",
            "response": f"Message delivered to {target_card.agent_id}",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _send_status_update(self, target_agent: str, message: Dict):
        """Send status update to a specific agent"""
        target_card = await self.registry.get_agent(target_agent)
        if target_card:
            await self._send_message(target_card, message)
    
    async def receive_messages(self) -> Optional[Dict]:
        """Receive incoming messages"""
        try:
            message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
            return message
        except asyncio.TimeoutError:
            return None
    
    async def handle_incoming_message(self, message: Dict) -> Dict:
        """Handle incoming message from another agent"""
        message_type = message.get("type")
        
        if message_type == "task_delegation":
            return await self._handle_task_delegation(message)
        elif message_type == "status_update":
            return await self._handle_status_update(message)
        elif message_type == "direct_message":
            return await self._handle_direct_message(message)
        else:
            return {"error": f"Unknown message type: {message_type}"}
    
    async def _handle_task_delegation(self, message: Dict) -> Dict:
        """Handle incoming task delegation"""
        # Add to message queue for processing by the agent
        await self.message_queue.put(message)
        return {"status": "accepted", "message": "Task delegation received"}
    
    async def _handle_status_update(self, message: Dict) -> Dict:
        """Handle incoming status update"""
        print(f"Status update from {message['from']}: {message['status']}")
        return {"status": "received"}
    
    async def _handle_direct_message(self, message: Dict) -> Dict:
        """Handle incoming direct message"""
        print(f"Direct message from {message['from']}: {message['content']}")
        await self.message_queue.put(message)
        return {"status": "received"} 