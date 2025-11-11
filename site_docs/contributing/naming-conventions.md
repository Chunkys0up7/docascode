# Naming Conventions

Consistent naming makes documentation easier to find, organize, and maintain. Follow these conventions when creating new documentation files and folders.

---

## General Principles

### 1. Use Lowercase with Hyphens
**Format:** `lowercase-with-hyphens.md`

✅ **Good:**
- `getting-started.md`
- `api-reference.md`
- `how-to-deploy.md`

❌ **Bad:**
- `GettingStarted.md` (PascalCase)
- `getting_started.md` (underscores)
- `Getting Started.md` (spaces, capitals)

### 2. Be Descriptive and Specific
Names should clearly indicate content

✅ **Good:**
- `configure-ssl-certificates.md`
- `troubleshoot-auth-errors.md`
- `deploy-to-aws.md`

❌ **Bad:**
- `ssl.md` (too vague)
- `troubleshooting.md` (not specific)
- `deployment.md` (ambiguous)

### 3. Keep Names Concise
Aim for 2-5 words maximum

✅ **Good:**
- `api-authentication.md`
- `database-setup.md`

❌ **Bad:**
- `how-to-set-up-and-configure-the-database-for-first-time-use.md`

---

## File Naming by Type

### Concept Documents
**Pattern:** `[concept-name].md`

**Examples:**
- `knowledge-graphs.md`
- `procedure-generation.md`
- `mcp-integration.md`
- `dynamic-documentation.md`

**Guidelines:**
- Use nouns
- Describe the concept clearly
- Avoid verbs

### Tutorial Documents
**Pattern:** `tutorial-[what-you-build].md` or `[topic]-tutorial.md`

**Examples:**
- `tutorial-first-procedure.md`
- `tutorial-graph-visualization.md`
- `setup-tutorial.md`
- `deployment-tutorial.md`

**Guidelines:**
- Include "tutorial" in the name
- Describe what users will build
- Be specific about the learning goal

### How-To Guides
**Pattern:** `how-to-[action].md` or `[action]-guide.md`

**Examples:**
- `how-to-configure-auth.md`
- `how-to-deploy-production.md`
- `troubleshoot-errors.md`
- `backup-database.md`

**Guidelines:**
- Start with action verb or "how-to"
- Be task-oriented
- Focus on the goal

### Reference Documents
**Pattern:** `[component]-reference.md` or `api-[endpoint].md`

**Examples:**
- `api-reference.md`
- `cli-reference.md`
- `config-reference.md`
- `api-generate-procedure.md`

**Guidelines:**
- Include "reference" or component type
- Match technical naming
- Be precise

---

## Directory Naming

### General Guidelines
- Use lowercase with hyphens
- Use plural nouns for collections
- Be descriptive but concise

### Standard Directories

```
site_docs/
├── concepts/              # Concept documentation
├── tutorials/             # Tutorial content
├── how-to/               # How-to guides
├── reference/            # Reference documentation
├── samples/              # Sample implementations
├── contributing/         # Contribution guides
├── generated/            # Auto-generated content
└── assets/              # Images and media
    ├── images/
    ├── diagrams/
    └── downloads/
```

### Custom Directories
**Pattern:** `[category-name]/`

**Examples:**
- `concepts/`
- `api-docs/`
- `deployment-guides/`

✅ **Good:**
- `user-guides/`
- `admin-docs/`
- `developer-tools/`

❌ **Bad:**
- `UserGuides/` (capitals)
- `user_guides/` (underscores)
- `Guides for Users/` (spaces)

---

## Special Cases

### Index Files
Every directory should have an `index.md` that serves as the landing page.

**Pattern:** `index.md`

**Purpose:**
- Overview of the directory contents
- Navigation to sub-pages
- Introduction to the topic area

**Example:**
```
concepts/
├── index.md              # Overview of all concepts
├── knowledge-graphs.md
├── procedure-generation.md
└── mcp-integration.md
```

### Generated Documentation
**Pattern:** `[type]-[timestamp].md` or `[type]-[identifier].md`

**Examples:**
- `procedure-20250814-103929.md`
- `report-2025-11-11.md`
- `audit-q4-2025.md`

**Guidelines:**
- Include timestamp or identifier
- Use consistent format
- Make searchable

### Changelog and Version Files
**Pattern:** `CHANGELOG.md` or `[version].md`

**Examples:**
- `CHANGELOG.md`
- `v2.0.0.md`
- `release-notes.md`

**Guidelines:**
- Use UPPERCASE for root-level files (CHANGELOG.MD, README.md)
- Use version numbers for version-specific docs

### Configuration Examples
**Pattern:** `[config-type]-example.md` or `example-[config-type].md`

**Examples:**
- `mkdocs-example.yml`
- `example-workflow.yml`
- `sample-config.json`

---

## Naming Patterns

### Action-Based Names
For how-to guides and tasks:

**Pattern:** `[verb]-[object].md`

**Examples:**
- `configure-authentication.md`
- `deploy-application.md`
- `migrate-database.md`
- `troubleshoot-errors.md`

**Common verbs:**
- configure, setup, install
- deploy, build, run
- troubleshoot, debug, fix
- migrate, upgrade, update
- create, delete, modify

### Component-Based Names
For reference and technical docs:

**Pattern:** `[component]-[type].md`

**Examples:**
- `api-endpoints.md`
- `database-schema.md`
- `config-options.md`
- `cli-commands.md`

