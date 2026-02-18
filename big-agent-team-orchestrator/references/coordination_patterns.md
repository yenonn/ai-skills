# Coordination Patterns

## Parallel Execution Patterns

### Independent Task Parallelization
Use when tasks have no dependencies and can run simultaneously:

```
Task A ──┐
Task B ──┼─→ [Final Integration]
Task C ──┘
```

**Best for**: Research tasks, content generation, data processing
**Implementation**: Launch all tasks concurrently, then integrate results

### Sequential Dependency Chains
Use when tasks must complete in specific order:

```
Task A → Task B → Task C → [Final Result]
```

**Best for**: Build pipelines, validation sequences, approval workflows
**Implementation**: Each task receives output from previous task as input

### Parallel with Synchronization
Use when tasks can run in parallel but require synchronization points:

```
Task A ─┐
Task B ─┼→ [Sync Point] → Task D
Task C ─┘

Task E ─┐
Task F ─┼→ [Sync Point] → [Final Result]
Task G ─┘
```

**Best for**: Multi-team coordination, feature integration, quality gates
**Implementation**: Execute parallel phases, wait for completion, proceed to next phase

## Cross-Team Communication Protocols

### Hub-and-Spoke Model
Central coordinator manages all team communications:

```
[Coordinator] ↔ [Team A]
           ↕
        [Team B]
           ↕
        [Team C]
```

**Advantages**: Simplified coordination, centralized decision-making
**Use when**: Complex dependencies, need for consistent oversight

### Peer-to-Peer Network
Teams communicate directly with minimal central coordination:

```
Team A ↔ Team B ↔ Team C
  ↓       ↓       ↓
Team D ↔ Team E ↔ Team F
```

**Advantages**: Faster communication, reduced bottleneck risk
**Use when**: Mature teams, well-defined interfaces, low coordination overhead

### Hierarchical Communication
Multi-level team structure with clear reporting lines:

```
[Director] → [Team Lead A] → [Specialist A1]
                    ↓
            [Team Lead B] → [Specialist B1]
```

**Advantages**: Clear accountability, scalable management
**Use when**: Large projects, complex organizational structures

## Conflict Resolution Mechanisms

### Consensus Building
All teams must agree on decisions:

1. **Proposal Phase**: Present options to all teams
2. **Discussion Period**: Allow feedback and concerns
3. **Modification Round**: Refine proposal based on input
4. **Final Vote**: Require unanimous agreement
5. **Implementation**: Proceed with agreed solution

**Best for**: High-stakes decisions, technical architecture choices
**Time Cost**: High
**Quality**: Excellent when achieved

### Majority Rule
Decisions made by majority vote:

1. **Proposal Generation**: Teams submit preferred options
2. **Voting Period**: Each team casts vote
3. **Result Analysis**: Majority decision identified
4. **Implementation**: Proceed with majority choice
5. **Documentation**: Record decision rationale

**Best for**: Process decisions, resource allocation
**Time Cost**: Medium
**Quality**: Good with diverse perspectives

### Expert Delegation
Designated expert makes final decision:

1. **Expert Identification**: Pre-assign authority for decision type
2. **Information Gathering**: Expert collects relevant input
3. **Analysis Phase**: Expert evaluates options and impacts
4. **Decision Making**: Expert selects optimal approach
5. **Communication**: Explain decision to all teams

**Best for**: Technical decisions, time-sensitive situations
**Time Cost**: Low
**Quality**: Depends on expert competence

## Resource Allocation Strategies

### Fixed Capacity Model
Each agent has fixed allocation percentage:

- **Agent A**: 40% of project resources
- **Agent B**: 35% of project resources
- **Agent C**: 25% of project resources

**Benefits**: Predictable allocation, simple management
**Drawbacks**: Inflexible, may not optimize for actual needs

### Dynamic Load Balancing
Resources allocated based on current workload and capabilities:

1. **Continuous Monitoring**: Track agent utilization and performance
2. **Capacity Assessment**: Evaluate remaining available capacity
3. **Task Prioritization**: Match high-priority tasks to available agents
4. **Adaptive Rebalancing**: Adjust allocations based on changing needs

**Benefits**: Optimal resource utilization, responsive to changes
**Drawbacks**: Complex implementation, requires monitoring systems

### Priority-Based Allocation
Resources allocated according to task and agent priority levels:

- **Critical Tasks**: Assigned to highest-capacity agents
- **High Priority**: Given to agents with relevant expertise
- **Medium Priority**: Distributed across available agents
- **Low Priority**: Assigned to remaining capacity

**Benefits**: Ensures critical work gets best resources
**Drawbacks**: May underutilize capacity for lower-priority work