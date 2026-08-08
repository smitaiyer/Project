#!/usr/bin/env python3
"""
Microsoft Writing Style Guide Checker
Validates Markdown documentation against Microsoft's style guide.
Generates an HTML report with inline previews and suggestions.
"""

import json
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple
from datetime import datetime

@dataclass
class Violation:
    file: str
    line_num: int
    rule_id: int
    rule_name: str
    severity: str  # 'error', 'warning', 'suggestion'
    original_text: str
    suggested_fix: str
    explanation: str
    context_before: str = ""
    context_after: str = ""

class MSStyleChecker:
    def __init__(self):
        self.violations = []
        self.rules = self._define_rules()

    def _define_rules(self):
        return {
            1: {
                "name": "Contractions",
                "check": self._check_missing_contractions,
                "severity": "suggestion"
            },
            2: {
                "name": "Passive Voice",
                "check": self._check_passive_voice,
                "severity": "warning"
            },
            3: {
                "name": "Capitalization (Product Names)",
                "check": self._check_product_capitalization,
                "severity": "error"
            },
            4: {
                "name": "Terminology Consistency",
                "check": self._check_terminology,
                "severity": "warning"
            },
            5: {
                "name": "Heading Hierarchy",
                "check": self._check_heading_hierarchy,
                "severity": "error"
            },
            6: {
                "name": "Numbered List Format",
                "check": self._check_list_format,
                "severity": "warning"
            },
            7: {
                "name": "Oxford Comma",
                "check": self._check_oxford_comma,
                "severity": "suggestion"
            },
            8: {
                "name": "Ambiguous Pronouns",
                "check": self._check_ambiguous_pronouns,
                "severity": "warning"
            },
            9: {
                "name": "Second Person Voice",
                "check": self._check_second_person,
                "severity": "suggestion"
            },
            10: {
                "name": "Wordy Phrases",
                "check": self._check_wordy_phrases,
                "severity": "suggestion"
            },
            11: {
                "name": "Jargon & Undefined Terms",
                "check": self._check_jargon,
                "severity": "error"
            },
            12: {
                "name": "Weak Phrases",
                "check": self._check_weak_phrases,
                "severity": "suggestion"
            },
            13: {
                "name": "Link Text Clarity",
                "check": self._check_link_text,
                "severity": "warning"
            },
            14: {
                "name": "Code Block Formatting",
                "check": self._check_code_blocks,
                "severity": "warning"
            },
            15: {
                "name": "Vague Quantifiers",
                "check": self._check_vague_quantifiers,
                "severity": "suggestion"
            }
        }

    def check_file(self, filepath: str) -> List[Violation]:
        """Check a single Markdown file for style violations."""
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for rule_id, rule in self.rules.items():
            rule["check"](filepath, lines, rule_id)

        return self.violations

    def check_files(self, filepaths: List[str]) -> List[Violation]:
        """Check multiple files."""
        for filepath in filepaths:
            self.check_file(filepath)
        return self.violations

    # ===== RULE IMPLEMENTATIONS =====

    def _check_missing_contractions(self, filepath: str, lines: List[str], rule_id: int):
        """Find overly formal phrases that should use contractions."""
        patterns = [
            (r"\bdo not\b", "do not", "don't"),
            (r"\bcan not\b", "can not", "can't"),
            (r"\bcannot\b", "cannot", "can't"),
            (r"\byou are\b", "you are", "you're"),
            (r"\bit is\b", "it is", "it's"),
            (r"\byou will\b", "you will", "you'll"),
            (r"\bwe are\b", "we are", "we're"),
        ]
        for i, line in enumerate(lines, 1):
            for pattern, original, contraction in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self._add_violation(
                        filepath, i, rule_id,
                        self.rules[rule_id]["name"],
                        "suggestion",
                        line.strip(),
                        line.replace(original, contraction),
                        f"Use '{contraction}' to sound conversational. Formal tone avoids contractions, but Microsoft style guide recommends them for approachability."
                    )

    def _check_passive_voice(self, filepath: str, lines: List[str], rule_id: int):
        """Detect passive voice constructions."""
        passive_patterns = [
            (r"\bis\s+\w+ed\b", "is [verb]ed"),
            (r"\bwas\s+\w+ed\b", "was [verb]ed"),
            (r"\bbeing\s+\w+ed\b", "being [verb]ed"),
            (r"\bby\s+the\s+\w+", "by the [subject]"),
        ]
        for i, line in enumerate(lines, 1):
            if any(re.search(pattern, line) for pattern, _ in passive_patterns):
                self._add_violation(
                    filepath, i, rule_id,
                    self.rules[rule_id]["name"],
                    "warning",
                    line.strip(),
                    "[Rewrite in active voice]",
                    "Use active voice (~95% of the time). Make the subject perform the action. Example: 'The user deletes the file' instead of 'The file is deleted by the user.'"
                )

    def _check_product_capitalization(self, filepath: str, lines: List[str], rule_id: int):
        """Check for inconsistent Microsoft product name capitalization."""
        products = [
            (r"\bazure\s+portal", "Azure Portal"),
            (r"\bazure\s+sdk", "Azure SDK"),
            (r"\bazure\s+devops", "Azure DevOps"),
            (r"\bazure\s+ad", "Azure AD"),
            (r"\bpython\s+sdk", "Python SDK"),
            (r"\b\.net\s+\d", ".NET [version]"),
        ]
        for i, line in enumerate(lines, 1):
            for pattern, correct in products:
                if re.search(pattern, line, re.IGNORECASE) and not re.search(correct, line):
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        self._add_violation(
                            filepath, i, rule_id,
                            self.rules[rule_id]["name"],
                            "error",
                            line.strip(),
                            line.replace(match.group(), correct),
                            f"Capitalize Microsoft product names consistently. Use '{correct}' on first mention."
                        )

    def _check_terminology(self, filepath: str, lines: List[str], rule_id: int):
        """Check for inconsistent terminology."""
        # Simple check: flag if terms are mixed within a file
        terminology_pairs = [
            ("sign in", "log in"),
            ("dialog box", "dialog"),
            ("Azure SDK", "SDK"),
        ]
        file_text = "".join(lines)
        for term1, term2 in terminology_pairs:
            if term1.lower() in file_text.lower() and term2.lower() in file_text.lower():
                for i, line in enumerate(lines, 1):
                    if term2.lower() in line.lower():
                        self._add_violation(
                            filepath, i, rule_id,
                            self.rules[rule_id]["name"],
                            "warning",
                            line.strip(),
                            f"[Use '{term1}' consistently; found both '{term1}' and '{term2}']",
                            f"Terminology consistency: use one term per concept. Choose '{term1}' or '{term2}' and use it throughout."
                        )

    def _check_heading_hierarchy(self, filepath: str, lines: List[str], rule_id: int):
        """Ensure heading hierarchy doesn't skip levels."""
        heading_levels = []
        for i, line in enumerate(lines, 1):
            match = re.match(r'^(#{1,6})\s', line)
            if match:
                level = len(match.group(1))
                heading_levels.append((level, i, line.strip()))

        # Check for skips
        for idx, (level, line_num, text) in enumerate(heading_levels):
            if idx > 0:
                prev_level = heading_levels[idx - 1][0]
                if level - prev_level > 1:
                    self._add_violation(
                        filepath, line_num, rule_id,
                        self.rules[rule_id]["name"],
                        "error",
                        text,
                        f"{text.replace('#', '##')}",  # Suggest fixing by demoting
                        f"Heading hierarchy should not skip levels. Found h{prev_level} followed by h{level}. Use h{prev_level + 1}."
                    )

    def _check_list_format(self, filepath: str, lines: List[str], rule_id: int):
        """Check numbered list formatting."""
        for i, line in enumerate(lines, 1):
            # Check for numbered lists starting with lowercase
            if re.match(r'^\d+\.\s+[a-z]', line):
                corrected = re.sub(r'^(\d+\.\s+)([a-z])', r'\1', line)
                self._add_violation(
                    filepath, i, rule_id,
                    self.rules[rule_id]["name"],
                    "warning",
                    line.strip(),
                    line[0:2] + line[2].upper() + line[3:].rstrip(),
                    "List items should start with a capital letter."
                )

    def _check_oxford_comma(self, filepath: str, lines: List[str], rule_id: int):
        """Detect missing Oxford commas in lists of 3+ items."""
        for i, line in enumerate(lines, 1):
            # Simple pattern: three items separated by commas and 'and' without preceding comma
            if re.search(r'\w+,\s+\w+\s+and\s+\w+', line) and ',' not in line[line.rfind('and') - 5:line.rfind('and')]:
                self._add_violation(
                    filepath, i, rule_id,
                    self.rules[rule_id]["name"],
                    "suggestion",
                    line.strip(),
                    line.replace(" and ", ", and "),
                    "Use Oxford comma before 'and' in lists of 3+ items for clarity: 'x, y, and z'."
                )

    def _check_ambiguous_pronouns(self, filepath: str, lines: List[str], rule_id: int):
        """Flag ambiguous pronouns at sentence start."""
        for i in range(1, len(lines)):
            line = lines[i]
            if re.match(r'^(It|This|That|These|Those)\s+', line):
                self._add_violation(
                    filepath, i + 1, rule_id,
                    self.rules[rule_id]["name"],
                    "warning",
                    line.strip(),
                    "[Clarify what 'It'/'This' refers to]",
                    "Avoid pronouns without clear antecedents. Example: 'Install the SDK. The SDK requires .NET 6' instead of 'Install the SDK. It requires .NET 6.'"
                )

    def _check_second_person(self, filepath: str, lines: List[str], rule_id: int):
        """Detect third-person voice where second person is better."""
        patterns = [
            (r"\bthe user\b", "you"),
            (r"\bone can\b", "you can"),
            (r"\badministrators?\b", "you"),
        ]
        for i, line in enumerate(lines, 1):
            for pattern, suggestion in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self._add_violation(
                        filepath, i, rule_id,
                        self.rules[rule_id]["name"],
                        "suggestion",
                        line.strip(),
                        line.replace(re.search(pattern, line, re.IGNORECASE).group(), suggestion),
                        f"Use second-person 'you' instead of third-person. More conversational and direct."
                    )

    def _check_wordy_phrases(self, filepath: str, lines: List[str], rule_id: int):
        """Detect wordy/redundant phrases."""
        wordy = [
            ("in order to", "to"),
            ("at this point in time", "now"),
            ("there is", "[rewrite with active verb]"),
            ("there are", "[rewrite with active verb]"),
        ]
        for i, line in enumerate(lines, 1):
            for wordy_phrase, fix in wordy:
                if wordy_phrase in line.lower():
                    self._add_violation(
                        filepath, i, rule_id,
                        self.rules[rule_id]["name"],
                        "suggestion",
                        line.strip(),
                        line.replace(wordy_phrase, fix),
                        f"Replace '{wordy_phrase}' with '{fix}' for brevity and clarity."
                    )

    def _check_jargon(self, filepath: str, lines: List[str], rule_id: int):
        """Flag undefined jargon and acronyms."""
        acronyms = [
            (r'\bRBAC\b', "role-based access control (RBAC)"),
            (r'\bAPI\b(?!\s+\()', "API (Application Programming Interface)"),
            (r'\bJSON\b(?!\s+\()', "JSON (JavaScript Object Notation)"),
        ]
        for i, line in enumerate(lines, 1):
            for pattern, full_term in acronyms:
                if re.search(pattern, line) and full_term.replace(f" ({pattern.replace(chr(92), '').replace('b', '').replace('\\', '')})", "") not in line:
                    self._add_violation(
                        filepath, i, rule_id,
                        self.rules[rule_id]["name"],
                        "error",
                        line.strip(),
                        line.replace(re.search(pattern, line).group(), full_term.split(" (")[0]),
                        f"Define acronyms on first use. Replace with '{full_term}'."
                    )

    def _check_weak_phrases(self, filepath: str, lines: List[str], rule_id: int):
        """Detect weak opening phrases."""
        weak = [
            ("Please note", "[Rewrite without placeholder]"),
            ("It should be noted", "[Rewrite without placeholder]"),
            ("You can ", "[Remove and start with verb]"),
        ]
        for i, line in enumerate(lines, 1):
            for weak_phrase, fix in weak:
                if weak_phrase in line:
                    self._add_violation(
                        filepath, i, rule_id,
                        self.rules[rule_id]["name"],
                        "suggestion",
                        line.strip(),
                        line.replace(weak_phrase, fix),
                        f"Remove '{weak_phrase}' and start directly with the action or key info."
                    )

    def _check_link_text(self, filepath: str, lines: List[str], rule_id: int):
        """Check for vague link text."""
        vague_links = [
            (r'\[click here\]', "use descriptive text"),
            (r'\[link\]', "use descriptive text"),
            (r'\[more information\]', "use descriptive text"),
        ]
        for i, line in enumerate(lines, 1):
            for pattern, fix in vague_links:
                if re.search(pattern, line, re.IGNORECASE):
                    self._add_violation(
                        filepath, i, rule_id,
                        self.rules[rule_id]["name"],
                        "warning",
                        line.strip(),
                        f"[Descriptive link text describing the target]",
                        f"Use descriptive link text instead of '{pattern}'. Example: '[Learn about Azure authentication](url)'"
                    )

    def _check_code_blocks(self, filepath: str, lines: List[str], rule_id: int):
        """Check code block formatting."""
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('```') and not re.match(r'```\w+', line.strip()):
                self._add_violation(
                    filepath, i, rule_id,
                    self.rules[rule_id]["name"],
                    "warning",
                    line.strip(),
                    line.replace('```', '```python  # or appropriate language'),
                    "Specify the language in code fences for syntax highlighting. Example: ```python, ```json, ```csharp."
                )

    def _check_vague_quantifiers(self, filepath: str, lines: List[str], rule_id: int):
        """Detect vague quantifiers."""
        vague = [
            ("several", "specific number"),
            ("many", "specific number"),
            ("some", "specific number"),
            ("a lot", "specific number"),
        ]
        for i, line in enumerate(lines, 1):
            for vague_word, suggestion in vague:
                if f" {vague_word} " in line.lower():
                    self._add_violation(
                        filepath, i, rule_id,
                        self.rules[rule_id]["name"],
                        "suggestion",
                        line.strip(),
                        line.replace(vague_word, "[specific number/percentage]"),
                        f"Replace vague '{vague_word}' with specific numbers or percentages for clarity."
                    )

    def _add_violation(self, file: str, line_num: int, rule_id: int, rule_name: str,
                      severity: str, original: str, suggested: str, explanation: str):
        """Add a violation to the list."""
        violation = Violation(
            file=file,
            line_num=line_num,
            rule_id=rule_id,
            rule_name=rule_name,
            severity=severity,
            original_text=original,
            suggested_fix=suggested,
            explanation=explanation
        )
        self.violations.append(violation)

