#!/usr/bin/env python3
"""
Generate a human-friendly summary of SCA findings with waiver support.

Input:  EVIDENCE/P09/sca_report.json (Grype JSON format)
        policy/waivers.yml (optional)
Output: EVIDENCE/P09/sca_summary.md
"""

from __future__ import annotations

import json
import os
import yaml
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

REPORT_PATH = Path("EVIDENCE/P09/sca_report.json")
SUMMARY_PATH = Path("EVIDENCE/P09/sca_summary.md")
WAIVERS_PATH = Path("policy/waivers.yml")
MAX_HIGHLIGHTS = 10


def load_report() -> Dict[str, Any]:
    """Загружает отчёт Grype"""
    if not REPORT_PATH.exists():
        raise FileNotFoundError(f"SCA report not found at {REPORT_PATH}")
    with REPORT_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_waivers() -> Dict[str, Any]:
    """Загружает waivers, если файл существует"""
    if not WAIVERS_PATH.exists():
        return {"waivers": [], "policy": {}}

    with WAIVERS_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def severity_key(value: str) -> str:
    """Нормализует severity"""
    severity_map = {
        "critical": "CRITICAL",
        "high": "HIGH",
        "medium": "MEDIUM",
        "low": "LOW",
        "negligible": "NEGLIGIBLE",
        "unknown": "UNKNOWN"
    }
    normalized = (value or "UNKNOWN").strip().lower()
    return severity_map.get(normalized, "UNKNOWN")


