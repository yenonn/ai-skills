---
name: big-agent-team
description: Large-scale multi-agent orchestration system for complex projects. Use when you need to coordinate multiple specialized agents (Frontend, Backend, QA, DevOps) for projects requiring task decomposition, parallel execution, dependency management, and shared memory. Invoke with phrases like "use big agent team", "orchestrate with multiple agents", "coordinate team for project", or "run multi-agent workflow".
---

# Big Agent Team Orchestrator

## How to Invoke This Skill

In OpenCode, you can invoke this skill by:

1. **Direct invocation**: Ask me to "load the big-agent-team skill" or "use the big agent team orchestrator"
2. **Natural language**: Say things like:
   - "Help me orchestrate a multi-agent team for this project"
   - "Use the big agent team to build a web application"
   - "Coordinate multiple agents to work on this feature"
   - "Run a multi-agent workflow for this task"

3. **For specific tasks**:
   - "Analyze this project with the agent team: [your requirements]"
   - "Orchestrate agents to build: [project description]"

## Overview

This skill provides a comprehensive framework for coordinating multiple AI agents to work together efficiently on complex projects. It handles the entire lifecycle of multi-agent coordination from initial task analysis through completion, ensuring optimal resource utilization and successful project delivery.

## Core Capabilities

### 1. Task Analysis & Decomposition
Break down complex requirements into manageable components:
- **Requirements Analysis**: Parse user requests and identify core objectives
- **Component Identification**: Extract discrete work units and their relationships
- **Dependency Mapping**: Create execution order and parallelization opportunities
- **Resource Assessment**: Evaluate skill requirements and agent capabilities needed

### 2. Agent Selection & Team Assembly
Match tasks to appropriate agents based on capabilities:
- **Capability Mapping**: Align task requirements with available agent skills
- **Workload Distribution**: Balance assignments across team members
- **Expertise Matching**: Assign specialized tasks to domain-specific agents
- **Resource Optimization**: Minimize overhead while maximizing effectiveness

### 3. Workflow Orchestration
Manage execution flow and team coordination:
- **Execution Planning**: Create detailed step-by-step workflows
- **Dependency Management**: Handle task prerequisites and sequencing
- **Parallel Coordination**: Enable concurrent execution where possible
- **Quality Gates**: Implement checkpoints and validation stages

### 4. Communication & Memory Management
Enable effective information sharing and knowledge persistence:
- **Shared Context**: Establish common knowledge base for all agents
- **Progress Updates**: Track task completion and status
- **Handoff Protocols**: Define clean transitions between agents
- **Memory Integration**: Store and retrieve relevant project information

### 5. Adaptive Coordination
Adjust strategies based on execution results:
- **Performance Monitoring**: Track team efficiency and task completion
- **Dynamic Rebalancing**: Redistribute work based on progress and capability
- **Issue Resolution**: Address blockers and coordinate problem-solving
- **Optimization**: Continuously improve coordination strategies

## Workflow Execution

### Phase 1: Project Initialization
1. **Analyze Request**: Parse requirements and identify scope
2. **Decompose Tasks**: Break down into executable components
3. **Assess Resources**: Evaluate available agents and capabilities
4. **Design Architecture**: Plan team structure and coordination approach

### Phase 2: Team Assembly
1. **Select Agents**: Choose optimal team members for each task
2. **Define Roles**: Establish responsibilities and authority levels
3. **Set Communication**: Establish shared context and protocols
4. **Initialize Memory**: Create shared knowledge base and tracking systems

### Phase 3: Execution Management
1. **Launch Workflows**: Initiate tasks according to dependency map
2. **Monitor Progress**: Track completion and identify issues
3. **Coordinate Handoffs**: Manage transitions between agents
4. **Adapt Strategies**: Adjust based on real-time performance

### Phase 4: Quality Assurance
1. **Validate Outputs**: Ensure deliverables meet requirements
2. **Integration Testing**: Verify component compatibility
3. **Performance Review**: Assess team efficiency and outcomes
4. **Documentation**: Record lessons learned and best practices

## Usage Patterns

### Complex Feature Development
Use for multi-phase feature development requiring specialized expertise:
- **Frontend + Backend Integration**: Coordinate UI/UX design with API development
- **Database + API Coordination**: Align data modeling with service implementation
- **Testing + Deployment**: Balance quality assurance with delivery timelines

### Multi-Team Projects
Apply when coordinating separate teams with different specializations:
- **Cross-Platform Development**: Synchronize mobile, web, and API teams
- **Business + Technical Alignment**: Coordinate business analysis with technical implementation
- **Security + Development Integration**: Balance security requirements with feature delivery

### Research & Analysis Tasks
Deploy for comprehensive research requiring multiple perspectives:
- **Market + Technical Analysis**: Combine industry research with technical feasibility studies
- **Legal + Compliance Review**: Integrate regulatory requirements with business operations
- **User Research + Product Design**: Align user needs with product strategy

## Implementation Scripts

### scripts/team_coordinator.py
Orchestrates agent assignments and execution flow:
- Manages task queues and agent availability
- Tracks progress and handles handoffs
- Implements adaptive load balancing
- Provides real-time status updates

### scripts/memory_manager.py
Handles shared knowledge and context persistence:
- Creates and maintains shared memory spaces
- Manages context injection for agent handoffs
- Tracks project state and decision history
- Enables cross-agent knowledge sharing

### scripts/workflow_engine.py
Executes coordination logic and dependency management:
- Implements execution planning algorithms
- Manages task dependencies and parallelization
- Provides quality gates and validation
- Handles error recovery and adaptive strategies

## Reference Materials

### references/coordination_patterns.md
Detailed patterns for different coordination scenarios:
- Parallel execution strategies
- Sequential dependency management
- Cross-team communication protocols
- Conflict resolution mechanisms

### references/agent_capabilities.md
Comprehensive guide to available agent specializations:
- Technical expertise mapping
- Domain knowledge inventory
- Performance characteristics
- Optimal assignment guidelines

### references/workflow_templates.md
Reusable workflow templates for common scenarios:
- Feature development patterns
- Research coordination frameworks
- Quality assurance processes
- Deployment coordination strategies

## Best Practices

### Maximize Parallelization
- Identify independent tasks that can run concurrently
- Minimize serialization points in workflows
- Balance parallel work with quality oversight

### Optimize Communication
- Establish clear handoff protocols between agents
- Maintain shared context for team awareness
- Use consistent terminology and documentation standards

### Ensure Quality
- Implement checkpoints and validation stages
- Balance speed with thoroughness
- Maintain audit trails for decisions and changes

### Enable Adaptability
- Build in feedback loops for continuous improvement
- Design for graceful failure and recovery
- Maintain flexibility for scope changes