import asyncio
import os
from typing import Optional
from orchestration.conversation_manager import ConversationManager
from orchestration.router import AgentRouter
from llm_providers.factory import LLMProviderFactory
from llm_providers.base import LLMConfig
from mcp_integration.server import MCPServerManager
from mcp_integration.client import MCPClientManager
from a2a_protocol.agent_registry import AgentRegistry
from a2a_protocol.communication import A2AClient
from agents.research_agent import ResearchAgent
from agents.planning_agent import PlanningAgent
from tools.tool_manager import ToolManager
from tools.implementations import get_default_tools

async def setup_llm_providers() -> LLMProviderFactory:
    """Setup LLM providers with validation"""
    factory = LLMProviderFactory()
    
    print("🔍 Validating LLM provider API keys...")
    validation_status = factory.validate_all_providers()
    
    for provider, is_valid in validation_status.items():
        if is_valid:
            print(f"   ✅ {provider}: API key found")
        else:
            print(f"   ❌ {provider}: API key missing or invalid")
    
    # Check if at least one provider is available
    if not any(validation_status.values()):
        print("⚠️  Warning: No LLM providers have valid API keys!")
        print("   Please set environment variables:")
        print("   - OPENAI_API_KEY for OpenAI")
        print("   - ANTHROPIC_API_KEY for Anthropic")
    
    print("✅ LLM provider factory initialized")
    return factory

async def setup_mcp_integration() -> tuple[MCPServerManager, MCPClientManager]:
    """Setup MCP server and client managers"""
    server_manager = MCPServerManager()
    client_manager = MCPClientManager()
    
    # Register default tools with MCP server
    default_tools = get_default_tools()
    for tool_name, tool_config in default_tools.items():
        await server_manager.register_tool(
            tool_name,
            tool_config["instance"],
            tool_config["schema"]
        )
    
    print("✅ MCP integration initialized")
    return server_manager, client_manager

async def setup_a2a_protocol() -> tuple[AgentRegistry, A2AClient]:
    """Setup A2A protocol components"""
    registry = AgentRegistry()
    
    # Create a system A2A client for coordination
    system_client = A2AClient("system", registry)
    
    print("✅ A2A protocol initialized")
    return registry, system_client

async def setup_tools() -> ToolManager:
    """Setup tool manager with default tools"""
    tool_manager = ToolManager()
    
    # Register default tools
    default_tools = get_default_tools()
    for tool_name, tool_config in default_tools.items():
        tool_manager.register_tool(
            tool_name,
            tool_config["instance"],
            tool_config["schema"]
        )
    
    print("✅ Tool manager initialized with default tools")
    return tool_manager

async def create_agents(llm_factory: LLMProviderFactory, 
                       mcp_manager: MCPServerManager,
                       registry: AgentRegistry) -> dict:
    """Create and initialize specialized agents"""
    agents = {}
    
    # Create A2A clients for each agent
    research_client = A2AClient("research-001", registry)
    planning_client = A2AClient("planning-001", registry)
    
    # Try to create research agent with OpenAI
    try:
        research_agent = ResearchAgent(
            "research-001",
            llm_factory.get_provider("openai"),
            mcp_manager,
            research_client
        )
        await research_agent.initialize()
        agents["research"] = research_agent
        print("✅ Research agent created with OpenAI provider")
    except Exception as e:
        print(f"⚠️  Could not initialize research agent with OpenAI: {e}")
        
        # Try fallback to Anthropic
        try:
            research_agent = ResearchAgent(
                "research-001",
                llm_factory.get_provider("anthropic"),
                mcp_manager,
                research_client
            )
            await research_agent.initialize()
            agents["research"] = research_agent
            print("✅ Research agent created with Anthropic provider (fallback)")
        except Exception as e2:
            print(f"❌ Could not initialize research agent with any provider: {e2}")
    
    # Try to create planning agent with Anthropic
    try:
        planning_agent = PlanningAgent(
            "planning-001", 
            llm_factory.get_provider("anthropic"),
            mcp_manager,
            planning_client
        )
        await planning_agent.initialize()
        agents["planning"] = planning_agent
        print("✅ Planning agent created with Anthropic provider")
    except Exception as e:
        print(f"⚠️  Could not initialize planning agent with Anthropic: {e}")
        
        # Try fallback to OpenAI
        try:
            planning_agent = PlanningAgent(
                "planning-001",
                llm_factory.get_provider("openai"),
                mcp_manager,
                planning_client
            )
            await planning_agent.initialize()
            agents["planning"] = planning_agent
            print("✅ Planning agent created with OpenAI provider (fallback)")
        except Exception as e2:
            print(f"❌ Could not initialize planning agent with any provider: {e2}")
    
    return agents

