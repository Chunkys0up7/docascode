# Developer Onboarding Guide

Welcome to the Engineering team! This guide will help you get started with our development environment and practices.

## Getting Started

### 1. Development Environment Setup

#### Prerequisites
- macOS 12+ or Ubuntu 20.04+
- 16GB RAM minimum
- 50GB available disk space

#### Required Tools
```bash
# Install Homebrew (macOS)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install essential tools
brew install git node python3 docker

# Install IDE (choose one)
brew install --cask visual-studio-code
brew install --cask jetbrains-toolbox
```

### 2. Repository Access

Clone the main repositories:
```bash
git clone git@github.com:company/backend-api.git
git clone git@github.com:company/frontend-app.git
git clone git@github.com:company/infrastructure.git
```

### 3. Configuration

Create your local environment file:
```bash
cp .env.example .env
```

Key environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis cache connection
- `API_KEY`: Development API key (get from 1Password)
- `AWS_PROFILE`: Your AWS profile name

## Development Workflow

### Branch Strategy

We use Git Flow:
- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Emergency production fixes

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **Write code with tests**
   - All new code requires unit tests
   - Aim for 80%+ code coverage
   - Integration tests for API endpoints

3. **Commit messages**
   Follow conventional commits:
   ```
   feat: add user authentication
   fix: resolve memory leak in data processor
   docs: update API documentation
   test: add tests for payment service
   ```

4. **Create pull request**
   - Assign at least one reviewer
   - Link related Jira ticket
   - Ensure CI passes
   - Request QA review if needed

### Code Review Guidelines

As a reviewer:
- Check for code quality and maintainability
- Verify test coverage
- Look for security vulnerabilities
- Ensure documentation is updated
- Approve only when ready for production

As an author:
- Respond to all comments
- Make requested changes
- Re-request review after updates

## Testing

### Unit Tests
```bash
npm test
# or
pytest tests/unit
```

### Integration Tests
```bash
npm run test:integration
# or
pytest tests/integration
```

### E2E Tests
```bash
npm run test:e2e
```

## CI/CD Pipeline

Our pipeline includes:
1. **Lint**: Code style checks
2. **Test**: Unit and integration tests
3. **Build**: Create Docker images
4. **Security Scan**: Vulnerability scanning
5. **Deploy**: Automatic to staging, manual to production

## Coding Standards

### Python
- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use Black for formatting

### JavaScript/TypeScript
- Follow Airbnb style guide
- Use ESLint and Prettier
- Prefer functional components (React)
- Use TypeScript for type safety

### API Design
- RESTful principles
- Versioned endpoints (`/api/v1/`)
- Proper HTTP status codes
- Comprehensive error messages

## Common Tasks

### Running Locally
```bash
# Backend
cd backend-api
npm install
npm run dev

# Frontend
cd frontend-app
npm install
npm start
```

### Database Migrations
```bash
# Create migration
npm run migrate:create add_user_table

# Run migrations
npm run migrate:up

# Rollback
npm run migrate:down
```

### Debugging
- Use VS Code debugger configurations
- Check logs in `logs/` directory
- Use `console.log` sparingly, prefer proper logging
- Leverage browser DevTools for frontend

## Resources

- [Internal Wiki](https://wiki.company.com)
- [API Documentation](https://api-docs.company.com)
- [Jira Board](https://company.atlassian.net)
- [Slack Channels](https://company.slack.com)
  - `#engineering`: General engineering discussion
  - `#help-backend`: Backend support
  - `#help-frontend`: Frontend support
  - `#devops`: Infrastructure and deployment

## Getting Help

- Ask in Slack channels
- Schedule pair programming sessions
- Attend daily standups
- Reach out to your mentor

Welcome aboard! 🚀
