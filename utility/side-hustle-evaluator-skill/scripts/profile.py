#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户画像管理脚本 (User Profile Manager)

管理副业评估的第一步「自我评估」产出的用户画像文件。
画像文件为一次性创建、可复用、可增量更新的持久化 JSON 文件。

支持的操作：
  1. create  — 首次创建画像（从对话收集的信息生成）
  2. load    — 加载已有画像（供后续评估直接复用）
  3. update  — 增量更新画像（仅更新指定的字段，保留其余不变）
  4. validate — 校验画像完整性（检查必填字段，返回缺失项和建议）

画像文件默认保存路径: /workspace/side-hustle-evaluator/user-profile.json

用法:
  # 创建画像
  python profile.py create --json '{
    "name": "张三",
    "daily_hours": 2.0,
    "time_quality": "整块",
    "sustainability": "长期",
    "hard_skills": ["Python编程", "数据分析", "英语翻译"],
    "soft_skills": ["沟通表达", "项目管理"],
    "interests": ["科技", "教育", "写作"],
    "resources": ["笔记本电脑", "稳定的网络", "启动资金5000元"],
    "family_support": "已沟通",
    "main_job": "数据分析师",
    "main_job_monthly_salary": 15000,
    "main_job_monthly_hours": 160
  }'

  # 加载画像
  python profile.py load

  # 更新画像（仅更新指定字段）
  python profile.py update --json '{"daily_hours": 3.0, "hard_skills": ["Python编程", "数据分析", "英语翻译", "视频剪辑"]}'

  # 校验画像
  python profile.py validate

输出: JSON 格式的操作结果
"""

import json
import sys
import os
import argparse
from datetime import datetime
from copy import deepcopy

# 默认画像文件路径
DEFAULT_PROFILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "user-profile.json"
)

# 画像 schema 定义
PROFILE_SCHEMA = {
    "version": "1.0",
    "fields": {
        # ===== 必填字段（核心信息）=====
        "name": {
            "type": str,
            "required": True,
            "description": "用户姓名/昵称",
            "example": "张三",
        },
        "daily_hours": {
            "type": (int, float),
            "required": True,
            "description": "每日可投入副业的小时数",
            "example": 2.0,
        },
        "time_quality": {
            "type": str,
            "required": True,
            "description": "时间质量：整块 / 碎片化 / 混合",
            "enum": ["整块", "碎片化", "混合"],
            "example": "整块",
        },
        "sustainability": {
            "type": str,
            "required": True,
            "description": "可持续投入时长：短期(1-3月) / 中期(3-6月) / 长期(6月+)",
            "enum": ["短期", "中期", "长期"],
            "example": "长期",
        },
        "hard_skills": {
            "type": list,
            "required": True,
            "description": "硬技能列表",
            "example": ["Python编程", "数据分析"],
        },
        "soft_skills": {
            "type": list,
            "required": True,
            "description": "软技能列表",
            "example": ["沟通表达", "项目管理"],
        },
        "interests": {
            "type": list,
            "required": True,
            "description": "兴趣领域列表",
            "example": ["科技", "教育"],
        },
        "resources": {
            "type": list,
            "required": True,
            "description": "可用资源列表",
            "example": ["笔记本电脑", "启动资金5000元"],
        },
        "family_support": {
            "type": str,
            "required": True,
            "description": "家庭支持情况：已沟通 / 待沟通 / 不支持",
            "enum": ["已沟通", "待沟通", "不支持"],
            "example": "已沟通",
        },
        # ===== 选填字段（补充信息）=====
        "main_job": {
            "type": str,
            "required": False,
            "description": "主业/职业",
            "example": "数据分析师",
        },
        "main_job_monthly_salary": {
            "type": (int, float),
            "required": False,
            "description": "主业月薪资（元）",
            "example": 15000,
        },
        "main_job_monthly_hours": {
            "type": (int, float),
            "required": False,
            "description": "主业月工作小时数",
            "example": 160,
        },
        "risk_tolerance": {
            "type": str,
            "required": False,
            "description": "风险偏好：保守 / 稳健 / 激进",
            "enum": ["保守", "稳健", "激进"],
            "example": "稳健",
        },
        "notes": {
            "type": str,
            "required": False,
            "description": "其他备注",
            "example": "希望副业能与主业技能互补",
        },
    },
}


def _load_existing(path: str) -> dict:
    """加载已有画像文件"""
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_profile(path: str, data: dict) -> None:
    """保存画像文件"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_profile(data: dict, path: str = DEFAULT_PROFILE_PATH) -> dict:
    """
    创建用户画像

    输入: 用户提供的个人信息字典
    输出: 创建结果（含画像内容、校验状态、建议）
    """
    # 检查是否已存在
    existing = _load_existing(path)
    if existing:
        return {
            "status": "error",
            "message": f"画像文件已存在: {path}。如需修改请使用 update 操作。",
            "existing_profile_created_at": existing.get("created_at"),
            "hint": "使用 'python profile.py update --json ...' 来更新画像",
        }

    # 构建画像
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    profile = {
        "created_at": now,
        "updated_at": now,
        "version": PROFILE_SCHEMA["version"],
        "data": {},
    }

    # 填充数据
    for key, value in data.items():
        if key in PROFILE_SCHEMA["fields"]:
            profile["data"][key] = value

    # 校验
    validation = validate_profile_data(profile["data"])

    # 生成建议
    suggestions = _generate_suggestions(profile["data"])

    # 保存
    _save_profile(path, profile)

    return {
        "status": "created",
        "message": "用户画像创建成功",
        "file_path": path,
        "validation": validation,
        "suggestions": suggestions,
        "profile": profile["data"],
    }


