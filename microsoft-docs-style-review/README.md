# Microsoft Docs Style & Terminology Review Skill

A Claude Code skill for reviewing technical documentation against the Microsoft Writing Style Guide. Generates detailed HTML reports with inline previews and concrete rewrite suggestions.

## Quick Start

### Using the Skill in Claude Code

```
/microsoft-docs:style-and-terminology-review
```

Upload your Markdown documentation files (one or multiple), and Claude will:
1. Check against 15 common MS style violations
2. Generate a professional HTML report
3. Show inline previews of problems and fixes
4. Provide actionable suggestions

### Example Workflow

1. **Upload docs** → getting-started.md, api-reference.md, troubleshooting.md
2. **Run skill** → `I need to audit these docs for Microsoft style guide compliance`
3. **Download report** → ms-docs-review.html
4. **Review findings** → Dashboard shows 35 violations (5 errors, 18 warnings, 12 suggestions)
5. **Apply fixes** → Use suggested rewrites from the report

---

## What the Skill Checks (15 Rules)

| # | Check | Severity | What It Detects |
|---|-------|----------|-----------------|
| 1 | Contractions | Suggestion | Overly formal phrases that should use contractions (don't, can't, you'll) |
| 2 | Passive Voice | Warning | Passive constructions; recommends active voice |
| 3 | Capitalization (Products) | Error | Inconsistent product name capitalization (azure portal → Azure Portal) |
| 4 | Terminology Consistency | Warning | Mixed terminology (sign in vs. log in, dialog vs. dialog box) |
| 5 | Heading Hierarchy | Error | Skipped heading levels (h1 → h3, should be h1 → h2 → h3) |
| 6 | Numbered List Format | Warning | List items not starting with capital letter or missing periods |
| 7 | Oxford Comma | Suggestion | Missing Oxford comma before "and" in lists (x, y and z → x, y, and z) |
| 8 | Ambiguous Pronouns | Warning | Pronouns without clear antecedent (It, This, That at sentence start) |
| 9 | Second Person Voice | Suggestion | Third-person usage where second-person is better (the user → you) |
| 10 | Wordy Phrases | Suggestion | Redundant phrases (in order to → to, there is → [active verb]) |
| 11 | Jargon & Undefined Terms | Error | Acronyms/jargon used without definition (RBAC, API, JSON) |
| 12 | Weak Phrases | Suggestion | Filler phrases (Please note, it should be noted, you can) |
| 13 | Link Text Clarity | Warning | Vague link text (click here, link, more information) |
| 14 | Code Block Formatting | Warning | Code blocks without language specification |
| 15 | Vague Quantifiers | Suggestion | Vague numbers (many, several, a lot → specific numbers) |

---

## Report Format

The generated HTML report includes:

### Dashboard
- **Total violations** count
- **Severity breakdown** (Errors, Warnings, Suggestions with color coding)
- **Files reviewed** summary

### Detailed Findings
Each violation shows:
- **Rule name** (e.g., "Passive Voice")
- **Location** (File name, line number)
- **Severity badge** (Error 🔴, Warning 🟡, Suggestion 🔵)
- **Side-by-side comparison**:
  - Left: Original text (red background)
  - Right: Suggested fix (blue background)
- **Explanation**: Why it violates the style guide

### Statistics Tab
- **Top 10 violation types** with frequency chart
- **Summary** of files reviewed and total violations

### Design
- **Blue/white/red color scheme** for clarity
- **Mobile-responsive** layout
- **Self-contained HTML** (no external dependencies)
- **Downloadable and shareable**

---

## Examples

### Example 1: Passive Voice
```
❌ Original:
"The file was deleted by the user."

✓ Suggested:
"The user deleted the file."

Why:
Use active voice (~95% of the time). Make the subject perform the action.
```

### Example 2: Product Capitalization
```
❌ Original:
"Use azure portal to configure settings."

✓ Suggested:
"Use Azure Portal to configure settings."

Why:
Capitalize Microsoft product names consistently. Use 'Azure Portal' on first mention.
```

### Example 3: Undefined Jargon
```
❌ Original:
"Configure the RBAC policy in your subscription."

✓ Suggested:
"Configure the role-based access control (RBAC) policy in your subscription."

Why:
Define acronyms on first use. Replace with 'role-based access control (RBAC)'.
```

---

## Installation

### Option 1: In Claude Code (Recommended)
The skill is available as `/microsoft-docs:style-and-terminology-review` in Claude Code's skill library.

### Option 2: Manual Installation
1. Copy the `microsoft-docs-style-review/` folder to your Claude Code skills directory
2. Restart Claude Code
3. The skill will appear in the skill list with `/microsoft-docs:style-and-terminology-review`

### Option 3: Run the Script Directly
```bash
cd microsoft-docs-style-review
python scripts/ms-style-checker.py docs/getting-started.md docs/api-reference.md
# Outputs: ms-docs-review.html
```

---

## How to Interpret Results

### Priority Guide

1. **Fix all Errors first** (red badges)
   - Breaks style guide rules or creates clarity/accessibility issues
   - Examples: Product capitalization, undefined jargon, heading hierarchy

2. **Address Warnings second** (yellow badges)
   - Deviates from recommended practice
   - Examples: Passive voice, ambiguous pronouns, weak link text

3. **Polish with Suggestions last** (blue badges)
   - Stylistic improvements for better tone/clarity
   - Examples: Add contractions, use Oxford comma, replace wordy phrases

### Sample Report Interpretation

**Report shows**: 35 total violations (5 errors, 18 warnings, 12 suggestions)

**Action plan**:
1. Fix 5 errors (~10 minutes) → Product names, undefined acronyms, heading hierarchy
2. Address 18 warnings (~20 minutes) → Passive voice, pronouns, link text
3. Polish 12 suggestions (~15 minutes) → Tone, contractions, wordiness

**Total time**: ~45 minutes for full compliance

---

## Based On

This skill is built on the **[Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide)**, Microsoft's official standard for technical documentation. All rules and explanations reference this authoritative source.

### Key Principles from the Guide

1. **Be warm and relaxed** — Use conversational tone, including contractions
2. **Be ready to lend a hand** — Show empathy, provide clear solutions
3. **Be crisp and clear** — Simple language, easy to scan
4. **Write like you speak** — Read aloud; sounds like a conversation, not a memo
5. **Use second person** — Address readers directly as "you"
6. **Use active voice** — Make the subject perform the action (~95% of the time)

---

## Tips & Tricks

### Batch Processing
Upload multiple files at once:
```
I need to review these 5 files for style compliance: 
getting-started.md, api-reference.md, faq.md, troubleshooting.md, release-notes.md
```

The report will group violations by file with line numbers, making it easy to navigate and fix.

### Iterative Review
Run the skill multiple times:
1. **First pass**: Fix all errors and warnings
2. **Second pass**: Polish suggestions and tone
3. **Final pass**: Verify consistency across all files

### Custom Terminology
If your team uses specific terminology:
1. Mention it when running the skill
2. The skill will flag inconsistencies
3. Example: "We use 'sign in' consistently, not 'log in'"

### Team Handoff
The HTML report is perfect for sharing with writers:
- No technical knowledge required to understand suggestions
- Clear before/after examples
- Exportable and printable
- Includes explanations tied to Microsoft style guide

---

## What's Not Covered

This skill focuses on **Microsoft Writing Style Guide** compliance. It does NOT:

- ❌ Validate technical accuracy (does the code work?)
- ❌ Check API completeness (are all parameters documented?)
- ❌ Validate OpenAPI schemas (use `check-api-doc-compliance` for that)
- ❌ Check SEO or metadata
- ❌ Spell-check or grammar (use separate tools for that)
- ❌ Enforce brand capitalization outside Microsoft products

For those needs, pair this skill with other tools:
- **Technical accuracy** → Code review tools, testing frameworks
- **API completeness** → `check-api-doc-compliance` skill
- **Spelling/grammar** → Grammarly, LanguageTool
- **SEO** → Semrush, Ahrefs

---

## Feedback & Improvements

Found a violation being flagged incorrectly? Or a style rule we should add?

1. **Report in issue** with example text and expected behavior
2. **Suggest rules** for new style checks
3. **Propose improvements** to existing checks

---

## License & Attribution

This skill is based on the [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide), published by Microsoft under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

---

## Support

**How to use this skill**: See "Quick Start" section above or run `/help microsoft-docs:style-and-terminology-review`

**Questions**: Add your question as an issue or check the FAQ in the documentation

**Want to customize?** The Python script (`scripts/ms-style-checker.py`) can be modified to add custom checks or adjust existing ones.
