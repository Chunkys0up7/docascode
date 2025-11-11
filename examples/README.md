# DocAsCode MCP Service - Examples

This directory contains comprehensive examples and test data for the DocAsCode MCP service.

## Contents

### Knowledge Graphs

Example knowledge graphs demonstrating different use cases:

- **`mortgage_graph.json`** - Mortgage underwriting workflow
  - 18 nodes (processes, systems, roles, regulations, contexts)
  - Context-aware steps (location, property type)
  - Demonstrates conditional flows

- **`it_onboarding_graph.json`** - IT employee onboarding
  - Department-specific onboarding (Developer, Designer)
  - Remote employee handling
  - System provisioning workflows

- **`software_dev_graph.json`** - Software development lifecycle
  - Sprint planning through production deployment
  - CI/CD pipeline integration
  - QA and security scanning

- **`compliance_graph.json`** - Regulatory compliance processes
  - Multi-regulation support (SOC 2, GDPR, HIPAA)
  - Risk assessment and controls
  - Audit workflows

### Sample Documents

Professional documents for testing cataloguing and search:

- **`sample_documents/security_policy.md`** - Information security policy
  - Password requirements
  - Access control policies
  - Incident response
  - Compliance frameworks

- **`sample_documents/developer_guide.md`** - Developer onboarding guide
  - Environment setup
  - Development workflow
  - Git flow and PR process
  - Code review guidelines

- **`sample_documents/api_documentation.md`** - REST API documentation
  - Authentication
  - Endpoint reference
  - Error handling
  - Rate limiting

- **`sample_documents/gdpr_compliance.md`** - GDPR compliance guide
  - Data subject rights
  - Legal bases for processing
  - Data breach response
  - International transfers

- **`sample_documents/incident_response.md`** - Incident response plan
  - Classification and severity levels
  - Response phases
  - Communication plan
  - Specific incident types

### Utilities

- **`usage_demo.py`** - Demonstrates all 8 MCP tools
- **`load_test_data.py`** - Loads all test data into the service
- **`test_all_tools.py`** - Comprehensive testing of all tools

## Usage

### 1. Load Test Data

First, load all example data into the service:

```bash
python examples/load_test_data.py
```

This will:
- Copy graphs to `data/graphs/`
- Copy templates to `templates/`
- Catalogue all sample documents (with embeddings)

### 2. Run Usage Demonstrations

See all tools in action with realistic examples:

```bash
python examples/usage_demo.py
```

This demonstrates:
- Creating documents from templates
- Transforming between formats
- Cataloguing and searching documents
- Generating context-aware procedures
- Querying knowledge graphs
- Updating graphs
- Extracting entities

### 3. Run Comprehensive Tests

Test all tools with all example data:

```bash
python examples/test_all_tools.py
```

This runs:
- Procedure generation from all 4 graphs
- Search queries on catalogued documents
- Document transformations (MD/HTML/JSON/TEXT)
- Template rendering
- Graph queries (statistics, paths, neighbors)
- Entity extraction

## Example Scenarios

### Mortgage Underwriting

Generate procedure for rural property in New Mexico:

```python
from mcp_server.tools import generate_procedure

result = await generate_procedure(
    graph_file="mortgage_underwriting.json",
    start_node="Loan Application",
    filters={"location": "New Mexico", "property_type": "rural"}
)
```

This includes:
- Credit verification
- Rural property appraisal (with special form)
- NM-specific mortgage rule checks
- Approval document generation

### IT Onboarding

Generate onboarding procedure for remote developer:

```python
result = await generate_procedure(
    graph_file="it_onboarding_graph.json",
    start_node="Employee Onboarding",
    filters={"role": "Developer", "location": "Remote"}
)
```

This includes:
- User account creation
- Equipment shipping (for remote)
- Developer tool installation
- Security training
- Access permissions

### Document Search

Search for security-related documents:

```python
from mcp_server.tools import search_documents

result = await search_documents(
    query="incident response security procedures",
    filters={"tags": ["security"]},
    limit=5
)
```

Returns relevant documents with:
- Similarity scores
- Snippets with highlights
- Metadata (author, tags, dates)

## Adding Your Own Data

### Custom Knowledge Graphs

Create a graph JSON file following this structure:

```json
{
  "nodes": [
    {
      "id": "Node ID",
      "label": "Display Name",
      "type": "process|system|role|regulation|context",
      "properties": {}
    }
  ],
  "edges": [
    {
      "source": "Source Node ID",
      "target": "Target Node ID",
      "relation": "requires|performed_by|applies_to|conditional_on|precedes",
      "properties": {}
    }
  ],
  "metadata": {
    "name": "Graph Name",
    "description": "Description",
    "version": "1.0"
  }
}
```

Save to `data/graphs/your_graph.json`

### Custom Documents

Add markdown documents to catalogue:

```python
from mcp_server.tools import catalogue_document

result = await catalogue_document(
    content=your_markdown_content,
    title="Document Title",
    metadata={
        "author": "Author Name",
        "tags": ["tag1", "tag2"],
        "description": "Description"
    }
)
```

### Custom Templates

Create Jinja2 templates in `templates/`:

```jinja
# {{ title }}

**Author:** {{ author }}
**Date:** {{ date }}

{{ content }}

{% for section in sections %}
## {{ section.title }}
{{ section.content }}
{% endfor %}
```

Use with `create_document`:

```python
result = await create_document(
    template_name="your_template.j2",
    context={"title": "...", "author": "...", ...}
)
```

## Data Statistics

After loading test data:

- **4 Knowledge Graphs** (83 total nodes, 58 edges)
- **5 Sample Documents** (~15,000 words catalogued)
- **7 Templates** (procedure, policy, report, runbook, etc.)

## Performance Benchmarks

Typical performance on example data:

- **Generate Procedure**: 50-100ms
- **Search Documents**: 200-300ms (including embedding)
- **Transform Document**: 20-50ms
- **Create from Template**: 30-60ms
- **Query Graph**: 10-30ms

## Next Steps

1. **Explore the data** - Browse graphs and documents
2. **Run the demos** - See tools in action
3. **Test with MCP** - Start server and use with Claude Desktop
4. **Add your data** - Create custom graphs, documents, templates
5. **Extend the service** - Add new tools or enhance existing ones

For more information, see the main [README.md](../README.md).