### Feature-Based Names
For concept and overview docs:

**Pattern:** `[feature-name].md`

**Examples:**
- `authentication.md`
- `caching.md`
- `notifications.md`
- `workflows.md`

---

## File Extensions

### Markdown Files
**Extension:** `.md`

All documentation should use `.md` extension:
- `documentation.md` ✅
- `documentation.markdown` ❌
- `documentation.txt` ❌

### Configuration Files
Use appropriate extensions:
- YAML: `.yml` or `.yaml`
- JSON: `.json`
- TOML: `.toml`

### Images
Use web-friendly formats:
- `.png` - Screenshots, diagrams
- `.jpg` or `.jpeg` - Photos
- `.svg` - Logos, icons
- `.gif` - Simple animations

---

## Versioning in Names

### Don't Include Versions in Filenames
Version-specific content goes in separate directories, not filenames.

❌ **Bad:**
- `api-v2.md`
- `guide-2024.md`
- `tutorial-old.md`

✅ **Good:**
```
v2/
├── api-reference.md
└── migration-guide.md
v3/
├── api-reference.md
└── migration-guide.md
```

### Exception: Archival
Only include version/date for archived content:

✅ **Acceptable:**
- `archived-api-v1.md`
- `deprecated-workflow-2024.md`

---

## URL-Friendly Names

Names become URLs, so make them clean:

### Avoid Special Characters
❌ **Bad:**
- `api_reference.md` → `/api_reference/`
- `How To Deploy.md` → `/How%20To%20Deploy/`
- `config&setup.md` → `/config&setup/`

✅ **Good:**
- `api-reference.md` → `/api-reference/`
- `how-to-deploy.md` → `/how-to-deploy/`
- `config-and-setup.md` → `/config-and-setup/`

### Keep URLs Short
Short filenames create shorter, more shareable URLs.

✅ **Good:**
- `/getting-started/` - Easy to remember and share
- `/api/auth/` - Clean and professional

❌ **Bad:**
- `/getting-started-with-our-platform-for-the-first-time/`
- `/application-programming-interface-authentication-endpoint/`

---

## Naming Checklist

Before naming a file, check:

- [ ] Lowercase with hyphens
- [ ] Descriptive and specific
- [ ] 2-5 words
- [ ] URL-friendly
- [ ] No special characters
- [ ] Appropriate for doc type
- [ ] Matches directory conventions
- [ ] No version in name (unless archived)
- [ ] Uses standard extensions

---

## Examples by Category

### Concepts
```
concepts/
├── index.md
├── knowledge-graphs.md
├── procedure-generation.md
├── dynamic-documentation.md
└── mcp-integration.md
```

### Tutorials
```
tutorials/
├── index.md
├── tutorial-first-procedure.md
├── tutorial-graph-visualization.md
├── tutorial-custom-workflow.md
└── getting-started-tutorial.md
```

### How-To Guides
```
how-to/
├── index.md
├── how-to-deploy-production.md
├── how-to-configure-ssl.md
├── how-to-backup-data.md
└── troubleshoot-common-errors.md
```

### Reference
```
reference/
├── index.md
├── api-reference.md
├── cli-reference.md
├── config-reference.md
└── api/
    ├── index.md
    ├── generate-procedure.md
    ├── verify-credit.md
    └── loan-application.md
```

---

## Migration Guide

### Renaming Existing Files

If you need to rename files:

1. **Update the filename**
   ```bash
   git mv old-name.md new-name.md
   ```

2. **Update internal links**
   Search for references to the old filename:
   ```bash
   grep -r "old-name.md" site_docs/
   ```

3. **Update navigation**
   Update `mkdocs.yml` if the file is in nav

4. **Add redirect (optional)**
   Consider adding a redirect from old URL to new

5. **Create PR**
   Document the rename in PR description

---

## Common Mistakes

### Mistake 1: Using Underscores
❌ `api_reference.md`
✅ `api-reference.md`

### Mistake 2: Mixed Case
❌ `APIReference.md`
✅ `api-reference.md`

### Mistake 3: Too Vague
❌ `guide.md`
✅ `deployment-guide.md`

### Mistake 4: Too Long
❌ `how-to-configure-and-set-up-authentication-for-production.md`
✅ `configure-auth.md`

### Mistake 5: Special Characters
❌ `api&config.md`
✅ `api-and-config.md`

### Mistake 6: Spaces
❌ `Getting Started.md`
✅ `getting-started.md`

---

## Tools and Helpers

### Validation Script

Check if a filename follows conventions:

```bash
# Check filename format
if [[ $filename =~ ^[a-z0-9-]+\.md$ ]]; then
    echo "✅ Valid filename"
else
    echo "❌ Invalid filename"
fi
```

### Rename Helper

```bash
# Convert to proper format
filename="My Document.md"
new_name=$(echo "$filename" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
echo "$new_name"  # Outputs: my-document.md
```

---

## Questions?

If you're unsure about naming:

1. Look at existing files in the same category
2. Check this guide
3. Ask in team chat
4. When in doubt, be descriptive and use hyphens

---

## Related Resources

- [Style Guide](style-guide.md) - Writing standards
- [Contributing Guide](index.md) - How to contribute
- [Templates](templates/index.md) - Documentation templates

---

**Last Updated:** 2025-11-11
**Maintained By:** Documentation Team
