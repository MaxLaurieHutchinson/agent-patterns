"""
Observer Pattern Implementation
Event-driven agent coordination with pub/sub messaging.
"""

from typing import Callable, Any, Optional, Protocol
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import uuid
import asyncio
from concurrent.futures import ThreadPoolExecutor


@dataclass
class Event:
    """An event in the system."""
    topic: str
    data: dict
    source: str = "unknown"
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 0  # Higher = more important
    
    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "topic": self.topic,
            "data": self.data,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority
        }


class EventHandler(Protocol):
    """Protocol for event handlers."""
    def __call__(self, event: Event) -> Any:
        ...


class EventBus:
    """
    Central event bus for pub/sub communication.
    
    Supports:
    - Topic-based routing
    - Wildcard patterns (*, **)
    - Synchronous and asynchronous handlers
    - Event history
    """
    
    def __init__(self, max_history: int = 1000):
        self.subscribers: dict[str, list[EventHandler]] = defaultdict(list)
        self.wildcard_subscribers: list[tuple[str, EventHandler]] = []
        self.history: list[Event] = []
        self.max_history = max_history
        self._executor = ThreadPoolExecutor(max_workers=10)
        self._async_mode = False
    
    def subscribe(self, pattern: str, handler: EventHandler):
        """
        Subscribe to events matching a pattern.
        
        Patterns:
        - "task.completed" - exact match
        - "task.*" - any single level
        - "agent.**" - any multi-level
        """
        if '*' in pattern:
            self.wildcard_subscribers.append((pattern, handler))
        else:
            self.subscribers[pattern].append(handler)
    
    def unsubscribe(self, pattern: str, handler: EventHandler):
        """Unsubscribe a handler from a pattern."""
        if '*' in pattern:
            self.wildcard_subscribers = [
                (p, h) for p, h in self.wildcard_subscribers
                if not (p == pattern and h == handler)
            ]
        else:
            if handler in self.subscribers[pattern]:
                self.subscribers[pattern].remove(handler)
    
    def publish(self, event: Event) -> int:
        """
        Publish an event to all matching subscribers.
        
        Returns:
            Number of subscribers notified
        """
        # Store in history
        self.history.append(event)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        # Find matching handlers
        handlers = self._get_matching_handlers(event.topic)
        
        # Notify handlers
        notified = 0
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    # Async handler - schedule it
                    asyncio.create_task(handler(event))
                else:
                    # Sync handler - call directly or in thread
                    handler(event)
                notified += 1
            except Exception as e:
                print(f"Error notifying handler for {event.topic}: {e}")
        
        return notified
    
    def publish_simple(self, topic: str, data: dict, 
                       source: str = "unknown", priority: int = 0) -> int:
        """Convenience method to create and publish an event."""
        event = Event(
            topic=topic,
            data=data,
            source=source,
            priority=priority
        )
        return self.publish(event)
    
    def _get_matching_handlers(self, topic: str) -> list[EventHandler]:
        """Get all handlers matching a topic."""
        handlers = []
        
        # Exact match handlers
        if topic in self.subscribers:
            handlers.extend(self.subscribers[topic])
        
        # Wildcard handlers
        for pattern, handler in self.wildcard_subscribers:
            if self._topic_matches(pattern, topic):
                handlers.append(handler)
        
        return handlers
    
    def _topic_matches(self, pattern: str, topic: str) -> bool:
        """Check if a topic matches a pattern."""
        pattern_parts = pattern.split(".")
        topic_parts = topic.split(".")

        def match(p_idx: int, t_idx: int) -> bool:
            while p_idx < len(pattern_parts):
                part = pattern_parts[p_idx]

                if part == "**":
                    # "**" matches zero or more topic levels.
                    if p_idx == len(pattern_parts) - 1:
                        return True
                    for next_idx in range(t_idx, len(topic_parts) + 1):
                        if match(p_idx + 1, next_idx):
                            return True
                    return False

                if t_idx >= len(topic_parts):
                    return False

                if part != "*" and part != topic_parts[t_idx]:
                    return False

                p_idx += 1
                t_idx += 1

            return t_idx == len(topic_parts)

        return match(0, 0)
    
    def get_history(self, topic_pattern: Optional[str] = None,
                    since: Optional[datetime] = None,
                    source: Optional[str] = None) -> list[Event]:
        """Get event history with optional filtering."""
        events = self.history
        
        if topic_pattern:
            events = [e for e in events if self._topic_matches(topic_pattern, e.topic)]
        
        if since:
            events = [e for e in events if e.timestamp >= since]
        
        if source:
            events = [e for e in events if e.source == source]
        
        return events
    
    def replay(self, topic: str, handler: EventHandler,
               since: Optional[datetime] = None):
        """Replay historical events to a handler."""
        events = self.get_history(topic_pattern=topic, since=since)
        for event in events:
            try:
                handler(event)
            except Exception as e:
                print(f"Error replaying event {event.event_id}: {e}")


