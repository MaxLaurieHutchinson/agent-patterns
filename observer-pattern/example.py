"""
Observer Pattern Example
Demonstrates event-driven agent coordination.
"""

from implementation import EventBus, AgentObserver, CoordinatorAgent, LoggingAgent, NotificationAgent, Event


def demo_basic_pubsub():
    """Demonstrate basic publish/subscribe."""
    print("\n" + "="*60)
    print("BASIC PUB/SUB DEMO")
    print("="*60)
    
    # Create event bus
    bus = EventBus()
    
    # Create simple handlers
    events_received = []
    
    def task_handler(event: Event):
        events_received.append(f"Task handler: {event.topic}")
        print(f"   📋 Task handler received: {event.topic}")
    
    def all_handler(event: Event):
        events_received.append(f"All handler: {event.topic}")
        print(f"   📡 All handler received: {event.topic}")
    
    # Subscribe
    print("\n📌 Subscribing handlers...")
    bus.subscribe("task.created", task_handler)
    bus.subscribe("task.completed", task_handler)
    bus.subscribe("*", all_handler)  # Wildcard
    
    # Publish events
    print("\n📤 Publishing events...")
    bus.publish_simple("task.created", {"task_id": "T1", "name": "Write report"})
    bus.publish_simple("task.completed", {"task_id": "T1", "result": "Done"})
    bus.publish_simple("user.login", {"user_id": "U123"})  # Won't match task_handler
    
    print(f"\n📊 Total events received: {len(events_received)}")


def demo_wildcard_patterns():
    """Demonstrate wildcard pattern matching."""
    print("\n" + "="*60)
    print("WILDCARD PATTERNS DEMO")
    print("="*60)
    
    bus = EventBus()
    
    # Track which handlers receive which events
    received = {}
    
    def make_handler(name):
        def handler(event: Event):
            if name not in received:
                received[name] = []
            received[name].append(event.topic)
        return handler
    
    # Subscribe with different patterns
    print("\n📌 Subscribing with patterns...")
    patterns = [
        ("task.*", "Task wildcard"),
        ("task.*.high", "Task high priority"),
        ("agent.**", "Agent multi-level"),
        ("*.error", "Any error"),
        ("**", "Everything"),
    ]
    
    for pattern, name in patterns:
        bus.subscribe(pattern, make_handler(name))
        print(f"   '{pattern}' -> {name}")
    
    # Publish test events
    print("\n📤 Publishing test events...")
    test_events = [
        "task.created",
        "task.completed.high",
        "agent.state.changed",
        "agent.memory.updated.user",
        "system.error",
        "user.login",
    ]
    
    for topic in test_events:
        bus.publish_simple(topic, {"test": True})
        print(f"\n   Published: {topic}")
        print("   Handlers notified:", end=" ")
        notified = []
        for name, topics in received.items():
            if topic in topics:
                notified.append(name)
        print(", ".join(notified) if notified else "None")


def demo_agent_coordination():
    """Demonstrate multi-agent coordination."""
    print("\n" + "="*60)
    print("MULTI-AGENT COORDINATION DEMO")
    print("="*60)
    
    # Create event bus
    bus = EventBus()
    
    # Create specialized agents
    coordinator = CoordinatorAgent("coordinator", bus)
    logger = LoggingAgent("logger", bus)
    notifier = NotificationAgent("notifier", bus)
    
    print("\n🤖 Agents initialized:")
    print(f"   - Coordinator (interests: {coordinator.interests})")
    print(f"   - Logger (interests: {logger.interests})")
    print(f"   - Notifier (interests: {notifier.interests})")
    
    # Simulate task workflow
    print("\n📋 Simulating task workflow...")
    
    # Step 1: Task created
    print("\n1️⃣ User creates a task")
    bus.publish_simple(
        "task.created",
        {
            "task_id": "TASK-001",
            "type": "research",
            "name": "Research AI trends",
            "priority": "high"
        },
        source="user_portal"
    )
    
    # Step 2: Task progress
    print("\n2️⃣ Research agent reports progress")
    bus.publish_simple(
        "task.progress",
        {
            "task_id": "TASK-001",
            "progress": 50,
            "status": "gathering_data"
        },
        source="research_agent"
    )
    
    # Step 3: Task completed
    print("\n3️⃣ Research agent completes task")
    bus.publish_simple(
        "task.completed",
        {
            "task_id": "TASK-001",
            "result": "AI trends report: [summary]"
        },
        source="research_agent"
    )
    
    # Step 4: Task fails (different task)
    print("\n4️⃣ Another task fails")
    bus.publish_simple(
        "task.failed",
        {
            "task_id": "TASK-002",
            "error": "API timeout",
            "retryable": True
        },
        source="writer_agent",
        priority=5
    )
    
    print(f"\n📊 Logger captured {len(logger.logs)} events")


