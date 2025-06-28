from typing import Dict, List, Any
from .base_agent import BaseAgent
from llm_providers.base import BaseLLMProvider, LLMConfig
from mcp_integration.server import MCPServerManager
from a2a_protocol.communication import A2AClient

class ResearchAgent(BaseAgent):
    def __init__(self, agent_id: str, llm_provider: BaseLLMProvider, 
                 mcp_manager: MCPServerManager, a2a_client: A2AClient):
        super().__init__(agent_id, llm_provider, mcp_manager, a2a_client)
        self.capabilities = ["web_search", "data_analysis", "report_generation"]
        self.tools = ["web_search", "pdf_reader", "database_query", "summarize"]
    
    async def process_task(self, task: Dict) -> Dict:
        """Handle research-specific tasks"""
        task_type = task.get("type", "general")
        
        await self.set_status("processing")
        
        try:
            if task_type == "web_search" or "search" in task.get("message", "").lower():
                result = await self._perform_web_search(task.get("query", task.get("message", "")))
            elif task_type == "data_analysis" or "analyze" in task.get("message", "").lower():
                result = await self._analyze_data(task.get("data", task.get("message", "")))
            elif task_type == "report_generation" or "report" in task.get("message", "").lower():
                result = await self._generate_report(task)
            else:
                result = await self._general_research(task)
            
            await self.set_status("idle")
            return {"success": True, "result": result, "agent": self.agent_id}
        
        except Exception as e:
            await self.set_status("error")
            return {"success": False, "error": str(e), "agent": self.agent_id}
    
    async def _perform_web_search(self, query: str) -> str:
        """Perform web search for information"""
        await self.update_memory("last_search_query", query)
        
        # Use LLM to help refine search strategy
        llm_config = LLMConfig(
            model_name="gpt-3.5-turbo",  # Default model
            temperature=0.3
        )
        
        search_strategy_prompt = f"""
        You are a research assistant. Given the query: "{query}"
        
        1. Break down the search into key topics
        2. Suggest refined search terms
        3. Identify what types of sources would be most valuable
        
        Respond with a structured search plan.
        """
        
        try:
            search_plan = await self.llm_provider.generate_response(
                [{"role": "user", "content": search_strategy_prompt}],
                llm_config
            )
            
            # Simulate web search results
            search_results = f"""
            Search Plan: {search_plan}
            
            Simulated Search Results for: "{query}"
            
            1. Primary Source: Academic paper on the topic
            2. News Articles: Recent developments and trends
            3. Expert Opinions: Industry leader perspectives
            4. Statistical Data: Relevant metrics and figures
            
            Note: This is a simulation. In production, integrate with actual search APIs.
            """
            
            await self.update_memory("last_search_results", search_results)
            return search_results
            
        except Exception as e:
            return f"Error performing web search: {str(e)}"
    
    async def _analyze_data(self, data_description: str) -> str:
        """Analyze data and provide insights"""
        await self.update_memory("last_analysis_request", data_description)
        
        llm_config = LLMConfig(
            model_name="gpt-4",  # Use more capable model for analysis
            temperature=0.2
        )
        
        analysis_prompt = f"""
        You are a data analyst. Analyze the following data description: "{data_description}"
        
        Provide:
        1. Key patterns and trends
        2. Statistical insights
        3. Actionable recommendations
        4. Potential limitations or caveats
        
        Structure your analysis professionally.
        """
        
        try:
            analysis = await self.llm_provider.generate_response(
                [{"role": "user", "content": analysis_prompt}],
                llm_config
            )
            
            await self.update_memory("last_analysis", analysis)
            return analysis
            
        except Exception as e:
            return f"Error analyzing data: {str(e)}"
    
    async def _generate_report(self, task: Dict) -> str:
        """Generate comprehensive research report"""
        topic = task.get("message", "General Research Topic")
        context = task.get("context", {})
        
        await self.update_memory("current_report_topic", topic)
        
        # First, gather information
        search_results = await self._perform_web_search(topic)
        
        # Then analyze and synthesize
        llm_config = LLMConfig(
            model_name="gpt-4",
            temperature=0.4
        )
        
        report_prompt = f"""
        Generate a comprehensive research report on: "{topic}"
        
        Based on these search results: {search_results}
        
        Structure the report with:
        1. Executive Summary
        2. Background and Context
        3. Key Findings
        4. Analysis and Insights
        5. Recommendations
        6. Conclusion
        
        Make it professional and well-researched.
        """
        
        try:
            report = await self.llm_provider.generate_response(
                [{"role": "user", "content": report_prompt}],
                llm_config
            )
            
            await self.update_memory("last_report", report)
            return report
            
        except Exception as e:
            return f"Error generating report: {str(e)}"
    
    async def _general_research(self, task: Dict) -> str:
        """Handle general research requests"""
        message = task.get("message", "")
        
        # Determine the best research approach
        if "search" in message.lower() or "find" in message.lower():
            return await self._perform_web_search(message)
        elif "analyze" in message.lower() or "examine" in message.lower():
            return await self._analyze_data(message)
        else:
            # Default to comprehensive research
            search_result = await self._perform_web_search(message)
            analysis = await self._analyze_data(f"Research findings: {search_result}")
            
            return f"Research Results:\n{search_result}\n\nAnalysis:\n{analysis}"
    
    async def get_research_history(self) -> Dict[str, Any]:
        """Get history of research activities"""
        return {
            "last_search_query": await self.get_memory("last_search_query"),
            "last_search_results": await self.get_memory("last_search_results"), 
            "last_analysis": await self.get_memory("last_analysis"),
            "last_report": await self.get_memory("last_report"),
            "current_report_topic": await self.get_memory("current_report_topic")
        }
    
    async def export_research_data(self) -> str:
        """Export research data for external use"""
        history = await self.get_research_history()
        
        export_data = f"""
        Research Agent Export - {self.agent_id}
        ======================================
        
        Recent Search Query: {history.get('last_search_query', 'N/A')}
        
        Last Analysis Request: {await self.get_memory('last_analysis_request')}
        
        Current Report Topic: {history.get('current_report_topic', 'N/A')}
        
        Agent Status: {self.status}
        Capabilities: {', '.join(self.capabilities)}
        """
        
        return export_data 