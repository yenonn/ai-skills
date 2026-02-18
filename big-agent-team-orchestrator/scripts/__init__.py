"""
Agent Team Orchestrator - Multi-agent coordination system

This package provides a comprehensive framework for coordinating multiple AI agents
to work together efficiently on complex projects.
"""

from .team_coordinator import (
    TeamCoordinator,
    Task,
    TaskStatus,
    AgentInfo,
    AgentStatus,
)

from .memory_manager import (
    MemoryManager,
    MemoryEntry,
    MemoryType,
    SharedContext,
    ContextInjector,
)

from .workflow_engine import (
    WorkflowEngine,
    AdaptiveWorkflowEngine,
    WorkflowNode,
    TaskNode,
    WorkflowStatus,
    ExecutionStrategy,
)

from .orchestrator import (
    AgentTeamOrchestrator,
    OrchestrationStrategy,
)

__all__ = [
    # Team Coordinator
    "TeamCoordinator",
    "Task",
    "TaskStatus",
    "AgentInfo",
    "AgentStatus",
    # Memory Manager
    "MemoryManager",
    "MemoryEntry",
    "MemoryType",
    "SharedContext",
    "ContextInjector",
    # Workflow Engine
    "WorkflowEngine",
    "AdaptiveWorkflowEngine",
    "WorkflowNode",
    "TaskNode",
    "WorkflowStatus",
    "ExecutionStrategy",
    # Orchestrator
    "AgentTeamOrchestrator",
    "OrchestrationStrategy",
]

__version__ = "1.0.0"