async def create_agentic_system():
    """Create and configure the complete agentic system"""
    print("🚀 Initializing Modular Agentic System...")
    
    # Initialize core components
    llm_factory = await setup_llm_providers()
    mcp_manager, mcp_client = await setup_mcp_integration()
    registry, system_a2a_client = await setup_a2a_protocol()
    tool_manager = await setup_tools()
    
    # Create specialized agents
    agents = await create_agents(llm_factory, mcp_manager, registry)
    
    if not agents:
        print("❌ No agents could be initialized. Please check your API keys.")
        return None, None, {}, tool_manager
    
    # Setup orchestration
    router = AgentRouter(llm_factory, mcp_manager, system_a2a_client)
    
    # Register agents with router
    for agent_id, agent in agents.items():
        router.register_agent(agent.agent_id, agent)
    
    # Create conversation manager
    conversation_manager = ConversationManager(router)
    
    # Start MCP server
    try:
        mcp_server = await mcp_manager.start_server()
        print("✅ MCP server started")
    except Exception as e:
        print(f"⚠️  Could not start MCP server: {e}")
    
    # Show provider information
    print("\n📊 Provider Information:")
    active_providers = llm_factory.list_active_providers()
    for provider_name in llm_factory.list_providers():
        try:
            info = llm_factory.get_provider_info(provider_name)
            status = "🟢 ACTIVE" if provider_name in active_providers else "🔴 INACTIVE"
            print(f"   {provider_name}: {status}")
            print(f"      Model: {info['default_model']}")
            print(f"      API Key: {'✅' if info['api_key_available'] else '❌'}")
        except Exception as e:
            print(f"   {provider_name}: ❌ ERROR - {e}")
    
    print(f"\n🎉 Modular Agentic System initialized successfully!")
    print(f"📊 System Status:")
    print(f"   - Agents: {len(agents)}")
    print(f"   - Tools: {len(tool_manager.list_tools())}")
    print(f"   - LLM Providers: {len(active_providers)}")
    
    return conversation_manager, router, agents, tool_manager

async def run_interactive_demo(conversation_manager: ConversationManager):
    """Run an interactive demo of the system"""
    print("\n🤖 Welcome to the Modular Agentic System Demo!")
    print("💡 Try commands like:")
    print("   - 'search for information about artificial intelligence'")
    print("   - 'plan a project to build a web application'")
    print("   - 'analyze the current state of renewable energy'")
    print("   - 'break down the task of learning machine learning'")
    print("   - Type 'quit' to exit\n")
    
    user_id = "demo_user"
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("🤔 Processing...")
            response = await conversation_manager.process_user_input(user_id, user_input)
            print(f"🤖 Assistant: {response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")

async def run_system_tests(conversation_manager: ConversationManager, router: AgentRouter):
    """Run basic system tests"""
    print("\n🧪 Running system tests...")
    
    test_user = "test_user"
    test_cases = [
        "search for recent developments in AI",
        "plan a 3-month software development project",
        "analyze data trends in technology sector",
        "break down the task of learning Python programming"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case}")
        try:
            response = await conversation_manager.process_user_input(test_user, test_case)
            print(f"✅ Test {i} passed: Response received")
        except Exception as e:
            print(f"❌ Test {i} failed: {e}")
    
    # Test agent status
    agent_status = await router.get_agent_status()
    print(f"📊 Agent status: {len(agent_status)} agents operational")
    
    print("🧪 System tests completed")

async def main():
    """Main entry point"""
    try:
        # Create the system
        system_result = await create_agentic_system()
        if system_result[0] is None:  # conversation_manager is None
            print("❌ System initialization failed. Exiting.")
            return 1
        
        conversation_manager, router, agents, tool_manager = system_result
        
        # Check command line arguments or environment variables for demo mode
        demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
        test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
        
        if test_mode:
            await run_system_tests(conversation_manager, router)
        elif demo_mode:
            await run_interactive_demo(conversation_manager)
        else:
            print("\n✨ System is ready!")
            print("💡 Set DEMO_MODE=true to run interactive demo")
            print("💡 Set TEST_MODE=true to run system tests")
            print("🔗 HTTP API endpoints would be available at http://localhost:8000")
            
            # Keep the system running
            print("\n⏸️  Press Ctrl+C to stop the system")
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down system...")
                
                # Graceful shutdown
                for agent in agents.values():
                    await agent.shutdown()
                
                print("✅ System shutdown complete")
    
    except Exception as e:
        print(f"❌ Failed to start system: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main()) 