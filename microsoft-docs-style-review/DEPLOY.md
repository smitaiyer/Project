# Deployment Guide

## Skill Summary

**Name**: `microsoft-docs:style-and-terminology-review`

**Purpose**: Review Microsoft technical documentation for style guide adherence and terminology consistency

**Type**: Documentation review

**Input**: Markdown files (.md)

**Output**: Interactive HTML report with inline previews and suggestions

---

## What You Have

✅ **SKILL.md** — Production-ready Claude Code skill definition
✅ **Python Script** (`scripts/ms-style-checker.py`) — 15 style checks + HTML generation
✅ **Test Documents** — Sample Markdown files with intentional violations
✅ **Test Results** — Report showing skill works (31 violations detected)
✅ **README.md** — Complete user guide with examples
✅ **This Guide** — Deployment and troubleshooting

---

## How to Use

### 1. In Claude Code IDE (Easiest)

If the skill has been added to your Claude Code skills library:

```
/microsoft-docs:style-and-terminology-review
```

Upload your Markdown files and Claude will generate the HTML report.

### 2. Command Line (Direct Script)

```bash
cd microsoft-docs-style-review
python scripts/ms-style-checker.py path/to/doc1.md path/to/doc2.md
```

Output: `ms-docs-review.html` in current directory

### 3. In Claude.ai

Copy the SKILL.md content into Claude.ai with your documents and ask:
"Review these Markdown files for Microsoft style guide violations and generate an HTML report."

---

## File Structure

```
microsoft-docs-style-review/
├── SKILL.md                          # Skill definition (for Claude Code)
├── README.md                         # User guide
├── DEPLOY.md                         # This file
├── scripts/
│   └── ms-style-checker.py          # Python script (15 checks + HTML generation)
├── test-docs/
│   ├── getting-started.md           # Sample doc with violations
│   └── api-reference.md             # Sample doc with violations
├── evals/
│   └── evals.json                   # Test case definitions
└── ms-docs-style-review-workspace/
    └── iteration-1/
        ├── eval-batch-multi-file-review/
        │   ├── eval_metadata.json
        │   ├── grading.json
        │   └── with_skill/outputs/
        │       └── ms-docs-review.html
        └── timing.json
```

---

## Quick Test

To verify the skill works:

```bash
cd microsoft-docs-style-review
python scripts/ms-style-checker.py test-docs/getting-started.md test-docs/api-reference.md
open ms-docs-review.html
```

Expected: Opens HTML report showing 31 violations (8 errors, 17 warnings, 6 suggestions)

---

## Features

✨ **15 Style Checks**
- Contractions, passive voice, capitalization, terminology, headings, lists, Oxford comma, pronouns, second person, wordy phrases, jargon, weak phrases, link text, code blocks, vague quantifiers

📊 **Rich HTML Report**
- Summary dashboard with violation counts
- Violations grouped by file with line numbers
- Inline previews (original vs. suggested fix)
- Severity color-coding (red/yellow/blue)
- Statistics tab with top violations chart
- Self-contained (no external dependencies)

🎯 **Actionable Suggestions**
- Each violation includes explanation tied to Microsoft Writing Style Guide
- Concrete rewrite examples
- Severity levels (Error/Warning/Suggestion)

⚡ **Performance**
- Processes 2 documents (~2000 lines) in <2 seconds
- Generates professional HTML report
- No API calls or external dependencies

---

## Using the Report

### Dashboard Summary
Shows at-a-glance metrics:
- Total violations: 31
- By severity: 8 errors, 17 warnings, 6 suggestions
- Files reviewed: 2

### Detailed Findings
For each violation:
1. **Rule name** — What style guide rule is violated
2. **Location** — File name and line number
3. **Severity** — Error (red), Warning (yellow), or Suggestion (blue)
4. **Original text** — What you wrote (left side, red background)
5. **Suggested fix** — What to change it to (right side, blue background)
6. **Explanation** — Why it's a violation, linked to the style guide

### Statistics Tab
- Bar chart showing top 10 violations by frequency
- Helps identify which rules to focus on first

---

## Example Workflow

### Scenario: Review API Documentation Before Publishing

**Step 1**: Upload files
```
Files: api-reference.md, errors.md, authentication.md, rate-limits.md
```

**Step 2**: Run skill
```
"I need to review these API docs for Microsoft style guide compliance before we publish"
```

**Step 3**: Claude reviews all 4 files and generates report

**Step 4**: Download `ms-docs-review.html`

**Step 5**: Review the dashboard
```
Summary: 47 violations (6 errors, 23 warnings, 18 suggestions)
```

**Step 6**: Filter by severity
- **Fix first**: 6 errors (likely product capitalization, undefined acronyms)
- **Address next**: 23 warnings (passive voice, unclear links)
- **Polish**: 18 suggestions (tone, wordiness, contractions)

**Step 7**: Make corrections using suggested rewrites

**Step 8**: Re-run skill to verify improvements

---

## Customization

### Modify Checks

Edit `scripts/ms-style-checker.py` to:
- Add new style rules (add a method like `_check_my_rule`)
- Adjust existing rules (modify pattern matching)
- Change severity levels
- Add organization-specific terminology checks

### Adjust Report Styling

HTML styling is embedded in the script's `generate_html_report()` function. Edit the `<style>` section to customize:
- Colors (blue/white/red scheme)
- Fonts and typography
- Layout and spacing
- Badge styling

### Add Custom Terminology

In the `_check_terminology()` method, add your org's terms:
```python
terminology_pairs = [
    ("sign in", "log in"),           # Microsoft standard
    ("My Product v1", "My Product"), # Your custom term
]
```

---

## Troubleshooting

### Issue: Report shows no violations

**Possible causes**:
- File is already fully compliant (unlikely for new docs)
- Wrong file path or file doesn't exist
- File is empty or has no text

**Solution**: Verify file path and content, try test files first

### Issue: Python script not found

**Solution**:
```bash
# Make sure you're in the right directory
cd microsoft-docs-style-review
python scripts/ms-style-checker.py test-docs/getting-started.md
```

### Issue: HTML report looks broken in browser

**Solution**:
- Try a different browser (Chrome, Firefox, Safari all work)
- Ensure JavaScript is enabled
- Open the file directly: `file:///path/to/ms-docs-review.html`

### Issue: Want to integrate with CI/CD

**Solution**: The Python script can be called from your CI pipeline:
```bash
python ms-style-checker.py $DOCS_PATH && echo "Review complete" || echo "Review failed"
```

---

## Integration Ideas

### With VS Code
1. Install the "Run" extension
2. Create a task that calls the Python script
3. Bind to keyboard shortcut (Ctrl+Shift+R)
4. Automatically opens report in default browser

### With GitHub Actions
```yaml
- name: Style Review
  run: |
    python scripts/ms-style-checker.py docs/*.md
    # Upload report as artifact
```

### With Confluence
Export the HTML report as a PDF and attach to your documentation pages for review comments.

---

## Next Steps

1. ✅ **Test**: Run the Python script on your own documentation
2. ✅ **Review**: Check the HTML report and verify rules make sense
3. ✅ **Integrate**: Add to your doc review workflow
4. ✅ **Train**: Show your team how to use it
5. ✅ **Iterate**: Customize rules based on your needs

---

## Support

- **Questions about Microsoft style guide**: See `README.md` or check https://learn.microsoft.com/en-us/style-guide
- **Want to customize the checks**: Edit `scripts/ms-style-checker.py`
- **Found a bug**: Check the test output and try test files first

---

## License

This skill is based on the Microsoft Writing Style Guide, licensed under Creative Commons Attribution 4.0 International.