def load_profile(path: str = DEFAULT_PROFILE_PATH) -> dict:
    """
    加载用户画像

    输出: 画像内容、校验状态、距上次更新的时间
    """
    profile = _load_existing(path)
    if not profile:
        return {
            "status": "not_found",
            "message": "未找到画像文件。请先使用 create 操作创建画像。",
            "hint": "使用 'python profile.py create --json ...' 来创建画像",
        }

    # 校验
    validation = validate_profile_data(profile.get("data", {}))

    # 计算距上次更新的时间
    updated_at = profile.get("updated_at", "")
    created_at = profile.get("created_at", "")

    return {
        "status": "loaded",
        "message": "用户画像加载成功",
        "file_path": path,
        "created_at": created_at,
        "updated_at": updated_at,
        "validation": validation,
        "profile": profile.get("data", {}),
    }


def update_profile(data: dict, path: str = DEFAULT_PROFILE_PATH) -> dict:
    """
    增量更新用户画像（仅更新指定字段，保留其余不变）

    输入: 需要更新的字段字典
    输出: 更新结果（含变更摘要）
    """
    profile = _load_existing(path)
    if not profile:
        return {
            "status": "not_found",
            "message": "未找到画像文件。请先使用 create 操作创建画像。",
            "hint": "使用 'python profile.py create --json ...' 来创建画像",
        }

    # 记录变更
    changes = {}
    old_data = deepcopy(profile["data"])

    # 更新指定字段
    for key, value in data.items():
        if key in PROFILE_SCHEMA["fields"]:
            old_value = profile["data"].get(key)
            profile["data"][key] = value
            if old_value != value:
                changes[key] = {"old": old_value, "new": value}

    # 更新时间戳
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    profile["updated_at"] = now

    # 校验
    validation = validate_profile_data(profile["data"])

    # 保存
    _save_profile(path, profile)

    # 生成建议
    suggestions = _generate_suggestions(profile["data"])

    return {
        "status": "updated",
        "message": f"用户画像更新成功，共变更 {len(changes)} 个字段",
        "file_path": path,
        "updated_at": now,
        "changes": changes,
        "validation": validation,
        "suggestions": suggestions,
        "profile": profile["data"],
    }


