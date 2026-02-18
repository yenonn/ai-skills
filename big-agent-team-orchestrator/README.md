# Agent Team Orchestrator

A comprehensive multi-agent coordination system that handles task decomposition, agent selection, workflow orchestration, and resource optimization for complex projects.

## Overview

The Agent Team Orchestrator coordinates multiple AI agents to work together efficiently on complex projects. It automatically:

- **Analyzes requirements** and breaks them into components
- **Selects appropriate agents** based on task requirements
- **Creates execution plans** with dependency management
- **Executes workflows** with parallel task processing
- **Manages shared memory** for cross-agent knowledge sharing

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  AgentTeamOrchestrator                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │ TeamCoordinator │  │  MemoryManager  │  │WorkflowEngine│ │
│  │                 │  │                 │  │             │  │
│  │ - Agents        │  │ - Contexts      │  │ - Tasks     │  │
│  │ - Tasks         │  │ - Memory        │  │ - Graph     │  │
│  │ - Assignments   │  │ - Agent States  │  │ - Execution │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Installation

No external dependencies required - uses Python standard library only.

```bash
# Navigate to the skill directory
cd ~/.config/opencode/skills/big-agent-team-orchestrator

# Verify installation
python3 scripts/test_orchestrator.py
```

## Quick Start

### 1. Using the CLI

```bash
# Run a demo orchestration
python3 scripts/cli.py demo

# Analyze a project request (without executing)
python3 scripts/cli.py analyze "Build a React frontend with API integration"

# Execute full orchestration
python3 scripts/cli.py orchestrate "Build a web app with database" --project "MyProject"

# Check orchestrator status
python3 scripts/cli.py status
```

### 2. Using Python API

```python
from scripts import AgentTeamOrchestrator, OrchestrationStrategy

# Initialize orchestrator
orchestrator = AgentTeamOrchestrator(
    strategy=OrchestrationStrategy.AUTOMATIC,
    storage_path="/tmp/my_project"
)

# Run complete orchestration
result = orchestrator.orchestrate_complete_project(
    user_request="Build a React frontend with Node.js backend and PostgreSQL",
    project_name="Full Stack Application"
)

# Check results
print(f"Success: {result['success']}")
print(f"Tasks: {len(result['tasks'])}")
print(f"Duration: {result['total_duration']:.2f}s")
```

## CLI Commands

### `orchestrate` - Run Full Orchestration

```bash
python3 scripts/cli.py orchestrate "Your project description" [options]

Options:
  --project, -p    Project name (default: "Orchestrated Project")
  --strategy, -s   Strategy: automatic, request_based, scheduled
  --storage, -d    Path for persistent storage
  --json, -j       Output results as JSON
```

**Example:**
```bash
python3 scripts/cli.py orchestrate \
  "Build an e-commerce platform with user authentication, product catalog, and payment integration" \
  --project "E-Commerce Platform" \
  --strategy automatic \
  --json
```

### `analyze` - Analyze Without Executing

```bash
python3 scripts/cli.py analyze "Your project description" [options]

Options:
  --json, -j       Output as JSON
```

**Example:**
```bash
python3 scripts/cli.py analyze "Create a REST API with database and testing"
```

**Output:**
```
REQUEST ANALYSIS
============================================================

Original Request: Create a REST API with database and testing

Components (3):
  - [component-0] BACKEND
    Description: Backend implementation
    Priority: 2
  - [component-1] DATABASE
    Description: Database setup and operations
    Priority: 2
  - [component-2] TESTING
    Description: Testing and validation
    Priority: 2

Dependencies (2):
  - component-0: Sequential dependency
  - component-1: Sequential dependency

Estimated Resources:
  Min Agents: 1
  Max Agents: 5
  Estimated Duration: 3600s
```

### `status` - Check Orchestrator Status

```bash
python3 scripts/cli.py status [--storage /path/to/storage]
```

### `demo` - Run Demo Orchestration

```bash
python3 scripts/cli.py demo
```

## Python API Reference

### AgentTeamOrchestrator

Main orchestrator class for multi-agent coordination.

