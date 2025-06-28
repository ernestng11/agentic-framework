# LLM Provider Test Suite

This directory contains comprehensive tests for the LLM providers in the modular agentic system.

## 📁 Test Files

- **`test_openai_provider.py`** - Comprehensive OpenAI provider tests
- **`test_all_providers.py`** - Quick validation for all providers  
- **`run_tests.py`** - Interactive test runner
- **`README.md`** - This documentation

## 🚀 Running Tests

### Prerequisites

1. **Install dependencies** (if not already done):
   ```bash
   pip install python-dotenv  # Optional, for .env file loading
   ```

2. **Set up your API keys** in `.env` file:
   ```bash
   # Copy the example and add your keys
   cp .env.example .env
   
   # Edit .env with your actual API keys:
   OPENAI_API_KEY=sk-your-openai-key-here
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
   ```

### Test Options

#### Option 1: Interactive Test Runner
```bash
python tests/run_tests.py
```
This provides a menu to choose which tests to run.

#### Option 2: Direct Test Execution

**Test OpenAI Provider (Comprehensive):**
```bash
python tests/test_openai_provider.py
```

**Test All Providers (Quick Check):**
```bash
python tests/test_all_providers.py
```

#### Option 3: Using Python's unittest module
```bash
python -m pytest tests/  # If you have pytest installed
```

## 🧪 Test Coverage

### OpenAI Provider Tests (`test_openai_provider.py`)

1. **API Key Validation** - Checks if OPENAI_API_KEY is set and valid
2. **Provider Initialization** - Tests provider setup and configuration
3. **Factory Integration** - Tests integration with LLMProviderFactory
4. **Text Generation** - Tests basic text generation functionality
5. **Tool Calling** - Tests function calling capabilities
6. **Error Handling** - Tests error handling with invalid inputs

### All Providers Test (`test_all_providers.py`)

- Quick validation of all available providers
- API key availability check
- Basic functionality test for each provider
- Provider information retrieval

## 📊 Expected Output

### Successful OpenAI Test:
```
🚀 Starting OpenAI Provider Tests
==================================================

🧪 Test 1: API Key Validation
----------------------------------------
✅ API key found: sk-proj-********************
✅ API key validation: True

🧪 Test 2: Provider Initialization
----------------------------------------
✅ Default model: gpt-3.5-turbo
✅ Available models: gpt-4, gpt-4-turbo, gpt-3.5-turbo...
✅ Provider initialization successful

...

==================================================
📊 TEST SUMMARY
==================================================
✅ PASS API Key Validation
✅ PASS Provider Initialization
✅ PASS Factory Integration
✅ PASS Text Generation
✅ PASS Tool Calling
✅ PASS Error Handling

Results: 6/6 tests passed
🎉 All tests passed! Your OpenAI provider is working correctly.
```

### Failed Test Example:
```
🧪 Test 1: API Key Validation
----------------------------------------
❌ No API key found in environment variables
   Please set OPENAI_API_KEY in your .env file
```

## 🛠️ Troubleshooting

### Common Issues

1. **"No API key found"**
   - Ensure `.env` file exists with `OPENAI_API_KEY=your-key`
   - Check that you're running from the project root directory

2. **"llm_providers directory not found"**
   - Run tests from the project root directory
   - Ensure the project structure is intact

3. **"Import error"**
   - Make sure you're running from the project root
   - Check that all required packages are installed

4. **"OpenAI API error"**
   - Verify your API key is valid and has credits
   - Check your internet connection
   - Ensure the API key has the correct permissions

### Debug Mode

To see more detailed output, you can modify the test files to include debug information:

```python
# Add at the top of test files
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔧 Extending Tests

To add new tests:

1. Create a new test file following the naming pattern `test_*.py`
2. Import the necessary modules from the project
3. Use the existing test structure as a template
4. Add your test to the `run_tests.py` menu if needed

Example test function:
```python
async def test_new_functionality(self):
    """Test new functionality"""
    print("\n🧪 Test: New Functionality")
    print("-" * 40)
    
    try:
        # Your test code here
        result = await some_function()
        
        if result:
            print("✅ New functionality working")
            return True
        else:
            print("❌ New functionality failed")
            return False
            
    except Exception as e:
        print(f"❌ New functionality error: {e}")
        return False
``` 