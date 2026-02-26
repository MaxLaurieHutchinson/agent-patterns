# Tool Use (MCP) Pattern

The Tool Use pattern implements Model Context Protocol (MCP) integration - a standardized way for LLMs to discover and use external tools.

## Core Concept

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Integration                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐         ┌─────────────────────────────┐   │
│  │   LLM       │◀───────▶│     MCP Tool Server         │   │
│  │             │         │                             │   │
│  │ Discovers   │         │  • Tool Registry            │   │
│  │ tools via   │         │  • Schema Definitions       │   │
│  │ manifest    │         │  • Execution Handler        │   │
│  │             │         │  • Result Formatter         │   │
│  └──────┬──────┘         └─────────────────────────────┘   │
│         │                                                   │
│         │ Call                                              │
│         ▼                                                   │
│  ┌─────────────┐         ┌─────────────────────────────┐   │
│  │ Tool Call   │────────▶│    External Services        │   │
│  │  Request    │         │                             │   │
│  │             │◀────────│  • APIs                     │   │
│  │ {tool:      │         │  • Databases                │   │
│  │  name,      │         │  • File Systems             │   │
│  │  params}    │         │  • Custom Functions         │   │
│  └─────────────┘         └─────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Key Components

### Tool Registry
- Discovers available tools
- Provides tool schemas
- Manages tool versions

### Tool Schema
- Name and description
- Parameter definitions (JSON Schema)
- Return type definitions

### Execution Handler
- Validates parameters
- Executes tool logic
- Handles errors
- Formats results

## When to Use

### ✅ Use MCP When:
- Need standardized tool interface
- Multiple tools from different sources
- Dynamic tool discovery
- Complex parameter validation
- Production tool systems

### ❌ Don't Use When:
- Single, simple tool
- Direct function calling is sufficient
- No need for discovery/registration

## Key Benefits

1. **Standardization** - Common interface for all tools
2. **Discoverability** - LLM can find available tools
3. **Type Safety** - Schema validation
4. **Composability** - Chain multiple tools
5. **Extensibility** - Easy to add new tools

## Related Patterns

- **ReAct Loop** - Uses tools through MCP
- **Plan-and-Execute** - Tools as execution primitives
- **Observer Pattern** - Tool execution events
- **Circuit Breaker** - Protect tool calls

## MCP Protocol Overview

```json
{
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
