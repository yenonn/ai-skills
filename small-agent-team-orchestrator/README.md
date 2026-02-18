# Agent Team Orchestrator

A comprehensive skill for coordinating a multi-agent development team consisting of an Architect, Coder, PR Reviewer, and QA/Tester for software development workflows with parallel execution support.

## Overview

The Agent Team Orchestrator skill provides a structured approach to software development by leveraging specialized agents with distinct roles:

| Agent | Role | Responsibilities |
|-------|------|------------------|
| **Architect** | System design | Technical specifications, architecture decisions, technology selection |
| **Coder** | Implementation | Feature development, testing, documentation, code quality |
| **PR Reviewer** | Quality assurance | Code review, security analysis, standards compliance |
| **QA/Tester** | Validation | Test execution, edge cases, integration testing, sign-off |

## Features

- **Multi-agent coordination** with specialized roles
- **Parallel execution** support for independent tasks
- **Dependency management** between tasks
- **Context preservation** across agent handoffs
- **Quality gates** at each workflow stage
- **Iteration tracking** with configurable limits
- **Subtask support** for task decomposition
- **Blocker tracking** and resolution

## Installation

```bash
# Load the skill in OpenCode
/skill load agent-team-orchestrator
```

## Quick Start

### Create and Track Tasks

```bash
# Create a new task
python scripts/task_tracker.py create "Feature Name" "architect" high

# Check task status
python scripts/task_tracker.py status task_001

# View team overview
python scripts/task_tracker.py team
```

### Delegate to Agents

```bash
# Delegate to Architect
python scripts/agent_delegator.py architect task_001 '{"requirements": "feature description"}'

# Delegate to Coder
python scripts/agent_delegator.py coder task_001 '{"specifications": "from architect"}'

# Delegate to Reviewer
python scripts/agent_delegator.py reviewer task_001 '{"implementation": "completed code"}'

# Delegate to QA
python scripts/agent_delegator.py qa task_001 '{"test_scenarios": [...]}'
```

## Workflow States

```
NEW → ANALYZING → PLANNING → IMPLEMENTING → REVIEWING → TESTING → COMPLETE
                                    ↑              ↓           ↑
                                    └── ITERATION ←───────────┘
```

| State | Description | Agent |
|-------|-------------|-------|
| `new` | Task created, awaiting start | Coordinator |
| `analyzing` | Requirements analysis | Architect |
| `planning` | Architecture design | Architect |
| `implementing` | Code development | Coder |
| `reviewing` | Code review | PR Reviewer |
| `testing` | QA validation | QA/Tester |
| `iteration` | Addressing feedback | Coder |
| `blocked` | Has blockers | Any |
| `complete` | Finished and approved | - |

## Task Management

### Creating Tasks

```bash
# Basic task creation
python scripts/task_tracker.py create "Task Title" <task_type> [priority]

# Task types: architect, coder, pr_reviewer, qa_tester
# Priorities: low, medium, high, critical

# Examples
python scripts/task_tracker.py create "Auth System" "architect" high
python scripts/task_tracker.py create "Bug Fix" "coder" critical
```

### Subtasks and Parallel Execution

```bash
# Create subtask under parent
python scripts/task_tracker.py subtask <parent_id> "Subtask Title" <type>

# Create parallel subtasks
python scripts/task_tracker.py subtask task_001 "API Service" "coder" --parallel-group auth
python scripts/task_tracker.py subtask task_001 "DB Layer" "coder" --parallel-group auth

# View parallel groups
python scripts/task_tracker.py parallel

# Check ready tasks (all dependencies met)
python scripts/task_tracker.py ready
```

### Dependencies

```bash
# Add dependency (task_002 depends on task_001)
python scripts/task_tracker.py depend task_002 task_001

# View task tree with dependencies
python scripts/task_tracker.py tree task_001
```

### Blockers

```bash
# Add blocker
python scripts/task_tracker.py blocker task_001 "Waiting for API key"

# Remove blocker by index
python scripts/task_tracker.py unblock task_001 0
```

### Quality Gates

```bash
# Set quality gate status
python scripts/task_tracker.py gate task_001 architecture_approved true
python scripts/task_tracker.py gate task_001 tests_passing true
python scripts/task_tracker.py gate task_001 review_approved true
python scripts/task_tracker.py gate task_001 qa_validated true
```

## Agent Delegation

### Architect

```bash
python scripts/agent_delegator.py architect <task_id> '{
  "feature": "Feature description",
  "requirements": ["req1", "req2"],
  "constraints": ["constraint1"]
}'
```

**Expected Deliverables:**
- Technical specifications document
- System architecture design
- API design documentation
- Database schema
- Technology stack decisions
- Security considerations

### Coder

```bash
python scripts/agent_delegator.py coder <task_id> '{
  "architect_specs": {...},
  "component": "Component name"
}'
```

**Expected Deliverables:**
- Working implementation
- Unit tests (>80% coverage)
- Integration tests
- Code documentation

