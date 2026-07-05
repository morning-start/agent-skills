#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
副业价值评估计算脚本 (Side Hustle Value Calculator)

本脚本实现副业评估第三步「价值核算」中的三笔关键账的精确计算：
1. 时间账 - 副业时薪计算与对比
2. 金钱账 - 投入产出比与回本周期
3. 机会账 - 机会成本评估

用法:
    python evaluate.py --json '{
        "side_hustle_name": "自媒体运营",
        "monthly_gross_income": 3000,
        "monthly_hours": 60,
        "main_job_monthly_salary": 15000,
        "main_job_monthly_hours": 160,
        "startup_cost": 2000,
        "monthly_operating_cost": 500,
        "alternative_hourly_value": 100,
        "alternative_skill_value": "学习视频剪辑，预计3个月后可接单，时薪150+"
    }'

输出: JSON 格式的完整评估报告
"""

import json
import sys
import argparse
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class TimeAccount:
    """时间账：副业时薪计算与对比"""
    side_hustle_hourly_rate: float = 0.0          # 副业时薪
    main_job_hourly_rate: float = 0.0              # 主业时薪
    hourly_ratio: float = 0.0                      # 副业时薪 / 主业时薪
    time_verdict: str = ""                          # 时间账结论
    time_score: int = 0                             # 时间账评分 (0-10)
    time_analysis: str = ""                         # 详细分析文本


@dataclass
class MoneyAccount:
    """金钱账：投入产出比与回本周期"""
    monthly_net_income: float = 0.0                 # 月净收入
    total_monthly_cost: float = 0.0                 # 月总成本（运营）
    roi_percentage: float = 0.0                     # 月投资回报率
    payback_months: float = 0.0                     # 回本周期（月）
    annual_net_profit: float = 0.0                  # 年净利润
    money_verdict: str = ""                          # 金钱账结论
    money_score: int = 0                             # 金钱账评分 (0-10)
    money_analysis: str = ""                         # 详细分析文本


@dataclass
class OpportunityAccount:
    """机会账：机会成本评估"""
    monthly_opportunity_cost: float = 0.0           # 月机会成本（金钱）
    monthly_opportunity_cost_hours: float = 0.0     # 月机会成本（小时）
    net_gain_vs_alternative: float = 0.0            # 相比替代方案的净收益差
    opportunity_verdict: str = ""                    # 机会账结论
    opportunity_score: int = 0                       # 机会账评分 (0-10)
    opportunity_analysis: str = ""                   # 详细分析文本


@dataclass
class OverallAssessment:
    """综合评估"""
    total_score: int = 0                             # 总分 (0-30)
    recommendation: str = ""                          # 建议
    risk_level: str = ""                              # 风险等级
    key_insights: list = field(default_factory=list)  # 关键洞察


@dataclass
class EvaluationResult:
    """完整评估结果"""
    side_hustle_name: str = ""
    time_account: TimeAccount = field(default_factory=TimeAccount)
    money_account: MoneyAccount = field(default_factory=MoneyAccount)
    opportunity_account: OpportunityAccount = field(default_factory=OpportunityAccount)
    overall: OverallAssessment = field(default_factory=OverallAssessment)


def calculate_time_account(
    monthly_gross_income: float,
    monthly_hours: float,
    main_job_monthly_salary: float,
    main_job_monthly_hours: float,
) -> TimeAccount:
    """
    计算时间账
    公式: 副业时薪 = 副业月总收入 / 月投入小时数
    """
    result = TimeAccount()

    # 副业时薪
    if monthly_hours > 0:
        result.side_hustle_hourly_rate = round(monthly_gross_income / monthly_hours, 2)
    else:
        result.side_hustle_hourly_rate = 0.0
        result.time_analysis = "错误：月投入小时数不能为0"
        result.time_verdict = "数据不足"
        return result

    # 主业时薪
    if main_job_monthly_hours > 0:
        result.main_job_hourly_rate = round(main_job_monthly_salary / main_job_monthly_hours, 2)
    else:
        result.main_job_hourly_rate = 0.0

    # 时薪比率
    if result.main_job_hourly_rate > 0:
        result.hourly_ratio = round(result.side_hustle_hourly_rate / result.main_job_hourly_rate, 2)
    else:
        result.hourly_ratio = float('inf') if result.side_hustle_hourly_rate > 0 else 0.0

    # 评分与结论
    ratio = result.hourly_ratio
    if ratio == float('inf'):
        result.time_score = 8
        result.time_verdict = "主业无参照，需结合绝对值判断"
        result.time_analysis = (
            f"副业时薪为 ¥{result.side_hustle_hourly_rate}/小时。"
            f"由于无法获取主业时薪进行对比，建议将副业时薪与当地平均时薪进行横向比较。"
        )
    elif ratio >= 0.8:
        result.time_score = 9
        result.time_verdict = "优秀 — 副业时薪接近或超过主业"
        result.time_analysis = (
            f"副业时薪 ¥{result.side_hustle_hourly_rate}/小时，"
            f"达到主业时薪的 {ratio*100:.0f}%。"
            f"从时间价值角度看，这份副业非常值得投入。"
        )
    elif ratio >= 0.5:
        result.time_score = 7
        result.time_verdict = "良好 — 副业时薪达到主业一半以上"
        result.time_analysis = (
            f"副业时薪 ¥{result.side_hustle_hourly_rate}/小时，"
            f"为主业时薪的 {ratio*100:.0f}%。"
            f"如果该副业能带来技能提升或长期复利，仍然值得考虑。"
        )
    elif ratio >= 0.3:
        result.time_score = 5
        result.time_verdict = "一般 — 副业时薪偏低"
        result.time_analysis = (
            f"副业时薪 ¥{result.side_hustle_hourly_rate}/小时，"
            f"仅为主业时薪的 {ratio*100:.0f}%。"
            f"除非有明确的学习价值或长期增长空间，否则从纯经济角度不太划算。"
        )
    else:
        result.time_score = 2
        result.time_verdict = "较差 — 副业时薪远低于主业"
        result.time_analysis = (
            f"副业时薪仅 ¥{result.side_hustle_hourly_rate}/小时，"
            f"不到主业时薪的 {ratio*100:.0f}%。"
            f"强烈建议重新评估，考虑是否有更高价值的时间利用方式。"
        )

    return result


def calculate_money_account(
    monthly_gross_income: float,
    monthly_hours: float,
    startup_cost: float,
    monthly_operating_cost: float,
) -> MoneyAccount:
    """
    计算金钱账
    月净收入 = 月总收入 - 月运营成本
    月ROI = 月净收入 / 月总成本 × 100%
    回本周期 = 启动成本 / 月净收入
    """
    result = MoneyAccount()

    # 月净收入
    result.monthly_net_income = round(monthly_gross_income - monthly_operating_cost, 2)

    # 月总运营成本
    result.total_monthly_cost = round(monthly_operating_cost, 2)

    # 月投资回报率
    if monthly_operating_cost > 0:
        result.roi_percentage = round(
            (result.monthly_net_income / monthly_operating_cost) * 100, 1
        )
    else:
        result.roi_percentage = float('inf') if result.monthly_net_income > 0 else 0.0

    # 回本周期
    if result.monthly_net_income > 0:
        result.payback_months = round(startup_cost / result.monthly_net_income, 1)
    else:
        result.payback_months = float('inf')

    # 年净利润
    result.annual_net_profit = round(result.monthly_net_income * 12 - startup_cost, 2)

    # 评分与结论
    if result.monthly_net_income <= 0:
        result.money_score = 1
        result.money_verdict = "亏损 — 月净收入为负"
        result.money_analysis = (
            f"月总收入 ¥{monthly_gross_income}，月运营成本 ¥{monthly_operating_cost}，"
            f"月净亏损 ¥{abs(result.monthly_net_income)}。"
            f"加上启动成本 ¥{startup_cost}，这份副业目前处于亏损状态，不建议继续投入。"
        )
    elif result.payback_months <= 2:
        result.money_score = 9
        result.money_verdict = "优秀 — 回本周期极短"
        result.money_analysis = (
            f"月净收入 ¥{result.monthly_net_income}，启动成本 ¥{startup_cost}，"
            f"仅需 {result.payback_months} 个月即可回本。"
            f"年净利润预估 ¥{result.annual_net_profit}，投资回报率 {result.roi_percentage}%。"
            f"从财务角度看非常值得投入。"
        )
    elif result.payback_months <= 6:
        result.money_score = 7
        result.money_verdict = "良好 — 回本周期合理"
        result.money_analysis = (
            f"月净收入 ¥{result.monthly_net_income}，启动成本 ¥{startup_cost}，"
            f"预计 {result.payback_months} 个月回本。"
            f"年净利润预估 ¥{result.annual_net_profit}，投资回报率 {result.roi_percentage}%。"
            f"属于可接受的投资周期。"
        )
    elif result.payback_months <= 12:
        result.money_score = 5
        result.money_verdict = "一般 — 回本周期较长"
        result.money_analysis = (
            f"月净收入 ¥{result.monthly_net_income}，启动成本 ¥{startup_cost}，"
            f"需要 {result.payback_months} 个月才能回本。"
            f"年净利润预估 ¥{result.annual_net_profit}。"
            f"建议评估是否有缩短回本周期的方法，或考虑降低启动成本。"
        )
    else:
        result.money_score = 3
        result.money_verdict = "较差 — 回本周期过长"
        result.money_analysis = (
            f"月净收入 ¥{result.monthly_net_income}，启动成本 ¥{startup_cost}，"
            f"回本需要 {result.payback_months} 个月以上。"
            f"资金效率较低，建议谨慎考虑。"
        )

    return result


def calculate_opportunity_account(
    monthly_gross_income: float,
    monthly_hours: float,
    monthly_operating_cost: float,
    alternative_hourly_value: float,
    alternative_skill_value: str = "",
) -> OpportunityAccount:
    """
    计算机会账
    月机会成本 = 替代方案时薪 × 副业月投入小时数
    净收益差 = 副业月净收入 - 月机会成本
    """
    result = OpportunityAccount()

    # 月机会成本
    result.monthly_opportunity_cost = round(alternative_hourly_value * monthly_hours, 2)
    result.monthly_opportunity_cost_hours = monthly_hours

    # 副业月净收入
    side_hustle_net = monthly_gross_income - monthly_operating_cost

    # 净收益差
    result.net_gain_vs_alternative = round(side_hustle_net - result.monthly_opportunity_cost, 2)

    # 评分与结论
    if result.net_gain_vs_alternative > 0:
        result.opportunity_score = 8
        result.opportunity_verdict = "正收益 — 副业收益超过机会成本"
        result.opportunity_analysis = (
            f"将同样的 {monthly_hours} 小时用于替代方案（时薪 ¥{alternative_hourly_value}），"
            f"可获得 ¥{result.monthly_opportunity_cost}/月。"
            f"而当前副业月净收入为 ¥{side_hustle_net}，"
            f"净收益差为 +¥{result.net_gain_vs_alternative}。"
            f"从机会成本角度看，这份副业是划算的。"
        )
    elif result.net_gain_vs_alternative > -500:
        result.opportunity_score = 5
        result.opportunity_verdict = "基本持平 — 副业收益接近机会成本"
        result.opportunity_analysis = (
            f"替代方案可获 ¥{result.monthly_opportunity_cost}/月，"
            f"当前副业月净收入 ¥{side_hustle_net}，"
            f"净收益差为 ¥{result.net_gain_vs_alternative}。"
            f"经济上基本持平，需考虑副业是否带来技能提升、人脉拓展等隐性价值。"
        )
    else:
        result.opportunity_score = 3
        result.opportunity_verdict = "负收益 — 机会成本高于副业收益"
        result.opportunity_analysis = (
            f"替代方案可获 ¥{result.monthly_opportunity_cost}/月，"
            f"而当前副业月净收入仅 ¥{side_hustle_net}，"
            f"每月「亏」了 ¥{abs(result.net_gain_vs_alternative)}。"
            f"除非副业有显著的长期成长性，否则建议考虑替代方案。"
        )

    # 附加技能价值提示
    if alternative_skill_value:
        result.opportunity_analysis += (
            f"\n\n替代方案附加价值：{alternative_skill_value}。"
            f"请综合权衡短期收入与长期成长。"
        )

    return result


def generate_overall_assessment(
    time_account: TimeAccount,
    money_account: MoneyAccount,
    opportunity_account: OpportunityAccount,
) -> OverallAssessment:
    """生成综合评估"""
    result = OverallAssessment()

    # 总分 (0-30)
    result.total_score = time_account.time_score + money_account.money_score + opportunity_account.opportunity_score

    # 风险等级
    if result.total_score >= 24:
        result.risk_level = "低风险"
    elif result.total_score >= 18:
        result.risk_level = "中低风险"
    elif result.total_score >= 12:
        result.risk_level = "中风险"
    elif result.total_score >= 6:
        result.risk_level = "中高风险"
    else:
        result.risk_level = "高风险"

    # 关键洞察
    insights = []
    if time_account.hourly_ratio != float('inf') and time_account.hourly_ratio < 0.5:
        insights.append(f"⚠️ 副业时薪仅为主业的 {time_account.hourly_ratio*100:.0f}%，时间价值偏低")
    if money_account.payback_months > 6 and money_account.payback_months != float('inf'):
        insights.append(f"⚠️ 回本周期需 {money_account.payback_months} 个月，资金效率较低")
    if money_account.monthly_net_income <= 0:
        insights.append("🚨 月净收入为负，当前处于亏损状态")
    if opportunity_account.net_gain_vs_alternative < -500:
        insights.append(f"⚠️ 机会成本较高，每月「亏」了 ¥{abs(opportunity_account.net_gain_vs_alternative)}")
    if time_account.hourly_ratio >= 0.8:
        insights.append(f"✅ 副业时薪达到主业 {time_account.hourly_ratio*100:.0f}%，时间价值优秀")
    if money_account.payback_months <= 3 and money_account.payback_months != float('inf'):
        insights.append(f"✅ 回本周期仅 {money_account.payback_months} 个月，资金效率高")
    if opportunity_account.net_gain_vs_alternative > 0:
        insights.append(f"✅ 净收益差为正 (+¥{opportunity_account.net_gain_vs_alternative}/月)，优于替代方案")

    if not insights:
        insights.append("各项指标处于中等水平，建议结合SWOT分析做最终判断")

    result.key_insights = insights

    # 综合建议
    if result.total_score >= 24:
        result.recommendation = (
            "强烈推荐投入。各项指标表现优秀，副业时薪有竞争力、"
            "投入产出比合理、机会成本可控。建议全力推进，同时注意风险监控。"
        )
    elif result.total_score >= 18:
        result.recommendation = (
            "推荐投入，但需关注短板。整体表现良好，"
            "建议针对评分较低的维度进行优化（如提升效率、降低成本等）。"
        )
    elif result.total_score >= 12:
        result.recommendation = (
            "可以尝试，但需谨慎。部分指标不够理想，"
            "建议先小规模试水（1-3个月），验证数据后再决定是否加大投入。"
        )
    elif result.total_score >= 6:
        result.recommendation = (
            "不建议投入。多项指标表现不佳，"
            "建议重新评估方向，或寻找替代方案。"
        )
    else:
        result.recommendation = (
            "强烈不建议投入。综合评分很低，"
            "这份副业在当前条件下风险远大于收益，请考虑其他方向。"
        )

    return result


def evaluate(data: dict) -> dict:
    """
    主评估函数
    输入: 包含评估参数的字典
    输出: 完整评估结果的字典
    """
    # 提取参数
    name = data.get("side_hustle_name", "未命名副业")
    monthly_gross_income = float(data.get("monthly_gross_income", 0))
    monthly_hours = float(data.get("monthly_hours", 0))
    main_job_monthly_salary = float(data.get("main_job_monthly_salary", 0))
    main_job_monthly_hours = float(data.get("main_job_monthly_hours", 0))
    startup_cost = float(data.get("startup_cost", 0))
    monthly_operating_cost = float(data.get("monthly_operating_cost", 0))
    alternative_hourly_value = float(data.get("alternative_hourly_value", 0))
    alternative_skill_value = str(data.get("alternative_skill_value", ""))

    # 计算三笔账
    time_account = calculate_time_account(
        monthly_gross_income, monthly_hours,
        main_job_monthly_salary, main_job_monthly_hours,
    )
    money_account = calculate_money_account(
        monthly_gross_income, monthly_hours,
        startup_cost, monthly_operating_cost,
    )
    opportunity_account = calculate_opportunity_account(
        monthly_gross_income, monthly_hours,
        monthly_operating_cost,
        alternative_hourly_value, alternative_skill_value,
    )

    # 综合评估
    overall = generate_overall_assessment(time_account, money_account, opportunity_account)

    # 组装结果
    result = EvaluationResult(
        side_hustle_name=name,
        time_account=time_account,
        money_account=money_account,
        opportunity_account=opportunity_account,
        overall=overall,
    )

    # 转换为字典，处理 inf 值
    def sanitize(obj):
        if isinstance(obj, float) and obj == float('inf'):
            return "∞"
        elif isinstance(obj, float) and obj == float('-inf'):
            return "-∞"
        elif isinstance(obj, dict):
            return {k: sanitize(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [sanitize(i) for i in obj]
        return obj

    return sanitize(asdict(result))


def main():
    parser = argparse.ArgumentParser(description="副业价值评估计算工具")
    parser.add_argument(
        "--json", "-j",
        type=str,
        required=True,
        help="JSON格式的评估参数",
    )
    args = parser.parse_args()

    try:
        data = json.loads(args.json)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON解析失败: {str(e)}"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    try:
        result = evaluate(data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": f"计算失败: {str(e)}"}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
