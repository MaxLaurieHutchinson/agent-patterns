"""
Tool Use (MCP) Implementation
Model Context Protocol for standardized tool integration.
"""

from typing import Any, Callable, Optional, Protocol
from dataclasses import dataclass, field
from datetime import datetime
import json
import time
import os
from abc import ABC, abstractmethod


@dataclass
class ToolSchema:
    """JSON Schema for a tool."""
    name: str
    description: str
    parameters: dict  # JSON Schema object
    returns: Optional[dict] = None
    examples: list[dict] = field(default_factory=list)


@dataclass
class ToolCall:
    """A call to a tool."""
    tool_name: str
    parameters: dict
    call_id: str = field(default_factory=lambda: f"call_{int(time.time()*1000)}")
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ToolResult:
    """Result from a tool execution."""
    call_id: str
    success: bool
    data: Any = None
    error: Optional[str] = None
    duration_ms: float = 0.0


class MCPTool(ABC):
    """
    Abstract base class for MCP-compatible tools.
    """
    
    def __init__(self):
        self._schema: Optional[ToolSchema] = None
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description."""
        pass
    
    @property
    def schema(self) -> ToolSchema:
        """Get tool schema."""
        if self._schema is None:
            self._schema = self._build_schema()
        return self._schema
    
    @abstractmethod
    def _build_schema(self) -> ToolSchema:
        """Build the tool schema."""
        pass
    
    @abstractmethod
    def _execute(self, **params) -> Any:
        """Execute the tool logic."""
        pass
    
    def validate(self, params: dict) -> tuple[bool, Optional[str]]:
        """
        Validate parameters against schema.
        
        Returns:
            (is_valid, error_message)
        """
        schema = self.schema.parameters
        required = schema.get("required", [])
        properties = schema.get("properties", {})
        
        # Check required parameters
        for req in required:
            if req not in params:
                return False, f"Missing required parameter: '{req}'"
        
        # Check parameter types
        for key, value in params.items():
            if key in properties:
                expected_type = properties[key].get("type")
                if expected_type and not self._check_type(value, expected_type):
                    return False, (
                        f"Parameter '{key}' should be {expected_type}, "
                        f"got {type(value).__name__}"
                    )
        
        return True, None
    
    def _check_type(self, value: Any, expected: str) -> bool:
        """Check if value matches expected type."""
        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict
        }
        
        expected_class = type_map.get(expected)
        if expected_class is None:
            return True  # Unknown type, allow
        
        return isinstance(value, expected_class)
    
    def execute(self, call: ToolCall) -> ToolResult:
        """
        Execute the tool with validation and error handling.
        """
        start_time = time.time()
        
        # Validate
        is_valid, error = self.validate(call.parameters)
        if not is_valid:
            return ToolResult(
                call_id=call.call_id,
                success=False,
                error=f"Validation error: {error}",
                duration_ms=(time.time() - start_time) * 1000
            )
        
        # Execute
        try:
            result = self._execute(**call.parameters)
            return ToolResult(
                call_id=call.call_id,
                success=True,
                data=result,
                duration_ms=(time.time() - start_time) * 1000
            )
        except Exception as e:
            return ToolResult(
                call_id=call.call_id,
                success=False,
                error=f"Execution error: {str(e)}",
                duration_ms=(time.time() - start_time) * 1000
            )
    
    def to_dict(self) -> dict:
        """Convert to dictionary for LLM consumption."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.schema.parameters
        }


class CalculatorTool(MCPTool):
    """Calculator tool for mathematical operations."""
    
    @property
    def name(self) -> str:
        return "calculator"
    
    @property
    def description(self) -> str:
        return "Perform mathematical calculations. Supports +, -, *, /, **, %."
    
    def _build_schema(self) -> ToolSchema:
        return ToolSchema(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate"
                    }
                },
                "required": ["expression"]
            },
            examples=[
                {"expression": "2 + 2"},
                {"expression": "(10 * 5) / 2"}
            ]
        )
    
    def _execute(self, expression: str) -> dict:
        """Safely evaluate mathematical expression."""
        # Safe evaluation - only allow math operations
        allowed_chars = set("0123456789+-*/.() %")
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Invalid characters in expression")
        
        result = eval(expression, {"__builtins__": {}}, {})
        return {
            "expression": expression,
            "result": result
        }


class SearchTool(MCPTool):
    """Mock search tool for demonstration."""
    
    @property
    def name(self) -> str:
        return "search"
    
    @property
    def description(self) -> str:
        return "Search for information on a given topic."
    
    def _build_schema(self) -> ToolSchema:
        return ToolSchema(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        )
    
    def _execute(self, query: str, limit: int = 5) -> dict:
        """Mock search execution."""
        # Mock results
        mock_db = {
            "python": ["Python Official Docs", "Python Tutorial", "Python Cookbook"],
            "javascript": ["MDN JavaScript", "JavaScript.info", "ES6 Features"],
            "ai": ["Introduction to AI", "Machine Learning Basics", "Neural Networks"]
        }
        
        results = []
        for key, values in mock_db.items():
            if key in query.lower():
                results.extend(values)
        
        if not results:
            results = [f"Result for '{query}' #{i+1}" for i in range(min(limit, 3))]
        
        return {
            "query": query,
            "results": results[:limit],
            "total": len(results)
        }