### PR Reviewer

```bash
python scripts/agent_delegator.py reviewer <task_id> '{
  "implementation": "summary",
  "files_changed": [...],
  "test_coverage": "85%"
}'
```

**Review Checklist:**
- Security review
- Code quality
- Test coverage
- Performance
- Architectural compliance

### QA/Tester

```bash
python scripts/agent_delegator.py qa <task_id> '{
  "test_scenarios": ["scenario1", "scenario2"],
  "acceptance_criteria": ["criteria1"]
}'
```

**Expected Deliverables:**
- Test execution results
- Bug reports
- Coverage analysis
- Sign-off recommendation

### Context Management

```bash
# Get current assignee
python scripts/agent_delegator.py current task_001

# Get full task context
python scripts/agent_delegator.py context task_001

# Get delegation history
python scripts/agent_delegator.py history task_001
```

## Example Workflow

### Feature Development with Parallel Execution

```bash
# 1. Create main task
python scripts/task_tracker.py create "User Management" "architect" high

# 2. Architect analyzes and designs
python scripts/agent_delegator.py architect task_001 '{
  "features": ["registration", "authentication", "profile"],
  "constraints": ["must integrate with existing system"]
}'

# 3. Create parallel subtasks
python scripts/task_tracker.py subtask task_001 "Auth Service" "coder" --parallel-group user_mgmt
python scripts/task_tracker.py subtask task_001 "Profile Service" "coder" --parallel-group user_mgmt

# 4. Implement in parallel
python scripts/task_tracker.py update task_002 implementing coder
python scripts/agent_delegator.py coder task_002 '{"architect_specs": {...}}'

python scripts/task_tracker.py update task_003 implementing coder
python scripts/agent_delegator.py coder task_003 '{"architect_specs": {...}}'

# 5. Review each component
python scripts/agent_delegator.py reviewer task_002 '{"implementation": {...}}'

# 6. QA validates integration
python scripts/task_tracker.py update task_001 testing qa_tester
python scripts/agent_delegator.py qa task_001 '{"test_scenarios": [...]}'

# 7. Set quality gates
python scripts/task_tracker.py gate task_001 architecture_approved true
python scripts/task_tracker.py gate task_001 tests_passing true
python scripts/task_tracker.py gate task_001 review_approved true
python scripts/task_tracker.py gate task_001 qa_validated true

# 8. Complete
python scripts/task_tracker.py update task_001 complete
```

## Architecture

```
agent-team-orchestrator/
├── SKILL.md                    # Main skill definition & orchestration instructions
├── README.md                   # This file
├── scripts/
│   ├── task_tracker.py         # Task management with dependencies & parallel support
│   └── agent_delegator.py      # Agent coordination with context preservation
└── references/
    ├── workflow-patterns.md    # Development workflows & parallel patterns
    ├── integration-examples.md # Usage examples & command reference
    └── sub-agent-examples.md   # Agent implementation examples
```

## Configuration

### Task States
- `new`, `analyzing`, `planning`, `implementing`, `reviewing`, `testing`, `iteration`, `blocked`, `complete`

### Priorities
- `low`, `medium`, `high`, `critical`

### Quality Gates
- `architecture_approved`
- `tests_passing`
- `review_approved`
- `qa_validated`

### Iteration Limits
- Default: 3 maximum iterations
- Configurable per task via `max_iterations` field

## Best Practices

### Communication
- Include comprehensive context when delegating
- Document decisions at each handoff
- Use clear, actionable feedback

### Quality Assurance
- Never skip PR review
- Require >80% test coverage
- Use quality gates for checkpoints
- Always validate with QA

### Parallel Execution
- Group independent tasks in parallel groups
- Set dependencies before starting
- Monitor parallel group progress

### Iteration Management
- Track iteration count
- Escalate if >3 iterations needed
- Document iteration reasons

## Troubleshooting

### Task not found
```bash
# Verify task ID format (task_001, task_002, etc.)
python scripts/task_tracker.py team  # List all tasks
```

### Context not preserved
```bash
# Check delegation history
python scripts/agent_delegator.py history task_001

# Get current context
python scripts/agent_delegator.py context task_001
```

### Blocked tasks
```bash
# View blockers
python scripts/task_tracker.py status task_001

# Remove resolved blocker
python scripts/task_tracker.py unblock task_001 0
```

### Too many iterations
```bash
# Check iteration count
python scripts/task_tracker.py status task_001

# If stuck, escalate or decompose into smaller tasks
```

## Storage

Data is stored in `.dev_team/` directory:

```
.dev_team/
├── tasks.json        # Task definitions and state
├── delegations.json  # Delegation records
├── context.json      # Accumulated context per task
└── history.json      # Full delegation history
```

## License

This skill is provided as-is for use with OpenCode. Modify and adapt as needed for your team workflows.

---

**Agent Team Orchestrator** - Coordinating software development through specialized AI agents with parallel execution support
