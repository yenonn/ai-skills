---
name: agent-team-orchestrator
description: Coordinates a multi-agent team consisting of an Architect, PR Reviewer, Coder, and Debug Agent for software development workflows. Use when you need architectural planning, code review expertise, implementation coordination, or bug investigation. Triggers when user requests team-based development approach with role specialization, architectural decisions, PR review processes, debugging workflows, or coordinated coding tasks.
---

# Agent Team Orchestrator

Coordinates a multi-agent team for comprehensive software development workflows with parallel execution support and intelligent task decomposition.

## Team Roles

### Architect Agent
- Analyzes requirements and creates technical architecture
- Designs system components and data flow
- Makes technology stack decisions
- Creates technical specifications and blueprints
- Considers security, performance, and scalability
- Defines success criteria and quality gates

### Coder Agent
- Implements features based on architectural specifications
- Writes clean, maintainable, modular code
- Creates comprehensive tests (unit, integration, e2e)
- Documents code and APIs thoroughly
- Addresses review feedback iteratively
- Follows software design patterns (SOLID, DRY, KISS)
- Ensures code is extensible and human-readable

### PR Reviewer Agent
- Reviews code for quality, security, and best practices
- Validates architectural compliance
- Checks test coverage (>80% target)
- Provides actionable, prioritized feedback
- Security vulnerability assessment
- Performance and scalability review

### Debug Agent
- Investigates and diagnoses bugs and issues
- Analyzes error logs, stack traces, and reproduction steps
- Identifies root causes using systematic debugging approaches
- Proposes targeted fixes with minimal code changes
- Verifies fixes resolve the issue without regressions
- Documents bug causes and prevention strategies
- Collaborates with Coder on complex fixes

### QA/Tester Agent (Optional)
- Creates comprehensive test strategies
- Validates edge cases and error handling
- Performs integration and regression testing
- Documents test scenarios and results

## Workflow Orchestration

### State Machine

```
[NEW] → [ANALYZING] → [PLANNING] → [IMPLEMENTING] → [REVIEWING] → [TESTING] → [COMPLETE]
           ↓              ↓              ↓               ↓            ↓
        (Architect)   (Architect)   (Coder)        (Reviewer)    (QA)
                          ↓              ↓               ↓
                       [ITERATION] ← ← ← ← ← ← ← ← ← ← ←

[NEW] → [DEBUGGING] → [IMPLEMENTING] → [REVIEWING] → [COMPLETE]
           ↓              ↓               ↓
        (Debug)        (Coder)        (Reviewer)
```

### Task States
- `new`: Task created, awaiting analysis
- `analyzing`: Architect analyzing requirements
- `planning`: Architecture and specifications being created
- `implementing`: Coder implementing features
- `debugging`: Debug Agent investigating issues
- `reviewing`: PR Reviewer examining code
- `testing`: QA validation in progress
- `iteration`: Addressing feedback
- `blocked`: Task has blockers
- `complete`: Task finished and approved

### Parallel Execution Patterns

**Pattern 1: Independent Components**
When multiple components can be developed independently:
```
┌─────────────┐
│  Architect  │ (Plans all components)
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────────┐
│         Parallel Implementation       │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│  │ Coder A │ │ Coder B │ │ Coder C │ │
│  │(Auth)   │ │(API)    │ │(DB)     │ │
│  └─────────┘ └─────────┘ └─────────┘ │
└──────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│  Reviewer   │ (Reviews combined PR)
└─────────────┘
```

**Pattern 2: Staggered Handoff**
For dependent components:
```
Architect → Coder(Component A) → Reviewer(A)
                  ↓ (passes context)
            Coder(Component B) → Reviewer(B)
                  ↓
            Coder(Component C) → Reviewer(C)
```

**Pattern 3: Debug Flow**
For bug fixes and issue resolution:
```
┌─────────────┐
│    Debug    │ (Investigates & diagnoses)
└──────┬──────┘
       │ (passes root cause & fix strategy)
       ▼
┌─────────────┐
│    Coder    │ (Implements targeted fix)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Reviewer  │ (Validates fix)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Debug    │ (Verifies fix resolves issue)
└─────────────┘
```

## Agent Delegation Prompts

### Architect Prompt Template

When delegating to the Architect agent, use:

