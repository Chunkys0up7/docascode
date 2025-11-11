# Quick Start Guide: Docs as Code Implementation

This guide helps you get started with Week 1 of the docs-as-code rollout. Follow these steps to set up your foundation.

---

## Prerequisites

- Git repository with MkDocs configured (✅ Already done!)
- Python 3.11+ installed
- GitHub repository with Actions enabled
- Admin access to repository settings

---

## Week 1: Day 1-2 - CI/CD Setup

### Step 1: Review Configuration Files

The following files have been created in your repository:

```
.github/
├── workflows/
│   ├── docs-build.yml       # Build and test workflow
│   └── docs-deploy.yml      # Deployment workflow
├── PULL_REQUEST_TEMPLATE/
│   └── documentation.md     # PR template for docs
├── CODEOWNERS               # Documentation ownership
└── dependabot.yml           # Automated dependency updates

.markdownlint.json           # Markdown linting rules
.vale.ini                    # Prose linting configuration
```

### Step 2: Enable GitHub Pages

1. Go to your repository on GitHub
2. Navigate to **Settings** > **Pages**
3. Under "Build and deployment":
   - Source: **GitHub Actions**
4. Click **Save**

### Step 3: Configure Branch Protection

1. Go to **Settings** > **Branches**
2. Click **Add rule** for `main` branch
3. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (1 minimum)
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - Select status checks: `build-and-test`
4. Click **Save changes**

### Step 4: Test the Workflow

1. Create a test branch:
   ```bash
   git checkout -b test/docs-workflow
   ```

2. Make a small change to any documentation file:
   ```bash
   echo "\n## Test Update" >> site_docs/index.md
   ```

3. Commit and push:
   ```bash
   git add site_docs/index.md
   git commit -m "docs: test CI/CD workflow"
   git push origin test/docs-workflow
   ```

4. Create a Pull Request on GitHub

5. Verify:
   - ✅ Build workflow runs automatically
   - ✅ Status checks appear on PR
   - ✅ Build artifacts are created

6. Merge the PR and verify:
   - ✅ Deploy workflow runs
   - ✅ Documentation is published to GitHub Pages
   - ✅ You can access your docs at the Pages URL

---

## Week 1: Day 3-4 - Documentation Standards

### Step 1: Review the Style Guide

Read the [Implementation Checklist](implementation-checklist.md) for detailed tasks.

### Step 2: Create Style Guide

Create `site_docs/contributing/style-guide.md` with your documentation standards:

```markdown
# Documentation Style Guide

## Tone and Voice
- Use active voice
- Write in present tense
- Be concise and clear
- Use "you" to address the reader

## Formatting
- Use ATX-style headers (#, ##, ###)
- Use dashes (-) for unordered lists
- Use code fences with language identifiers
- Maximum line length: 120 characters

## Structure
- Start with H1 (single # - only once per page)
- Use descriptive headings
- Include a table of contents for long pages
- End with "Next steps" or "Related pages"

[... continue with more guidelines ...]
```

### Step 3: Create Contribution Guide

Create `site_docs/contributing/index.md`:

```markdown
# Contributing to Documentation

## Getting Started
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Start local server: `mkdocs serve`
4. Make your changes
5. Preview at http://localhost:8000

## Workflow
1. Create a feature branch: `git checkout -b docs/your-topic`
2. Make your changes
3. Test locally
4. Push and create a Pull Request
5. Address review feedback
6. Merge when approved

[... continue with more details ...]
```

### Step 4: Update Navigation

Add the new pages to `mkdocs.yml`:

```yaml
nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - Implementation:
      - Roadmap: implementation-roadmap.md
      - Checklist: implementation-checklist.md
      - Quick Start: quick-start-guide.md
  - Contributing:
      - Overview: contributing/index.md
      - Style Guide: contributing/style-guide.md
  # ... rest of your navigation
```

---

## Week 1: Day 5 - Quality Tools

### Step 1: Install Quality Tools

