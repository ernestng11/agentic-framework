from typing import Dict, Optional, Any
try:
    from mcp import McpClient
except ImportError:
    McpClient = None

class MCPClientManager:
    def __init__(self):
        self.connections: Dict[str, Any] = {}
    
    async def connect_to_server(self, server_name: str, params: Dict):
        """Connect to external MCP server"""
        if McpClient is None:
            raise ImportError("MCP package not installed. Please install with: pip install mcp")
        
        # Implementation depends on MCP package API
        # This would typically create a connection to an external MCP server
        # using the provided parameters (transport type, address, etc.)
        try:
            client = McpClient()
            # Configure client connection based on params
            await client.connect(params)
            self.connections[server_name] = client
            return client
        except Exception as e:
            raise Exception(f"Failed to connect to MCP server {server_name}: {str(e)}")
    
    async def call_external_tool(self, server: str, tool: str, args: Dict) -> Any:
        """Call tool on external MCP server"""
        if server not in self.connections:
            raise ValueError(f"No connection to server: {server}")
        
        client = self.connections[server]
        try:
            # Call the tool on the external server
            result = await client.call_tool(tool, args)
            return result
        except Exception as e:
            raise Exception(f"Failed to call tool {tool} on server {server}: {str(e)}")
    
    async def list_available_tools(self, server: str) -> list:
        """List available tools on a server"""
        if server not in self.connections:
            raise ValueError(f"No connection to server: {server}")
        
        client = self.connections[server]
        try:
            tools = await client.list_tools()
            return tools
        except Exception as e:
            raise Exception(f"Failed to list tools on server {server}: {str(e)}")
    
    async def disconnect_from_server(self, server_name: str):
        """Disconnect from MCP server"""
        if server_name in self.connections:
            client = self.connections[server_name]
            await client.disconnect()
            del self.connections[server_name] 