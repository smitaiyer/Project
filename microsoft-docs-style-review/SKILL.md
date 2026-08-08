---
name: microsoft-docs-style-and-terminology-review
description: |
  Review Microsoft technical documentation for style guide adherence and terminology consistency. 
  Use this skill whenever you're editing, auditing, or validating Microsoft technology documentation 
  (Azure, .NET, M365, Windows, Power Platform, etc.) for compliance with the Microsoft Writing Style 
  Guide. The skill checks for the 15 most common violations (including contractions, passive voice, capitalization, 
  terminology consistency, list formatting, tone, clarity), generates an inline HTML report with concrete 
  rewrite suggestions and severity levels, and supports batch processing of multiple Markdown files.
  
  Triggers on: style guide review, documentation audit, MS doc validation, technical writing QA, 
  terminology consistency check, style violations, API documentation review, release notes review.
trigger: Microsoft documentation style review, MS style guide compliance, doc editing, terminology audit
compatibility:
  required_tools: []
  dependencies: []
---

# Microsoft Docs Style & Terminology Review

## Overview

This skill reviews your Microsoft technical documentation (Markdown files) against the Microsoft Writing Style Guide and generates a detailed, actionable HTML report. Each violation is flagged with:
- **Severity level** (Error, Warning, Suggestion)
- **Location** (file, line number, section)
- **Problem description** (why it violates the style guide)
- **Suggested fix** (concrete rewrite example)
- **Inline preview** (original text + corrected text side-by-side)

The output is a single downloadable/viewable HTML file suitable for editorial review and hand-off to writers.

## How to Use

### Input
Upload one or more Markdown files (`.md`) containing Microsoft technical documentation. Files can include:
- API reference documentation
- Tutorial and how-to guides
- Conceptual overviews
- Release notes
- Product documentation

### Process
The skill will:
1. Parse each Markdown file while preserving structure
2. Run 15 style and terminology checks
3. Extract context around each violation
4. Generate rewrite suggestions using MS guide principles
5. Produce a single HTML report

### Output
An HTML file (`ms-docs-review.html`) with:
- **Summary dashboard** (total violations, severity breakdown, file list)
- **Detailed findings** organized by file, with inline previews
- **Violation types breakdown** (chart showing most common issues)
- **Actionable suggestions** for each finding
- **Export options** (review notes, accepted/rejected changes)

---

## Style Guide Checks (15 Most Common Violations)

