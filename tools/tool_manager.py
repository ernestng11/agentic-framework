from typing import Dict, Any, Callable, List, Optional
import asyncio
import inspect

class ToolManager:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.tool_schemas: Dict[str, Dict] = {}
        self.tool_metadata: Dict[str, Dict] = {}
    
    def register_tool(self, name: str, func: Callable, schema: Dict, metadata: Optional[Dict] = None):
        """Register a new tool"""
        self.tools[name] = func
        self.tool_schemas[name] = schema
        self.tool_metadata[name] = metadata or {}
        print(f"Registered tool: {name}")
    
    async def execute_tool(self, name: str, arguments: Dict) -> Any:
        """Execute tool with given arguments"""
        if name not in self.tools:
            raise ValueError(f"Tool {name} not found")
        
        func = self.tools[name]
        
        try:
            # Check if the function is async
            if inspect.iscoroutinefunction(func):
                result = await func(**arguments)
            else:
                result = func(**arguments)
            
            return {
                "success": True,
                "result": result,
                "tool": name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tool": name
            }
    
    def get_tool_schema(self, name: str) -> Dict:
        """Get tool schema for LLM tool calling"""
        return self.tool_schemas.get(name, {})
    
    def list_tools(self) -> List[str]:
        """List all registered tools"""
        return list(self.tools.keys())
    
    def get_all_schemas(self) -> Dict[str, Dict]:
        """Get all tool schemas"""
        return self.tool_schemas.copy()
    
    def unregister_tool(self, name: str):
        """Unregister a tool"""
        if name in self.tools:
            del self.tools[name]
            del self.tool_schemas[name]
            del self.tool_metadata[name]
            print(f"Unregistered tool: {name}")
    
    def get_tool_info(self, name: str) -> Dict:
        """Get comprehensive information about a tool"""
        if name not in self.tools:
            return {"error": f"Tool {name} not found"}
        
        return {
            "name": name,
            "schema": self.tool_schemas[name],
            "metadata": self.tool_metadata[name],
            "signature": str(inspect.signature(self.tools[name]))
        }
    
    async def execute_multiple_tools(self, tool_calls: List[Dict]) -> List[Dict]:
        """Execute multiple tools concurrently"""
        tasks = []
        
        for call in tool_calls:
            tool_name = call.get("name")
            arguments = call.get("arguments", {})
            
            if tool_name in self.tools:
                task = self.execute_tool(tool_name, arguments)
                tasks.append(task)
            else:
                tasks.append(asyncio.create_task(self._return_error(tool_name or "unknown")))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to error results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "success": False,
                    "error": str(result),
                    "tool": tool_calls[i].get("name", "unknown")
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _return_error(self, tool_name: str) -> Dict:
        """Return error for unknown tool"""
        return {
            "success": False,
            "error": f"Tool {tool_name} not found",
            "tool": tool_name
        }
    
    def validate_tool_call(self, name: str, arguments: Dict) -> Dict:
        """Validate a tool call without executing it"""
        if name not in self.tools:
            return {"valid": False, "error": f"Tool {name} not found"}
        
        schema = self.tool_schemas.get(name, {})
        function_schema = schema.get("function", {})
        parameters = function_schema.get("parameters", {})
        
        # Basic validation - in production, use jsonschema library
        required_params = parameters.get("required", [])
        
        missing_params = [param for param in required_params if param not in arguments]
        
        if missing_params:
            return {
                "valid": False,
                "error": f"Missing required parameters: {missing_params}"
            }
        
        return {"valid": True}
    
    def create_openai_tools_format(self) -> List[Dict]:
        """Convert tool schemas to OpenAI tools format"""
        return list(self.tool_schemas.values())
    
    def create_anthropic_tools_format(self) -> List[Dict]:
        """Convert tool schemas to Anthropic tools format"""
        anthropic_tools = []
        
        for name, schema in self.tool_schemas.items():
            if schema.get("type") == "function":
                function = schema["function"]
                anthropic_tool = {
                    "name": function["name"],
                    "description": function["description"],
                    "input_schema": function["parameters"]
                }
                anthropic_tools.append(anthropic_tool)
        
        return anthropic_tools
    
    async def get_tool_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics for all tools"""
        # In a real implementation, this would track actual usage
        return {
            "total_tools": len(self.tools),
            "tools": list(self.tools.keys()),
            "schemas_count": len(self.tool_schemas),
            "metadata_count": len(self.tool_metadata)
        } 