def generate_html_report(violations: List[Violation], output_file: str = "ms-docs-review.html"):
    """Generate an HTML report from violations."""

    # Group violations by file and severity
    violations_by_file = {}
    severity_counts = {"error": 0, "warning": 0, "suggestion": 0}
    rule_counts = {}

    for v in violations:
        if v.file not in violations_by_file:
            violations_by_file[v.file] = []
        violations_by_file[v.file].append(v)
        severity_counts[v.severity] += 1
        rule_counts[v.rule_name] = rule_counts.get(v.rule_name, 0) + 1

    # Sort rules by frequency
    top_rules = sorted(rule_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microsoft Style Guide Review Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #0078d4 0%, #0063b1 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; }}
        h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header-meta {{ font-size: 0.95em; opacity: 0.9; }}
        .dashboard {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 40px; }}
        .stat-card {{ background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .stat-card h3 {{ color: #666; font-size: 0.9em; text-transform: uppercase; margin-bottom: 10px; }}
        .stat-number {{ font-size: 2.5em; font-weight: bold; }}
        .stat-number.error {{ color: #d13438; }}
        .stat-number.warning {{ color: #ffd700; }}
        .stat-number.suggestion {{ color: #0078d4; }}
        .tabs {{ display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #ddd; }}
        .tab {{ padding: 12px 20px; cursor: pointer; border: none; background: none; font-size: 1em; color: #666; border-bottom: 3px solid transparent; transition: all 0.3s; }}
        .tab.active {{ color: #0078d4; border-bottom-color: #0078d4; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .violation-item {{ background: white; padding: 20px; margin-bottom: 15px; border-radius: 8px; border-left: 4px solid #ddd; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .violation-item.error {{ border-left-color: #d13438; }}
        .violation-item.warning {{ border-left-color: #ffd700; }}
        .violation-item.suggestion {{ border-left-color: #0078d4; }}
        .violation-header {{ display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px; }}
        .violation-title {{ font-weight: 600; font-size: 1.05em; color: #333; }}
        .severity-badge {{ padding: 4px 12px; border-radius: 20px; font-size: 0.85em; font-weight: 600; text-transform: uppercase; }}
        .severity-badge.error {{ background: #fde7e9; color: #d13438; }}
        .severity-badge.warning {{ background: #fff4ce; color: #9c6c00; }}
        .severity-badge.suggestion {{ background: #dbeafe; color: #0078d4; }}
        .location {{ color: #666; font-size: 0.9em; margin-bottom: 10px; }}
        .code-comparison {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 15px 0; font-family: 'Courier New', monospace; }}
        .code-block {{ padding: 12px; border-radius: 4px; font-size: 0.9em; overflow-x: auto; }}
        .original {{ background: #ffefef; border: 1px solid #d13438; color: #d13438; }}
        .suggested {{ background: #f0f7ff; border: 1px solid #0078d4; color: #0078d4; }}
        .original::before {{ content: '❌ '; font-weight: bold; }}
        .suggested::before {{ content: '✓ '; font-weight: bold; }}
        .explanation {{ background: #f9f9f9; padding: 12px; border-radius: 4px; margin: 10px 0; font-size: 0.95em; border-left: 3px solid #0078d4; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .chart {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .rule-bar {{ display: flex; align-items: center; margin-bottom: 12px; }}
        .rule-name {{ flex: 0 0 200px; font-size: 0.9em; }}
        .rule-bar-fill {{ flex: 1; height: 20px; background: linear-gradient(90deg, #0078d4, #00bcf2); border-radius: 3px; margin: 0 10px; }}
        .rule-count {{ flex: 0 0 40px; text-align: right; font-weight: 600; color: #333; }}
        .summary {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .file-section {{ margin-bottom: 30px; }}
        .file-header {{ background: #f0f0f0; padding: 15px; border-radius: 4px; margin-bottom: 15px; font-weight: 600; color: #333; }}
        footer {{ text-align: center; color: #666; font-size: 0.9em; margin-top: 40px; padding: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📋 Microsoft Style Guide Review</h1>
            <p class="header-meta">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {len(violations)} total violations across {len(violations_by_file)} file(s)</p>
        </header>

        <div class="dashboard">
            <div class="stat-card">
                <h3>Total Violations</h3>
                <div class="stat-number">{len(violations)}</div>
            </div>
            <div class="stat-card">
                <h3>Errors</h3>
                <div class="stat-number error">{severity_counts['error']}</div>
            </div>
            <div class="stat-card">
                <h3>Warnings</h3>
                <div class="stat-number warning">{severity_counts['warning']}</div>
            </div>
            <div class="stat-card">
                <h3>Suggestions</h3>
                <div class="stat-number suggestion">{severity_counts['suggestion']}</div>
            </div>
        </div>

        <div class="tabs">
            <button class="tab active" onclick="showTab(event, 'findings')">📌 Detailed Findings</button>
            <button class="tab" onclick="showTab(event, 'stats')">📊 Statistics</button>
        </div>

        <div id="findings" class="tab-content active">
"""

    # Add findings by file
    for filepath in sorted(violations_by_file.keys()):
        file_violations = sorted(violations_by_file[filepath], key=lambda v: v.line_num)
        html += f'<div class="file-section"><div class="file-header">📄 {filepath} ({len(file_violations)} issues)</div>'

        for v in file_violations:
            html += f"""
            <div class="violation-item {v.severity}">
                <div class="violation-header">
                    <div class="violation-title">{v.rule_name}</div>
                    <span class="severity-badge {v.severity}">{v.severity}</span>
                </div>
                <div class="location">Line {v.line_num} in {filepath}</div>
                <div class="code-comparison">
                    <div class="code-block original">{v.original_text}</div>
                    <div class="code-block suggested">{v.suggested_fix}</div>
                </div>
                <div class="explanation">💡 {v.explanation}</div>
            </div>
"""
        html += '</div>'

    # Add statistics tab
    html += f"""
        </div>

        <div id="stats" class="tab-content">
            <div class="summary">
                <h2>Review Summary</h2>
                <p><strong>Files reviewed:</strong> {len(violations_by_file)}</p>
                <p><strong>Total violations:</strong> {len(violations)}</p>
                <p><strong>Most common issues:</strong></p>
            </div>
            <div class="chart">
                <h3>Top 10 Violation Types</h3>
"""

    max_count = max(count for _, count in top_rules) if top_rules else 1
    for rule_name, count in top_rules:
        width_pct = (count / max_count * 100) if max_count > 0 else 0
        html += f"""
                <div class="rule-bar">
                    <div class="rule-name">{rule_name}</div>
                    <div class="rule-bar-fill" style="width: {width_pct}%;"></div>
                    <div class="rule-count">{count}</div>
                </div>
"""

    html += """
            </div>
        </div>

        <footer>
            <p>This report was generated using the Microsoft Writing Style Guide. For more information, visit <a href="https://learn.microsoft.com/en-us/style-guide" target="_blank">Microsoft Style Guide</a>.</p>
            <p>💼 Generated by Microsoft Docs Style & Terminology Review Skill</p>
        </footer>
    </div>

    <script>
        function showTab(evt, tabName) {
            var i, tabcontent, tabs;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].classList.remove("active");
            }
            tabs = document.getElementsByClassName("tab");
            for (i = 0; i < tabs.length; i++) {
                tabs[i].classList.remove("active");
            }
            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.classList.add("active");
        }
    </script>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_file

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ms-style-checker.py <file1.md> [file2.md] ...")
        sys.exit(1)

    checker = MSStyleChecker()
    files = sys.argv[1:]
    checker.check_files(files)

    output = generate_html_report(checker.violations)
    print(f"Report generated: {output}")
    print(f"Total violations: {len(checker.violations)}")
