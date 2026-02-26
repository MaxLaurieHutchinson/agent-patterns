# Tool Use (MCP) Pattern

The Tool Use pattern implements Model Context Protocol (MCP)-style integration: a standardized way for LLMs to discover and use external tools.

## Core Concept

```
LLM -> Tool Registry/Manifest -> Tool Call -> Tool Execution -> Structured Result
```

## Key Components

### Tool Registry
- Discovers available tools
- Provides tool schemas
- Routes execution requests to tools

### Tool Schema
- Name and description
- Parameter definitions (JSON Schema-like)
- Optional return hints/examples

### Execution Handler
- Validates parameters
- Executes tool logic
- Handles errors consistently
- Returns structured `ToolResult`

## When to Use

### ✅ Use MCP When:
- Need a standardized tool interface
- Multiple tools from different sources
- Dynamic tool discovery
- Schema-based parameter validation
- Production-oriented tool integration architecture

### ❌ Don't Use When:
- Single, simple tool
- Direct function calling is enough
- Discovery/registration adds unnecessary overhead

## Key Benefits

1. **Standardization** - Common interface for tools
2. **Discoverability** - LLMs can inspect available tools
3. **Validation** - Schema/type checks before execution
4. **Composability** - Registry supports many tools
5. **Extensibility** - New tools plug in with minimal wiring

## This Repository's Implementation

- Core implementation: `implementation.py`
- Demo script: `example.py`
- Includes example tools: calculator, search, filesystem
- Provides an MCP-style manifest for LLM prompt injection

### Security Notes

- Filesystem tool operations are constrained to the configured `base_path`.
- Attempts to escape the base directory (for example via `../`) are rejected.
- This is still a demo implementation and should be further hardened for production.

## Related Patterns

- **ReAct Loop** - Uses tools through structured action calls
- **Plan-and-Execute** - Tools can be execution primitives
- **Observer Pattern** - Tool execution events can be published
- **Circuit Breaker** - Protects tool calls to external dependencies

## Manifest Shape (Example)

```json
{
  "version": "1.0",
  "tools": [
    {
      "name": "search",
      "description": "Search for information",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {"type": "string"}
        },
        "required": ["query"]
      }
    }
  ]
}
```
