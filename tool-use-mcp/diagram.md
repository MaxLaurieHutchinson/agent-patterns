# Tool Use (MCP) Architecture

## System Overview

```mermaid
graph TB
    subgraph "Agent"
        A[LLM]
        TC[Tool Caller]
        TR[Tool Registry]
    end
    
    subgraph "MCP Server"
        TM[Tool Manager]
        TV[Tool Validator]
        TE[Tool Executor]
    end
    
    subgraph "Tools"
        T1[Search Tool]
        T2[Calculator]
        T3[File System]
        T4[Database]
    end
    
    A -->|discovers| TR
    TR -->|registers| TM
    A -->|requests| TC
    TC -->|validates| TV
    TV -->|executes| TE
    TE --> T1
    TE --> T2
    TE --> T3
    TE --> T4
```

## Tool Discovery Flow

```mermaid
sequenceDiagram
    participant LLM as LLM
    participant AG as Agent
    participant TR as Tool Registry
    participant TS as Tool Server
    
    LLM->>AG: Start session
    AG->>TR: Discover tools
    TR->>TS: Request manifest
    TS-->>TR: Return tool definitions
    TR-->>AG: Available tools list
    AG-->>LLM: Tool descriptions
    
    LLM->>AG: Call search_tool
    AG->>TR: Get tool schema
    TR-->>AG: Schema definition
    AG->>TS: Execute with params
    TS-->>AG: Return result
    AG-->>LLM: Formatted result
```

## Component Diagram

```mermaid
classDiagram
    class MCPTool {
        +name: str
        +description: str
        +parameters: JSONSchema
        +returns: JSONSchema
        +execute(params)
        +get_schema()
        +validate(params)
    }
    
    class ToolRegistry {
        +tools: dict
        +register(tool)
        +unregister(name)
        +get_tool(name)
        +list_tools()
        +discover()
    }
    
    class ToolValidator {
        +validate(params, schema)
        +sanitize(params)
        +check_types(params, schema)
    }
    
    class ToolExecutor {
        +execute(tool, params)
        +handle_error(error)
        +format_result(result)
        +timeout: float
    }
    
    class MCPServer {
        +registry: ToolRegistry
        +validator: ToolValidator
        +executor: ToolExecutor
        +handle_request(request)
        +get_manifest()
    }
    
    class ToolCall {
        +tool_name: str
        +parameters: dict
        +call_id: str
        +timestamp: datetime
    }
    
    class ToolResult {
        +call_id: str
        +success: bool
        +data: any
        +error: str
        +duration: float
    }
    
    MCPTool --> ToolRegistry : registered in
    ToolRegistry --> MCPServer : managed by
    MCPServer --> ToolValidator : uses
    MCPServer --> ToolExecutor : uses
    ToolExecutor --> MCPTool : executes
    ToolCall --> ToolExecutor : processed by
    ToolExecutor --> ToolResult : produces
```

## Tool Execution Flow

```
┌──────────────────────────────────────────────────────────────┐
│                     Tool Execution                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  LLM Request                                                 │
│  "Search for Python tutorials"                               │
│       │                                                      │
│       ▼                                                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 1. Intent Recognition                                  │  │
│  │                                                        │  │
│  │ Match: search_tool                                     │  │
│  │ Confidence: 0.95                                       │  │
│  │ Extracted params: {query: "Python tutorials"}          │  │
│  └────────────────────┬──────────────────────────────────┘  │
│                       │                                      │
│                       ▼                                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 2. Schema Validation                                   │  │
│  │                                                        │  │
│  │ Tool: search_tool                                      │  │
│  │ Required params: ["query"]                             │  │
│  │ Provided: {query: "Python tutorials"}                  │  │
│  │                                                        │  │
│  │ ✓ query: string (valid)                                │  │
│  │                                                        │  │
│  │ Validation: PASSED                                     │  │
│  └────────────────────┬──────────────────────────────────┘  │
│                       │                                      │
│                       ▼                                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 3. Tool Execution                                      │  │
│  │                                                        │  │
│  │ Calling: search_tool                                   │  │
│  │ Params: {query: "Python tutorials"}                    │  │
│  │                                                        │  │
│  │ Executing...                                           │  │
│  │ [External API call]                                    │  │
│  │                                                        │  │
│  │ Duration: 450ms                                        │  │
│  └────────────────────┬──────────────────────────────────┘  │
│                       │                                      │
│                       ▼                                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 4. Result Processing                                   │  │
│  │                                                        │  │
│  │ Raw result:                                            │  │
│  │ {                                                      │  │
│  │   "results": [...],                                    │  │
│  │   "total": 150,                                        │  │
│  │   "page": 1                                            │  │
│  │ }                                                      │  │
│  │                                                        │  │
│  │ Formatted for LLM:                                     │  │
│  │ "Found 150 Python tutorials. Top results: ..."         │  │
│  └────────────────────┬──────────────────────────────────┘  │
│                       │                                      │
│                       ▼                                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 5. Response to LLM                                     │  │
│  │                                                        │  │
│  │ <Tool Result>                                          │  │
│  │ search_tool found 150 Python tutorials.                │  │
│  │ Here are the top 3 results:                            │  │
│  │ 1. Python Official Tutorial                            │  │
│  │ 2. Real Python - Learn Python Programming              │  │
│  │ 3. Python for Beginners - Full Course                  │  │
│  │ </Tool Result>                                         │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Error Handling

```
┌─────────────────────────────────────────────────────────────┐
│                   Error Handling                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Validation Error                                           │
│  ┌──────────────┐                                           │
│  │ Missing param│──▶ Return: {                              │
│  │ Wrong type   │     error: "Validation failed",          │
│  │ Invalid value│     details: "Parameter 'x' must be      │
│  └──────────────┘              a number, got 'abc'"         │
│                              }                              │
│                                                             │
│  Execution Error                                            │
│  ┌──────────────┐                                           │
│  │ API timeout  │──▶ Return: {                              │
│  │ Network error│     error: "Execution failed",           │
│  │ Tool crash   │     details: "Request timeout after 30s",│
│  └──────────────┘     retryable: true                       │
│                              }                              │
│                                                             │
│  Result Error                                               │
│  ┌──────────────┐                                           │
│  │ Bad format   │──▶ Return: {                              │
│  │ Missing field│     error: "Invalid result",             │
│  │ Type mismatch│     details: "Missing required field      │
│  └──────────────┘              'id' in response"            │
│                              }                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
