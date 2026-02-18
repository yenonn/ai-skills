#!/usr/bin/env python3
"""
Integration Tests for Agent Team Orchestrator

Run with: python test_orchestrator.py
"""

import sys
import json
import tempfile
from pathlib import Path

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from scripts.team_coordinator import (
    TeamCoordinator,
    Task,
    AgentInfo,
    TaskStatus,
    AgentStatus,
)
from scripts.memory_manager import MemoryManager, SharedContext, MemoryType
from scripts.workflow_engine import WorkflowEngine, TaskNode, ExecutionStrategy
from scripts.orchestrator import AgentTeamOrchestrator, OrchestrationStrategy


def test_team_coordinator():
    """Test TeamCoordinator functionality"""
    print("\n--- Testing TeamCoordinator ---")

    coordinator = TeamCoordinator()

    # Add agents
    agent1 = AgentInfo(
        id="agent-1", name="Test Agent 1", capabilities=["python", "testing"]
    )
    agent2 = AgentInfo(
        id="agent-2", name="Test Agent 2", capabilities=["javascript", "react"]
    )
    coordinator.add_agent(agent1)
    coordinator.add_agent(agent2)
    assert len(coordinator.agents) == 2, "Should have 2 agents"

    # Add tasks
    task1 = Task(
        id="task-1", title="Test Task 1", description="First test task", priority=1
    )
    task2 = Task(
        id="task-2",
        title="Test Task 2",
        description="Second test task",
        dependencies=["task-1"],
        priority=2,
    )
    coordinator.add_task(task1)
    coordinator.add_task(task2)
    assert len(coordinator.tasks) == 2, "Should have 2 tasks"

    # Assign and complete task
    result = coordinator.assign_task("task-1", "agent-1")
    assert result is True, "Should assign task successfully"
    assert coordinator.tasks["task-1"].status == TaskStatus.IN_PROGRESS

    result = coordinator.complete_task("task-1", {"output": "completed"})
    assert result is True, "Should complete task successfully"
    assert coordinator.tasks["task-1"].status == TaskStatus.COMPLETED

    # Get status
    status = coordinator.get_team_status()
    assert status["tasks"]["completed"] == 1
    assert status["tasks"]["total"] == 2

    print("  TeamCoordinator: PASSED")
    return True


def test_memory_manager():
    """Test MemoryManager functionality"""
    print("\n--- Testing MemoryManager ---")

    with tempfile.TemporaryDirectory() as tmpdir:
        manager = MemoryManager(storage_path=tmpdir)

        # Create context
        context = SharedContext(
            project_id="test-project",
            name="Test Project",
            description="Test project for memory manager",
        )
        context_id = manager.create_context(context)
        assert context_id == "test-project"

        # Add memory entries
        entry_id = manager.add_memory(
            content={"test": "data"},
            memory_type=MemoryType.COMMON_KNOWLEDGE,
            context_id=context_id,
        )
        assert entry_id is not None

        # Retrieve memory
        entries = manager.get_context_memory(context_id)
        assert len(entries) >= 1

        # Update agent state
        manager.add_to_agent_state(
            context_id, agent_id="test-agent", state_data={"status": "active"}
        )
        state = manager.get_agent_state(context_id, "test-agent")
        assert state is not None and state["status"] == "active"

        # Save and load
        manager.save_to_disk()
        loaded = manager.load_from_disk()
        assert loaded >= 1

    print("  MemoryManager: PASSED")
    return True