def filter_waived_vulnerabilities(
        matches: List[Dict[str, Any]],
        waivers_data: Dict[str, Any]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Разделяет уязвимости на waived и non-waived"""
    active_waivers = [
        w for w in waivers_data.get("waivers", [])
        if w.get("status", "").lower() in ["active", "approved"]
    ]

    waived_vulns = []
    non_waived_matches = []

    for match in matches:
        vuln = match.get("vulnerability", {})
        artifact = match.get("artifact", {})
        vuln_id = vuln.get("id", "")
        package = artifact.get("name", "")
        version = artifact.get("version", "")

        is_waived = False
        for waiver in active_waivers:
            if waiver.get("vulnerability_id") == vuln_id:
                is_waived = True
                waived_vulns.append({
                    "vulnerability": vuln,
                    "artifact": artifact,
                    "waiver": waiver
                })
                break

        if not is_waived:
            non_waived_matches.append(match)

    return non_waived_matches, waived_vulns


def build_highlights(matches: List[Dict[str, Any]], severity_filter: List[str] = None) -> List[str]:
    """Создаёт список важных уязвимостей"""
    if severity_filter is None:
        severity_filter = ["CRITICAL", "HIGH"]

    highlights = []
    for match in matches:
        vuln = match.get("vulnerability", {})
        artifact = match.get("artifact", {})
        severity = severity_key(vuln.get("severity", "UNKNOWN"))

        if severity not in severity_filter:
            continue

        cve = vuln.get("id", "UNKNOWN")
        package = artifact.get("name", "unknown")
        version = artifact.get("version", "unknown")
        description = vuln.get("description", "")

        fix_versions = vuln.get("fix", {}).get("versions") or []
        if fix_versions:
            fix_hint = f"→ **Fix available**: update to {fix_versions[0]}"
        else:
            fix_hint = "→ **No fix available**, consider mitigation"

        if len(description) > 150:
            description = description[:147] + "..."

        highlights.append(
            f"### {cve} ({severity})\n"
            f"- **Package**: {package}@{version}\n"
            f"- **Description**: {description}\n"
            f"- **Action**: {fix_hint}\n"
        )

        if len(highlights) >= MAX_HIGHLIGHTS:
            highlights.append("*(showing first 10 Critical/High issues)*")
            break

    if not highlights:
        highlights.append("- No Critical/High issues detected 🎉")

    return highlights


def build_waiver_section(waived_vulns: List[Dict[str, Any]]) -> List[str]:
    """Создаёт секцию про waivers"""
    if not waived_vulns:
        return ["- No active waivers applied"]

    lines = [f"- **Waived vulnerabilities**: {len(waived_vulns)}"]

    waived_counts = Counter()
    for item in waived_vulns:
        severity = severity_key(item["vulnerability"].get("severity", "UNKNOWN"))
        waived_counts[severity] += 1

    lines.append("  - By severity:")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]:
        if sev in waived_counts:
            lines.append(f"    - {sev}: {waived_counts[sev]}")

    lines.append("\n### Active Waivers (examples)")
    for item in waived_vulns[:3]:
        waiver = item["waiver"]
        vuln = item["vulnerability"]
        lines.append(
            f"- **{waiver.get('id', 'N/A')}**: {vuln.get('id', 'N/A')}\n"
            f"  - Package: {waiver.get('package', 'N/A')}\n"
            f"  - Reason: {waiver.get('justification', 'N/A')[:100]}...\n"
            f"  - Review due: {waiver.get('review_due', 'N/A')}"
        )

    if len(waived_vulns) > 3:
        lines.append(f"  - ... and {len(waived_vulns) - 3} more")

    return lines


def build_action_plan(counts: Counter, total: int, waived_count: int) -> List[str]:
    """Создаёт план действий"""
    lines = ["## Recommended Action Plan", ""]

    critical = counts.get("CRITICAL", 0)
    high = counts.get("HIGH", 0)
    medium = counts.get("MEDIUM", 0)
    low = counts.get("LOW", 0)

    if critical > 0:
        lines.append("### 🔴 Immediate Actions (Critical)")
        lines.append("1. **Stop deployment** if not already deployed")
        lines.append("2. **Assess exploitability** within 24 hours")
        lines.append("3. **Apply patches** or implement compensating controls")
        lines.append("4. **Update waivers** if risks are accepted")

    if high > 0:
        lines.append("### 🟡 High Priority (High)")
        lines.append("1. **Schedule updates** within 7 days")
        lines.append("2. **Review in next security meeting**")
        lines.append("3. **Consider temporary mitigations**")

    if medium > 0:
        lines.append("### 🔵 Medium Priority (Medium)")
        lines.append("1. **Plan updates** within 30 days")
        lines.append("2. **Monitor for new fixes**")
        lines.append("3. **Include in next sprint** if feasible")

    if low > 0:
        lines.append("### ⚪ Low Priority (Low/Negligible)")
        lines.append("1. **Review during next dependency audit**")
        lines.append("2. **Update with next major release**")

    if waived_count > 0:
        lines.append("### 📋 Waiver Management")
        lines.append("1. **Review scheduled waivers** before expiry")
        lines.append("2. **Document decisions** in DS1 section")
        lines.append("3. **Re-assess waived vulnerabilities** quarterly")

    lines.append("\n### 📚 References")
    lines.append("- **Update Policy**: See `policy/waivers.yml` for SLA per severity")
    lines.append("- **DS1 Integration**: Use this report for Dependency Security section")
    lines.append("- **Workflow**: [View full SCA workflow]")

    return lines


def write_summary(report: Dict[str, Any], waivers_data: Dict[str, Any]) -> None:
    """Генерирует финальный markdown отчёт"""
    matches = report.get("matches", [])

    non_waived_matches, waived_vulns = filter_waived_vulnerabilities(matches, waivers_data)
    waived_count = len(waived_vulns)

    counts = Counter()
    for match in non_waived_matches:
        severity = severity_key(
            match.get("vulnerability", {}).get("severity", "UNKNOWN")
        )
        counts[severity] += 1

    total_non_waived = sum(counts.values())
    total_all = len(matches)

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    commit = os.getenv("GITHUB_SHA") or "unknown"
    run_id = os.getenv("GITHUB_RUN_ID") or "N/A"

    lines = [
        "# SCA Security Summary (P09)",
        "",
        "## 📊 Executive Summary",
        f"- **Generated**: {generated_at}",
        f"- **Commit**: `{commit[:8]}`",
        f"- **Workflow Run**: #{run_id}",
        f"- **Total vulnerabilities found**: {total_all}",
        f"- **After waivers**: {total_non_waived} require attention",
        f"- **Waivers applied**: {waived_count}",
        "",
        "## 📈 Severity Distribution",
    ]

    if total_all == 0:
        lines.append("- No vulnerabilities detected. ✅")
    else:
        for level in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "NEGLIGIBLE", "UNKNOWN"]:
            count = counts.get(level, 0)
            if count > 0:
                lines.append(f"- **{level}**: {count}")

        lines.append("")
        if total_non_waived > 0:
            lines.append("### Risk Level (without waivers)")
            critical_high = counts.get("CRITICAL", 0) + counts.get("HIGH", 0)
            if critical_high == 0:
                lines.append("- ✅ **Low risk**: No Critical/High severity issues")
            elif critical_high < 3:
                lines.append(f"- ⚠️ **Medium risk**: {critical_high} Critical/High issues")
            else:
                lines.append(f"- 🚨 **High risk**: {critical_high} Critical/High issues")

    lines.append("")
    lines.append("## 📝 Waivers Status")
    lines.extend(build_waiver_section(waived_vulns))

    lines.append("")
    lines.append("## 🚨 Critical & High Vulnerabilities (Requiring Action)")
    highlights = build_highlights(non_waived_matches, ["CRITICAL", "HIGH"])
    lines.extend(highlights)

    medium_highlights = build_highlights(non_waived_matches, ["MEDIUM"])
    if len(medium_highlights) > 1:
        lines.append("")
        lines.append("## ⚠️ Medium Vulnerabilities (Schedule Updates)")
        lines.extend(medium_highlights[:5])

    lines.append("")
    lines.extend(build_action_plan(counts, total_non_waived, waived_count))

    lines.extend([
        "",
        "---",
        "**How to use this report:**",
        "1. Review Critical/High findings immediately",
        "2. Update waivers in `policy/waivers.yml` as needed",
        "3. Reference findings in DS1 (Dependency Security) section",
        "4. Re-run after dependency updates",
        "",
        "*Generated automatically by CI/CD Security Pipeline*"
    ])

    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"✓ Summary written to {SUMMARY_PATH}")
    print(f"  - Total vulnerabilities: {total_all}")
    print(f"  - After waivers: {total_non_waived}")
    print(f"  - Critical/High: {counts.get('CRITICAL', 0) + counts.get('HIGH', 0)}")


def main() -> None:
    """Основная функция"""
    print("Generating SCA summary with waiver support...")

    try:
        report = load_report()
        waivers_data = load_waivers()
        write_summary(report, waivers_data)
    except Exception as e:
        print(f"Error generating summary: {e}")
        raise


if __name__ == "__main__":
    main()