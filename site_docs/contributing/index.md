# Contributing to Documentation

Thank you for your interest in contributing to the documentation! This guide will help you get started.

## Quick Links

- [Style Guide](style-guide.md) - Writing standards and conventions
- [Quick Start Guide](../quick-start-guide.md) - Getting started with Week 1
- [Implementation Roadmap](../implementation-roadmap.md) - Overall strategy

---

## Getting Started

### Prerequisites

- Git installed on your machine
- Python 3.11 or higher
- Text editor or IDE
- GitHub account with repository access

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Chunkys0up7/docascode.git
   cd docascode
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the development server**
   ```bash
   mkdocs serve
   ```

5. **View the documentation**
   Open your browser to http://localhost:8000

---

## Contribution Workflow

### 1. Create a Feature Branch

```bash
# Ensure you're on the main branch and up to date
git checkout main
git pull origin main

# Create a new branch
git checkout -b docs/your-topic-name
```

**Branch naming conventions:**
- `docs/feature-name` - New documentation
- `docs/update-section` - Updates to existing docs
- `docs/fix-issue` - Fixing documentation issues

### 2. Make Your Changes

- Write your documentation following the [Style Guide](style-guide.md)
- Preview your changes locally with `mkdocs serve`
- Test all links and code examples
- Check for spelling and grammar

### 3. Commit Your Changes

```bash
git add site_docs/your-file.md
git commit -m "docs: add documentation for feature X"
```

**Commit message format:**
- `docs: add ...` - New documentation
- `docs: update ...` - Updates to existing docs
- `docs: fix ...` - Bug fixes in documentation
- `docs: refactor ...` - Reorganization without content changes

### 4. Push and Create a Pull Request

```bash
git push origin docs/your-topic-name
```

Then:
1. Go to the repository on GitHub
2. Click "Compare & pull request"
3. Fill out the PR template
4. Request review from appropriate reviewers
5. Address feedback
6. Merge when approved

---

## Documentation Standards

### File Organization

```
site_docs/
├── index.md                    # Home page
├── getting-started.md          # Getting started guide
├── concepts/                   # Conceptual documentation
│   └── concept-name.md
├── samples/                    # Sample implementations
│   └── sample-name.md
├── reference/                  # API and reference docs
│   └── api-name.md
├── contributing/               # Contribution guides
│   ├── index.md
│   └── style-guide.md
└── generated/                  # Auto-generated procedures
    └── procedure-*.md
```

### Frontmatter

All documentation files should include frontmatter:

```yaml
---
title: Page Title
description: Brief description of the page content
date: 2025-11-11
tags:
  - tag1
  - tag2
---
```

### Content Structure

Every documentation page should follow this structure:

1. **Title (H1)** - Single H1 at the top
2. **Introduction** - Brief overview (2-3 sentences)
3. **Main Content** - Organized with H2 and H3 headings
4. **Next Steps** - Links to related pages or what to do next

---

## Quality Checks

Before submitting your PR, ensure:

### Content Quality
- [ ] Information is accurate and up-to-date
- [ ] Code examples are tested and work
- [ ] Screenshots are clear and current
- [ ] No placeholder text (TODO, TBD, etc.)
- [ ] Grammar and spelling are correct

### Formatting
- [ ] Follows the style guide
- [ ] Proper heading hierarchy
- [ ] Lists are formatted consistently
- [ ] Code blocks have language identifiers
- [ ] Tables are properly formatted

### Links and References
- [ ] All internal links work
- [ ] External links are valid
- [ ] Images load correctly
- [ ] Cross-references are accurate

### Local Testing
```bash
# Build the documentation
mkdocs build --strict

# Check for broken links (once configured)
# markdown-link-check site_docs/**/*.md

# Lint markdown (once configured)
# markdownlint site_docs/**/*.md
```

---

## Review Process

### What to Expect

1. **Automated Checks** - CI/CD pipeline runs automatically
   - Build test
   - Link validation (coming soon)
   - Markdown linting (coming soon)

2. **Peer Review** - Assigned reviewers will:
   - Check technical accuracy
   - Verify style compliance
   - Test examples
   - Suggest improvements

3. **Iterations** - You may need to:
   - Address reviewer comments
   - Make requested changes
   - Clarify content
   - Fix issues found by automation

4. **Approval and Merge** - Once approved:
   - PR is merged to main
   - Documentation auto-deploys
   - Changes are live within minutes

### Review Guidelines

**For Authors:**
- Respond to feedback promptly
- Ask questions if feedback is unclear
- Make requested changes or explain why not
- Keep the PR focused and manageable

**For Reviewers:**
- Review within 24 hours when possible
- Be constructive and specific
- Suggest improvements, don't just criticize
- Approve when standards are met

---

## Types of Documentation

### Concepts
Explain ideas, architecture, and design decisions. Answer "What is X?" and "Why does X exist?"

**Structure:**
- Overview
- Key concepts
- How it works
- Use cases
- Related concepts

### Tutorials
Step-by-step guides for beginners. Answer "How do I learn X?"

**Structure:**
- What you'll build
- Prerequisites
- Step-by-step instructions
- Verification steps
- Next steps

### How-To Guides
Task-oriented recipes. Answer "How do I do X?"

**Structure:**
- Problem statement
- Prerequisites
- Steps to complete
- Verification
- Troubleshooting

### Reference
Technical descriptions of APIs, configurations, etc. Answer "What are the details of X?"

**Structure:**
- Description
- Parameters
- Return values
- Examples
- Related references

---

## Getting Help

### Resources

- [Style Guide](style-guide.md) - Writing standards
- [Quick Start Guide](../quick-start-guide.md) - Getting started
- [Implementation Roadmap](../implementation-roadmap.md) - Long-term plan
- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material Theme Docs](https://squidfunk.github.io/mkdocs-material/)

### Support Channels

- **GitHub Issues** - Bug reports and feature requests
- **Pull Request Comments** - Specific feedback on changes
- **Team Chat** - Quick questions and discussions

---

## Recognition

Contributors are recognized in several ways:

- Git commit history shows all contributions
- Git-authors plugin tracks authorship
- Significant contributors listed in acknowledgments
- Documentation improvements celebrated in team updates

Thank you for helping improve our documentation!
