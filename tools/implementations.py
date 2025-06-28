from typing import List, Dict, Any, Optional
import json
import asyncio
from datetime import datetime

class WebSearchTool:
    """Tool for searching the web for information"""
    
    async def __call__(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search the web for information"""
        # Simulate web search - in production, integrate with actual search APIs
        await asyncio.sleep(0.5)  # Simulate API delay
        
        simulated_results = [
            {
                "title": f"Result 1 for '{query}'",
                "url": "https://example.com/result1",
                "snippet": f"This is a comprehensive overview of {query} with detailed information.",
                "source": "example.com",
                "date": datetime.now().isoformat()
            },
            {
                "title": f"Latest news about {query}",
                "url": "https://news.example.com/article",
                "snippet": f"Recent developments and trends related to {query}.",
                "source": "news.example.com",
                "date": datetime.now().isoformat()
            },
            {
                "title": f"Expert analysis: {query}",
                "url": "https://expert.example.com/analysis", 
                "snippet": f"In-depth expert analysis and professional insights on {query}.",
                "source": "expert.example.com",
                "date": datetime.now().isoformat()
            }
        ]
        
        return simulated_results[:max_results]

class DatabaseQueryTool:
    """Tool for querying databases"""
    
    def __init__(self):
        # Simulate a database with sample data
        self.mock_database = {
            "users": [
                {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
                {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user"},
                {"id": 3, "name": "Charlie", "email": "charlie@example.com", "role": "user"}
            ],
            "products": [
                {"id": 1, "name": "Laptop", "price": 999.99, "category": "electronics"},
                {"id": 2, "name": "Book", "price": 19.99, "category": "books"},
                {"id": 3, "name": "Coffee", "price": 4.99, "category": "food"}
            ]
        }
    
    async def __call__(self, query: str, database: str = "main") -> List[Dict]:
        """Query database for information"""
        await asyncio.sleep(0.2)  # Simulate query time
        
        # Parse simple queries - in production, use proper SQL parsing
        query_lower = query.lower()
        
        if "users" in query_lower:
            if "admin" in query_lower:
                return [user for user in self.mock_database["users"] if user["role"] == "admin"]
            return self.mock_database["users"]
        
                elif "products" in query_lower:
            if "electronics" in query_lower:
                return [product for product in self.mock_database["products"] if product["category"] == "electronics"]
            return self.mock_database["products"]
        
        else:
            return [{"error": f"Could not parse query: {query}"}]

class FileReaderTool:
    """Tool for reading and processing files"""
    
    async def __call__(self, file_path: str, file_type: str = "auto") -> Dict[str, Any]:
        """Read and process file content"""
        await asyncio.sleep(0.3)  # Simulate file reading
        
        # Simulate file reading - in production, read actual files
        if file_type == "auto":
            if file_path.endswith('.pdf'):
                file_type = "pdf"
            elif file_path.endswith('.txt'):
                file_type = "text"
            elif file_path.endswith('.json'):
                file_type = "json"
            else:
                file_type = "unknown"
        
        simulated_content = {
            "file_path": file_path,
            "file_type": file_type,
            "content": f"Simulated content from {file_path}",
            "metadata": {
                "size": "1024 bytes",
                "created": datetime.now().isoformat(),
                "processed": datetime.now().isoformat()
            }
        }
        
        if file_type == "pdf":
            simulated_content["pages"] = 5
            simulated_content["text_content"] = f"Extracted text from PDF: {file_path}"
        elif file_type == "json":
            simulated_content["parsed_data"] = {"sample": "data", "from": file_path}
        
        return simulated_content

class CalculatorTool:
    """Tool for mathematical calculations"""
    
    async def __call__(self, expression: str, precision: int = 2) -> Dict[str, Any]:
        """Perform mathematical calculations"""
        try:
            # Simple calculator - in production, use a proper math parser
            # Only allow basic operations for security
            allowed_chars = set("0123456789+-*/.() ")
            if not all(c in allowed_chars for c in expression):
                return {"error": "Invalid characters in expression"}
            
            result = eval(expression)
            rounded_result = round(result, precision)
            
            return {
                "expression": expression,
                "result": rounded_result,
                "precision": precision,
                "calculated_at": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {"error": f"Calculation error: {str(e)}"}

class TextSummarizerTool:
    """Tool for summarizing text content"""
    
    async def __call__(self, text: str, max_length: int = 100, style: str = "brief") -> Dict[str, Any]:
        """Summarize text content"""
        await asyncio.sleep(0.4)  # Simulate processing time
        
        # Simple summarization - in production, use LLM or NLP library
        sentences = text.split('.')
        
        if style == "brief":
            summary = '. '.join(sentences[:2]) + '.' if len(sentences) > 2 else text
        elif style == "detailed":
            summary = '. '.join(sentences[:4]) + '.' if len(sentences) > 4 else text
        else:
            summary = text[:max_length] + "..." if len(text) > max_length else text
        
        return {
            "original_text": text,
            "summary": summary,
            "original_length": len(text),
            "summary_length": len(summary),
            "style": style,
            "compression_ratio": round(len(summary) / len(text), 2) if text else 0
        }

class EmailSenderTool:
    """Tool for sending emails"""
    
    async def __call__(self, to: str, subject: str, body: str, cc: Optional[str] = None) -> Dict[str, Any]:
        """Send email (simulated)"""
        await asyncio.sleep(1.0)  # Simulate email sending
        
        # Simulate email sending - in production, integrate with email service
        email_data = {
            "to": to,
            "subject": subject,
            "body": body,
            "cc": cc,
            "sent_at": datetime.now().isoformat(),
            "message_id": f"msg_{datetime.now().timestamp()}",
            "status": "sent"
        }
        
        # Simulate some basic validation
        if "@" not in to:
            email_data["status"] = "failed"
            email_data["error"] = "Invalid email address"
        
        return email_data

class SchedulerTool:
    """Tool for scheduling and calendar operations"""
    
    def __init__(self):
        self.mock_calendar = []
    
    async def __call__(self, action: str, **kwargs) -> Dict[str, Any]:
        """Perform calendar/scheduling operations"""
        await asyncio.sleep(0.3)
        
        if action == "create_event":
            event = {
                "id": f"event_{len(self.mock_calendar) + 1}",
                "title": kwargs.get("title", "New Event"),
                "start_time": kwargs.get("start_time"),
                "end_time": kwargs.get("end_time"),
                "description": kwargs.get("description", ""),
                "created_at": datetime.now().isoformat()
            }
            self.mock_calendar.append(event)
            return {"action": "create_event", "event": event, "status": "created"}
        
        elif action == "list_events":
            return {"action": "list_events", "events": self.mock_calendar}
        
        elif action == "delete_event":
            event_id = kwargs.get("event_id")
            self.mock_calendar = [e for e in self.mock_calendar if e["id"] != event_id]
            return {"action": "delete_event", "event_id": event_id, "status": "deleted"}
        
        else:
            return {"error": f"Unknown action: {action}"}

# Tool registration helper
def get_default_tools() -> Dict[str, Dict]:
    """Get default tool configurations"""
    return {
        "web_search": {
            "instance": WebSearchTool(),
            "schema": {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Search the web for information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of results",
                                "default": 5
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        },
        "database_query": {
            "instance": DatabaseQueryTool(),
            "schema": {
                "type": "function", 
                "function": {
                    "name": "database_query",
                    "description": "Query database for information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Database query"
                            },
                            "database": {
                                "type": "string",
                                "description": "Database name",
                                "default": "main"
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        },
        "file_reader": {
            "instance": FileReaderTool(),
            "schema": {
                "type": "function",
                "function": {
                    "name": "file_reader",
                    "description": "Read and process files",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the file"
                            },
                            "file_type": {
                                "type": "string",
                                "description": "File type (auto, pdf, text, json)",
                                "default": "auto"
                            }
                        },
                        "required": ["file_path"]
                    }
                }
            }
        },
        "calculator": {
            "instance": CalculatorTool(),
            "schema": {
                "type": "function",
                "function": {
                    "name": "calculator",
                    "description": "Perform mathematical calculations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Mathematical expression to evaluate"
                            },
                            "precision": {
                                "type": "integer",
                                "description": "Decimal precision",
                                "default": 2
                            }
                        },
                        "required": ["expression"]
                    }
                }
            }
        },
        "text_summarizer": {
            "instance": TextSummarizerTool(),
            "schema": {
                "type": "function",
                "function": {
                    "name": "text_summarizer",
                    "description": "Summarize text content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Text to summarize"
                            },
                            "max_length": {
                                "type": "integer",
                                "description": "Maximum summary length",
                                "default": 100
                            },
                            "style": {
                                "type": "string",
                                "description": "Summary style (brief, detailed, truncate)",
                                "default": "brief"
                            }
                        },
                        "required": ["text"]
                    }
                }
            }
        }
    } 