```
# Architecture Analysis Request

**Task ID**: {task_id}
**Priority**: {priority}

## Requirements
{detailed_requirements}

## Context
- Project: {project_name}
- Existing Codebase: {codebase_summary}
- Constraints: {constraints}

## Deliverables Required
1. Technical specifications document
2. System architecture design (include diagrams if helpful)
3. API design documentation
4. Database schema (if applicable)
5. Technology stack decisions with rationale
6. Security considerations
7. Performance requirements
8. Success criteria and quality gates

## Output Format
Provide a structured response with:
- **Architecture Overview**: High-level design
- **Component Design**: Detailed component breakdown
- **Data Flow**: How data moves through the system
- **API Specifications**: Endpoints, request/response formats
- **Security Plan**: Authentication, authorization, data protection
- **Performance Strategy**: Caching, optimization, scaling
- **Implementation Guidance**: Priority order, dependencies, risks

After analysis, prepare handoff context for the Coder agent.
```

### Coder Prompt Template

When delegating to the Coder agent:

```
# Implementation Request

**Task ID**: {task_id}
**Assigned to**: Coder Agent
**State**: implementing

## Architectural Specifications
{architect_specs}

## Implementation Requirements
- Follow architectural specifications exactly
- Write clean, modular, extensible code
- Include comprehensive error handling
- Add inline documentation for complex logic
- Follow existing codebase patterns and conventions

## Required Deliverables
1. Working implementation matching specifications
2. Unit tests (>80% coverage target)
3. Integration tests for key workflows
4. Code documentation
5. Configuration files if needed

## Quality Standards
- [ ] All functions have docstrings/comments
- [ ] Error handling for all edge cases
- [ ] No hardcoded values (use config)
- [ ] Follows DRY and SOLID principles
- [ ] Security best practices applied
- [ ] Performance considerations addressed

## Context from Previous Agents
{previous_context}

After implementation, prepare code for PR Review.
```

### PR Reviewer Prompt Template

When delegating to the PR Reviewer:

```
# Code Review Request

**Task ID**: {task_id}
**Reviewer**: PR Reviewer Agent

## Implementation to Review
{implementation_summary}

## Files Changed
{file_list_with_descriptions}

## Review Checklist

### Security Review
- [ ] Input validation and sanitization
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] Authentication/authorization correctness
- [ ] Sensitive data handling
- [ ] Dependencies security audit

### Code Quality
- [ ] Follows architectural specifications
- [ ] Clean, readable, maintainable code
- [ ] Proper error handling
- [ ] No code duplication
- [ ] Appropriate abstractions
- [ ] Consistent naming conventions

### Testing
- [ ] Test coverage >80%
- [ ] Edge cases covered
- [ ] Integration tests present
- [ ] Tests are meaningful (not just coverage)

### Performance
- [ ] No obvious bottlenecks
- [ ] Efficient algorithms/data structures
- [ ] Appropriate caching strategy
- [ ] Database query optimization

## Output Format
Provide structured feedback:
- **CRITICAL**: Must fix before merge (security, bugs)
- **HIGH**: Strongly recommended (quality, performance)
- **MEDIUM**: Suggested improvements
- **LOW**: Nice to have (style, minor optimizations)

If approved, provide merge recommendation.
If changes needed, list specific actionable items for iteration.
```

### QA/Tester Prompt Template

```
# Testing & Validation Request

**Task ID**: {task_id}
**QA Agent**: Tester

## Implementation Summary
{implementation_summary}

## Test Requirements
1. Validate all functional requirements met
2. Test edge cases and error scenarios
3. Integration testing across components
4. Performance validation
5. Security testing checklist

## Test Scenarios to Execute
{test_scenarios}

## Acceptance Criteria
{acceptance_criteria}

## Output Required
- Test execution results
- Bug report (if any found)
- Coverage analysis
- Sign-off recommendation
```

### Debug Agent Prompt Template

```
# Debug Investigation Request

**Task ID**: {task_id}
**Debug Agent**: Debugger
**State**: debugging

## Issue Description
{issue_description}

## Reproduction Steps
{reproduction_steps}

## Available Context
- Error logs: {error_logs}
- Stack traces: {stack_traces}
- Environment: {environment_info}
- Recent changes: {recent_changes}

## Debugging Requirements
1. Reproduce and confirm the issue
2. Identify root cause through systematic analysis
3. Trace the bug through the code path
4. Determine affected components and scope
5. Propose minimal, targeted fix
6. Identify potential side effects of fix
7. Recommend prevention strategies

## Debugging Methodology
- [ ] Verify reproduction steps work
- [ ] Analyze error messages and stack traces
- [ ] Review recent code changes in affected areas
- [ ] Check data flow and state mutations
- [ ] Identify the exact line(s) causing the issue
- [ ] Determine why the bug occurs (not just what)

## Output Format
Provide structured findings:
- **Root Cause**: Clear explanation of why the bug occurs
- **Affected Code**: Specific files and lines involved
- **Proposed Fix**: Minimal changes to resolve the issue
- **Verification Steps**: How to confirm the fix works
- **Regression Risks**: Potential side effects to watch
- **Prevention**: How to prevent similar bugs in the future

After diagnosis, prepare handoff context for the Coder agent.
```

