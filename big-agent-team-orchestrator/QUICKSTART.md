# Quick Start: Using Big Agent Team in OpenCode

## Step 1: Load the Skill

In your OpenCode session, say one of these:

```
Load the big-agent-team skill
```

or

```
I want to use the big agent team orchestrator
```

## Step 2: Describe Your Project

Once the skill is loaded, describe what you want to build:

```
Orchestrate a team to build a React frontend with Node.js API and PostgreSQL database
```

or

```
Help me coordinate agents to create an e-commerce platform with:
- User authentication
- Product catalog
- Shopping cart
- Payment integration
```

## Step 3: The Orchestrator Will

1. **Analyze** your requirements
2. **Identify** components (frontend, backend, database, testing, etc.)
3. **Select** appropriate agents for each component
4. **Create** an execution plan with dependencies
5. **Execute** the workflow
6. **Report** results

## Example Conversation

```
You: Load the big-agent-team skill

Claude: [Loads skill] Big Agent Team Orchestrator is ready.
        What project would you like me to coordinate?

You: Build a blog platform with React frontend, Express API,
     MongoDB database, and comprehensive testing

Claude: Analyzing your requirements...

        Components identified:
        - Frontend (React) - Frontend Specialist
        - Backend (Express API) - Backend Developer
        - Database (MongoDB) - Backend Developer
        - Testing - QA Specialist

        Creating execution plan...
        [Executes workflow]

        Results:
        - 4 tasks completed
        - 4 agents coordinated
        - Duration: 4.2s
```

## Available Commands

Once the skill is loaded, you can:

| Say This                     | To Do This                                |
| ---------------------------- | ----------------------------------------- |
| "Analyze [requirements]"     | Break down requirements without executing |
| "Orchestrate [project]"      | Run full orchestration                    |
| "Show team status"           | See current agent/task status             |
| "What agents are available?" | List agent types and capabilities         |

## Agent Types

| Agent               | Specialization             | Handles                 |
| ------------------- | -------------------------- | ----------------------- |
| Frontend Specialist | React, Typescript, CSS, JS | UI components, styling  |
| Backend Developer   | Golang, Python, APIs       | Server logic, databases |
| QA Specialist       | Testing, Validation        | Test suites, quality    |
| DevOps Engineer     | CI/CD, Infrastructure      | Deployment, pipelines   |

## Tips

1. **Be specific** - Include technologies you want to use
2. **Mention dependencies** - "API depends on database schema"
3. **Include testing** - Add "with testing" to include QA
4. **Request deployment** - Add "with deployment" for DevOps

## Example Requests

```
# Simple web app
Orchestrate agents to build a todo app with React and Express

# Full stack with testing
Coordinate a team to create a REST API with PostgreSQL,
authentication, and comprehensive test coverage

# Complex project
Use the big agent team to build an e-commerce platform with:
- Next.js frontend
- Node.js microservices
- PostgreSQL and Redis
- Stripe payment integration
- Docker deployment
- Full test suite
```