def validate_profile_data(data: dict) -> dict:
    """
    校验画像数据完整性

    输出: 校验结果（含缺失字段、类型错误、枚举值错误）
    """
    result = {
        "is_complete": True,
        "missing_required": [],
        "type_errors": [],
        "enum_errors": [],
        "warnings": [],
    }

    for field_name, field_def in PROFILE_SCHEMA["fields"].items():
        value = data.get(field_name)

        # 必填检查
        if field_def["required"] and (value is None or value == "" or value == []):
            result["missing_required"].append({
                "field": field_name,
                "description": field_def["description"],
            })
            result["is_complete"] = False
            continue

        # 跳过空的可选字段
        if value is None:
            continue

        # 类型检查
        expected_type = field_def["type"]
        if expected_type == list:
            if not isinstance(value, list):
                result["type_errors"].append({
                    "field": field_name,
                    "expected": "list",
                    "got": type(value).__name__,
                })
        elif isinstance(expected_type, tuple):
            if not isinstance(value, expected_type):
                result["type_errors"].append({
                    "field": field_name,
                    "expected": "或".join(t.__name__ for t in expected_type),
                    "got": type(value).__name__,
                })
        elif not isinstance(value, expected_type):
            result["type_errors"].append({
                "field": field_name,
                "expected": expected_type.__name__,
                "got": type(value).__name__,
            })

        # 枚举值检查
        if "enum" in field_def and isinstance(value, str):
            if value not in field_def["enum"]:
                result["enum_errors"].append({
                    "field": field_name,
                    "allowed": field_def["enum"],
                    "got": value,
                })

    # 生成警告
    if data.get("daily_hours", 0) < 1:
        result["warnings"].append("每日可用时间不足1小时，建议避免需要重度运营或及时沟通的项目")
    if data.get("family_support") == "不支持":
        result["warnings"].append("家庭不支持做副业，建议先沟通达成共识再开始")
    if data.get("sustainability") == "短期" and data.get("daily_hours", 0) < 2:
        result["warnings"].append("短期投入且时间有限，建议优先选择低启动成本项目")

    return result


def validate_profile(path: str = DEFAULT_PROFILE_PATH) -> dict:
    """校验已有画像文件"""
    profile = _load_existing(path)
    if not profile:
        return {
            "status": "not_found",
            "message": "未找到画像文件。",
        }

    validation = validate_profile_data(profile.get("data", {}))

    return {
        "status": "validated",
        "file_path": path,
        "created_at": profile.get("created_at"),
        "updated_at": profile.get("updated_at"),
        "validation": validation,
    }


