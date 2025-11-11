# DocAsCode MCP Service - Complete Setup & Testing Guide

**Status:** ✅ All code pushed to repository
**Branch:** `claude/powerful-project-setup-011CV2YYBAacMpyiZTgTXuTW`
**Last Commit:** `48dd37a - feat: add comprehensive test data suite`

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Load Test Data](#load-test-data)
4. [Test the Tools](#test-the-tools)
5. [Use with Claude Desktop](#use-with-claude-desktop)
6. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### System Requirements

- **Python:** 3.10 or higher
- **OS:** macOS, Linux, or Windows (WSL recommended)
- **Memory:** 4GB RAM minimum (8GB recommended)
- **Disk Space:** 2GB available

### Check Python Version

```bash
python --version
# Should show: Python 3.10.x or higher

# If not, install Python 3.10+
# macOS: brew install python@3.10
# Ubuntu: sudo apt install python3.10
```

---

## 📦 Installation

### Step 1: Clone/Navigate to Repository

```bash
# If not already in the directory
cd /path/to/docascode

# Confirm you're on the right branch
git branch --show-current
# Should show: claude/powerful-project-setup-011CV2YYBAacMpyiZTgTXuTW

# Pull latest changes (if needed)
git pull origin claude/powerful-project-setup-011CV2YYBAacMpyiZTgTXuTW
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate

# Windows:
# venv\Scripts\activate

# Your prompt should now show (venv)
```

### Step 3: Install Dependencies

```bash
# Basic installation (core features)
pip install -e .

# This installs:
# - mcp SDK
# - networkx (graphs)
# - chromadb (vector search)
# - sentence-transformers (embeddings)
# - jinja2 (templates)
# - pydantic (models)
# - markdown, beautifulsoup4 (document processing)
# - loguru (logging)
# - typer (CLI)
```

**Wait for installation to complete** (~2-3 minutes)

### Step 4: Verify Installation

```bash
# Check if package is installed
python -c "import mcp_server; print('✓ Package installed successfully')"

# Should output: ✓ Package installed successfully
```

### Step 5: Optional - Install Additional Features

```bash
# For NLP features (entity extraction with spaCy)
pip install -e ".[nlp]"
python -m spacy download en_core_web_sm

# For PDF support
pip install -e ".[pdf]"

# For DOCX support
pip install -e ".[docx]"

# For everything
pip install -e ".[all]"
```

---

## 📊 Load Test Data

### Step 1: Ensure Project Structure

```bash
# The installation should have created this structure:
ls -la

# You should see:
# - mcp_server/        (MCP service code)
# - examples/          (test data)
# - templates/         (Jinja2 templates)
# - tests/             (test suite)
# - data/              (will be created)
# - pyproject.toml
# - README.md
```

### Step 2: Load All Test Data

```bash
# Run the data loader
python examples/load_test_data.py
```

**Expected Output:**
```
============================================================
Loading Test Data into DocAsCode MCP Service
============================================================

Loading example graphs...
  ✓ Loaded: mortgage_graph.json
  ✓ Loaded: it_onboarding_graph.json
  ✓ Loaded: software_dev_graph.json
  ✓ Loaded: compliance_graph.json
✓ Loaded 4 graphs to data/graphs

Loading example templates...
  ✓ Loaded: simple_doc.md.j2
  ✓ Loaded: procedure.md.j2
  ✓ Loaded: report.md.j2
  ✓ Loaded: policy.md.j2
  ✓ Loaded: runbook.md.j2
  ✓ Loaded: release_notes.md.j2
✓ Loaded 6 templates to templates

Loading and cataloguing sample documents...
  ✓ Catalogued: Information Security Policy (ID: doc-...)
  ✓ Catalogued: Developer Onboarding Guide (ID: doc-...)
  ✓ Catalogued: API Documentation (ID: doc-...)
  ✓ Catalogued: GDPR Compliance Guide (ID: doc-...)
  ✓ Catalogued: Incident Response Plan (ID: doc-...)
✓ Catalogued 5/5 documents

============================================================
✓ Test data loaded successfully!
============================================================

Loaded Data Summary:
  Graphs: data/graphs
  Templates: templates
  Documents: Indexed in ChromaDB

Next Steps:
  1. Run 'python examples/usage_demo.py' to see tools in action
  2. Start MCP server: 'python -m mcp_server.server'
  3. Use with Claude Desktop
```

### Step 3: Verify Data Loaded

```bash
# Check graphs
ls -la data/graphs/
# Should show 4 .json files

# Check templates
ls -la templates/
# Should show 6+ .j2 files

# Check ChromaDB index
ls -la data/indices/chroma/
# Should show database files
```

---

## 🧪 Test the Tools

### Test 1: Run Usage Demonstrations

```bash
python examples/usage_demo.py
```

**This demonstrates:**
- ✅ Creating documents from templates
- ✅ Transforming formats (Markdown → HTML/JSON/Text)
- ✅ Cataloguing and searching documents
- ✅ Generating procedures from graphs
- ✅ Querying knowledge graphs
- ✅ Updating graphs
- ✅ Extracting entities

**Expected Output:** ~200 lines showing each tool working with examples

### Test 2: Run Comprehensive Tests

```bash
python examples/test_all_tools.py
```

**This tests:**
- 4 knowledge graphs with multiple scenarios
- 5+ search queries across documents
- 4 document format transformations
- Graph operations (statistics, paths, neighbors)
- Entity extraction

**Expected Output:**
```
======================================================================
  DocAsCode MCP Service - Comprehensive Tool Testing
======================================================================

======================================================================
  TEST 1: Generate Procedures from All Graphs
======================================================================

📋 Mortgage Underwriting (NM Rural)
✓ Success
  num_steps: 7

  Generated Steps:
    - Loan Application
    - Verify Credit Score
    - Request Appraisal
    - Rural Property Appraisal
    - Check NM Mortgage Rule 12
    - Generate Approval Document

[... more tests ...]

======================================================================
  All Tests Completed!
======================================================================
```

### Test 3: Test Individual Tools

**Create a Document:**
```bash
python -c "
import asyncio
from mcp_server.tools import create_document

async def test():
    result = await create_document(
        template_name='simple_doc.md.j2',
        context={
            'title': 'Test Document',
            'author': 'Test User',
            'date': '2025-01-15',
            'content': 'This is a **test**.'
        }
    )
    print(result['content'] if result['success'] else result['error'])

asyncio.run(test())
"
```

**Search Documents:**
```bash
python -c "
import asyncio
from mcp_server.tools import search_documents

async def test():
    result = await search_documents(
        query='security incident response',
        limit=3
    )
    for doc in result['results']:
        print(f\"- {doc['title']} (score: {doc['score']:.2f})\")

asyncio.run(test())
"
```

**Generate Procedure:**
```bash
python -c "
import asyncio
from mcp_server.tools import generate_procedure

async def test():
    result = await generate_procedure(
        graph_file='mortgage_underwriting.json',
        start_node='Loan Application',
        filters={'location': 'New Mexico', 'property_type': 'rural'},
        output_format='list'
    )
    print(result['content'] if result['success'] else result['error'])

asyncio.run(test())
"
```

---

## 🖥️ Use with Claude Desktop

### Step 1: Locate Claude Desktop Config

**macOS:**
```bash
# Config location
~/Library/Application Support/Claude/claude_desktop_config.json

# Open in editor
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

### Step 2: Add MCP Server Configuration

Edit the config file to add your server:

```json
{
  "mcpServers": {
    "docascode": {
      "command": "python",
      "args": [
        "-m",
        "mcp_server.server"
      ],
      "cwd": "/FULL/PATH/TO/docascode",
      "env": {
        "DOCASCODE_DATA_DIR": "data",
        "DOCASCODE_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Important:** Replace `/FULL/PATH/TO/docascode` with your actual path!

**Get your full path:**
```bash
# Run this in your docascode directory
pwd
# Copy the output and use it in the config
```

### Step 3: Restart Claude Desktop

1. Quit Claude Desktop completely
2. Reopen Claude Desktop
3. Start a new conversation

### Step 4: Verify Connection

In Claude Desktop, type:

```
Can you list the available MCP tools?
```

Claude should show:
- create_document
- transform_document
- catalogue_document
- search_documents
- generate_procedure
- query_graph
- update_graph
- extract_entities

### Step 5: Test with Real Queries

**Example 1: Search for Security Content**
```
Search my documents for "incident response procedures"
```

**Example 2: Generate a Procedure**
```
Generate a procedure for onboarding a remote developer using the IT onboarding graph
```

**Example 3: Create a Document**
```
Create a simple document with title "Meeting Notes", author "John Doe",
and content "Discussed Q1 roadmap"
```

**Example 4: Transform a Document**
```
Transform this markdown to HTML:
# Hello World
This is a **test**.
```

---

## 🐛 Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'mcp_server'"

**Solution:**
```bash
# Ensure you're in the right directory
pwd
# Should show: /path/to/docascode

# Reinstall the package
pip install -e .

# Verify
python -c "import mcp_server; print('OK')"
```

### Issue 2: "ModuleNotFoundError: No module named 'loguru'"

**Solution:**
```bash
# Dependencies weren't installed
pip install -e .

# Or install specific dependency
pip install loguru
```

### Issue 3: ChromaDB Database Errors

**Solution:**
```bash
# Clear and rebuild index
rm -rf data/indices/chroma/

# Reload data
python examples/load_test_data.py
```

### Issue 4: "Graph file not found"

**Solution:**
```bash
# Check graphs exist
ls data/graphs/

# If empty, reload data
python examples/load_test_data.py
```

### Issue 5: Claude Desktop Not Finding Server

**Check these:**

1. **Correct path in config?**
   ```bash
   # Get full path
   cd /path/to/docascode
   pwd
   # Use this EXACT path in config
   ```

2. **Python in PATH?**
   ```bash
   which python
   # Use full path if needed: "/usr/local/bin/python"
   ```

3. **Virtual environment active?**
   ```bash
   # If using venv, you need full path to venv python
   # In config, use:
   "command": "/path/to/docascode/venv/bin/python"
   ```

4. **Restart Claude Desktop completely**
   - Quit (Cmd+Q on Mac, not just close window)
   - Reopen

### Issue 6: Slow Performance

**Solutions:**

1. **First run is slow (downloading embeddings model)**
   - The sentence-transformers model downloads on first use (~100MB)
   - Subsequent runs are fast

2. **Check system resources**
   ```bash
   # Monitor while running
   top
   # Look for python processes
   ```

3. **Reduce document batch size**
   - Only catalogue documents you need
   - Clear old indices: `rm -rf data/indices/chroma/`

### Issue 7: Import Errors

**Solution:**
```bash
# Check Python version
python --version
# Must be 3.10+

# Check installation
pip list | grep -E "mcp|networkx|chromadb|jinja2"

# Should see all packages listed
```

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Virtual environment activated
- [ ] Package installed (`python -c "import mcp_server"`)
- [ ] Test data loaded (4 graphs, 5 documents, 7 templates)
- [ ] Usage demo runs successfully
- [ ] Comprehensive tests pass
- [ ] Claude Desktop config updated
- [ ] MCP server shows in Claude Desktop
- [ ] Can execute tools from Claude

---

## 📊 Expected Performance

On a standard laptop:

| Operation | First Run | Subsequent |
|-----------|-----------|------------|
| Load test data | ~30 seconds | N/A |
| Generate procedure | ~100ms | ~50ms |
| Search documents | ~500ms | ~200ms |
| Transform document | ~50ms | ~20ms |
| Create from template | ~60ms | ~30ms |

**First run is slower** due to:
- Downloading embedding models (~100MB)
- Creating ChromaDB indices
- Caching templates

---

## 🎓 What's Next?

### Beginner Path
1. ✅ Run all demos to see capabilities
2. ✅ Try searches with different queries
3. ✅ Generate procedures with different contexts
4. ✅ Explore the sample documents

### Intermediate Path
1. Create your own knowledge graph
2. Add your own documents to catalogue
3. Create custom templates
4. Modify filters and contexts

### Advanced Path
1. Extend the MCP service with new tools
2. Integrate with external APIs
3. Add Neo4j for persistent graphs
4. Implement advanced NLP features

---

## 📚 Key Files Reference

| File | Purpose |
|------|---------|
| `SETUP_GUIDE.md` | This guide |
| `README.md` | Project overview |
| `IMPLEMENTATION_SUMMARY.md` | Architecture details |
| `TEST_DATA_SUMMARY.md` | Test data documentation |
| `examples/README.md` | Examples documentation |
| `pyproject.toml` | Package configuration |
| `.env.example` | Configuration template |

---

## 🆘 Getting Help

1. **Check logs:**
   ```bash
   # Enable debug logging
   export DOCASCODE_LOG_LEVEL=DEBUG
   python examples/usage_demo.py
   ```

2. **Review documentation:**
   - README.md - Project overview
   - IMPLEMENTATION_SUMMARY.md - Architecture
   - TEST_DATA_SUMMARY.md - Test data
   - examples/README.md - Examples

3. **Test individual components:**
   ```bash
   # Test graph engine
   python -c "from mcp_server.core import GraphEngine; print('OK')"

   # Test transformer
   python -c "from mcp_server.core import DocumentTransformer; print('OK')"

   # Test indexer
   python -c "from mcp_server.core import DocumentIndexer; print('OK')"
   ```

4. **Common issues:**
   - Virtual environment not activated
   - Wrong Python version (need 3.10+)
   - Missing dependencies
   - Incorrect paths in Claude config

---

## 🎉 Success!

If you've completed all steps, you now have:

✅ Full MCP service installed and running
✅ 4 knowledge graphs loaded
✅ 5 professional documents catalogued
✅ 7 templates ready to use
✅ 8 powerful MCP tools available
✅ Integration with Claude Desktop

**You're ready to use the DocAsCode MCP service!** 🚀

---

**Last Updated:** 2025-01-15
**Version:** 1.0
**Branch:** claude/powerful-project-setup-011CV2YYBAacMpyiZTgTXuTW