def test_workflow_engine():
    """Test WorkflowEngine functionality"""
    print("\n--- Testing WorkflowEngine ---")

    engine = WorkflowEngine(strategy=ExecutionStrategy.HYBRID)

    # Add tasks
    task1 = TaskNode(
        id="wf-task-1",
        title="Workflow Task 1",
        description="First workflow task",
        dependencies=[],
    )
    task2 = TaskNode(
        id="wf-task-2",
        title="Workflow Task 2",
        description="Second workflow task",
        dependencies=["wf-task-1"],
    )
    task3 = TaskNode(
        id="wf-task-3",
        title="Workflow Task 3",
        description="Third workflow task",
        dependencies=["wf-task-1"],
    )

    engine.add_task(task1)
    engine.add_task(task2)
    engine.add_task(task3)
    assert len(engine.tasks) == 3

    # Build graph
    engine.build_graph()
    assert len(engine.task_graph) == 3

    # Create execution plan
    plan = engine.create_execution_plan()
    assert len(plan) > 0

    # Execute workflow
    results = engine.execute_workflow(max_parallel_tasks=2)
    assert results["success"] is True
    assert results["completed_tasks"] > 0

    print("  WorkflowEngine: PASSED")
    return True


def test_orchestrator():
    """Test AgentTeamOrchestrator functionality"""
    print("\n--- Testing AgentTeamOrchestrator ---")

    with tempfile.TemporaryDirectory() as tmpdir:
        orchestrator = AgentTeamOrchestrator(
            strategy=OrchestrationStrategy.AUTOMATIC, storage_path=tmpdir
        )

        # Test requirement analysis
        analysis = orchestrator.analyze_requirements(
            "Build a frontend with API and database"
        )
        assert "components" in analysis
        assert len(analysis["components"]) > 0

        # Test complete orchestration
        result = orchestrator.orchestrate_complete_project(
            user_request="Create a simple web application with testing",
            project_name="Test Orchestration Project",
        )

        assert result["project_name"] == "Test Orchestration Project"
        assert "tasks" in result
        assert "agents" in result
        assert "execution_results" in result

        # Test status
        status = orchestrator.get_team_status()
        assert "tasks" in status
        assert "agents" in status

        # Test monitoring
        monitor = orchestrator.monitor_execution()
        assert "active_contexts" in monitor
        assert "memory_entries" in monitor

    print("  AgentTeamOrchestrator: PASSED")
    return True


def test_integration():
    """Test full integration of all components"""
    print("\n--- Testing Full Integration ---")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize orchestrator
        orchestrator = AgentTeamOrchestrator(
            strategy=OrchestrationStrategy.AUTOMATIC, storage_path=tmpdir
        )

        # Run complete workflow
        result = orchestrator.orchestrate_complete_project(
            user_request="Build a React frontend with Node.js backend, PostgreSQL database, and comprehensive testing",
            project_name="Full Stack Integration Test",
        )

        # Verify all components worked together
        assert result["success"] is True, (
            f"Integration failed: {result.get('error', 'Unknown error')}"
        )
        assert len(result["tasks"]) > 0, "No tasks created"
        assert len(result["agents"]) > 0, "No agents selected"
        assert result["execution_results"]["completed_tasks"] > 0, "No tasks completed"

        # Verify memory persistence
        orchestrator.memory_manager.save_to_disk()
        loaded = orchestrator.memory_manager.load_from_disk()
        assert loaded > 0, "Memory not persisted"

        print(f"  Integration Test: PASSED")
        print(f"    - Tasks: {len(result['tasks'])}")
        print(f"    - Agents: {len(result['agents'])}")
        print(f"    - Completed: {result['execution_results']['completed_tasks']}")
        print(f"    - Duration: {result['total_duration']:.2f}s")

    return True


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("AGENT TEAM ORCHESTRATOR - TEST SUITE")
    print("=" * 60)

    tests = [
        ("TeamCoordinator", test_team_coordinator),
        ("MemoryManager", test_memory_manager),
        ("WorkflowEngine", test_workflow_engine),
        ("Orchestrator", test_orchestrator),
        ("Integration", test_integration),
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success, None))
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"  {name}: FAILED - {e}")

    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)

    passed = sum(1 for _, success, _ in results if success)
    failed = len(results) - passed

    for name, success, error in results:
        status = "PASSED" if success else f"FAILED: {error}"
        print(f"  {name}: {status}")

    print(f"\nTotal: {passed}/{len(results)} passed, {failed} failed")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