class FileSystemTool(MCPTool):
    """File system operations tool."""
    
    def __init__(self, base_path: str = "."):
        super().__init__()
        self.base_path = os.path.abspath(base_path)
    
    @property
    def name(self) -> str:
        return "filesystem"
    
    @property
    def description(self) -> str:
        return "Read and write files. Use with caution."
    
    def _build_schema(self) -> ToolSchema:
        return ToolSchema(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["read", "write", "list"],
                        "description": "Operation to perform"
                    },
                    "path": {
                        "type": "string",
                        "description": "File or directory path"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write (for write operation)"
                    }
                },
                "required": ["operation", "path"]
            }
        )
    
    def _execute(self, operation: str, path: str, content: Optional[str] = None) -> dict:
        """Execute file operation."""
        full_path = self._resolve_path(path)
        
        if operation == "read":
            with open(full_path, "r", encoding="utf-8") as f:
                return {"content": f.read()}
        
        elif operation == "write":
            parent_dir = os.path.dirname(full_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content or "")
            return {"status": "written", "path": path}
        
        elif operation == "list":
            items = os.listdir(full_path)
            return {"items": items}
        
        else:
            raise ValueError(f"Unknown operation: {operation}")

    def _resolve_path(self, path: str) -> str:
        """Resolve a path and ensure it stays within base_path."""
        candidate = os.path.abspath(os.path.join(self.base_path, path))
        if os.path.commonpath([self.base_path, candidate]) != self.base_path:
            raise ValueError("Path escapes base path")
        return candidate


class MCPRegistry:
    """
    Registry for MCP tools.
    
    Manages tool registration, discovery, and execution.
    """
    
    def __init__(self):
        self.tools: dict[str, MCPTool] = {}
        self.call_history: list[tuple[ToolCall, ToolResult]] = []
    
    def register(self, tool: MCPTool):
        """Register a tool."""
        self.tools[tool.name] = tool
    
    def unregister(self, name: str):
        """Unregister a tool."""
        if name in self.tools:
            del self.tools[name]
    
    def get_tool(self, name: str) -> Optional[MCPTool]:
        """Get a tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> list[dict]:
        """List all available tools."""
        return [tool.to_dict() for tool in self.tools.values()]
    
    def get_manifest(self) -> dict:
        """Get MCP manifest for LLM consumption."""
        return {
            "version": "1.0",
            "tools": self.list_tools()
        }
    
    def execute(self, tool_name: str, parameters: dict) -> ToolResult:
        """
        Execute a tool by name.
        
        Args:
            tool_name: Name of the tool
            parameters: Parameters for the tool
            
        Returns:
            ToolResult with execution outcome
        """
        tool = self.get_tool(tool_name)
        if not tool:
            return ToolResult(
                call_id=f"error_{int(time.time()*1000)}",
                success=False,
                error=f"Tool '{tool_name}' not found"
            )
        
        call = ToolCall(tool_name=tool_name, parameters=parameters)
        result = tool.execute(call)
        
        self.call_history.append((call, result))
        
        return result
    
    def call_tool(self, tool_call_str: str) -> ToolResult:
        """
        Parse and execute a tool call from string.
        
        Expected format:
        tool_name(param1=value1, param2=value2)
        """
        try:
            # Parse tool call
            tool_name = tool_call_str.split("(")[0].strip()
            args_str = tool_call_str.split("(")[1].rstrip(")")
            
            # Parse parameters
            params = {}
            if args_str:
                for arg in args_str.split(","):
                    if "=" in arg:
                        key, value = arg.split("=", 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        
                        # Try to parse as JSON
                        try:
                            value = json.loads(value)
                        except json.JSONDecodeError:
                            pass  # Keep as string
                        
                        params[key] = value
            
            return self.execute(tool_name, params)
        
        except Exception as e:
            return ToolResult(
                call_id=f"parse_error_{int(time.time()*1000)}",
                success=False,
                error=f"Failed to parse tool call: {e}"
            )


class MCPAgent:
    """
    Agent that uses MCP tools through the registry.
    """
    
    def __init__(self, registry: MCPRegistry):
        self.registry = registry
    
    def get_system_prompt(self) -> str:
        """Generate system prompt with available tools."""
        manifest = self.registry.get_manifest()
        
        tools_desc = "\n\n".join([
            f"Tool: {tool['name']}\n"
            f"Description: {tool['description']}\n"
            f"Parameters: {json.dumps(tool['parameters'], indent=2)}"
            for tool in manifest['tools']
        ])
        
        return f"""You are an AI assistant with access to tools.

Available tools:
{tools_desc}

To use a tool, respond with:
TOOL_CALL: tool_name(parameter1=value1, parameter2=value2)

The system will execute the tool and return the result."""
    
    def process_llm_response(self, response: str) -> tuple[str, Optional[ToolResult]]:
        """
        Process LLM response to detect and execute tool calls.
        
        Returns:
            (processed_response, tool_result)
        """
        if "TOOL_CALL:" in response:
            # Extract tool call
            tool_call_str = response.split("TOOL_CALL:")[1].strip()
            
            # Execute
            result = self.registry.call_tool(tool_call_str)
            
            # Format result back
            if result.success:
                formatted = f"Tool result: {json.dumps(result.data)}"
            else:
                formatted = f"Tool error: {result.error}"
            
            return formatted, result
        
        return response, None
