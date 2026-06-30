#!/usr/bin/env python3
"""
report_generator.py — 架构评估报告生成器

将 software-design skill 的评估结果结构化导出为 Markdown 文件，
存于 output/ 目录，便于用户留存和分享。

用法:
    python report_generator.py <评估数据 JSON> [--output output/report.md]

输入 JSON 格式:
    {
        "project_name": "项目名称",
        "scenario": "design | evaluate",
        "overall_scores": {"maintainability": 7, "performance": 6, ...},
        "findings": [
            {"severity": "critical|warning|suggestion", "title": "...", "detail": "..."}
        ],
        "recommendations": [
            {"priority": "immediate|short|medium|long", "action": "...", "effort": "..."}
        ],
        "tradeoffs": [
            {"decision": "...", "gains": "...", "losses": "...", "preconditions": "..."}
        ],
        "roadmap": [
            {"phase": 1, "name": "...", "tasks": [...], "duration": "..."}
        ],
        "assumptions": ["基于默认假设: ..."]
    }
"""

import json
import os
import sys
import argparse
from datetime import datetime


REPORT_TEMPLATE = """# {project_name} — 架构{type_label}报告

> 生成时间: {timestamp}
> 场景: {scenario_label}

---

## 1. 高层执行摘要

### 总体评分

| 维度 | 评分 | 说明 |
|------|:----:|------|
{score_rows}

### 核心发现

{findings_section}

### 推荐动作

{recommendations_section}

---

## 2. 权衡分析

{tradeoffs_section}

---

## 3. {roadmap_title}

{roadmap_section}

---

## 4. 假设与约束

{assumptions_section}

---

*报告由 software-design skill 自动生成*
"""


def generate_report(data, output_path=None):
    """生成结构化 Markdown 报告"""
    project_name = data.get("project_name", "未命名项目")
    scenario = data.get("scenario", "design")

    # 场景类型
    type_label = "设计" if scenario == "design" else "评估"
    scenario_label = "初始架构设计" if scenario == "design" else "现有架构评估"
    roadmap_title = "演进路线图" if scenario == "evaluate" else "实施路线图"

    # 评分表格
    scores = data.get("overall_scores", {})
    if scores:
        score_rows = "\n".join(
            f'| {name} | {score}/10 | {desc} |'
            for name, (score, desc) in scores.items()
        )
    else:
        score_rows = "| - | - | 尚未评分 |"

    # 发现
    findings = data.get("findings", [])
    if findings:
        severity_labels = {
            "critical": "🔴 严重",
            "warning": "🟠 警告",
            "suggestion": "🟢 建议",
        }
        findings_section = "\n".join(
            f"- **{severity_labels.get(f.get('severity', 'suggestion'), '📌')}**: {f.get('title', '')}\n"
            f"  > {f.get('detail', '')}"
            for f in findings
        )
    else:
        findings_section = "> 暂未识别到明显问题。"

    # 推荐动作
    recommendations = data.get("recommendations", [])
    if recommendations:
        priority_labels = {
            "immediate": "🚨 立即",
            "short": "⚡ 短期",
            "medium": "📋 中期",
            "long": "🔭 长期",
        }
        recommendations_section = "\n".join(
            f"- **{priority_labels.get(r.get('priority', 'medium'), '📋')}**: {r.get('action', '')} "
            f"({r.get('effort', '待估算')})"
            for r in recommendations
        )
    else:
        recommendations_section = "> 暂无可推荐动作。"

    # 权衡分析
    tradeoffs = data.get("tradeoffs", [])
    if tradeoffs:
        tradeoffs_section = "\n\n".join(
            f"### {t.get('decision', '决策点')}\n\n"
            f"| 维度 | 内容 |\n"
            f"|------|------|\n"
            f"| **优点** | {t.get('gains', '-')} |\n"
            f"| **缺点/成本** | {t.get('losses', '-')} |\n"
            f"| **适用条件** | {t.get('preconditions', '-')} |\n"
            f"| **不适用场景** | {t.get('tradeoffs_extra', '-')} |\n"
            for t in tradeoffs
        )
    else:
        tradeoffs_section = "> 暂无需权衡分析。"

    # 路线图
    roadmap = data.get("roadmap", [])
    if roadmap:
        roadmap_section = "\n\n".join(
            f"### Phase {p.get('phase', i+1)}: {p.get('name', '')} ({p.get('duration', '')})\n"
            + "\n".join(f"- {t}" for t in p.get("tasks", []))
            for i, p in enumerate(roadmap)
        )
    else:
        roadmap_section = "> 暂未制定路线图。"

    # 假设
    assumptions = data.get("assumptions", [])
    if assumptions:
        assumptions_section = "\n".join(f"- ⚠️ {a}" for a in assumptions)
    else:
        assumptions_section = "> 无额外假设。"

    # 组装报告
    report = REPORT_TEMPLATE.format(
        project_name=project_name,
        type_label=type_label,
        scenario_label=scenario_label,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        score_rows=score_rows,
        findings_section=findings_section,
        recommendations_section=recommendations_section,
        tradeoffs_section=tradeoffs_section,
        roadmap_title=roadmap_title,
        roadmap_section=roadmap_section,
        assumptions_section=assumptions_section,
    )

    # 输出
    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"报告已生成: {output_path}")
    else:
        print(report)

    return report


def main():
    parser = argparse.ArgumentParser(description="架构评估报告生成器")
    parser.add_argument("input", help="评估数据 JSON 文件路径")
    parser.add_argument("--output", "-o", default=None, help="输出文件路径（默认为 output/<项目名>-report.md）")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not args.output:
        project_name = data.get("project_name", "unknown")
        args.output = os.path.join("output", f"{project_name}-report.md")

    generate_report(data, args.output)


if __name__ == "__main__":
    main()