```python
from scripts import AgentTeamOrchestrator, OrchestrationStrategy

orchestrator = AgentTeamOrchestrator(
    strategy=OrchestrationStrategy.AUTOMATIC,  # or REQUEST_BASED, SCHEDULED
    storage_path="/tmp/project_data"           # optional, for persistence
)
```

**Methods:**

| Method | Description |
|--------|-------------|
| `analyze_requirements(request)` | Analyze and decompose user requirements |
| `select_agents_for_components(components)` | Select agents for task components |
| `create_tasks_from_analysis(analysis)` | Create task objects from analysis |
| `initialize_shared_context(project_name)` | Initialize shared memory context |
| `coordinate_workflow(tasks, agents, context_id)` | Execute workflow coordination |
| `orchestrate_complete_project(request, name)` | Run complete orchestration |
| `get_team_status()` | Get current team status |
| `monitor_execution()` | Monitor ongoing execution |

### TeamCoordinator

Manages agents, tasks, and assignments.

```python
from scripts import TeamCoordinator, Task, AgentInfo

coordinator = TeamCoordinator()

# Add agents
coordinator.add_agent(AgentInfo(
    id="dev-1",
    name="Developer",
    capabilities=["python", "javascript"]
))

# Add tasks
coordinator.add_task(Task(
    id="task-1",
    title="Implement Feature",
    description="Build the main feature",
    priority=2
))

# Assign and complete
coordinator.assign_task("task-1", "dev-1")
coordinator.complete_task("task-1", {"output": "completed"})

# Get status
status = coordinator.get_team_status()
```

### MemoryManager

Handles shared knowledge and context persistence.

```python
from scripts import MemoryManager, SharedContext, MemoryType

manager = MemoryManager(storage_path="/tmp/memory")

# Create context
context = SharedContext(
    project_id="my-project",
    name="My Project",
    description="Project description"
)
context_id = manager.create_context(context)

# Add memory
manager.add_memory(
    content={"decision": "use_react"},
    memory_type=MemoryType.DECISION_HISTORY,
    context_id=context_id
)

# Update agent state
manager.add_to_agent_state(context_id, "agent-1", {"status": "active"})

# Persist to disk
manager.save_to_disk()
```

### WorkflowEngine

Executes dependency-based workflows.

```python
from scripts import WorkflowEngine, TaskNode, ExecutionStrategy

engine = WorkflowEngine(strategy=ExecutionStrategy.HYBRID)

# Add tasks with dependencies
engine.add_task(TaskNode(
    id="task-1",
    title="Setup Database",
    description="Initialize database schema",
    dependencies=[]
))

engine.add_task(TaskNode(
    id="task-2", 
    title="Build API",
    description="Create REST endpoints",
    dependencies=["task-1"]  # depends on task-1
))

# Build dependency graph
engine.build_graph()

# Create execution plan
plan = engine.create_execution_plan()
print(f"Parallel groups: {len(plan)}")

# Execute workflow
results = engine.execute_workflow(
    max_parallel_tasks=3,
    timeout=3600
)
```

## Component Detection

The orchestrator automatically detects components from natural language:

| Keywords | Component Type | Agent Selected |
|----------|---------------|----------------|
| `frontend`, `ui`, `react`, `vue` | Frontend | Frontend Specialist |
| `backend`, `api`, `server`, `node` | Backend | Backend Developer |
| `database`, `db`, `sql`, `postgres` | Database | Backend Developer |
| `test`, `testing`, `qa` | Testing | QA Specialist |
| `deploy`, `deployment`, `ci/cd` | Deployment | DevOps Engineer |

## Memory Types

```python
from scripts import MemoryType

MemoryType.TASK_RESULTS      # Results from completed tasks
MemoryType.DECISION_HISTORY  # Decisions made during project
MemoryType.COMMON_KNOWLEDGE  # Shared project knowledge
MemoryType.AGENT_CONTEXT     # Agent-specific context
MemoryType.TEMPORARY         # Temporary working memory
```

## Execution Strategies

```python
from scripts import ExecutionStrategy

ExecutionStrategy.SEQUENTIAL  # Execute tasks one by one
ExecutionStrategy.PARALLEL    # Execute all tasks in parallel
ExecutionStrategy.HYBRID      # Parallel within groups, sequential between
```

## Example: Full Project Workflow

