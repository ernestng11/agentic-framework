#!/usr/bin/env python3
"""
Test Runner for LLM Providers
Simple script to run different test suites.
"""

import asyncio
import sys
from pathlib import Path

def print_menu():
    """Print test menu options"""
    print("\n🧪 LLM Provider Test Suite")
    print("=" * 30)
    print("1. Test OpenAI Provider (comprehensive)")
    print("2. Test All Providers (quick check)")
    print("3. Exit")
    print("\nEnter your choice (1-3): ", end="")

async def run_openai_tests():
    """Run OpenAI comprehensive tests"""
    try:
        from test_openai_provider import main as openai_main
        await openai_main()
    except ImportError as e:
        print(f"❌ Could not import OpenAI tests: {e}")
    except Exception as e:
        print(f"❌ OpenAI tests failed: {e}")

async def run_all_provider_tests():
    """Run quick tests for all providers"""
    try:
        from test_all_providers import main as all_main
        await all_main()
    except ImportError as e:
        print(f"❌ Could not import provider tests: {e}")
    except Exception as e:
        print(f"❌ Provider tests failed: {e}")

async def main():
    """Main test runner"""
    
    # Check if we're in the right directory
    if not Path("llm_providers").exists():
        print("❌ Error: llm_providers directory not found!")
        print("   Please run this script from the project root directory.")
        return
    
    while True:
        print_menu()
        
        try:
            choice = input().strip()
            
            if choice == "1":
                print("\n🚀 Running OpenAI Provider Tests...")
                await run_openai_tests()
                
            elif choice == "2":
                print("\n🚀 Running All Provider Tests...")
                await run_all_provider_tests()
                
            elif choice == "3":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Ask if user wants to continue
        print("\nPress Enter to continue or Ctrl+C to exit...")
        try:
            input()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    asyncio.run(main()) 