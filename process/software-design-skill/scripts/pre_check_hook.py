#!/usr/bin/env python3
"""
pre_check_hook.py — 前置检查钩子

在 software-design skill 执行前运行，检查上下文中是否包含足够的业务与系统信息。
若缺失必填项，返回需补充的问题列表，阻塞主流程直到补齐。

用法:
    python pre_check_hook.py <context_file_or_json>

返回:
    JSON 对象: {"pass": true/false, "missing_items": [...], "questions": [...]}
"""

import json
import sys
import re


REQUIRED_FIELDS = {
    "business_goal": {
        "label": "核心业务目标",
        "question": "请用 1-2 句话描述项目的核心业务目标是什么？",
        "hint": "例如：构建一个支持多租户的 SaaS 电商平台",
    },
    "feature_list": {
        "label": "功能列表",
        "question": "请列出当前已知的核心功能需求有哪些？",
        "hint": "例如：用户注册登录、商品管理、订单处理、支付对接",
    },
    "current_state": {
        "label": "项目现状",
        "question": "项目处于什么阶段？（从零开始 / 已有代码库 / 正在重构）",
        "hint": "已有代码库请说明语言、框架和大致的代码量",
    },
}

OPTIONAL_FIELDS = {
    "non_functional": {
        "label": "非功能需求",
        "question": "是否有性能、可用性、安全合规方面的要求？（可跳过）",
        "default_assumption": "未指定非功能需求，默认按普通 Web 应用标准处理（< 1000 QPS, 99.9% 可用性）",
    },
    "tech_stack": {
        "label": "技术栈偏好",
        "question": "是否有偏好的技术栈或必须兼容的现有系统？（可跳过）",
        "default_assumption": "未指定技术栈，默认按主流方案推荐",
    },
    "constraints": {
        "label": "约束条件",
        "question": "是否有预算、时间、部署环境方面的约束？（可跳过）",
        "default_assumption": "未指定约束，默认按中等规模项目估算",
    },
}


def parse_context(context_input):
    """解析输入上下文，支持 JSON 字符串或文件路径"""
    if not context_input:
        return {}

    # 尝试解析为 JSON
    try:
        if context_input.strip().startswith("{"):
            return json.loads(context_input)
    except json.JSONDecodeError:
        pass

    # 尝试作为文件路径读取
    try:
        with open(context_input, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    # 尝试作为纯文本解析，提取关键信息
    return _parse_plain_text(context_input)


def _parse_plain_text(text):
    """从纯文本中尝试提取结构化信息"""
    result = {}
    text_lower = text.lower()

    # 检测项目阶段
    if any(kw in text_lower for kw in ["从零", "新项目", "启动", "设计"]):
        result["current_state"] = "greenfield"
    elif any(kw in text_lower for kw in ["评估", "审查", "重构", "改进", "现有"]):
        result["current_state"] = "existing"

    # 检测关键词
    goal_match = re.search(r"(?:目标|目的|要做|构建|开发)[：:]\s*(.+?)(?:[。.；;]|$)", text)
    if goal_match:
        result["business_goal"] = goal_match.group(1).strip()

    # 检测是否包含足够信息
    word_count = len(text.split())
    if word_count > 50:
        result["_sufficient_context"] = True

    return result


def check_context(context):
    """
    检查上下文完整性。
    返回: (pass: bool, report: dict)
    """
    missing_required = []
    questions = []
    assumptions = []

    # 检查必填项
    for key, field in REQUIRED_FIELDS.items():
        value = context.get(key)
        if not value:
            missing_required.append(field["label"])
            questions.append(field["question"])
        elif isinstance(value, str) and len(value.strip()) < 5:
            missing_required.append(f"{field['label']}（信息不足）")
            questions.append(f"关于{field['label']}，能否提供更多细节？{field['hint']}")

    # 检查选填项（缺失不阻塞，但记录默认假设）
    for key, field in OPTIONAL_FIELDS.items():
        value = context.get(key)
        if not value:
            questions.append(field["question"])
            if "default_assumption" in field:
                assumptions.append(field["default_assumption"])

    passed = len(missing_required) == 0

    return passed, {
        "pass": passed,
        "scenario": _detect_scenario(context),
        "missing_required": missing_required,
        "questions": questions,
        "assumptions": assumptions,
        "summary": (
            "上下文检查通过，可以继续"
            if passed
            else f"缺少 {len(missing_required)} 项必填信息，请补充后再继续"
        ),
    }


def _detect_scenario(context):
    """检测用户所处场景"""
    state = context.get("current_state", "")
    text = json.dumps(context, ensure_ascii=False)

    if "greenfield" in str(state) or "从零" in text or "设计" in text:
        return "design-initiator"
    elif "existing" in str(state) or "评估" in text or "审查" in text:
        return "architecture-evaluator"
    else:
        return "ambiguous"


def main():
    context_source = sys.argv[1] if len(sys.argv) > 1 else ""
    context = parse_context(context_source)
    passed, report = check_context(context)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