### 1. Contractions
**Rule**: Use contractions (don't, can't, it's, you'll, we're) to sound conversational and friendly. Missing contractions create a stiff, corporate tone.  
**Severity**: Suggestion  
**Example**:
- ❌ Weak: "You cannot use this feature until you have upgraded."
- ✓ Better: "You can't use this feature until you've upgraded."

### 2. Passive Voice
**Rule**: Use active voice. Make the subject perform the action.  
**Severity**: Warning  
**Example**:
- ❌ Bad: "The file was deleted by the user."
- ✓ Good: "The user deleted the file."

### 3. Capitalization (Product Names)
**Rule**: Capitalize Microsoft product/feature names consistently.  
**Severity**: Error  
**Example**:
- ❌ Bad: "Use azure portal to configure settings."
- ✓ Good: "Use Azure Portal to configure settings."

### 4. Terminology Consistency
**Rule**: Use consistent terms throughout the document (e.g., "sign in" vs "log in", "dialog box" vs "dialog").  
**Severity**: Warning  
**Example**:
- ❌ Bad: Mixing "Azure SDK" and "Azure sdk" or "dialog" and "dialog box"
- ✓ Good: Use one term consistently throughout.

### 5. Headings Hierarchy
**Rule**: Use proper heading hierarchy (h1 → h2 → h3, no skipping levels).  
**Severity**: Error  
**Example**:
- ❌ Bad: `# Title` → `### Subsection` (skips h2)
- ✓ Good: `# Title` → `## Section` → `### Subsection`

### 6. Numbered List Format
**Rule**: Use proper list formatting; each item starts with a capital letter and ends with a period if it's a complete sentence.  
**Severity**: Warning  
**Example**:
- ❌ Bad: `1. download the file` / `1. This is incomplete sentence`
- ✓ Good: `1. Download the file.` / `1. This is a complete sentence.`

### 7. Oxford Comma
**Rule**: Use the Oxford comma in lists of three or more items.  
**Severity**: Suggestion  
**Example**:
- ❌ Weak: "attributes, methods and properties"
- ✓ Better: "attributes, methods, and properties"

### 8. Semicolons in Lists
**Rule**: Use semicolons instead of commas in complex list items.  
**Severity**: Suggestion  

### 9. Ambiguous Pronouns
**Rule**: Avoid pronouns (it, this, that) without a clear antecedent.  
**Severity**: Warning  
**Example**:
- ❌ Bad: "Install the SDK. It requires .NET 6."
- ✓ Good: "Install the SDK. The SDK requires .NET 6."

### 10. Second Person Voice
**Rule**: Use "you" to address the reader; avoid "we" in procedural docs.  
**Severity**: Suggestion  
**Example**:
- ❌ Weak: "We can use Azure DevOps to..."
- ✓ Better: "You can use Azure DevOps to..."

### 11. Wordy Phrases
**Rule**: Replace wordy/weak phrases with crisp alternatives: "in order to" → "to", "at this point in time" → "now", "there is/are" → active verbs.  
**Severity**: Suggestion  
**Example**:
- ❌ Wordy: "There are several ways in which you can configure this setting."
- ✓ Crisp: "You can configure this setting in several ways."

### 12. Jargon & Undefined Terms
**Rule**: Define technical terms on first use or link to glossary. Avoid unexplained acronyms.  
**Severity**: Error  
**Example**:
- ❌ Bad: "Configure the RBAC policy..." (undefined)
- ✓ Good: "Configure the role-based access control (RBAC) policy..."

### 13. Weak Phrases
**Rule**: Avoid "Please note," "it should be noted," "You can access" (just say "Access").  
**Severity**: Suggestion  
**Example**:
- ❌ Weak: "You can enter your credentials in the login form."
- ✓ Better: "Enter your credentials in the login form."

### 14. Link Text Clarity
**Rule**: Use descriptive link text, not "click here", "link", or "more information".  
**Severity**: Warning  
**Example**:
- ❌ Bad: `[click here](docs.microsoft.com/learn)`
- ✓ Good: `[Learn about Azure authentication](docs.microsoft.com/learn)`

### 15. Code Block Formatting
**Rule**: Specify language in code fences; use proper indentation and syntax highlighting.  
**Severity**: Warning  
**Example**:
- ❌ Bad: `` `code here` ``
- ✓ Good: ` ```csharp ... ``` `

---

## How to Interpret the Report

### Severity Levels

- **Error** (🔴): Breaks Microsoft style guide rules or creates accessibility/clarity issues. Should be fixed.
- **Warning** (🟡): Deviates from recommended practice. Should be addressed in most cases.
- **Suggestion** (🔵): Stylistic improvement or best practice. Consider addressing during polish phase.

### Example Report Entry

```
FILE: getting-started.md | LINE 24
┌─ VIOLATION: Passive Voice
│  SEVERITY: Warning
│  RULE: Use active voice
│
│  Original (line 24):
│  "The configuration is performed by the administrator."
│
│  Suggested Fix:
│  "The administrator performs the configuration."
│
│  Why: Active voice is clearer and more direct.
└─ [Accept] [Reject] [Edit]
```

---

## Instructions for Claude

When the user uploads Markdown files:

1. **Parse files**: Read all `.md` files provided. Preserve file paths and line numbers.

2. **Run checks**: For each file, scan content and apply the 15 style checks above.

3. **Extract context**: Capture the problematic sentence/line + 1 line before/after for context.

4. **Generate suggestions**: For each violation, provide:
   - Clear explanation of the rule
   - Concrete rewrite example (original → suggested)
   - Why the suggestion is better

5. **Categorize findings**:
   - Group by file
   - Track severity (error, warning, suggestion)
   - Count violations by type

6. **Build HTML report**:
   - Use the template below
   - Include inline previews (original text highlighted, suggested fix shown)
   - Add summary dashboard with charts
   - Make it printable and downloadable

7. **Return the file**: Provide `ms-docs-review.html` as downloadable output.

---

## HTML Report Template

The report should include:

### Section 1: Summary Dashboard
```
Total Violations: 23
- Errors: 3
- Warnings: 12
- Suggestions: 8

Files Reviewed: 3
Most Common Issues:
  1. Passive Voice (8)
  2. Capitalization (5)
  3. Contractions (4)
```

### Section 2: Findings by File
For each file, show:
- File name & path
- Line number
- Violation type & severity
- Original text (with problem highlighted)
- Suggested fix
- Explanation
- [Accept/Reject/Edit] buttons

### Section 3: Violation Type Breakdown
- Visual chart (bar or pie) showing distribution
- Actionable summary ("Focus on eliminating passive voice...")

### Section 4: Notes & Export
- User can leave editorial notes
- Export as JSON, CSV, or HTML (for archival)

---

## Tips for Best Results

1. **Batch multiple files**: Upload all docs at once; the report will handle them collectively.
2. **Review by severity**: Start with Errors, then Warnings, then Suggestions.
3. **Use suggestions wisely**: Not all suggestions need to be implemented—some style choices are contextual.
4. **Terminology glossary**: If you have a specific terminology list (e.g., your org's preferred terms), mention it and the skill will validate against it.
5. **Iterative review**: You can run the review multiple times as you edit; the skill tracks progress.

---

## Example Workflow

**Input**: `api-reference.md`, `getting-started.md`, `troubleshooting.md`

**Processing**:
1. Reads all 3 files
2. Runs 15 checks on each
3. Finds 23 total violations across files
4. Prioritizes by severity (errors first)

**Output**: `ms-docs-review.html` with:
- Summary: 3 errors, 12 warnings, 8 suggestions
- Detailed inline previews for each violation
- Suggested fixes for every issue
- Severity color-coding
- Downloadable for sharing with writers

---

## What's Not Covered

This skill focuses on the **Microsoft Writing Style Guide** (clarity, tone, grammar, terminology). It does NOT:
- Validate technical accuracy (does the code example work?)
- Check completeness (are all parameters documented?)
- Validate OpenAPI schemas (use `check-api-doc-compliance` for that)
- Check SEO or metadata (use other tools for that)

For those, pair this skill with other tools in your workflow.

---

## Feedback

Found an issue with the skill or the Microsoft style guide interpretation? Let me know, and I can refine the checks.
