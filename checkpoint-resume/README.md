# Checkpoint + Resume Pattern

Checkpoint + Resume persists workflow state after each step so interrupted runs can continue from the last safe point.

## Core Concept

```
Execute Step -> Save Checkpoint -> Interrupt? -> Resume from Checkpoint
```

## Why This Pattern

- Handles process restarts and transient failures.
- Prevents redoing completed work.
- Improves reliability for long-running jobs.

## This Repository's Starter

- `implementation.py` provides JSON checkpoint storage and a resumable runner.
- `example.py` demonstrates an interrupted run and resume.
