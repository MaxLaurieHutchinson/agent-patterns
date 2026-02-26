"""
Tool Use (MCP) Example
Demonstrates Model Context Protocol for tool integration.
"""

from implementation import (
    MCPRegistry, MCPAgent, CalculatorTool, SearchTool,
    FileSystemTool, ToolCall, MCPTool
)


def demo_basic_tools():
    """Demonstrate basic tool registration and execution."""
    print("\n" + "="*60)
    print("BASIC TOOLS DEMO")
    print("="*60)
    
    # Create registry
    registry = MCPRegistry()
    
    # Register tools
    print("\n🔧 Registering tools...")
    registry.register(CalculatorTool())
    registry.register(SearchTool())
    
    # List available tools
    print("\n📋 Available tools:")
    for tool_def in registry.list_tools():
        print(f"   - {tool_def['name']}: {tool_def['description']}")
    
    # Execute calculator
    print("\n🧮 Executing calculator...")
    result = registry.execute("calculator", {"expression": "100 / 4 + 25"})
    print(f"   Success: {result.success}")
    print(f"   Result: {result.data}")
    print(f"   Duration: {result.duration_ms:.2f}ms")
    
    # Execute search
    print("\n🔍 Executing search...")
    result = registry.execute("search", {"query": "python tutorials", "limit": 3})
    print(f"   Success: {result.success}")
    print(f"   Found: {result.data['total']} results")
    print(f"   Top results: {result.data['results']}")


def demo_validation():
    """Demonstrate parameter validation."""
    print("\n" + "="*60)
    print("VALIDATION DEMO")
    print("="*60)
    
    registry = MCPRegistry()
    registry.register(CalculatorTool())
    
    # Valid call
    print("\n✅ Valid call:")
    result = registry.execute("calculator", {"expression": "2 + 2"})
    print(f"   Result: {result.success} - {result.data}")
    
    # Missing required parameter
    print("\n❌ Missing required parameter:")
    result = registry.execute("calculator", {})
    print(f"   Result: {result.success} - {result.error}")
    
    # Wrong type
    print("\n❌ Wrong parameter type:")
    result = registry.execute("calculator", {"expression": 123})
    print(f"   Result: {result.success} - {result.error}")
    
    # Unknown tool
    print("\n❌ Unknown tool:")
    result = registry.execute("nonexistent", {})
    print(f"   Result: {result.success} - {result.error}")


def demo_string_parsing():
    """Demonstrate parsing tool calls from strings."""
    print("\n" + "="*60)
    print("STRING PARSING DEMO")
    print("="*60)
    
    registry = MCPRegistry()
    registry.register(CalculatorTool())
    registry.register(SearchTool())
    
    # Parse and execute from string
    calls = [
        'calculator(expression="15 * 4")',
        'search(query="AI news", limit=5)',
        'calculator(expression="(100 + 50) / 3")',
    ]
    
    for call_str in calls:
        print(f"\n📝 Parsing: {call_str}")
        result = registry.call_tool(call_str)
        if result.success:
            print(f"   ✅ Result: {result.data}")
        else:
            print(f"   ❌ Error: {result.error}")
        print(f"   ⏱️  Duration: {result.duration_ms:.2f}ms")


def demo_agent_integration():
    """Demonstrate agent integration with tools."""
    print("\n" + "="*60)
    print("AGENT INTEGRATION DEMO")
    print("="*60)
    
    # Setup
    registry = MCPRegistry()
    registry.register(CalculatorTool())
    registry.register(SearchTool())
    
    agent = MCPAgent(registry)
    
    # Show system prompt
    print("\n🤖 System prompt with tools:")
    print("-"*60)
    print(agent.get_system_prompt())
    print("-"*60)
    
    # Simulate LLM responses
    print("\n💬 Simulating LLM interactions...")
    
    responses = [
        "I'll help you calculate that.",
        "TOOL_CALL: calculator(expression=\"125 * 8\")",
        "The result is 1000.",
    ]
    
    for response in responses:
        print(f"\n   LLM: {response}")
        processed, result = agent.process_llm_response(response)
        
        if result:
            print(f"   System: Executed tool call")
            print(f"   Result: {processed}")


def demo_custom_tool():
    """Demonstrate creating custom tools."""
    print("\n" + "="*60)
    print("CUSTOM TOOL DEMO")
    print("="*60)
    
    # Create a custom tool
    class WeatherTool(MCPTool):
        @property
        def name(self) -> str:
            return "weather"
        
        @property
        def description(self) -> str:
            return "Get weather information for a location."
        
        def _build_schema(self):
            from implementation import ToolSchema
            return ToolSchema(
                name=self.name,
                description=self.description,
                parameters={
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City name"
                        },
                        "units": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "default": "celsius"
                        }
                    },
                    "required": ["location"]
                }
            )
        
        def _execute(self, location: str, units: str = "celsius"):
            # Mock weather data
            mock_data = {
                "London": {"temp": 18, "condition": "Cloudy"},
                "New York": {"temp": 22, "condition": "Sunny"},
                "Tokyo": {"temp": 25, "condition": "Rainy"}
            }
            
            data = mock_data.get(location, {"temp": 20, "condition": "Unknown"})
            
            if units == "fahrenheit":
                data["temp"] = data["temp"] * 9/5 + 32
            
            return {
                "location": location,
                "temperature": data["temp"],
                "units": units,
                "condition": data["condition"]
            }
    
    # Use the custom tool
    registry = MCPRegistry()
    registry.register(WeatherTool())
    
    print("\n🌤️  Using custom weather tool:")
    
    for city in ["London", "New York", "Tokyo"]:
        result = registry.execute("weather", {"location": city})
        print(f"\n   {city}:")
        print(f"      {result.data['condition']}, {result.data['temperature']}°{result.data['units'][0].upper()}")


def demo_manifest():
    """Demonstrate MCP manifest generation."""
    print("\n" + "="*60)
    print("MANIFEST DEMO")
    print("="*60)
    
    registry = MCPRegistry()
    registry.register(CalculatorTool())
    registry.register(SearchTool())
    
    # Get manifest
    manifest = registry.get_manifest()
    
    print("\n📄 MCP Manifest:")
    import json
    print(json.dumps(manifest, indent=2))
    
    print("\n💡 This manifest is provided to LLMs so they can discover")
    print("   and understand available tools.")


def main():
    """Run all MCP demos."""
    print("\n" + "="*60)
    print("TOOL USE (MCP) PATTERN DEMONSTRATION")
    print("="*60)
    
    demo_basic_tools()
    demo_validation()
    demo_string_parsing()
    demo_agent_integration()
    demo_custom_tool()
    demo_manifest()
    
    print("\n" + "="*60)
    print("Demo complete!")
    print("="*60)
    
    print("""
📝 Key Concepts Demonstrated:

1. TOOL REGISTRY
   - Central registration of tools
   - Tool discovery via manifest
   - Schema-based tool definitions

2. PARAMETER VALIDATION
   - JSON Schema validation
   - Type checking
   - Required field validation

3. TOOL EXECUTION
   - Synchronous execution
   - Error handling
   - Result formatting
   - Duration tracking

4. AGENT INTEGRATION
   - System prompt generation
   - Tool call parsing from LLM
   - Result processing

5. CUSTOM TOOLS
   - Easy to extend MCPTool
   - Schema definition
   - Business logic implementation
""")


if __name__ == "__main__":
    main()