def _generate_suggestions(data: dict) -> list:
    """
    基于画像数据生成副业方向建议

    输出: 建议列表（适合的方向 + 应避免的方向）
    """
    suggestions = []
    skills = data.get("hard_skills", []) + data.get("soft_skills", [])
    interests = data.get("interests", [])
    daily_hours = data.get("daily_hours", 0)
    time_quality = data.get("time_quality", "")
    resources_str = " ".join(data.get("resources", []))

    # 技能匹配建议
    skill_directions = {
        "编程": ["程序员接单", "自动化工具开发", "技术写作"],
        "设计": ["自由设计", "UI/UX外包", "平面设计"],
        "写作": ["内容创作", "文案撰写", "自媒体运营"],
        "翻译": ["翻译兼职", "本地化服务"],
        "数据分析": ["数据咨询", "报告代写", "在线教学"],
        "摄影": ["摄影约拍", "图片素材销售"],
        "视频剪辑": ["短视频制作", "视频剪辑接单"],
        "英语": ["英语辅导", "翻译", "跨境电商"],
        "管理": ["项目管理咨询", "企业培训"],
        "沟通": ["销售代理", "客户服务外包", "社群运营"],
    }

    matched_directions = set()
    for skill in skills:
        for keyword, directions in skill_directions.items():
            if keyword.lower() in skill.lower():
                matched_directions.update(directions)

    if matched_directions:
        suggestions.append({
            "type": "recommended",
            "title": "基于技能推荐的副业方向",
            "items": list(matched_directions)[:5],
        })

    # 时间匹配建议
    if daily_hours < 1:
        suggestions.append({
            "type": "recommended",
            "title": "适合碎片化时间的方向",
            "items": ["微写作", "问卷调查", "知识付费小课"],
        })
    elif daily_hours >= 2 and time_quality == "整块":
        suggestions.append({
            "type": "recommended",
            "title": "适合整块时间的方向",
            "items": ["深度内容创作", "编程接单", "在线课程开发"],
        })

    # 资金相关建议
    if "启动资金" in resources_str or "资金" in resources_str:
        try:
            # 尝试提取资金数额
            import re
            amount_match = re.search(r'(\d+)', resources_str)
            if amount_match:
                amount = int(amount_match.group(1))
                if amount < 2000:
                    suggestions.append({
                        "type": "recommended",
                        "title": "适合低预算的方向",
                        "items": ["自媒体运营", "写作/文案", "技能教学"],
                    })
                elif amount >= 5000:
                    suggestions.append({
                        "type": "recommended",
                        "title": "预算充足，可考虑的方向",
                        "items": ["电商创业", "知识付费课程", "工作室"],
                    })
        except (ValueError, AttributeError):
            pass

    # 应避免的方向
    avoid = []
    if daily_hours < 1:
        avoid.append("需要实时在线客服/直播类项目")
    if "不支持" in data.get("family_support", ""):
        avoid.append("需要大量晚间或周末投入的项目（建议先解决家庭沟通）")
    if not any(kw in " ".join(skills) for kw in ["编程", "设计", "写作", "翻译", "摄影", "视频"]):
        avoid.append("高技能门槛方向（建议先投资学习一项硬技能）")

    if avoid:
        suggestions.append({
            "type": "avoid",
            "title": "建议避免的方向",
            "items": avoid,
        })

    return suggestions


def main():
    parser = argparse.ArgumentParser(description="用户画像管理工具")
    subparsers = parser.add_subparsers(dest="action", help="操作类型")

    # create
    create_parser = subparsers.add_parser("create", help="创建用户画像")
    create_parser.add_argument("--json", "-j", type=str, required=True, help="JSON格式的用户信息")
    create_parser.add_argument("--path", "-p", type=str, default=DEFAULT_PROFILE_PATH, help="画像文件路径")

    # load
    load_parser = subparsers.add_parser("load", help="加载用户画像")
    load_parser.add_argument("--path", "-p", type=str, default=DEFAULT_PROFILE_PATH, help="画像文件路径")

    # update
    update_parser = subparsers.add_parser("update", help="更新用户画像")
    update_parser.add_argument("--json", "-j", type=str, required=True, help="JSON格式的更新数据")
    update_parser.add_argument("--path", "-p", type=str, default=DEFAULT_PROFILE_PATH, help="画像文件路径")

    # validate
    validate_parser = subparsers.add_parser("validate", help="校验用户画像")
    validate_parser.add_argument("--path", "-p", type=str, default=DEFAULT_PROFILE_PATH, help="画像文件路径")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    try:
        if args.action == "create":
            data = json.loads(args.json)
            result = create_profile(data, args.path)
        elif args.action == "load":
            result = load_profile(args.path)
        elif args.action == "update":
            data = json.loads(args.json)
            result = update_profile(data, args.path)
        elif args.action == "validate":
            result = validate_profile(args.path)
        else:
            result = {"error": f"未知操作: {args.action}"}

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON解析失败: {str(e)}"}, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"操作失败: {str(e)}"}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
