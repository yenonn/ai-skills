# Agent Capabilities Reference

## Technical Expertise Mapping

### Code Development Agents

| Agent Type               | Primary Skills                          | Secondary Skills                     | Optimal Tasks                                               |
| ------------------------ | --------------------------------------- | ------------------------------------ | ----------------------------------------------------------- |
| **Frontend Specialist**  | React, Bun, Nextjs, CSS, Typescript     | UI/UX Design, Accessibility, Testing | Component development, UI implementation, responsive design |
| **Backend Developer**    | Python, Golang, APIs, Databases         | Architecture, Security, Performance  | API development, data modeling, service integration         |
| **Full-Stack Developer** | Frontend + Backend + DevOps             | Testing, Deployment, Monitoring      | End-to-end features, system integration, debugging          |
| **Database Engineer**    | SQL, NoSQL, Data Modeling, Optimization | Analytics, Migration, Performance    | Schema design, query optimization, data architecture        |
| **DevOps Engineer**      | CI/CD, Cloud Platforms, Infrastructure  | Security, Monitoring, Automation     | Deployment pipelines, infrastructure setup, monitoring      |

### Research & Analysis Agents

| Agent Type             | Primary Skills                              | Secondary Skills                          | Optimal Tasks                                              |
| ---------------------- | ------------------------------------------- | ----------------------------------------- | ---------------------------------------------------------- |
| **Market Research**    | Industry Analysis, Competitive Intelligence | Data Analysis, Trend Analysis             | Market studies, competitor analysis, business insights     |
| **Technical Research** | Technology Evaluation, Feasibility Analysis | Architecture Review, Performance Analysis | Technology selection, technical feasibility, system design |
| **Legal Research**     | Regulatory Compliance, Contract Analysis    | Risk Assessment, Policy Review            | Legal compliance, contract review, risk analysis           |
| **User Research**      | User Experience, Behavioral Analysis        | Survey Design, Data Interpretation        | User studies, usability testing, feedback analysis         |

### Specialized Domain Agents

| Agent Type              | Primary Skills                               | Secondary Skills                   | Optimal Tasks                                                   |
| ----------------------- | -------------------------------------------- | ---------------------------------- | --------------------------------------------------------------- |
| **Security Specialist** | Security Analysis, Threat Assessment         | Compliance, Risk Management        | Security audits, vulnerability assessment, compliance review    |
| **Data Scientist**      | Machine Learning, Statistical Analysis       | Data Engineering, Visualization    | Predictive modeling, data analysis, algorithm development       |
| **Project Manager**     | Planning, Coordination, Risk Management      | Communication, Documentation       | Project planning, timeline management, stakeholder coordination |
| **Quality Assurance**   | Testing Strategies, Automation, Bug Analysis | Documentation, Process Improvement | Test planning, quality assurance, process optimization          |

## Performance Characteristics

### Speed vs Quality Trade-offs

- **High Speed Agents**: Excel at rapid prototyping, initial drafts, basic implementations
- **High Quality Agents**: Provide thorough analysis, comprehensive testing, detailed documentation
- **Balanced Agents**: Offer good speed with acceptable quality, suitable for most production tasks

### Scalability Indicators

- **Highly Scalable**: Can handle large workloads with consistent performance
- **Moderately Scalable**: Performance degrades with increased workload size
- **Limited Scalable**: Best suited for focused, specific tasks

### Reliability Metrics

- **High Reliability**: Consistent output quality, minimal errors, predictable results
- **Moderate Reliability**: Good performance with occasional issues requiring oversight
- **Variable Reliability**: Results depend heavily on task complexity and clear requirements

## Optimal Assignment Guidelines

### Task Complexity Matching

- **Simple Tasks** (straightforward implementation): Assign to specialized single-domain agents
- **Medium Complexity** (multiple components): Use full-stack or multi-skilled agents
- **High Complexity** (cross-domain integration): Deploy coordinated teams with clear interfaces

### Deadline Sensitivity

- **Rush Projects** (tight deadlines): Prioritize speed-focused agents with proven delivery
- **Standard Projects** (normal timelines): Balance quality and speed with domain expertise
- **Long-term Projects** (extended timelines): Focus on quality, thoroughness, and maintainability

### Quality Requirements

- **Production Critical** (high stakes): Use highest quality agents with comprehensive testing
- **Standard Production** (normal quality): Balanced agents with appropriate oversight
- **Prototype/Exploration** (iterative development): Speed-focused agents with flexibility

## Team Composition Strategies

### Small Team (2-3 agents)

**Best for**: Focused features, specific components, tight deadlines

**Typical Structure**:

- Primary specialist (70% effort)
- Secondary specialist (25% effort)
- Coordinator/Reviewer (5% effort)

**Example**: Frontend + Backend development of specific feature

### Medium Team (4-7 agents)

**Best for**: Multi-component features, cross-functional requirements

**Typical Structure**:

- 2-3 primary specialists (60% effort)
- 1-2 secondary specialists (25% effort)
- 1 coordinator/quality assurance (15% effort)

**Example**: Full application development with testing and deployment

### Large Team (8+ agents)

**Best for**: Complex systems, multiple platforms, enterprise scale

**Typical Structure**:

- 4-6 primary specialists (50% effort)
- 2-3 secondary specialists (25% effort)
- 1-2 coordinators/managers (20% effort)
- 1 quality assurance (5% effort)

**Example**: Multi-platform system with security, compliance, and integration requirements

## Communication Protocols by Team Size

### 2-3 Agent Teams

- **Direct Communication**: Agents communicate directly when needed
- **Minimal Coordination**: Coordinator handles major milestones and integration
- **Simple Handoffs**: Clear task boundaries with minimal overlap

### 4-7 Agent Teams

- **Structured Communication**: Regular sync points and status updates
- **Moderate Coordination**: Coordinator manages dependencies and timing
- **Defined Interfaces**: Clear APIs and contracts between components

### 8+ Agent Teams

- **Hierarchical Communication**: Multiple coordination levels
- **Extensive Coordination**: Dedicated coordination and project management
- **Formal Processes**: Standardized handoffs, quality gates, and integration points

## Resource Optimization Patterns

### Capability-Based Assignment

Match agents to tasks based on their strongest skills:

- Review agent capabilities matrix
- Prioritize tasks by required expertise
- Assign high-complexity tasks to domain specialists
- Use generalists for integration and coordination

### Load-Based Balancing

Monitor agent capacity and distribute work accordingly:

- Track current task assignments and complexity
- Identify available capacity across team
- Balance high and low complexity tasks
- Adjust assignments based on progress and blockers

### Quality-Based Routing

Direct tasks to agents based on quality requirements:

- Critical tasks → highest quality agents
- Standard tasks → balanced quality/speed agents
- Experimental tasks → innovative/risk-tolerant agents

