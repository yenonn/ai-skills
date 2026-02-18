#!/usr/bin/env python3
"""
Workflow Engine - Executes coordination logic and dependency management

This script implements execution planning algorithms, manages task dependencies
and parallelization, provides quality gates and validation, handles error recovery
and adaptive strategies for multi-agent coordination.
"""

import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import heapq
import threading
from collections import defaultdict
from dataclasses import field as dataclass_field

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    """Status of workflow execution"""

    PLANNED = "planned"
    INITIATED = "initiated"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class ExecutionStrategy(Enum):
    """Execution strategies for workflow"""

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HYBRID = "hybrid"


@dataclass
class TaskNode:
    """Represents a task in the workflow graph"""

    id: str
    title: str
    description: str
    dependencies: List[str] = field(default_factory=list)
    estimated_duration: int = 3600
    assigned_agent: Optional[str] = None
    status: str = "pending"
    execution_order: Optional[int] = None
    parallel_group: Optional[int] = None
    priority: int = 1
    outputs: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None

    def __post_init__(self):
        if self.estimated_duration <= 0:
            self.estimated_duration = 3600

    def mark_complete(self, outputs: Optional[Dict[str, Any]] = None) -> None:
        """Mark this task as completed"""
        self.status = "completed"
        self.completed_at = time.time()
        if outputs:
            self.outputs.update(outputs)


class WorkflowNode:
    """Node in the workflow execution graph"""

    def __init__(
        self,
        task_id: str,
        task: TaskNode,
        predecessors: Optional[List[str]] = None,
        successors: Optional[List[str]] = None,
    ):
        self.task_id = task_id
        self.task = task
        self.predecessors: List[str] = predecessors if predecessors else []
        self.successors: List[str] = successors if successors else []
        self.children: List[str] = []  # Adjacency list for successors
        self.completed = False
        self.started_at: Optional[float] = None
        self.completed_at: Optional[float] = None

    def mark_complete(self, outputs: Optional[Dict[str, Any]] = None) -> None:
        """Mark this task as completed"""
        self.completed = True
        self.completed_at = time.time()
        if outputs:
            self.task.outputs.update(outputs)


