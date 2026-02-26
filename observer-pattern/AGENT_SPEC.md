# AGENT_SPEC

## Name
observer_event_bus

## Purpose
Coordinate agent behavior via topic-based event publication and subscription.

## Inputs
- `event` (object): `topic`, `data`, `source`, `priority`
- `subscriptions` (array): topic patterns

## Outputs
- `notified_count` (integer)
- optional `history` (array of events)

## Preconditions
- Event bus initialized.
- Subscribers registered with patterns.

## Procedure
1. Append event to bounded history.
2. Resolve matching handlers by exact/wildcard topic.
3. Invoke handlers (sync or async).
4. Return notified handler count.

## Safety Rules
- Keep wildcard semantics explicit (`*` single-level, `**` multi-level).
- Limit history size to bound memory.
- Catch and report handler exceptions.

## Failure Handling
- Continue dispatch when one handler fails.
- Preserve event history even if handlers fail.

## Telemetry
- publish count
- notified handler count
- handler error count

## Example I/O Contract
```json
{
  "input": {"topic": "task.failed", "data": {"task_id": "T1"}},
  "output": {"notified_count": 2},
  "status": "ok"
}
```