def demo_custom_agent():
    """Demonstrate creating custom observer agents."""
    print("\n" + "="*60)
    print("CUSTOM AGENT DEMO")
    print("="*60)
    
    bus = EventBus()
    
    # Create a custom agent that reacts to specific events
    class DataProcessingAgent(AgentObserver):
        def __init__(self, agent_id: str, event_bus: EventBus):
            super().__init__(agent_id, event_bus)
            self.processed_count = 0
            self.subscribe_to(["data.new", "data.batch"])
        
        def on_event(self, event: Event, matched_pattern: str):
            if event.topic == "data.new":
                self.process_single(event.data)
            elif event.topic == "data.batch":
                self.process_batch(event.data)
        
        def process_single(self, data: dict):
            self.processed_count += 1
            print(f"   [{self.agent_id}] Processing single item: {data.get('id')}")
        
        def process_batch(self, data: dict):
            items = data.get("items", [])
            self.processed_count += len(items)
            print(f"   [{self.agent_id}] Processing batch of {len(items)} items")
    
    # Create agent
    processor = DataProcessingAgent("processor_1", bus)
    
    print("\n📤 Publishing data events...")
    bus.publish_simple("data.new", {"id": "ITEM-1", "value": 100})
    bus.publish_simple("data.new", {"id": "ITEM-2", "value": 200})
    bus.publish_simple("data.batch", {
        "items": [
            {"id": "BATCH-1", "value": 10},
            {"id": "BATCH-2", "value": 20},
            {"id": "BATCH-3", "value": 30},
        ]
    })
    
    print(f"\n✅ Total items processed: {processor.processed_count}")


def demo_event_history():
    """Demonstrate event history and replay."""
    print("\n" + "="*60)
    print("EVENT HISTORY DEMO")
    print("="*60)
    
    bus = EventBus(max_history=100)
    
    # Publish some events
    print("\n📤 Publishing events to history...")
    for i in range(5):
        bus.publish_simple(
            f"event.type{i}",
            {"seq": i},
            source="test"
        )
    
    print(f"   History size: {len(bus.history)}")
    
    # Query history
    print("\n🔍 Querying history...")
    all_events = bus.get_history()
    print(f"   All events: {len(all_events)}")
    
    from_events = bus.get_history(source="test")
    print(f"   From 'test' source: {len(from_events)}")
    
    # Replay events
    print("\n🔄 Replaying events...")
    replayed = []
    
    def replay_handler(event: Event):
        replayed.append(event.topic)
    
    bus.replay("event.*", replay_handler)
    print(f"   Replayed {len(replayed)} events: {replayed}")


def main():
    """Run all observer pattern demos."""
    print("\n" + "="*60)
    print("OBSERVER PATTERN DEMONSTRATION")
    print("="*60)
    
    demo_basic_pubsub()
    demo_wildcard_patterns()
    demo_agent_coordination()
    demo_custom_agent()
    demo_event_history()
    
    print("\n" + "="*60)
    print("Demo complete!")
    print("="*60)
    
    print("""
📝 Key Concepts Demonstrated:

1. PUBLISH/SUBSCRIBE
   - Decoupled communication
   - Multiple subscribers per event
   - Event filtering

2. WILDCARD PATTERNS
   - * matches single level
   - ** matches multiple levels
   - Flexible topic hierarchies

3. AGENT COORDINATION
   - Coordinator distributes tasks
   - Logger monitors all activity
   - Notifier handles alerts

4. CUSTOM AGENTS
   - Easy to extend base class
   - Subscribe to relevant patterns
   - React to specific events

5. EVENT HISTORY
   - Automatic event storage
   - Query and filter past events
   - Replay for recovery/debugging
""")


if __name__ == "__main__":
    main()
