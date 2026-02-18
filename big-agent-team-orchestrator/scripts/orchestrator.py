#!/usr/bin/env python3
"""
Agent Team Orchestrator - Main orchestration logic

This script provides the entry point and integration logic for the multi-agent
coordination system, combining task analysis, agent selection, workflow execution,
and memory management.
"""

import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import our coordination modules
from scripts.team_coordinator import (
    TeamCoordinator,
    Task,
    TaskStatus,
    AgentInfo,
    AgentStatus,
)
from scripts.memory_manager import MemoryManager, SharedContext, MemoryType
from scripts.workflow_engine import WorkflowEngine, TaskNode, ExecutionStrategy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("team_orchestrator.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class OrchestrationStrategy(Enum):
    """Strategies for coordinating multiple agents"""

    AUTOMATIC = "automatic"
    REQUEST_BASED = "request_based"
    SCHEDULED = "scheduled"


class AgentTeamOrchestrator:
    """Main orchestrator class for multi-agent coordination"""

    def __init__(
        self,
        strategy: OrchestrationStrategy = OrchestrationStrategy.AUTOMATIC,
        storage_path: Optional[str] = None,
    ):
        """
        Initialize the orchestrator

        Args:
            strategy: Coordination strategy to use
            storage_path: Path for persistent storage
        """
        self.strategy = strategy

        # Initialize sub-systems
        self.team_coordinator = TeamCoordinator()
        self.memory_manager = MemoryManager(storage_path=storage_path)
        self.workflow_engine = WorkflowEngine()

        # State management
        self.active_contexts: Dict[str, SharedContext] = {}
        self.active_tasks: Dict[str, Task] = {}
        self.execution_monitoring: Dict[str, float] = {}

        logger.info("Agent Team Orchestrator initialized")

    def analyze_requirements(self, user_request: str) -> Dict[str, Any]:
        """
        Analyze and decompose user requirements

        Args:
            user_request: Natural language description of requirements

        Returns:
            Analysis results with task breakdown
        """
        logger.info(f"Analyzing requirements: {user_request}")

        analysis = {
            "original_request": user_request,
            "timestamp": time.time(),
            "components": [],
            "dependencies": [],
            "estimated_resources": {
                "min_agents": 1,
                "max_agents": 5,
                "estimated_duration": 3600,
            },
        }

        # Simple keyword-based component detection
        components = []

        if "frontend" in user_request.lower() or "ui" in user_request.lower():
            components.append(
                {
                    "type": "frontend",
                    "priority": 2,
                    "description": "Frontend implementation",
                }
            )

        if "backend" in user_request.lower() or "api" in user_request.lower():
            components.append(
                {
                    "type": "backend",
                    "priority": 2,
                    "description": "Backend implementation",
                }
            )

        if "database" in user_request.lower() or "db" in user_request.lower():
            components.append(
                {
                    "type": "database",
                    "priority": 2,
                    "description": "Database setup and operations",
                }
            )

        if "testing" in user_request.lower() or "test" in user_request.lower():
            components.append(
                {
                    "type": "testing",
                    "priority": 2,
                    "description": "Testing and validation",
                }
            )

        if "deploy" in user_request.lower() or "deployment" in user_request.lower():
            components.append(
                {
                    "type": "deployment",
                    "priority": 3,
                    "description": "Deployment and configuration",
                }
            )

        # Add default component if none found
        if not components:
            components.append(
                {
                    "type": "general",
                    "priority": 1,
                    "description": "General implementation task",
                }
            )

        analysis["components"] = components

        # Calculate dependencies
        deps = []
        component_ids = []

        for i, comp in enumerate(components):
            comp_id = f"component-{i}"
            component_ids.append(comp_id)
            analysis["components"][i]["id"] = comp_id

            if i > 0:
                deps.append(
                    {
                        "depends_on": component_ids[i - 1],
                        "reason": "Sequential dependency based on user request",
                    }
                )

        analysis["dependencies"] = deps

        return analysis

    def select_agents_for_components(self, components: List[Dict]) -> List[AgentInfo]:
        """
        Select appropriate agents for each component

        Args:
            components: Task components from analysis

        Returns:
            List of selected agents
        """
        logger.info(f"Selecting agents for {len(components)} components")

        selected_agents: List[AgentInfo] = []

        # Sample agent capabilities
        agent_definitions = [
            (
                "frontend-dev",
                "Frontend Specialist",
                ["react", "vue", "css", "javascript", "html", "api-consumption"],
            ),
            (
                "backend-dev",
                "Backend Developer",
                [
                    "nodejs",
                    "python",
                    "api-design",
                    "database",
                    "rest",
                    "authentication",
                ],
            ),
            (
                "qa-specialist",
                "Quality Assurance Specialist",
                ["testing", "testing-frameworks", "validation", "quality-control"],
            ),
            (
                "devops-lead",
                "DevOps Engineer",
                ["deployment", "ci-cd", "configuration", "infrastructure"],
            ),
        ]

        for comp in components:
            comp_type = comp["type"]
            priority = comp["priority"]

            # Select agent based on component type
            agent_id, agent_name, capabilities = agent_definitions[0]

            if comp_type in ["backend", "api"]:
                agent_id, agent_name, capabilities = agent_definitions[1]
            elif comp_type == "testing":
                agent_id, agent_name, capabilities = agent_definitions[2]
            elif comp_type == "deployment":
                agent_id, agent_name, capabilities = agent_definitions[3]

            agent = AgentInfo(
                id=agent_id,
                name=agent_name,
                capabilities=capabilities,
                specializations=[comp_type],
            )

            selected_agents.append(agent)
            self.team_coordinator.add_agent(agent)

        return selected_agents

    def create_tasks_from_analysis(self, analysis: Dict[str, Any]) -> List[Task]:
        """
        Create task objects from analysis

        Args:
            analysis: Analysis results

        Returns:
            List of Task objects
        """
        tasks = []

        for comp in analysis["components"]:
            task = Task(
                id=comp["id"],
                title=f"{comp['type'].capitalize()} Implementation",
                description=comp["description"],
                priority=comp["priority"],
                dependencies=[
                    dep["depends_on"]
                    for dep in analysis["dependencies"]
                    if dep["depends_on"] == comp["id"]
                ],
                metadata={"component_type": comp["type"]},
            )

            tasks.append(task)
            self.team_coordinator.add_task(task)

        return tasks

    def initialize_shared_context(self, project_name: str) -> str:
        """
        Initialize a shared context for the project

        Args:
            project_name: Name of the project

        Returns:
            Context ID
        """
        context_id = f"project-{time.time()}"

        context = SharedContext(
            project_id=context_id,
            name=project_name,
            description=f"Automated multi-agent coordination project",
            global_state={
                "project_created": datetime.now().isoformat(),
                "coordination_mode": self.strategy.value,
            },
        )

        context_id = self.memory_manager.create_context(context)

        # Add initial shared knowledge
        self.memory_manager.add_memory(
            content={}, memory_type=MemoryType.COMMON_KNOWLEDGE
        )

        self.active_contexts[context_id] = context

        return context_id

    def coordinate_workflow(
        self, tasks: List[Task], agents: List[AgentInfo], context_id: str
    ) -> Dict[str, Any]:
        """
        Coordinate workflow execution using selected agents

        Args:
            tasks: List of tasks to execute
            agents: List of available agents
            context_id: Shared context ID

        Returns:
            Execution results
        """
        # Step 1: Create workflow tasks
        workflow_tasks = []
        for task in tasks:
            workflow_task = TaskNode(
                id=task.id,
                title=task.title,
                description=task.description,
                dependencies=task.dependencies,
                estimated_duration=task.estimated_duration * 1000,
                priority=task.priority,
            )
            workflow_tasks.append(workflow_task)
            self.workflow_engine.add_task(workflow_task)

        # Step 2: Assign agents to tasks (simplified matching)
        assigned_count = 0
        for agent_id, agent in enumerate(agents):
            for task in workflow_tasks:
                if task.id not in [t.assigned_agent for t in workflow_tasks]:
                    task.assigned_agent = f"{agent_id}-{agent_id + 1}"
                    assigned_count += 1
                    break

        # Step 3: Build workflow graph
        self.workflow_engine.build_graph()

        # Step 4: Create execution plan
        plan = self.workflow_engine.create_execution_plan()
        logger.info(f"Execution plan created with {len(plan)} parallel groups")

        # Step 5: Execute workflow
        results = self.workflow_engine.execute_workflow(
            max_parallel_tasks=2,
            quality_gates=[
                t.id
                for t in workflow_tasks
                if t.metadata.get("component_type") == "general"
            ],
        )

        # Step 6: Save results to memory
        for result_task_id, result_data in results.items():
            self.memory_manager.add_memory(
                content={
                    "task_id": result_task_id,
                    "result": result_data,
                    "processed_at": time.time(),
                },
                memory_type=MemoryType.TASK_RESULTS,
                context_id=context_id,
            )

        # Step 7: Update agent states
        for workflow_task in workflow_tasks:
            if workflow_task.assigned_agent:
                self.memory_manager.add_to_agent_state(
                    context_id,
                    agent_id=workflow_task.assigned_agent,
                    state_data={
                        "status": workflow_task.status,
                        "last_activity": datetime.now().isoformat(),
                    },
                )

        return results

    def orchestrate_complete_project(
        self, user_request: str, project_name: str
    ) -> Dict[str, Any]:
        """
        Complete orchestration of a multi-agent project

        Args:
            user_request: Natural language description of requirements
            project_name: Name of the project

        Returns:
            Orchestration results
        """
        start_time = time.time()

        result = {
            "success": False,
            "project_name": project_name,
            "started_at": datetime.now().isoformat(),
            "analysis": None,
            "tasks": None,
            "agents": None,
            "execution_results": None,
            "completed_at": None,
            "total_duration": 0,
        }

        try:
            logger.info(f"=== Starting orchestration for project: {project_name} ===")

            # Phase 1: Requirements Analysis
            analysis = self.analyze_requirements(user_request)
            result["analysis"] = analysis

            # Phase 2: Context Initialization
            context_id = self.initialize_shared_context(project_name)
            logger.info(f"Initialized context: {context_id}")

            # Phase 3: Agent Selection
            agents = self.select_agents_for_components(analysis["components"])
            result["agents"] = [
                {"id": a.id, "name": a.name, "capabilities": a.capabilities}
                for a in agents
            ]

            # Phase 4: Task Creation
            tasks = self.create_tasks_from_analysis(analysis)
            result["tasks"] = [
                {"id": t.id, "title": t.title, "priority": t.priority} for t in tasks
            ]

            # Phase 5: Workflow Coordination
            execution_results = self.coordinate_workflow(tasks, agents, context_id)
            result["execution_results"] = execution_results

            # Complete
            result["success"] = execution_results.get("success", False)
            result["completed_at"] = datetime.now().isoformat()
            result["total_duration"] = time.time() - start_time

            # Save final state
            self.memory_manager.save_to_disk()

            logger.info(f"=== Orchestration completed: {result['success']} ===")
            logger.info(f"Total duration: {result['total_duration']:.2f}s")

        except Exception as e:
            logger.error(f"Orchestration failed: {e}", exc_info=True)
            result["error"] = str(e)

        return result

    def get_team_status(self) -> Dict[str, Any]:
        """Get current status of the entire team"""
        return self.team_coordinator.get_team_status()

    def monitor_execution(self) -> Dict[str, Any]:
        """Monitor ongoing execution"""
        return {
            "active_contexts": len(self.active_contexts),
            "memory_entries": len(self.memory_manager.memory_entries),
            "context_size": sum(
                len(ctx.agent_states) for ctx in self.active_contexts.values()
            ),
        }


def main():
    """Example usage of the Agent Team Orchestrator"""

    # Initialize orchestrator
    orchestrator = AgentTeamOrchestrator(
        strategy=OrchestrationStrategy.AUTOMATIC, storage_path="/tmp/agent_team_data"
    )

    # Example project request
    project_request = (
        "Build a React frontend with database integration and API endpoints"
    )
    project_name = "React Project with Database Integration"

    # Orchestrate the project
    orchestration_result = orchestrator.orchestrate_complete_project(
        user_request=project_request, project_name=project_name
    )

    # Display results
    print("\n" + "=" * 60)
    print("ORCHESTRATION RESULTS")
    print("=" * 60)

    print(f"\nProject: {orchestration_result['project_name']}")
    print(f"Status: {'SUCCESS' if orchestration_result['success'] else 'FAILED'}")
    print(f"Duration: {orchestration_result['total_duration']:.2f}s")

    print(f"\nTasks Created: {len(orchestration_result['tasks'])}")
    for task in orchestration_result["tasks"]:
        print(f"  - {task['id']}: {task['title']} (Priority: {task['priority']})")

    print(f"\nAgents Selected:")
    for agent in orchestration_result["agents"]:
        print(f"  - {agent['name']} ({agent['id']})")

    print(f"\nExecution Results:")
    results = orchestration_result["execution_results"]
    print(f"  Total Tasks: {results.get('total_tasks', 0)}")
    print(f"  Completed: {results.get('completed_tasks', 0)}")
    print(f"  Failed: {results.get('failed_tasks', 0)}")

    # Get team status
    team_status = orchestrator.get_team_status()
    print(f"\nTeam Status: {team_status['tasks']['completion_rate']:.1%} complete")

    return orchestration_result


if __name__ == "__main__":
    main()
