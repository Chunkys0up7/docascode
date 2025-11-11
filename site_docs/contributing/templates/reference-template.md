---
title: [API/Function/Command Name] Reference
description: Complete reference documentation for [name]
date: YYYY-MM-DD
tags:
  - reference
  - [api|cli|config]
  - [category]
status: draft
version: X.X.X
---

# [API/Function/Command Name]

<!--
Reference documentation is information-oriented and provides technical details.
It's dry, precise, and complete - like a dictionary or encyclopedia entry.
Target length: Varies based on complexity
-->

[One-line description of what this is]

---

## Synopsis

```[language]
[Signature/Syntax]
function_name(param1, param2, **kwargs)
# or
command [OPTIONS] ARGUMENTS
# or
config_key: value
```

---

## Description

[Detailed description of what this function/command/API does]

**Purpose:** [What it's designed for]

**When to use:** [Typical use cases]

---

## Parameters

### Required Parameters

#### `parameter_name`
- **Type:** `string | int | boolean | object`
- **Description:** [What this parameter does]
- **Constraints:** [Any limitations or validation rules]
- **Example:** `"example_value"`

#### `another_parameter`
- **Type:** `string | int | boolean | object`
- **Description:** [What this parameter does]
- **Default:** `default_value`
- **Constraints:** [Any limitations or validation rules]
- **Example:** `"example_value"`

### Optional Parameters

#### `optional_param`
- **Type:** `string | int | boolean | object`
- **Description:** [What this parameter does]
- **Default:** `null` or `default_value`
- **Required:** No
- **Example:** `"example_value"`

#### `**kwargs`
- **Type:** `object`
- **Description:** Additional optional parameters
- **Available options:**
  - `option1`: [Description]
  - `option2`: [Description]
  - `option3`: [Description]

---

## Return Value

### Success

**Type:** `[return_type]`

**Description:** [What is returned on success]

**Structure:**
```[language]
{
  "field1": "type - description",
  "field2": "type - description",
  "field3": {
    "nested1": "type - description",
    "nested2": "type - description"
  }
}
```

### Error

**Type:** `Error | Exception`

**Description:** [What is returned on error]

**Error codes:**
- `ERROR_CODE_1`: [When this occurs and what it means]
- `ERROR_CODE_2`: [When this occurs and what it means]
- `ERROR_CODE_3`: [When this occurs and what it means]

---

## Behavior

### Default Behavior

[Describe what happens when called with minimal/default parameters]

### Edge Cases

**Edge Case 1: [Scenario]**
- **Condition:** [When this happens]
- **Behavior:** [What the function does]
- **Result:** [What gets returned]

**Edge Case 2: [Scenario]**
- **Condition:** [When this happens]
- **Behavior:** [What the function does]
- **Result:** [What gets returned]

### Side Effects

[List any side effects, state changes, or external impacts]

- [Side effect 1]
- [Side effect 2]
- [Side effect 3]

---

## Examples

### Basic Example

[Description of what this example demonstrates]

```[language]
[Complete, working example code]
```

**Output:**
```
[Expected output]
```

---

### Example with Optional Parameters

[Description of what this example demonstrates]

```[language]
[Complete, working example code]
```

**Output:**
```
[Expected output]
```

---

### Advanced Example

[Description of what this example demonstrates]

```[language]
[Complete, working example code with error handling]
```

**Output:**
```
[Expected output]
```

---

### Error Handling Example

[Description of error scenario]

```[language]
[Example showing error handling]
```

**Output:**
```
[Error output or exception]
```

---

## Configuration

### Environment Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `VAR_NAME` | string | `default` | [What this controls] |
| `VAR_NAME_2` | integer | `100` | [What this controls] |
| `VAR_NAME_3` | boolean | `false` | [What this controls] |

### Configuration File

```[language]
# Example configuration
key1: value1
key2: value2
nested:
  key3: value3
  key4: value4
```

**Available options:**
- `key1`: [Description, type, default]
- `key2`: [Description, type, default]
- `nested.key3`: [Description, type, default]
- `nested.key4`: [Description, type, default]

---

## Performance

### Time Complexity

**Big O:** `O(n)` or `O(1)` or `O(n log n)`, etc.

**Explanation:** [Why this complexity]

### Space Complexity

**Big O:** `O(n)` or `O(1)` or `O(n²)`, etc.

**Explanation:** [Why this complexity]

### Performance Considerations

- [Consideration 1]
- [Consideration 2]
- [Consideration 3]

### Benchmarks

| Input Size | Time | Memory |
|------------|------|--------|
| 100 items | Xms | XMB |
| 1,000 items | Xms | XMB |
| 10,000 items | Xms | XMB |

---

## Compatibility

### Version History

| Version | Changes | Breaking Changes |
|---------|---------|------------------|
| 2.0.0 | [Major changes] | Yes - [what broke] |
| 1.5.0 | [New features] | No |
| 1.0.0 | Initial release | N/A |

### Deprecated Features

!!! warning "Deprecated in version X.X"
    `old_parameter` is deprecated and will be removed in version Y.Y.
    Use `new_parameter` instead.

### Platform Support

| Platform | Supported | Notes |
|----------|-----------|-------|
| Linux | ✅ Yes | All distributions |
| macOS | ✅ Yes | 10.15+ |
| Windows | ✅ Yes | Windows 10+ |
| BSD | ⚠️ Experimental | Limited testing |

---

## Security

### Security Considerations

[Important security notes about using this function/command/API]

**Authentication:**
[How authentication works]

**Authorization:**
[Required permissions or roles]

**Data Privacy:**
[How data is handled]

### Vulnerabilities

**Known Issues:**
- [CVE or security issue 1]
- [CVE or security issue 2]

**Mitigations:**
- [How to mitigate issue 1]
- [How to mitigate issue 2]

---

## Limitations

### Current Limitations

1. **[Limitation 1]**
   - **Description:** [What you can't do]
   - **Workaround:** [How to work around it]
   - **Planned:** [If/when this will be fixed]

2. **[Limitation 2]**
   - **Description:** [What you can't do]
   - **Workaround:** [How to work around it]
   - **Planned:** [If/when this will be fixed]

### Resource Limits

| Resource | Limit | Configurable |
|----------|-------|--------------|
| Max input size | XXX MB | Yes - see [config](#configuration) |
| Max connections | XXX | Yes - see [config](#configuration) |
| Rate limit | XXX/min | No |

---

## Related

### See Also

**Functions/Commands:**
- [`related_function()`](#) - [Brief description]
- [`another_function()`](#) - [Brief description]

**Concepts:**
- [Related concept](#) - [Brief description]

**How-to Guides:**
- [How to accomplish X](#) - [Brief description]

**Tutorials:**
- [Tutorial on Y](#) - [Brief description]

### Dependencies

**Required:**
- [Dependency 1] - version X.X+
- [Dependency 2] - version Y.Y+

**Optional:**
- [Optional dependency] - Enables [feature]

---

## Notes

### Implementation Details

[Technical details about the implementation]

### Best Practices

1. [Best practice 1]
2. [Best practice 2]
3. [Best practice 3]

### Common Pitfalls

!!! warning "Pitfall 1"
    [Description of common mistake]

    **Instead, do this:** [Correct approach]

!!! warning "Pitfall 2"
    [Description of common mistake]

    **Instead, do this:** [Correct approach]

---

## Changelog

### Version X.X.X (YYYY-MM-DD)

**Added:**
- [New feature 1]
- [New feature 2]

**Changed:**
- [Changed behavior 1]
- [Changed behavior 2]

**Deprecated:**
- [Deprecated feature 1]

**Removed:**
- [Removed feature 1]

**Fixed:**
- [Bug fix 1]
- [Bug fix 2]

### Version X.X.X (YYYY-MM-DD)

[Previous version changes]

---

## Metadata

**Module:** [Module name]
**Package:** [Package name]
**Source:** [Link to source code]
**Since:** Version X.X.X
**Status:** Stable | Beta | Deprecated
**Last Updated:** YYYY-MM-DD
**Maintainer:** @username

---

<!--
TEMPLATE USAGE NOTES:

1. Be precise and accurate
2. Include all parameters and options
3. Document edge cases and errors
4. Provide complete examples
5. Keep language neutral and factual
6. Include version information
7. Document all possible return values
8. Be comprehensive but organized

REFERENCE DOC BEST PRACTICES:

- Use third person ("it does", not "you do")
- Be complete and thorough
- Use consistent formatting
- Include type information
- Document all side effects
- Show all possible outcomes
- Link to related documentation
- Keep examples minimal but complete
- Update with each version change

DELETE THIS COMMENT BLOCK before publishing!
-->
