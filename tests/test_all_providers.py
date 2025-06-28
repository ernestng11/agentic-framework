#!/usr/bin/env python3
"""
Test script for All LLM Providers
Quick validation test for all available providers.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from llm_providers.factory import LLMProviderFactory

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded environment variables from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed. Make sure API keys are set in environment.")

async def test_all_providers():
    """Test all available LLM providers"""
    print("🧪 Testing All LLM Providers")
    print("=" * 40)
    
    try:
        factory = LLMProviderFactory()
        
        # Get validation status for all providers
        print("\n🔍 Checking API Key Availability:")
        validation_status = factory.validate_all_providers()
        
        available_providers = []
        
        for provider_name, is_valid in validation_status.items():
            if is_valid:
                print(f"   ✅ {provider_name}: API key found")
                available_providers.append(provider_name)
            else:
                print(f"   ❌ {provider_name}: API key missing")
        
        if not available_providers:
            print("\n❌ No providers have valid API keys!")
            print("   Please set the appropriate environment variables:")
            print("   - OPENAI_API_KEY for OpenAI")
            print("   - ANTHROPIC_API_KEY for Anthropic")
            return False
        
        print(f"\n🚀 Testing {len(available_providers)} available provider(s)...")
        
        # Test each available provider
        for provider_name in available_providers:
            print(f"\n📡 Testing {provider_name} provider:")
            print("-" * 30)
            
            try:
                # Get provider through factory
                provider = factory.get_provider(provider_name)
                print(f"   ✅ Provider initialized")
                
                # Get provider info
                info = factory.get_provider_info(provider_name)
                print(f"   ✅ Default model: {info['default_model']}")
                print(f"   ✅ Available models: {len(info.get('available_models', []))}")
                
                # Quick test message
                from llm_providers.base import LLMConfig
                
                config = LLMConfig(
                    model_name=info['default_model'],
                    temperature=0.3,
                    max_tokens=50
                )
                
                messages = [
                    {"role": "user", "content": "Say 'Test successful' and nothing else."}
                ]
                
                print(f"   📤 Sending test message...")
                response = await provider.generate_response(messages, config)
                
                if response and len(response.strip()) > 0:
                    print(f"   📥 Response: {response.strip()[:50]}{'...' if len(response.strip()) > 50 else ''}")
                    print(f"   ✅ {provider_name} provider working correctly!")
                else:
                    print(f"   ❌ {provider_name} returned empty response")
                
            except Exception as e:
                print(f"   ❌ {provider_name} failed: {e}")
        
        print(f"\n🎉 Provider testing completed!")
        return True
        
    except Exception as e:
        print(f"❌ Provider testing failed: {e}")
        return False

async def main():
    """Main test runner"""
    if not Path("llm_providers").exists():
        print("❌ Error: llm_providers directory not found!")
        print("   Please run this script from the project root directory.")
        return
    
    success = await test_all_providers()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main()) 