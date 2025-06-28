from typing import Dict, List, Any
from .base_agent import BaseAgent
from llm_providers.base import BaseLLMProvider, LLMConfig
from mcp_integration.server import MCPServerManager
from a2a_protocol.communication import A2AClient
import json
from datetime import datetime, timedelta

class PlanningAgent(BaseAgent):
    def __init__(self, agent_id: str, llm_provider: BaseLLMProvider, 
                 mcp_manager: MCPServerManager, a2a_client: A2AClient):
        super().__init__(agent_id, llm_provider, mcp_manager, a2a_client)
        self.capabilities = ["task_decomposition", "workflow_planning", "resource_allocation"]
        self.tools = ["calendar", "project_management", "timeline_generator", "resource_calculator"]
    
    async def process_task(self, task: Dict) -> Dict:
        """Handle planning and coordination tasks"""
        task_type = task.get("type", "general")
        message = task.get("message", "")
        
        await self.set_status("processing")
        
        try:
            if task_type == "task_decomposition" or "break down" in message.lower():
                result = await self._decompose_task(task)
            elif task_type == "workflow_planning" or "plan" in message.lower():
                result = await self._create_workflow_plan(task)
            elif task_type == "resource_allocation" or "resource" in message.lower():
                result = await self._allocate_resources(task)
            elif "schedule" in message.lower() or "timeline" in message.lower():
                result = await self._create_timeline(task)
            else:
                result = await self._general_planning(task)
            
            await self.set_status("idle")
            return {"success": True, "result": result, "agent": self.agent_id}
        
        except Exception as e:
            await self.set_status("error")
            return {"success": False, "error": str(e), "agent": self.agent_id}
    
    async def _decompose_task(self, task: Dict) -> str:
        """Break down complex tasks into manageable subtasks"""
        main_task = task.get("message", "")
        context = task.get("context", {})
        
        await self.update_memory("current_decomposition", main_task)
        
        llm_config = LLMConfig(
            model_name="claude-3-sonnet",  # Good for structured thinking
            temperature=0.3
        )
        
        decomposition_prompt = f"""
        You are an expert project manager. Break down this complex task into manageable subtasks:
        
        Main Task: "{main_task}"
        Context: {json.dumps(context, indent=2)}
        
        Provide:
        1. Clear task breakdown structure (WBS)
        2. Dependencies between tasks
        3. Estimated effort/time for each subtask
        4. Priority levels
        5. Required skills/resources
        
        Format as a structured plan.
        """
        
        try:
            decomposition = await self.llm_provider.generate_response(
                [{"role": "user", "content": decomposition_prompt}],
                llm_config
            )
            
            # Store the decomposition for future reference
            await self.update_memory("last_decomposition", {
                "task": main_task,
                "breakdown": decomposition,
                "created_at": datetime.now().isoformat()
            })
            
            return decomposition
            
        except Exception as e:
            return f"Error decomposing task: {str(e)}"
    
    async def _create_workflow_plan(self, task: Dict) -> str:
        """Create a detailed workflow plan"""
        project_description = task.get("message", "")
        requirements = task.get("context", {})
        
        await self.update_memory("current_workflow", project_description)
        
        llm_config = LLMConfig(
            model_name="claude-3-sonnet",
            temperature=0.2
        )
        
        workflow_prompt = f"""
        Create a comprehensive workflow plan for this project:
        
        Project: "{project_description}"
        Requirements: {json.dumps(requirements, indent=2)}
        
        Include:
        1. Project phases and milestones
        2. Task sequences and dependencies
        3. Resource requirements
        4. Risk assessment and mitigation
        5. Quality checkpoints
        6. Communication plan
        7. Success criteria
        
        Make it actionable and detailed.
        """
        
        try:
            workflow = await self.llm_provider.generate_response(
                [{"role": "user", "content": workflow_prompt}],
                llm_config
            )
            
            await self.update_memory("last_workflow", {
                "project": project_description,
                "plan": workflow,
                "created_at": datetime.now().isoformat()
            })
            
            return workflow
            
        except Exception as e:
            return f"Error creating workflow plan: {str(e)}"
    
    async def _allocate_resources(self, task: Dict) -> str:
        """Plan resource allocation for a project"""
        project_info = task.get("message", "")
        available_resources = task.get("context", {}).get("resources", {})
        
        await self.update_memory("current_allocation", project_info)
        
        llm_config = LLMConfig(
            model_name="gpt-4",
            temperature=0.3
        )
        
        allocation_prompt = f"""
        Plan optimal resource allocation for this project:
        
        Project: "{project_info}"
        Available Resources: {json.dumps(available_resources, indent=2)}
        
        Provide:
        1. Human resource allocation
        2. Budget distribution
        3. Technology/tool requirements
        4. Timeline considerations
        5. Resource optimization strategies
        6. Contingency planning
        7. Cost-benefit analysis
        
        Focus on efficiency and effectiveness.
        """
        
        try:
            allocation = await self.llm_provider.generate_response(
                [{"role": "user", "content": allocation_prompt}],
                llm_config
            )
            
            await self.update_memory("last_allocation", {
                "project": project_info,
                "allocation": allocation,
                "resources": available_resources,
                "created_at": datetime.now().isoformat()
            })
            
            return allocation
            
        except Exception as e:
            return f"Error allocating resources: {str(e)}"
    
    async def _create_timeline(self, task: Dict) -> str:
        """Create project timeline and schedule"""
        project_description = task.get("message", "")
        deadline = task.get("context", {}).get("deadline")
        
        await self.update_memory("current_timeline", project_description)
        
        # First decompose the task to get subtasks
        decomposition_result = await self._decompose_task(task)
        
        llm_config = LLMConfig(
            model_name="gpt-4",
            temperature=0.2
        )
        
        timeline_prompt = f"""
        Create a detailed project timeline based on this task breakdown:
        
        Project: "{project_description}"
        Deadline: {deadline or "Not specified"}
        Task Breakdown: {decomposition_result}
        
        Provide:
        1. Gantt chart-style timeline
        2. Critical path analysis
        3. Milestone dates
        4. Buffer time allocation
        5. Resource scheduling
        6. Risk windows
        7. Progress checkpoints
        
        Make it realistic and achievable.
        """
        
        try:
            timeline = await self.llm_provider.generate_response(
                [{"role": "user", "content": timeline_prompt}],
                llm_config
            )
            
            await self.update_memory("last_timeline", {
                "project": project_description,
                "timeline": timeline,
                "deadline": deadline,
                "created_at": datetime.now().isoformat()
            })
            
            return timeline
            
        except Exception as e:
            return f"Error creating timeline: {str(e)}"
    
    async def _general_planning(self, task: Dict) -> str:
        """Handle general planning requests"""
        message = task.get("message", "")
        
        # Determine the best planning approach
        if "break" in message.lower() or "decompose" in message.lower():
            return await self._decompose_task(task)
        elif "workflow" in message.lower() or "process" in message.lower():
            return await self._create_workflow_plan(task)
        elif "resource" in message.lower() or "allocate" in message.lower():
            return await self._allocate_resources(task)
        elif "timeline" in message.lower() or "schedule" in message.lower():
            return await self._create_timeline(task)
        else:
            # Comprehensive planning
            decomposition = await self._decompose_task(task)
            workflow = await self._create_workflow_plan(task)
            timeline = await self._create_timeline(task)
            
            return f"""
            Comprehensive Planning Report:
            
            TASK BREAKDOWN:
            {decomposition}
            
            WORKFLOW PLAN:
            {workflow}
            
            PROJECT TIMELINE:
            {timeline}
            """
    
    async def get_planning_history(self) -> Dict[str, Any]:
        """Get history of planning activities"""
        return {
            "last_decomposition": await self.get_memory("last_decomposition"),
            "last_workflow": await self.get_memory("last_workflow"),
            "last_allocation": await self.get_memory("last_allocation"),
            "last_timeline": await self.get_memory("last_timeline"),
            "current_project": {
                "decomposition": await self.get_memory("current_decomposition"),
                "workflow": await self.get_memory("current_workflow"),
                "allocation": await self.get_memory("current_allocation"),
                "timeline": await self.get_memory("current_timeline")
            }
        }
    
    async def create_project_summary(self) -> str:
        """Create a summary of all current planning activities"""
        history = await self.get_planning_history()
        
        summary = f"""
        Planning Agent Summary - {self.agent_id}
        ========================================
        
        Current Projects:
        - Task Decomposition: {history['current_project']['decomposition'] or 'None'}
        - Workflow Planning: {history['current_project']['workflow'] or 'None'}
        - Resource Allocation: {history['current_project']['allocation'] or 'None'}
        - Timeline Creation: {history['current_project']['timeline'] or 'None'}
        
        Agent Status: {self.status}
        Capabilities: {', '.join(self.capabilities)}
        
        Recent Activity:
        - Last decomposition: {history['last_decomposition']['created_at'] if history['last_decomposition'] else 'N/A'}
        - Last workflow: {history['last_workflow']['created_at'] if history['last_workflow'] else 'N/A'}
        - Last allocation: {history['last_allocation']['created_at'] if history['last_allocation'] else 'N/A'}
        - Last timeline: {history['last_timeline']['created_at'] if history['last_timeline'] else 'N/A'}
        """
        
        return summary 