class WorkflowEngine:
    """Main workflow engine for managing multi-agent task execution"""

    def __init__(self, strategy: ExecutionStrategy = ExecutionStrategy.HYBRID):
        """
        Initialize the workflow engine

        Args:
            strategy: Execution strategy to use
        """
        self.strategy = strategy
        self.tasks: Dict[str, TaskNode] = {}
        self.task_graph: Dict[str, WorkflowNode] = {}
        self.execution_log: List[Dict] = []
        self.results: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.RLock()
        self.progress_monitoring: Dict[str, float] = {}

    def add_task(self, task: TaskNode) -> None:
        """Add a task to the workflow"""
        with self.lock:
            self.tasks[task.id] = task
            logger.info(f"Added task: {task.title} ({task.id})")

    def build_graph(self) -> None:
        """Build the workflow dependency graph"""
        with self.lock:
            # Initialize workflow nodes
            for task_id, task in self.tasks.items():
                self.task_graph[task_id] = WorkflowNode(task_id, task)

            # Build adjacency list
            for task_id, workflow_node in self.task_graph.items():
                for dep_id in workflow_node.task.dependencies:
                    if dep_id in self.task_graph:
                        self.task_graph[dep_id].children.append(task_id)

            logger.info("Built workflow dependency graph")

    def create_execution_plan(self) -> List[Tuple[int, List[str]]]:
        """
        Create execution plan based on strategy using Kahn's algorithm

        Returns:
            List of (execution_order, task_ids) tuples for parallel groups
        """
        plan: List[Tuple[int, List[str]]] = []

        with self.lock:
            if not self.task_graph:
                return plan

            # Calculate in-degree for each task
            in_degree = {
                task_id: len(workflow_node.task.dependencies)
                for task_id, workflow_node in self.task_graph.items()
            }

            # Start with tasks that have no dependencies
            current_level = [
                task_id for task_id, degree in in_degree.items() if degree == 0
            ]

            parallel_groups: Dict[int, List[str]] = {}
            counter = 0

            while current_level:
                # Add current level as a parallel group
                parallel_groups[counter] = list(current_level)

                # Find next level of tasks
                next_level = []
                for task_id in current_level:
                    # Decrease in-degree for all children
                    for child_id in self.task_graph[task_id].children:
                        in_degree[child_id] -= 1
                        if in_degree[child_id] == 0:
                            next_level.append(child_id)

                current_level = next_level
                counter += 1

            # Convert to plan format
            plan = list(parallel_groups.items())

            # Update task nodes with execution info
            for group_id, task_ids in plan:
                for task_id in task_ids:
                    self.tasks[task_id].parallel_group = group_id
                    self.tasks[task_id].execution_order = group_id

            logger.info(f"Created execution plan with {len(plan)} parallel groups")

            return plan

    def execute_workflow(
        self,
        max_parallel_tasks: int = 3,
        timeout: Optional[int] = None,
        quality_gates: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Execute the workflow

        Args:
            max_parallel_tasks: Maximum number of parallel tasks
            timeout: Workflow timeout in seconds (optional)
            quality_gates: List of quality gate task IDs to validate

        Returns:
            Execution results
        """
        results = {
            "success": False,
            "total_tasks": len(self.tasks),
            "completed_tasks": 0,
            "failed_tasks": 0,
            "total_duration": 0,
            "tasks_completed": [],
            "tasks_failed": [],
            "errors": [],
            "quality_gate_results": {},
        }

        self.execution_log = []

        try:
            # Create execution plan
            plan = self.create_execution_plan()

            start_time = time.time()
            completed = 0
            failed_count = 0

            # Execute each parallel group
            for group_id, task_ids in plan:
                logger.info(
                    f"\n=== Executing Group {group_id} - Tasks: {len(task_ids)} ==="
                )

                if timeout and (time.time() - start_time) > timeout:
                    raise TimeoutError(f"Workflow timeout after {timeout} seconds")

                # Determine group size
                group_size = min(len(task_ids), max_parallel_tasks)

                for i in range(group_size):
                    task_id = task_ids[i % len(task_ids)]

                    # Check if this task has already completed
                    if self.tasks[task_id].status == "completed":
                        completed += 1
                        results["tasks_completed"].append(task_id)
                        continue

                    # Execute task
                    task = self.tasks[task_id]
                    task.status = "running"

                    # Execute logic (mock)
                    outputs = self.execute_single_task(task)

                    if outputs.get("success", False):
                        task.status = "completed"
                        task.mark_complete(outputs.get("outputs", {}))
                        task_graph_node = self.task_graph[task_id]
                        task_graph_node.mark_complete(outputs.get("outputs", {}))

                        completed += 1
                        results["tasks_completed"].append(task_id)

                        # Log progress
                        self.execution_log.append(
                            {
                                "timestamp": time.time() - start_time,
                                "task_id": task_id,
                                "status": "completed",
                                "duration": outputs.get(
                                    "duration", task.estimated_duration
                                ),
                            }
                        )

                        logger.info(f"✓ Completed task {task_id} ({task.title})")
                    else:
                        task.status = "failed"
                        failed_count += 1
                        results["tasks_failed"].append(task_id)
                        results["errors"].append(outputs.get("error", "Unknown error"))

                        logger.error(f"✗ Failed task {task_id} ({task.title})")

            # Check quality gates
            if quality_gates:
                for gate_id in quality_gates:
                    if gate_id in self.tasks:
                        gate_result = self.validate_quality_gate(gate_id)
                        results["quality_gate_results"][gate_id] = gate_result

            # Final results
            end_time = time.time()
            results["success"] = failed_count == 0
            results["completed_tasks"] = completed
            results["failed_tasks"] = failed_count
            results["total_duration"] = end_time - start_time

            logger.info(
                f"\n=== Workflow Execution Complete ===\n"
                f"Total: {len(self.tasks)} tasks, "
                f"Completed: {completed}, "
                f"Failed: {failed_count}, "
                f"Duration: {end_time - start_time:.2f}s"
            )

        except Exception as e:
            results["success"] = False
            results["errors"].append(str(e))
            logger.error(f"Workflow execution failed: {e}")

        return results

    def execute_single_task(self, task: TaskNode) -> Dict[str, Any]:
        """
        Execute a single task
        In a real system, this would invoke an agent
        """
        task.started_at = time.time()

        logger.info(f"Executing task: {task.id}")

        # Simulate task execution
        time.sleep(min(task.estimated_duration / 1000, 1.0))

        duration = time.time() - task.started_at

        # Mock outputs based on task metadata
        outputs = {
            "success": True,
            "outputs": {
                "task_id": task.id,
                "task_title": task.title,
                "completed": True,
            },
            "duration": int(duration),
        }

        return outputs

    def validate_quality_gate(self, task_id: str) -> Dict[str, Any]:
        """
        Validate task outputs against quality gates
        """
        if task_id not in self.tasks:
            return {"valid": False, "reason": "Task not found"}

        if task_id not in self.results:
            return {"valid": False, "reason": "Task not completed"}

        task_result = self.results.get(task_id, {})

        # Check required outputs
        if not task_result.get("completed"):
            return {"valid": False, "reason": "Task was not completed successfully"}

        # Additional validation logic would go here
        # For now, just check basic completion
        return {
            "valid": True,
            "completeness": task_result.get("completeness", 100),
            "quality_score": task_result.get("quality_score", 1.0),
        }

    def monitor_progress(self, task_id: str, progress_update: float) -> None:
        """
        Monitor progress of a task

        Args:
            task_id: Task to monitor
            progress_update: Progress value (0.0 to 1.0)
        """
        with self.lock:
            self.progress_monitoring[task_id] = progress_update
            logger.debug(f"Progress update for {task_id}: {progress_update:.1%}")

    def get_progress(self, task_id: str) -> Optional[float]:
        """
        Get progress of a task

        Args:
            task_id: Task to check progress for

        Returns:
            Progress value or None
        """
        with self.lock:
            return self.progress_monitoring.get(task_id)

    def pause_workflow(self) -> None:
        """Pause workflow execution"""
        logger.info("Workflow execution paused")

    def resume_workflow(self) -> None:
        """Resume workflow execution"""
        logger.info("Workflow execution resumed")

    def cancel_workflow(self) -> None:
        """Cancel current workflow execution"""
        logger.info("Workflow execution cancelled")


class AdaptiveWorkflowEngine(WorkflowEngine):
    """Adaptive workflow engine that adjusts execution based on performance"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.performance_history: List[Dict] = []
        self.agent_performance: Dict[str, float] = {}
        self.adaptation_threshold: float = 0.7

    def record_performance_metrics(
        self, task_id: str, duration: float, quality_score: float, agent_id: str = ""
    ) -> None:
        """
        Record performance metrics for task execution

        Args:
            task_id: Task that was executed
            duration: Execution duration
            quality_score: Quality assessment (0.0 to 1.0)
            agent_id: Agent that executed the task
        """
        metrics = {
            "task_id": task_id,
            "duration": duration,
            "quality_score": quality_score,
            "agent_id": agent_id,
            "timestamp": time.time(),
        }

        self.performance_history.append(metrics)

        if agent_id:
            self.agent_performance[agent_id] = quality_score

        logger.debug(f"Recorded performance metrics: {metrics}")

    def adaptive_task_reassignment(
        self, task_id: str, current_result: Dict[str, Any]
    ) -> bool:
        """
        Adapt task assignment based on performance

        Args:
            task_id: Task to reassign
            current_result: Current task results

        Returns:
            Whether reassignment was performed
        """
        if not current_result.get("success"):
            logger.warning(f"Task {task_id} failed, considering reassignment")
            return True

        # Check if reassignment needed based on performance thresholds
        if current_result.get("quality_score", 1.0) < self.adaptation_threshold:
            logger.warning(f"Low quality for task {task_id}, consider reassigning")
            return True

        return False

    def generate_optimization_recommendations(self) -> List[Dict]:
        """
        Generate recommendations for workflow optimization

        Returns:
            List of optimization recommendations
        """
        recommendations = []

        # Analyze task completion times
        if self.performance_history:
            avg_duration = sum(m["duration"] for m in self.performance_history) / len(
                self.performance_history
            )

            recommendations.append(
                {
                    "type": "duration_analysis",
                    "avg_duration": avg_duration,
                    "recommendation": f"Analyze {len(self.performance_history)} tasks "
                    f"completed in ~{avg_duration:.2f}s average",
                }
            )

        # Find patterns in failures
        failed_tasks = [
            m["task_id"] for m in self.performance_history if not m.get("success")
        ]

        if len(failed_tasks) > 3:
            recommendations.append(
                {
                    "type": "failure_pattern",
                    "count": len(failed_tasks),
                    "recommendation": f"Review {len(failed_tasks)} repeated failures",
                }
            )

        # Suggest parallelization opportunities
        if self.tasks:
            independent_tasks = [t for t in self.tasks.values() if not t.dependencies]

            if len(independent_tasks) > 1:
                recommendations.append(
                    {
                        "type": "parallelization_opportunity",
                        "count": len(independent_tasks),
                        "recommendation": f"Can parallelize {len(independent_tasks)} "
                        "independent tasks",
                    }
                )

        return recommendations


def main():
    """Example usage of the Workflow Engine"""

    # Initialize workflow engine
    engine = WorkflowEngine(strategy=ExecutionStrategy.HYBRID)

    # Add sample tasks
    engine.add_task(
        TaskNode(
            id="task-1",
            title="Design User Interface",
            description="Create responsive UI components",
            dependencies=[],
            priority=1,
        )
    )

    engine.add_task(
        TaskNode(
            id="task-2",
            title="Design Database Schema",
            description="Create database schema and models",
            dependencies=["task-1"],
            priority=2,
        )
    )

    engine.add_task(
        TaskNode(
            id="task-3",
            title="Implement Backend API",
            description="Create REST API endpoints",
            dependencies=["task-2"],
            priority=3,
        )
    )

    engine.add_task(
        TaskNode(
            id="task-4",
            title="Frontend Integration",
            description="Connect frontend to backend APIs",
            dependencies=["task-3"],
            priority=4,
        )
    )

    # Build graph
    engine.build_graph()

    # Get execution plan
    plan = engine.create_execution_plan()
    print(f"\nExecution Plan: {len(plan)} parallel groups")
    for group_id, task_ids in plan:
        print(f"  Group {group_id}: {task_ids}")

    # Execute workflow
    results = engine.execute_workflow(max_parallel_tasks=2)

    print(f"\nWorkflow Results:")
    print(json.dumps(results, indent=2))

    return engine, results


if __name__ == "__main__":
    main()