class AgentObserver:
    """
    Base class for agents that observe events.
    
    Agents can subscribe to events and react to them.
    """
    
    def __init__(self, agent_id: str, event_bus: Optional[EventBus] = None):
        self.agent_id = agent_id
        self.event_bus = event_bus
        self.subscriptions: list[tuple[str, EventHandler]] = []
        self.interests: list[str] = []
    
    def subscribe_to(self, patterns: list[str]):
        """Subscribe to event patterns."""
        if not self.event_bus:
            raise ValueError("No event bus configured")
        
        for pattern in patterns:
            handler = self._create_handler(pattern)
            self.event_bus.subscribe(pattern, handler)
            self.subscriptions.append((pattern, handler))
            self.interests.append(pattern)
    
    def _create_handler(self, pattern: str) -> EventHandler:
        """Create an event handler for a pattern."""
        def handler(event: Event):
            return self.on_event(event, pattern)
        return handler
    
    def on_event(self, event: Event, matched_pattern: str):
        """
        Called when a subscribed event is received.
        
        Override this method to handle events.
        """
        print(f"[{self.agent_id}] Received event: {event.topic} "
              f"(matched: {matched_pattern})")
    
    def unsubscribe_all(self):
        """Unsubscribe from all patterns."""
        if self.event_bus:
            for pattern, handler in self.subscriptions:
                self.event_bus.unsubscribe(pattern, handler)
        self.subscriptions.clear()
        self.interests.clear()
    
    def emit(self, topic: str, data: dict, priority: int = 0):
        """Emit an event to the bus."""
        if self.event_bus:
            self.event_bus.publish_simple(
                topic=topic,
                data=data,
                source=self.agent_id,
                priority=priority
            )


class CoordinatorAgent(AgentObserver):
    """
    A coordinator agent that manages task distribution
    using the observer pattern.
    """
    
    def __init__(self, agent_id: str, event_bus: EventBus):
        super().__init__(agent_id, event_bus)
        self.active_tasks: dict[str, dict] = {}
        
        # Subscribe to task events
        self.subscribe_to([
            "task.created",
            "task.completed",
            "task.failed"
        ])
    
    def on_event(self, event: Event, matched_pattern: str):
        """Handle task lifecycle events."""
        task_id = event.data.get("task_id")
        
        if event.topic == "task.created":
            self.active_tasks[task_id] = event.data
            print(f"[Coordinator] Tracking new task: {task_id}")
            
            # Assign task to appropriate agent
            task_type = event.data.get("type", "general")
            self.emit("task.assigned", {
                "task_id": task_id,
                "type": task_type,
                "assigned_to": self._select_agent(task_type)
            })
        
        elif event.topic == "task.completed":
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
                print(f"[Coordinator] Task completed: {task_id}")
        
        elif event.topic == "task.failed":
            print(f"[Coordinator] Task failed: {task_id}")
            # Could trigger retry logic here
    
    def _select_agent(self, task_type: str) -> str:
        """Select an agent for a task type."""
        agents = {
            "research": "research_agent",
            "writing": "writer_agent",
            "review": "review_agent"
        }
        return agents.get(task_type, "general_agent")


class LoggingAgent(AgentObserver):
    """Agent that logs all events for monitoring."""
    
    def __init__(self, agent_id: str, event_bus: EventBus):
        super().__init__(agent_id, event_bus)
        self.logs: list[Event] = []
        
        # Subscribe to all events
        self.subscribe_to(["**"])
    
    def on_event(self, event: Event, matched_pattern: str):
        """Log all events."""
        self.logs.append(event)
        print(f"[Logger] {event.timestamp.strftime('%H:%M:%S')} "
              f"{event.topic} from {event.source}")


class NotificationAgent(AgentObserver):
    """Agent that sends notifications for important events."""
    
    def __init__(self, agent_id: str, event_bus: EventBus):
        super().__init__(agent_id, event_bus)
        
        # Subscribe to high-priority events
        self.subscribe_to([
            "task.failed",
            "system.error",
            "*.critical"
        ])
    
    def on_event(self, event: Event, matched_pattern: str):
        """Send notifications for important events."""
        print(f"[Notifier] 🚨 ALERT: {event.topic}")
        print(f"           Source: {event.source}")
        print(f"           Data: {event.data}")
        # In production: send email, Slack, etc.
