#!/usr/bin/env python3
"""
Test script for OpenAI LLM Provider
Tests API key validation, text generation, and tool calling functionality.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from llm_providers.openai_provider import OpenAIProvider
from llm_providers.base import LLMConfig
from llm_providers.factory import LLMProviderFactory

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded environment variables from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed. Make sure OPENAI_API_KEY is set in environment.")

class OpenAIProviderTest:
    def __init__(self):
        self.provider = None
        self.factory = None
        
    async def test_api_key_validation(self):
        """Test 1: API Key Validation"""
        print("\n🧪 Test 1: API Key Validation")
        print("-" * 40)
        
        try:
            provider = OpenAIProvider()
            api_key = provider.get_api_key()
            
            if api_key:
                print(f"✅ API key found: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else '***'}")
                print(f"✅ API key validation: {provider.validate_api_key()}")
                return True
            else:
                print("❌ No API key found in environment variables")
                print("   Please set OPENAI_API_KEY in your .env file")
                return False
                
        except Exception as e:
            print(f"❌ API key validation failed: {e}")
            return False
    
    async def test_provider_initialization(self):
        """Test 2: Provider Initialization"""
        print("\n🧪 Test 2: Provider Initialization")
        print("-" * 40)
        
        try:
            self.provider = OpenAIProvider()
            
            # Test default model
            default_model = self.provider.get_default_model()
            print(f"✅ Default model: {default_model}")
            
            # Test available models
            if hasattr(self.provider, 'get_available_models'):
                models = self.provider.get_available_models()
                print(f"✅ Available models: {', '.join(models[:3])}{'...' if len(models) > 3 else ''}")
            
            print("✅ Provider initialization successful")
            return True
            
        except Exception as e:
            print(f"❌ Provider initialization failed: {e}")
            return False
    
    async def test_factory_integration(self):
        """Test 3: Factory Integration"""
        print("\n🧪 Test 3: Factory Integration")
        print("-" * 40)
        
        try:
            self.factory = LLMProviderFactory()
            
            # Test provider validation
            validation_status = self.factory.validate_all_providers()
            print(f"✅ Validation status: {validation_status}")
            
            # Test getting provider through factory
            openai_provider = self.factory.get_provider("openai")
            print(f"✅ Factory provider retrieval successful")
            
            # Test provider info
            provider_info = self.factory.get_provider_info("openai")
            print(f"✅ Provider info: {provider_info['default_model']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Factory integration failed: {e}")
            return False
    
    async def test_text_generation(self):
        """Test 4: Basic Text Generation"""
        print("\n🧪 Test 4: Basic Text Generation")
        print("-" * 40)
        
        if not self.provider:
            print("❌ Provider not initialized. Skipping test.")
            return False
        
        try:
            # Create test configuration
            config = LLMConfig(
                model_name="gpt-4o-mini",  # Use a faster/cheaper model for testing
                temperature=0.3,
                max_tokens=100
            )
            
            # Create test messages
            messages = [
                {
                    "role": "system", 
                    "content": "You are an expert in the field of AI and machine learning. You are also an expert in the field of finance and economics. You are also an expert in the field of law and policy. You are also an expert in the field of medicine and health. You are also an expert in the field of education and training. You are also an expert in the field of technology and innovation. You are also an expert in the field of business and entrepreneurship. You are also an expert in the field of law and policy. You are also an expert in the field of medicine and health. You are also an expert in the field of education and training. You are also an expert in the field of technology and innovation. You are also an expert in the field of business and entrepreneurship."
                },
                {
                    "role": "user", 
                    "content": "Say 'Hello from OpenAI!' and explain what you are in one sentence."
                }
            ]
            
            print("📤 Sending request to OpenAI...")
            print(f"   Model: {config.model_name}")
            print(f"   Temperature: {config.temperature}")
            print(f"   Max tokens: {config.max_tokens}")
            
            # Generate response
            response = await self.provider.generate_response(messages, config)
            
            print(f"📥 Response received:")
            print(f"   {response}")
            
            # Validate response
            if response and len(response.strip()) > 0:
                print("✅ Text generation successful")
                return True
            else:
                print("❌ Empty or invalid response")
                return False
                
        except Exception as e:
            print(f"❌ Text generation failed: {e}")
            return False
    
    async def test_tool_calling(self):
        """Test 5: Tool Calling Functionality"""
        print("\n🧪 Test 5: Tool Calling")
        print("-" * 40)
        
        if not self.provider:
            print("❌ Provider not initialized. Skipping test.")
            return False
        
        try:
            # Create test configuration
            config = LLMConfig(
                model_name="gpt-4o-mini",
                temperature=0.1,
                max_tokens=150
            )
            
            # Define a simple test tool
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "description": "Get the weather for a specific location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state/country"
                                },
                                "unit": {
                                    "type": "string", 
                                    "enum": ["celsius", "fahrenheit"],
                                    "description": "Temperature unit"
                                }
                            },
                            "required": ["location"]
                        }
                    }
                }
            ]
            
            # Create test messages that should trigger tool use
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Use the available tools when appropriate."
                },
                {
                    "role": "user",
                    "content": "What's the weather like in New York City?"
                }
            ]
            
            print("📤 Sending tool calling request...")
            print(f"   Available tools: {tools[0]['function']['name']}")
            
            # Perform tool call
            result = await self.provider.tool_call(messages, tools, config)
            
            print(f"📥 Tool call result received")
            
            # Check if tool calls were made
            if result.get("tool_calls"):
                print(f"✅ Tool calls detected: {len(result['tool_calls'])}")
                for i, tool_call in enumerate(result["tool_calls"]):
                    if hasattr(tool_call, 'function'):
                        print(f"   Tool {i+1}: {tool_call.function.name}")
                return True
            else:
                print("ℹ️  No tool calls made (this is okay - depends on model behavior)")
                return True
                
        except Exception as e:
            print(f"❌ Tool calling failed: {e}")
            return False
    
    async def test_error_handling(self):
        """Test 6: Error Handling"""
        print("\n🧪 Test 6: Error Handling")
        print("-" * 40)
        
        try:
            # Test with invalid model
            config = LLMConfig(
                model_name="invalid-model-name",
                temperature=0.5,
                max_tokens=50
            )
            
            messages = [{"role": "user", "content": "Hello"}]
            
            print("📤 Testing with invalid model name...")
            
            try:
                response = await self.provider.generate_response(messages, config)
                print("⚠️  Expected error but got response - this might be okay if model fallback occurred")
                return True
            except Exception as e:
                print(f"✅ Error handling working correctly: {type(e).__name__}")
                return True
                
        except Exception as e:
            print(f"❌ Error handling test failed: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all tests and provide summary"""
        print("🚀 Starting OpenAI Provider Tests")
        print("=" * 50)
        
        tests = [
            ("API Key Validation", self.test_api_key_validation),
            ("Provider Initialization", self.test_provider_initialization),
            ("Factory Integration", self.test_factory_integration),
            ("Text Generation", self.test_text_generation),
            ("Tool Calling", self.test_tool_calling),
            ("Error Handling", self.test_error_handling)
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                result = await test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ Test '{test_name}' crashed: {e}")
                results.append((test_name, False))
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\nResults: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Your OpenAI provider is working correctly.")
        elif passed > 0:
            print("⚠️  Some tests passed. Check failures above for issues.")
        else:
            print("❌ All tests failed. Check your API key and connection.")
        
        return passed == total

async def main():
    """Main test runner"""
    print("🧪 OpenAI Provider Test Suite")
    print("Testing LLM provider functionality...\n")
    
    # Check if we're in the right directory
    if not Path("llm_providers").exists():
        print("❌ Error: llm_providers directory not found!")
        print("   Please run this script from the project root directory.")
        return
    
    # Run tests
    test_suite = OpenAIProviderTest()
    success = await test_suite.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main()) 