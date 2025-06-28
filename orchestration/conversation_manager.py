from typing import Dict, List, Optional, Any
from .router import AgentRouter
import asyncio
from datetime import datetime
import json

class ConversationManager:
    def __init__(self, router: AgentRouter):
        self.router = router
        self.conversation_state: Dict[str, Dict] = {}
        self.conversation_history: Dict[str, List[Dict]] = {}
        self.active_sessions: Dict[str, bool] = {}
    
    async def process_user_input(self, user_id: str, message: str) -> str:
        """Process user input and coordinate agent responses"""
        
        # Initialize conversation state if new user
        if user_id not in self.conversation_state:
            await self._initialize_conversation(user_id)
        
        # Log the message
        await self._log_message(user_id, "user", message)
        
        # Analyze the message to determine task type and requirements
        task = await self._analyze_user_message(user_id, message)
        
        # Route to appropriate agent
        response = await self.router.route_task(task)
        
        # Log the response
        await self._log_message(user_id, "assistant", response)
        
        return response
    
    async def _initialize_conversation(self, user_id: str):
        """Initialize conversation state for new user"""
        self.conversation_state[user_id] = {
            "started_at": datetime.now().isoformat(),
            "context": {},
            "preferences": {},
            "last_activity": datetime.now().isoformat()
        }
        self.conversation_history[user_id] = []
        self.active_sessions[user_id] = True
        print(f"Initialized conversation for user: {user_id}")
    
    async def _log_message(self, user_id: str, role: str, content: str):
        """Log message to conversation history"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.conversation_history[user_id].append(message)
        
        # Update last activity
        if user_id in self.conversation_state:
            self.conversation_state[user_id]["last_activity"] = datetime.now().isoformat()
    
    async def _analyze_user_message(self, user_id: str, message: str) -> Dict:
        """Analyze user message to determine task requirements"""
        
        # Simple keyword-based analysis (in production, use LLM for this)
        task_type = "general"
        capabilities = []
        
        message_lower = message.lower()
        
        # Determine task type based on keywords
        if any(keyword in message_lower for keyword in ["search", "find", "research", "look up"]):
            task_type = "research"
            capabilities = ["web_search", "data_analysis"]
        elif any(keyword in message_lower for keyword in ["plan", "schedule", "organize", "break down"]):
            task_type = "planning"
            capabilities = ["task_decomposition", "workflow_planning"]
        elif any(keyword in message_lower for keyword in ["analyze", "report", "summarize"]):
            task_type = "analysis"
            capabilities = ["data_analysis", "report_generation"]
        elif any(keyword in message_lower for keyword in ["code", "program", "implement", "develop"]):
            task_type = "coding"
            capabilities = ["code_generation", "debugging"]
        
        # Get conversation context
        context = self.conversation_state.get(user_id, {}).get("context", {})
        history = self.conversation_history.get(user_id, [])[-5:]  # Last 5 messages
        
        task = {
            "type": task_type,
            "message": message,
            "user_id": user_id,
            "capabilities": capabilities,
            "context": context,
            "conversation_history": history,
            "timestamp": datetime.now().isoformat()
        }
        
        return task
    
    async def get_conversation_history(self, user_id: str, limit: Optional[int] = None) -> List[Dict]:
        """Get conversation history for user"""
        history = self.conversation_history.get(user_id, [])
        if limit:
            return history[-limit:]
        return history
    
    async def update_conversation_context(self, user_id: str, context_updates: Dict):
        """Update conversation context for user"""
        if user_id in self.conversation_state:
            self.conversation_state[user_id]["context"].update(context_updates)
            print(f"Updated context for user {user_id}: {context_updates}")
    
    async def set_user_preferences(self, user_id: str, preferences: Dict):
        """Set user preferences"""
        if user_id not in self.conversation_state:
            await self._initialize_conversation(user_id)
        
        self.conversation_state[user_id]["preferences"] = preferences
        print(f"Set preferences for user {user_id}: {preferences}")
    
    async def end_conversation(self, user_id: str):
        """End conversation for user"""
        if user_id in self.active_sessions:
            self.active_sessions[user_id] = False
            print(f"Ended conversation for user: {user_id}")
    
    async def cleanup_inactive_conversations(self, hours: int = 24):
        """Cleanup conversations inactive for specified hours"""
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        
        inactive_users = []
        for user_id, state in self.conversation_state.items():
            last_activity = datetime.fromisoformat(state["last_activity"])
            if last_activity.timestamp() < cutoff_time:
                inactive_users.append(user_id)
        
        for user_id in inactive_users:
            await self._cleanup_user_data(user_id)
            print(f"Cleaned up inactive conversation for user: {user_id}")
    
    async def _cleanup_user_data(self, user_id: str):
        """Clean up data for a specific user"""
        if user_id in self.conversation_state:
            del self.conversation_state[user_id]
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        total_conversations = len(self.conversation_state)
        active_conversations = sum(1 for active in self.active_sessions.values() if active)
        total_messages = sum(len(history) for history in self.conversation_history.values())
        
        return {
            "total_conversations": total_conversations,
            "active_conversations": active_conversations,
            "total_messages": total_messages,
            "router_status": await self.router.get_agent_status()
        }
    
    async def start_multi_agent_conversation(self, user_id: str, agents: List[str], topic: str) -> str:
        """Start a multi-agent conversation"""
        conversation_id = f"multi_{user_id}_{datetime.now().timestamp()}"
        
        # Initialize multi-agent context
        multi_context = {
            "type": "multi_agent",
            "agents": agents,
            "topic": topic,
            "started_at": datetime.now().isoformat()
        }
        
        await self.update_conversation_context(user_id, {"multi_agent": multi_context})
        
        # Notify agents about the multi-agent session
        for agent_id in agents:
            if agent_id in self.router.agents:
                # Send notification to agent about multi-agent session
                pass
        
        return f"Started multi-agent conversation with {len(agents)} agents on topic: {topic}" 