# Modular Agentic System

A comprehensive, production-ready implementation of a modular agentic system following modern standards including MCP (Model Context Protocol) and A2A (Agent-to-Agent) protocols.

## 🏗️ Architecture Overview

This system implements a modular architecture with the following core components:

- **LLM Provider Abstraction Layer**: Support for multiple LLM providers (OpenAI, Anthropic, etc.)
- **MCP Integration Layer**: Model Context Protocol for tool calling and resource management
- **A2A Protocol Implementation**: Agent-to-Agent communication and discovery
- **Agent Orchestration Layer**: Smart routing and conversation management
- **Specialized Agent Implementations**: Research and Planning agents with extensible design
- **Tool Calling System**: Comprehensive tool management and execution

## 📁 Project Structure

```
pl-agentic/
├── llm_providers/          # LLM provider abstraction layer
│   ├── base.py            # Base provider interface
│   ├── openai_provider.py # OpenAI implementation
│   ├── anthropic_provider.py # Anthropic implementation
│   └── factory.py         # Provider factory
├── mcp_integration/        # MCP protocol implementation
│   ├── server.py          # MCP server manager
│   └── client.py          # MCP client manager
├── a2a_protocol/          # Agent-to-Agent protocol
│   ├── agent_registry.py  # Agent discovery and registration
│   └── communication.py   # A2A communication client
├── orchestration/         # System orchestration
│   ├── router.py          # Agent routing logic
│   └── conversation_manager.py # Conversation state management
├── agents/                # Specialized agent implementations
│   ├── base_agent.py      # Base agent class
│   ├── research_agent.py  # Research specialist
│   └── planning_agent.py  # Planning specialist
├── tools/                 # Tool system
│   ├── tool_manager.py    # Tool registration and execution
│   └── implementations.py # Default tool implementations
├── main.py               # Application entry point
├── config.yaml           # System configuration
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container configuration
└── docker-compose.yml   # Multi-service deployment
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)
- API keys for LLM providers (OpenAI, Anthropic)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd pl-agentic
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Run the system:**
   ```bash
   python main.py
   ```

### Demo Mode

To run an interactive demo:
```bash
DEMO_MODE=true python main.py
```

### Test Mode

To run system tests:
```bash
TEST_MODE=true python main.py
```

## 🐳 Docker Deployment

### Single Container

```bash
docker build -t agentic-system .
docker run -p 8000:8000 --env-file .env agentic-system
```

### Full Stack with Docker Compose

```bash
docker-compose up -d
```

This starts:
- Main agentic system (port 8000)
- Agent registry (port 9000)
- Redis for caching (port 6379)
- PostgreSQL database (port 5432)
- Optional monitoring UI (port 3000)

## 🤖 Available Agents

### Research Agent (`research-001`)
Specializes in:
- Web search and information gathering
- Data analysis and insights
- Report generation
- Research synthesis

**Capabilities:** `web_search`, `data_analysis`, `report_generation`

### Planning Agent (`planning-001`)
Specializes in:
- Task decomposition and breakdown
- Workflow planning and process design
- Resource allocation optimization
- Timeline and schedule creation

**Capabilities:** `task_decomposition`, `workflow_planning`, `resource_allocation`

## 🛠️ Available Tools

- **web_search**: Search the web for information
- **database_query**: Query databases for data
- **file_reader**: Read and process various file types
- **calculator**: Perform mathematical calculations
- **text_summarizer**: Summarize text content
- **email_sender**: Send emails (simulated)
- **scheduler**: Calendar and scheduling operations

## 🔧 Configuration

### Environment Variables

Key environment variables in `.env`:

```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
A2A_API_KEY=your_a2a_key
DEMO_MODE=false
TEST_MODE=false
```

### System Configuration

Edit `config.yaml` to customize:
- LLM provider settings
- MCP server configurations
- A2A protocol settings
- Agent capabilities and tools
- Security and rate limiting

## 🔌 Extending the System

### Adding New Agents

1. Create a new agent class inheriting from `BaseAgent`:

```python
from agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self, agent_id, llm_provider, mcp_manager, a2a_client):
        super().__init__(agent_id, llm_provider, mcp_manager, a2a_client)
        self.capabilities = ["custom_capability"]
        self.tools = ["custom_tool"]
    
    async def process_task(self, task):
        # Implement custom logic
        return {"success": True, "result": "Custom result"}
```

2. Register the agent in `main.py`:

```python
custom_agent = CustomAgent("custom-001", llm_provider, mcp_manager, a2a_client)
await custom_agent.initialize()
router.register_agent(custom_agent.agent_id, custom_agent)
```

### Adding New Tools

1. Create a tool implementation:

```python
class CustomTool:
    async def __call__(self, parameter: str) -> dict:
        # Implement tool logic
        return {"result": f"Processed {parameter}"}
```

2. Register the tool:

```python
tool_manager.register_tool(
    "custom_tool",
    CustomTool(),
    {
        "type": "function",
        "function": {
            "name": "custom_tool",
            "description": "Custom tool description",
            "parameters": {
                "type": "object",
                "properties": {
                    "parameter": {"type": "string", "description": "Input parameter"}
                },
                "required": ["parameter"]
            }
        }
    }
)
```

### Adding New LLM Providers

1. Implement the provider interface:

```python
from llm_providers.base import BaseLLMProvider

class CustomProvider(BaseLLMProvider):
    async def generate_response(self, messages, config):
        # Implement custom provider logic
        pass
    
    async def tool_call(self, messages, tools, config):
        # Implement tool calling
        pass
```

2. Register with factory:

```python
llm_factory.register_provider("custom", CustomProvider)
```

## 📊 Monitoring and Observability

The system includes comprehensive logging and status tracking:

- Agent status monitoring
- Tool usage statistics
- Conversation history
- Performance metrics

Access system stats programmatically:

```python
# Get agent status
status = await router.get_agent_status()

# Get conversation stats  
stats = await conversation_manager.get_system_stats()

# Get tool usage
tool_stats = await tool_manager.get_tool_usage_stats()
```

## 🔒 Security Considerations

- API key management through environment variables
- Rate limiting and request validation
- Non-root container execution
- Input sanitization for tool calls
- Secure inter-agent communication

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

Run specific test categories:

```bash
# Test agents
pytest tests/test_agents.py

# Test tools
pytest tests/test_tools.py

# Test integration
pytest tests/test_integration.py
```

## 📈 Performance

- Asynchronous operation throughout
- Concurrent tool execution
- Efficient agent routing
- Optimized memory usage
- Horizontal scaling support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions and support:
- Review the implementation guide: `implementation-guide.md`
- Check the configuration examples in `config.yaml`
- Run system tests with `TEST_MODE=true`
- Enable debug mode for detailed logging

## 🛣️ Roadmap

- [ ] Enhanced MCP protocol integration
- [ ] Additional LLM provider support
- [ ] Advanced agent collaboration patterns
- [ ] Web UI for system management
- [ ] Performance optimization
- [ ] Extended tool library
- [ ] Production monitoring dashboard