## Coordination Instructions

### 1. Task Intake
When receiving a new task:
1. Analyze complexity to determine if team orchestration is needed
2. Create task in tracker with appropriate type
3. Determine if task can be parallelized
4. Identify dependencies between subtasks

### 2. Agent Spawning
Use the Task tool to spawn specialized agents:

```
For architectural analysis:
Task(subagent_type="general", description="Architecture Analysis", prompt=architect_prompt)

For implementation:
Task(subagent_type="general", description="Feature Implementation", prompt=coder_prompt)

For review:
Task(subagent_type="general", description="Code Review", prompt=reviewer_prompt)

For debugging:
Task(subagent_type="general", description="Bug Investigation", prompt=debug_prompt)
```

### 3. Context Preservation
Between agent handoffs, preserve:
- Original requirements
- Architectural decisions and rationale
- Implementation details and patterns used
- Review feedback and changes made
- Test results and coverage data
- Debug findings and root cause analysis

### 4. Quality Gates
Before transitioning between states:
- Debug → Coder: Root cause identified, fix strategy documented
- Architect → Coder: Architecture must be approved
- Coder → Reviewer: All tests passing, basic self-review done
- Reviewer → Complete: No critical issues, all high-priority addressed

### 5. Iteration Handling
When review requires changes:
1. Document specific issues clearly
2. Prioritize by severity
3. Coder addresses in priority order
4. Re-review only changed areas
5. Track iteration count (max 3 recommended)

## Usage Patterns

### Complex Feature Development
```
1. Create task → delegate to Architect
2. Review architecture → approve or iterate
3. Parallelize implementation if possible
4. Sequential review with integration focus
5. QA validation
6. Final approval and merge
```

### Bug Fix Workflow
```
1. Create task with reproduction steps
2. Debug Agent investigates and identifies root cause
3. Coder implements targeted fix based on diagnosis
4. Reviewer validates fix approach
5. QA confirms fix and no regressions
```

### Complex Bug Workflow
```
1. Create task with reproduction steps and context
2. Debug Agent investigates root cause
3. Architect reviews fix strategy (if architectural impact)
4. Coder implements fix
5. Reviewer validates fix
6. Debug Agent verifies fix resolves issue
7. QA confirms no regressions
```

### Refactoring Workflow
```
1. Architect analyzes current state and target state
2. Define migration strategy with rollback plan
3. Incremental implementation with tests
4. Review each increment
5. Full regression testing
```

## Task Delegation Guidelines

| Task Type | Primary Agent | Support Agents | Parallel Safe |
|-----------|---------------|----------------|---------------|
| New Feature | Architect → Coder | Reviewer, QA | Partial |
| Bug Fix | Debug → Coder | Reviewer | No |
| Complex Bug | Debug → Architect → Coder | Reviewer | No |
| Refactoring | Architect → Coder | Reviewer | Partial |
| Performance | Debug → Architect → Coder | Reviewer, QA | No |
| Security | Architect → Coder | Reviewer | No |
| Documentation | Coder | Reviewer | Yes |

## Error Recovery

### Blocked Tasks
1. Identify blocker source
2. Escalate to user if external dependency
3. Create subtask to resolve blocker
4. Resume when resolved

### Failed Reviews
1. Document all issues clearly
2. Provide code examples for fixes
3. Set priority for each issue
4. Track iteration count
5. Escalate if >3 iterations

### Context Loss
1. Review task history
2. Check delegation records
3. Re-delegate with summary context
4. User confirmation if critical context missing

## Metrics Tracking

Track for continuous improvement:
- Average time per state transition
- Iteration count per task type
- Review pass rate
- Test coverage trends
- Blocker frequency
- Debug accuracy rate (fixes that resolve issues on first attempt)
- Average debug investigation time

## Best Practices

1. **Start with Architecture**: Never skip planning phase
2. **Preserve Context**: Always pass full context between agents
3. **Parallelize Wisely**: Only parallelize independent components
4. **Review Thoroughly**: Never skip code review
5. **Test Continuously**: Tests should be written with code
6. **Document Decisions**: Keep architectural decision records
7. **Limit Iterations**: Set max iteration count to prevent loops
8. **Escalate Early**: Don't hesitate to ask user for clarification
9. **Debug Before Fixing**: Always investigate root cause before implementing fixes
10. **Minimal Bug Fixes**: Prefer targeted fixes over broad refactoring for bugs