Add to your `requirements.txt`:

```text
# Existing dependencies...

# Quality tools
markdownlint-cli
markdown-link-check
```

### Step 2: Install Vale

Vale is a prose linter. Install it:

**macOS:**
```bash
brew install vale
```

**Linux:**
```bash
wget https://github.com/errata-ai/vale/releases/download/v2.29.0/vale_2.29.0_Linux_64-bit.tar.gz
tar -xvzf vale_2.29.0_Linux_64-bit.tar.gz
sudo mv vale /usr/local/bin/
```

**Windows:**
```bash
choco install vale
```

### Step 3: Set Up Vale Styles

Create Vale configuration directory and download styles:

```bash
mkdir -p .vale/styles
cd .vale/styles

# Download Vale style
vale sync

# Or manually download styles
curl -L https://github.com/errata-ai/Vale/releases/latest/download/vale_Linux_64-bit.tar.gz -o vale.tar.gz
```

### Step 4: Test Quality Tools Locally

```bash
# Test markdownlint
npx markdownlint-cli site_docs/**/*.md

# Test Vale
vale site_docs/

# Test link checking
find site_docs -name "*.md" -exec markdown-link-check {} \;
```

---

## Verification Checklist

After completing Week 1, verify the following:

### CI/CD
- [ ] GitHub Actions workflows exist
- [ ] Build workflow runs on PRs
- [ ] Deploy workflow runs on main branch merges
- [ ] GitHub Pages is configured and working
- [ ] Branch protection is enabled
- [ ] Dependabot is enabled

### Documentation Standards
- [ ] Style guide created
- [ ] Contribution guide created
- [ ] PR template being used
- [ ] CODEOWNERS file configured
- [ ] Navigation updated

### Quality Tools
- [ ] Markdownlint configured
- [ ] Vale configured
- [ ] Link checker available
- [ ] Tools run successfully locally
- [ ] Tools planned for CI integration (Week 3)

---

## Troubleshooting

### GitHub Actions Failing

**Problem:** Workflow fails with permission errors

**Solution:**
1. Go to **Settings** > **Actions** > **General**
2. Under "Workflow permissions"
3. Select "Read and write permissions"
4. Click **Save**

### GitHub Pages Not Publishing

**Problem:** Pages URL shows 404

**Solution:**
1. Check that deploy workflow completed successfully
2. Verify Pages source is set to "GitHub Actions"
3. Wait a few minutes for propagation
4. Check the Actions tab for deployment status

### Build Failing Locally

**Problem:** `mkdocs build` fails

**Solution:**
1. Ensure all dependencies installed: `pip install -r requirements.txt`
2. Check for missing files referenced in `mkdocs.yml`
3. Verify Python version: `python --version` (should be 3.11+)
4. Clear cache: `rm -rf site/` and rebuild

### Vale Not Finding Styles

**Problem:** Vale reports missing styles

**Solution:**
1. Run `vale sync` to download styles
2. Check `.vale.ini` configuration
3. Verify styles directory exists: `.vale/styles/`

---

## Next Steps

After completing Week 1:

1. **Week 2:** Continue with documentation standards
   - Create templates
   - Document naming conventions
   - Train team on workflows

2. **Week 3:** Implement quality automation
   - Add linting to CI
   - Add link checking to CI
   - Fix existing issues

3. **Week 4:** Repository cleanup
   - Organize generated docs
   - Migrate legacy docs
   - Standardize structure

See the [Implementation Checklist](implementation-checklist.md) for detailed tasks.

---

## Resources

- [Implementation Roadmap](implementation-roadmap.md) - Overall strategy
- [Implementation Checklist](implementation-checklist.md) - Detailed tasks
- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material Theme Docs](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---

## Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review the GitHub Actions logs
3. Consult the MkDocs documentation
4. Create an issue in the repository
5. Ask the team in your communication channel

---

**Remember:** This is Week 1 of a 16-week journey. Focus on getting the foundation right. Don't rush - quality over speed!
