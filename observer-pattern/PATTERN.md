# Observer Pattern (Plain Language)

## What It Is
A publish/subscribe model where producers emit events and subscribers react without direct coupling.

## When To Use
- Event-driven workflows.
- Multiple agents need the same signals.
- You want modular coordination.

## When Not To Use
- Strict guaranteed delivery is required.
- Linear workflows are sufficient.

## Inputs
- Event topic
- Event payload
- Subscriber patterns

## Outputs
- Handler invocations
- Optional event history/replay

## Workflow
1. Subscribers register topic patterns.
2. Publisher emits event.
3. Event bus matches handlers.
4. Matching handlers execute.
5. Event can be queried/replayed from history.

## Failure Modes
- Over-broad wildcard subscriptions create noise.
- Slow handlers block synchronous publish paths.
- Missing retry/reliability for critical events.

## Safety Guardrails
- Use explicit topic naming conventions.
- Keep handler side effects bounded.
- Isolate critical delivery on stronger infrastructure when needed.

## Minimal Example
- `task.created` event published.
- Coordinator assigns worker.
- Logger records event.
- Notifier only reacts to failure topics.

## Evaluation Checklist
- [ ] Topic matching works as expected.
- [ ] Subscribers can be added/removed dynamically.
- [ ] Event history and replay function correctly.
- [ ] Non-matching topics do not trigger handlers.
