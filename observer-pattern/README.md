# Observer Pattern

The Observer pattern enables event-driven agent coordination. Agents subscribe to events and react to changes, enabling loose coupling and reactive behavior.

## Core Concept

```
Publishers -> Event Bus -> Subscribers
```

- **Event Bus** - Central hub for event distribution
- **Publishers** - Agents/components that emit events
- **Subscribers** - Agents/components that react to events

## Topic Pattern Semantics

- `task.created` - exact topic
- `task.*` - single-level wildcard (matches `task.created`, not `task.created.high`)
- `agent.**` - multi-level wildcard (matches `agent.state`, `agent.state.changed`, etc.)

## When to Use

### ✅ Use Observer Pattern When:
- Event-driven workflows
- Multi-agent coordination
- Real-time monitoring
- Loose coupling between components
- Need to broadcast to multiple consumers

### ❌ Don't Use When:
- Simple linear workflows
- Need guaranteed delivery semantics (use a queue/broker)
- Tight coupling is acceptable/preferred

## Key Benefits

1. **Loose Coupling** - Components do not need direct references
2. **Scalability** - Easy to add new subscribers
3. **Flexibility** - Dynamic subscribe/unsubscribe
4. **Reactivity** - Respond to changes quickly
5. **Extensibility** - New event types without heavy refactors

## This Repository's Implementation

- Core implementation: `implementation.py`
- Demo script: `example.py`
- Includes topic subscriptions, wildcard routing, event history, and replay
- Provides sample observer agents (`CoordinatorAgent`, `LoggingAgent`, `NotificationAgent`)

### Current Tradeoffs

- Delivery is in-process and best-effort (no persistence guarantees).
- Async handlers are fire-and-forget in this reference model.
- Ordering is straightforward for sync handlers but not globally serialized across async work.

## Related Patterns

- **Multi-Agent Debate** - Debate participants can coordinate through events
- **Memory Hierarchy** - Event streams can feed memory updates
- **Circuit Breaker** - Circuit state changes can be published as events
- **ReAct Loop** - ReAct agents can react to external event signals
