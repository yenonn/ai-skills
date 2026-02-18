#!/usr/bin/env python3
"""
Team Coordinator - Orchestrates agent assignments and execution flow

This script manages task queues, agent availability, and execution flow
for multi-agent coordination projects.
"""

import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class AgentStatus(Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"


@dataclass
class Task:
    """Represents a work unit that needs to be completed"""

    id: str
    title: str
    description: str
    assigned_agent: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 1
    dependencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_duration: int = 3600
    actual_duration: Optional[int] = None
    outputs: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class AgentInfo:
    """Represents an agent in the team"""

    id: str
    name: str
    capabilities: List[str]
    current_workload: int = 0
    max_workload: int = 100
    status: AgentStatus = AgentStatus.AVAILABLE
    performance_score: float = 1.0
    current_task: Optional[str] = None
    last_active: Optional[datetime] = field(default_factory=datetime.now)
    specializations: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.last_active is None:
            self.last_active = datetime.now()


class TeamCoordinator:
    """Main coordinator class for managing multi-agent teams"""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.agents: Dict[str, AgentInfo] = {}
        self.task_queue: List[str] = []
        self.completed_tasks: List[str] = []
        self.failed_tasks: List[str] = []
        self.execution_history: List[Dict] = []
        self.shared_context: Dict[str, Any] = {}

    def add_agent(self, agent: AgentInfo) -> None:
        """Add an agent to the team"""
        self.agents[agent.id] = agent
        logger.info(f"Added agent: {agent.name} ({agent.id})")

    def add_task(self, task: Task) -> None:
        """Add a task to the coordination system"""
        self.tasks[task.id] = task
        self.task_queue.append(task.id)
        logger.info(f"Added task: {task.title} ({task.id})")

    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """Assign a task to an available agent"""
        if task_id not in self.tasks or agent_id not in self.agents:
            return False

        task = self.tasks[task_id]
        agent = self.agents[agent_id]

        if agent.status != AgentStatus.AVAILABLE:
            logger.warning(f"Agent {agent_id} is not available")
            return False

        # Check dependencies
        for dep_id in task.dependencies:
            if self.tasks[dep_id].status != TaskStatus.COMPLETED:
                logger.warning(f"Task {task_id} has incomplete dependency {dep_id}")
                return False

        task.assigned_agent = agent_id
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()

        agent.status = AgentStatus.BUSY
        agent.current_workload += task.priority * 10
        agent.current_task = task_id
        agent.last_active = datetime.now()

        if task_id in self.task_queue:
            self.task_queue.remove(task_id)

        logger.info(f"Assigned task {task_id} to agent {agent_id}")
        return True

    def complete_task(
        self, task_id: str, outputs: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Mark a task as completed"""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        if task.status != TaskStatus.IN_PROGRESS:
            return False

        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()

        if outputs:
            task.outputs.update(outputs)

        # Calculate actual duration
        if task.started_at:
            duration = (task.completed_at - task.started_at).total_seconds()
            task.actual_duration = int(duration)

        # Update agent status
        if task.assigned_agent:
            agent = self.agents[task.assigned_agent]
            agent.status = AgentStatus.AVAILABLE
            agent.current_workload = max(0, agent.current_workload - task.priority * 10)
            agent.current_task = None
            agent.last_active = datetime.now()

        self.completed_tasks.append(task_id)
        logger.info(f"Completed task: {task_id}")
        return True

    def get_team_status(self) -> Dict[str, Any]:
        """Get current status of the entire team"""
        total_tasks = len(self.tasks)
        completed = len(self.completed_tasks)
        failed = len(self.failed_tasks)
        in_progress = len(
            [t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS]
        )

        agent_stats = {}
        for agent in self.agents.values():
            agent_stats[agent.id] = {
                "name": agent.name,
                "status": agent.status.value,
                "current_workload": agent.current_workload,
                "performance_score": agent.performance_score,
            }

        return {
            "timestamp": datetime.now().isoformat(),
            "tasks": {
                "total": total_tasks,
                "completed": completed,
                "failed": failed,
                "in_progress": in_progress,
                "completion_rate": completed / max(1, total_tasks),
            },
            "agents": agent_stats,
            "shared_context_size": len(self.shared_context),
        }


def main():
    """Example usage of the Team Coordinator"""

    # Initialize coordinator
    coordinator = TeamCoordinator()

    # Add sample agents
    coordinator.add_agent(
        AgentInfo(
            id="frontend-dev-1",
            name="Frontend Specialist",
            capabilities=["react", "css", "ui-design"],
            specializations=["component-development"],
        )
    )

    coordinator.add_agent(
        AgentInfo(
            id="backend-dev-1",
            name="Backend Specialist",
            capabilities=["nodejs", "api-design", "database"],
            specializations=["api-development"],
        )
    )

    # Add sample tasks
    coordinator.add_task(
        Task(
            id="task-1",
            title="Design User Interface",
            description="Create responsive UI components for the dashboard",
            priority=2,
            metadata={"required_capabilities": ["react", "css"]},
        )
    )

    coordinator.add_task(
        Task(
            id="task-2",
            title="Implement Backend API",
            description="Create REST API endpoints for user management",
            priority=2,
            dependencies=["task-1"],
            metadata={"required_capabilities": ["nodejs", "api-design"]},
        )
    )

    # Get team status
    status = coordinator.get_team_status()
    print(json.dumps(status, indent=2))

    return coordinator


if __name__ == "__main__":
    main()
