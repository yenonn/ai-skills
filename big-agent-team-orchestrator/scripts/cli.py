#!/usr/bin/env python3
"""
CLI Entry Point for Agent Team Orchestrator

Provides command-line interface for orchestrating multi-agent teams.

Usage:
    python cli.py orchestrate "Build a React frontend with API integration"
    python cli.py status
    python cli.py run-demo
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from scripts.orchestrator import AgentTeamOrchestrator, OrchestrationStrategy


def cmd_orchestrate(args: argparse.Namespace) -> int:
    """Execute orchestration for a project request"""
    print(f"\n{'=' * 60}")
    print("AGENT TEAM ORCHESTRATOR")
    print(f"{'=' * 60}")
    print(f"\nProject: {args.project_name}")
    print(f"Request: {args.request}")
    print(f"Strategy: {args.strategy}")
    print(f"{'=' * 60}\n")

    # Initialize orchestrator
    storage_path = args.storage_path or "/tmp/agent_team_data"
    strategy = OrchestrationStrategy(args.strategy)

    orchestrator = AgentTeamOrchestrator(strategy=strategy, storage_path=storage_path)

    # Execute orchestration
    result = orchestrator.orchestrate_complete_project(
        user_request=args.request, project_name=args.project_name
    )

    # Display results
    print(f"\n{'=' * 60}")
    print("ORCHESTRATION RESULTS")
    print(f"{'=' * 60}")
    print(f"\nStatus: {'SUCCESS' if result['success'] else 'FAILED'}")
    print(f"Duration: {result['total_duration']:.2f}s")

    if result.get("tasks"):
        print(f"\nTasks ({len(result['tasks'])}):")
        for task in result["tasks"]:
            print(f"  - {task['id']}: {task['title']} (Priority: {task['priority']})")

    if result.get("agents"):
        print(f"\nAgents ({len(result['agents'])}):")
        for agent in result["agents"]:
            print(f"  - {agent['name']} ({agent['id']})")

    if result.get("execution_results"):
        exec_results = result["execution_results"]
        print(f"\nExecution:")
        print(f"  Total Tasks: {exec_results.get('total_tasks', 0)}")
        print(f"  Completed: {exec_results.get('completed_tasks', 0)}")
        print(f"  Failed: {exec_results.get('failed_tasks', 0)}")

    if result.get("error"):
        print(f"\nError: {result['error']}")
        return 1

    # Output JSON if requested
    if args.json_output:
        print(f"\n{'=' * 60}")
        print("JSON OUTPUT")
        print(f"{'=' * 60}")
        print(json.dumps(result, indent=2, default=str))

    return 0 if result["success"] else 1


def cmd_status(args: argparse.Namespace) -> int:
    """Get current status of the orchestrator"""
    storage_path = args.storage_path or "/tmp/agent_team_data"

    orchestrator = AgentTeamOrchestrator(
        strategy=OrchestrationStrategy.AUTOMATIC, storage_path=storage_path
    )

    # Load existing state
    loaded = orchestrator.memory_manager.load_from_disk()

    print(f"\n{'=' * 60}")
    print("ORCHESTRATOR STATUS")
    print(f"{'=' * 60}")

    status = orchestrator.get_team_status()
    print(f"\nTask Summary:")
    print(f"  Total: {status['tasks']['total']}")
    print(f"  Completed: {status['tasks']['completed']}")
    print(f"  In Progress: {status['tasks']['in_progress']}")
    print(f"  Failed: {status['tasks']['failed']}")
    print(f"  Completion Rate: {status['tasks']['completion_rate']:.1%}")

    if status["agents"]:
        print(f"\nAgents ({len(status['agents'])}):")
        for agent_id, agent_info in status["agents"].items():
            print(f"  - {agent_info['name']} ({agent_id}): {agent_info['status']}")

    monitor = orchestrator.monitor_execution()
    print(f"\nMemory:")
    print(f"  Active Contexts: {monitor['active_contexts']}")
    print(f"  Memory Entries: {monitor['memory_entries']}")
    print(f"  Loaded from disk: {loaded}")

    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    """Run a demo orchestration"""
    print(f"\n{'=' * 60}")
    print("RUNNING DEMO ORCHESTRATION")
    print(f"{'=' * 60}\n")

    # Demo request
    demo_request = "Build a React frontend with database integration and API endpoints"
    demo_project = "Demo Full-Stack Project"

    orchestrator = AgentTeamOrchestrator(
        strategy=OrchestrationStrategy.AUTOMATIC, storage_path="/tmp/agent_team_demo"
    )

    result = orchestrator.orchestrate_complete_project(
        user_request=demo_request, project_name=demo_project
    )

    print(f"\n{'=' * 60}")
    print("DEMO RESULTS")
    print(f"{'=' * 60}")
    print(f"\nProject: {result['project_name']}")
    print(f"Status: {'SUCCESS' if result['success'] else 'FAILED'}")
    print(f"Duration: {result['total_duration']:.2f}s")

    if result.get("analysis"):
        print(f"\nComponents Identified: {len(result['analysis']['components'])}")
        for comp in result["analysis"]["components"]:
            print(f"  - {comp['type']}: {comp['description']}")

    team_status = orchestrator.get_team_status()
    print(f"\nTeam Status: {team_status['tasks']['completion_rate']:.1%} complete")

    return 0 if result["success"] else 1


def cmd_analyze(args: argparse.Namespace) -> int:
    """Analyze a request without executing"""
    print(f"\n{'=' * 60}")
    print("REQUEST ANALYSIS")
    print(f"{'=' * 60}\n")

    orchestrator = AgentTeamOrchestrator(strategy=OrchestrationStrategy.AUTOMATIC)

    analysis = orchestrator.analyze_requirements(args.request)

    print(f"Original Request: {analysis['original_request']}\n")

    print(f"Components ({len(analysis['components'])}):")
    for comp in analysis["components"]:
        print(f"  - [{comp['id']}] {comp['type'].upper()}")
        print(f"    Description: {comp['description']}")
        print(f"    Priority: {comp['priority']}")

    print(f"\nDependencies ({len(analysis['dependencies'])}):")
    for dep in analysis["dependencies"]:
        print(f"  - {dep['depends_on']}: {dep['reason']}")

    print(f"\nEstimated Resources:")
    resources = analysis["estimated_resources"]
    print(f"  Min Agents: {resources['min_agents']}")
    print(f"  Max Agents: {resources['max_agents']}")
    print(f"  Estimated Duration: {resources['estimated_duration']}s")

    if args.json_output:
        print(f"\n{'=' * 60}")
        print("JSON OUTPUT")
        print(f"{'=' * 60}")
        print(json.dumps(analysis, indent=2, default=str))

    return 0


def main() -> int:
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Agent Team Orchestrator CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s orchestrate "Build a React frontend" --project "My Project"
  %(prog)s analyze "Create API with database"
  %(prog)s status
  %(prog)s demo
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Orchestrate command
    orchestrate_parser = subparsers.add_parser(
        "orchestrate", help="Orchestrate a multi-agent project"
    )
    orchestrate_parser.add_argument(
        "request", help="Natural language description of the project requirements"
    )
    orchestrate_parser.add_argument(
        "--project",
        "-p",
        dest="project_name",
        default="Orchestrated Project",
        help="Name for the project",
    )
    orchestrate_parser.add_argument(
        "--strategy",
        "-s",
        choices=["automatic", "request_based", "scheduled"],
        default="automatic",
        help="Orchestration strategy to use",
    )
    orchestrate_parser.add_argument(
        "--storage", "-d", dest="storage_path", help="Path for persistent storage"
    )
    orchestrate_parser.add_argument(
        "--json",
        "-j",
        dest="json_output",
        action="store_true",
        help="Output results as JSON",
    )
    orchestrate_parser.set_defaults(func=cmd_orchestrate)

    # Status command
    status_parser = subparsers.add_parser(
        "status", help="Get current orchestrator status"
    )
    status_parser.add_argument(
        "--storage", "-d", dest="storage_path", help="Path to storage location"
    )
    status_parser.set_defaults(func=cmd_status)

    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run a demo orchestration")
    demo_parser.set_defaults(func=cmd_demo)

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyze a request without executing"
    )
    analyze_parser.add_argument(
        "request", help="Natural language description to analyze"
    )
    analyze_parser.add_argument(
        "--json",
        "-j",
        dest="json_output",
        action="store_true",
        help="Output results as JSON",
    )
    analyze_parser.set_defaults(func=cmd_analyze)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
