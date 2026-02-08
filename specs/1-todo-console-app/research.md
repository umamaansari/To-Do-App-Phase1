# Research: Todo In-Memory Python Console App

## Decision: Command Parsing Method
**Rationale**: For a simple CLI app with basic commands, using input().strip().split() is the simplest approach that meets our requirements without adding dependencies.
**Alternatives considered**: 
- Using argparse module (overkill for simple commands)
- Using shlex for better argument handling (unnecessary complexity)

## Decision: Task Storage Structure
**Rationale**: Using a list of dictionaries allows for easy iteration when displaying tasks and maintains insertion order.
**Alternatives considered**: 
- Dictionary with ID as key (more complex for listing operations)

## Decision: ID Generation Logic
**Rationale**: Finding the max existing ID + 1 ensures IDs remain dense even after deletes, which is better for user experience.
**Alternatives considered**: 
- Using len(tasks) + 1 after append (would create gaps in IDs after deletes)

## Decision: Update Command Input Style
**Rationale**: A hybrid approach provides both usability (interactive prompts when needed) and scriptability (full arguments).
**Alternatives considered**: 
- Only accepting full arguments (less user-friendly)
- Only interactive mode (not scriptable)

## Decision: List/View Output Formatting
**Rationale**: Using f-strings with fixed-width formatting provides clean output without external dependencies.
**Alternatives considered**: 
- Using external table library like tabulate (adds dependency unnecessarily)