```python
from scripts import (
    AgentTeamOrchestrator,
    OrchestrationStrategy,
    MemoryType
)

# 1. Initialize
orchestrator = AgentTeamOrchestrator(
    strategy=OrchestrationStrategy.AUTOMATIC,
    storage_path="/tmp/ecommerce_project"
)

# 2. Define project
request = """
Build an e-commerce platform with:
- React frontend with product catalog
- Node.js backend API
- PostgreSQL database
- User authentication
- Payment integration
- Comprehensive testing
"""

# 3. Execute orchestration
result = orchestrator.orchestrate_complete_project(
    user_request=request,
    project_name="E-Commerce Platform"
)

# 4. Review results
if result["success"]:
    print("Project orchestration completed!")
    print(f"Tasks executed: {len(result['tasks'])}")
    print(f"Agents used: {len(result['agents'])}")
    print(f"Total duration: {result['total_duration']:.2f}s")
    
    # Review execution details
    exec_results = result["execution_results"]
    print(f"Completed: {exec_results['completed_tasks']}")
    print(f"Failed: {exec_results['failed_tasks']}")
else:
    print(f"Orchestration failed: {result.get('error')}")

# 5. Check team status
status = orchestrator.get_team_status()
print(f"Completion rate: {status['tasks']['completion_rate']:.1%}")

# 6. Access memory for insights
memory = orchestrator.memory_manager
entries = memory.get_context_memory(
    list(orchestrator.active_contexts.keys())[0],
    memory_type=MemoryType.TASK_RESULTS
)
for entry in entries[:5]:
    print(f"Task result: {entry.content}")
```

## Running Tests

```bash
cd ~/.config/opencode/skills/big-agent-team-orchestrator
python3 scripts/test_orchestrator.py
```

**Expected output:**
```
============================================================
AGENT TEAM ORCHESTRATOR - TEST SUITE
============================================================

--- Testing TeamCoordinator ---
  TeamCoordinator: PASSED

--- Testing MemoryManager ---
  MemoryManager: PASSED

--- Testing WorkflowEngine ---
  WorkflowEngine: PASSED

--- Testing AgentTeamOrchestrator ---
  AgentTeamOrchestrator: PASSED

--- Testing Full Integration ---
  Integration Test: PASSED

============================================================
TEST RESULTS
============================================================
  TeamCoordinator: PASSED
  MemoryManager: PASSED
  WorkflowEngine: PASSED
  Orchestrator: PASSED
  Integration: PASSED

Total: 5/5 passed, 0 failed
```

## File Structure

```
big-agent-team-orchestrator/
├── SKILL.md                    # Skill metadata and description
├── README.md                   # This file
├── scripts/
│   ├── __init__.py            # Module exports
│   ├── team_coordinator.py    # Agent and task management
│   ├── memory_manager.py      # Shared memory and persistence
│   ├── workflow_engine.py     # Workflow execution engine
│   ├── orchestrator.py        # Main orchestrator
│   ├── cli.py                 # Command-line interface
│   └── test_orchestrator.py   # Integration tests
└── references/
    ├── coordination_patterns.md   # Coordination pattern docs
    ├── agent_capabilities.md      # Agent capability reference
    └── workflow_templates.md      # Workflow template examples
```

## Extending the Orchestrator

### Adding Custom Agents

```python
from scripts import AgentInfo, TeamCoordinator

coordinator = TeamCoordinator()

# Add custom agent type
coordinator.add_agent(AgentInfo(
    id="ml-engineer",
    name="ML Engineer",
    capabilities=["python", "tensorflow", "pytorch", "mlops"],
    specializations=["machine-learning", "data-science"]
))
```

### Custom Workflow Templates

```python
from scripts import WorkflowEngine, TaskNode

engine = WorkflowEngine()

# Define custom workflow
tasks = [
    TaskNode(id="data-prep", title="Data Preparation", dependencies=[]),
    TaskNode(id="training", title="Model Training", dependencies=["data-prep"]),
    TaskNode(id="eval", title="Evaluation", dependencies=["training"]),
    TaskNode(id="deploy", title="Deployment", dependencies=["eval"]),
]

for task in tasks:
    engine.add_task(task)

engine.build_graph()
results = engine.execute_workflow()
```

## License

Part of the OpenCode skills ecosystem.
