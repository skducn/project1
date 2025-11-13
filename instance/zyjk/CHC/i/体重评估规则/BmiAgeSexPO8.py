import re
from typing import List, Dict, Tuple


def parse_age_expression(exprs: List[str]) -> Tuple[List[int], List[int]]:
    """
    解析所有年龄表达式，返回满足条件的有效值（必要数量）和不满足的无效值（边界值）
    - 等于条件（年龄=X）：1个有效值（X），1个无效值（X±1选其一）
    - 范围条件（如66<=年龄<69）：2个有效值（起始+中间），2个无效值（上下边界外）
    - 其他单条件（>、>=、<、<=）：2个有效值，2个无效值
    输出年龄均为整数
    """
    # 合并所有年龄约束
    constraints = []
    for expr in exprs:
        expr = expr.strip()
        # 处理 "年龄=X" 格式
        eq_match = re.match(r'年龄=(\d+)', expr)
        if eq_match:
            x = int(eq_match.group(1))
            constraints.append(('eq', x))
            continue
        # 处理 "X<=年龄<Y" 格式
        range_match = re.match(r'(\d+)<=年龄<(\d+)', expr)
        if range_match:
            x = int(range_match.group(1))
            y = int(range_match.group(2))
            constraints.append(('ge', x))
            constraints.append(('lt', y))
            continue
        # 处理 "年龄>X" 格式
        gt_match = re.match(r'年龄>(\d+)', expr)
        if gt_match:
            x = int(gt_match.group(1))
            constraints.append(('gt', x))
            continue
        # 处理 "年龄>=X" 格式
        ge_match = re.match(r'年龄>=(\d+)', expr)
        if ge_match:
            x = int(ge_match.group(1))
            constraints.append(('ge', x))
            continue
        # 处理 "年龄<X" 格式
        lt_match = re.match(r'年龄<(\d+)', expr)
        if lt_match:
            x = int(lt_match.group(1))
            constraints.append(('lt', x))
            continue
        # 处理 "年龄<=X" 格式
        le_match = re.match(r'年龄<=(\d+)', expr)
        if le_match:
            x = int(le_match.group(1))
            constraints.append(('le', x))
            continue
        raise ValueError(f"不支持的年龄表达式格式：{expr}")

    # 计算所有满足约束的年龄（0-120岁合理范围）
    all_satisfied = []
    for age in range(0, 121):
        valid = True
        for op, val in constraints:
            if op == 'eq' and age != val:
                valid = False
            elif op == 'gt' and age <= val:
                valid = False
            elif op == 'ge' and age < val:
                valid = False
            elif op == 'lt' and age >= val:
                valid = False
            elif op == 'le' and age > val:
                valid = False
        if valid:
            all_satisfied.append(age)

    if not all_satisfied:
        raise ValueError("年龄表达式无有效取值")

    # 筛选必要的有效值（按需求控制数量）
    satisfied = []
    # 判断是否为纯等于条件（仅一个约束且为eq）
    is_eq_only = len(constraints) == 1 and constraints[0][0] == 'eq'
    if is_eq_only:
        # 等于条件：仅1个有效值
        satisfied = [all_satisfied[0]]
    else:
        # 范围/多条件：取2个（起始+中间，确保不重复）
        if len(all_satisfied) >= 2:
            satisfied = [all_satisfied[0], all_satisfied[min(1, len(all_satisfied) - 1)]]
        else:
            satisfied = all_satisfied  # 极端情况（如仅1个有效值）

    # 生成无效值（仅关键边界值，确保不重复且在合理范围）
    not_satisfied = []
    # 收集所有约束的边界点
    boundaries = set()
    for op, val in constraints:
        if op == 'eq':
            boundaries.add(val - 1)  # 小于目标值的边界
            boundaries.add(val + 1)  # 大于目标值的边界
        elif op == 'gt':
            boundaries.add(val)  # 等于目标值（不满足>）
            boundaries.add(val - 1)  # 小于目标值
        elif op == 'ge':
            boundaries.add(val - 1)  # 小于目标值（不满足>=）
        elif op == 'lt':
            boundaries.add(val)  # 等于目标值（不满足<）
            boundaries.add(val + 1)  # 大于目标值
        elif op == 'le':
            boundaries.add(val + 1)  # 大于目标值（不满足<=）

    # 筛选有效边界值（0-120之间，且不在satisfied中）
    for b in sorted(boundaries):
        if 0 <= b <= 120 and b not in satisfied and b not in all_satisfied:
            not_satisfied.append(b)
            if len(not_satisfied) >= 2:
                break  # 最多2个无效值，满足需求

    # 确保无效值至少1个（等于条件）或2个（其他条件）
    required_invalid_count = 1 if is_eq_only else 2
    while len(not_satisfied) < required_invalid_count:
        # 补充相邻的无效值
        for i in range(0, 121):
            if i not in all_satisfied and i not in not_satisfied:
                not_satisfied.append(i)
                break

    return satisfied, not_satisfied


def parse_bmi_expression(exprs: List[str]) -> Tuple[List[float], List[float]]:
    """
    解析所有BMI表达式，返回满足条件的有效值（2个）和不满足的无效值（2个）
    支持=、>、>=、<、<=运算符，保留1位小数
    """
    constraints = []
    for expr in exprs:
        expr = expr.strip()
        # 修复正则表达式，正确匹配 >=, <= 等运算符
        bmi_match = re.match(r'BMI(>=|<=|>|<|=)(\d+(\.\d+)?)', expr)
        if not bmi_match:
            raise ValueError(f"不支持的BMI表达式格式：{expr}")
        op = bmi_match.group(1)
        val = float(bmi_match.group(2))
        constraints.append((op, val))

    # 计算所有满足约束的BMI（10.0-40.0合理范围，0.1为步长）
    all_satisfied = []
    for bmi in [round(x * 0.1, 1) for x in range(100, 401)]:
        valid = True
        for op, val in constraints:
            if op == '=' and not (bmi == val):
                valid = False
            elif op == '>' and not (bmi > val):
                valid = False
            elif op == '>=' and not (bmi >= val):
                valid = False
            elif op == '<' and not (bmi < val):
                valid = False
            elif op == '<=' and not (bmi <= val):
                valid = False
        if valid:
            all_satisfied.append(bmi)

    if not all_satisfied:
        raise ValueError("BMI表达式无有效取值")

    # 筛选2个有效值（起始+中间）
    satisfied = []
    if len(all_satisfied) >= 2:
        satisfied = [all_satisfied[0], all_satisfied[min(1, len(all_satisfied) - 1)]]
    else:
        satisfied = all_satisfied  # 极端情况（仅1个有效值）

    # 生成无效值（边界值，保留1位小数）
    not_satisfied = []
    boundaries = set()
    for op, val in constraints:
        boundaries.add(round(val - 0.1, 1))
        boundaries.add(round(val + 0.1, 1))
        boundaries.add(val)

    # 筛选有效边界值（10.0-40.0之间，且不在satisfied中）
    for b in sorted(boundaries):
        if 10.0 <= b <= 40.0 and b not in satisfied and b not in all_satisfied:
            not_satisfied.append(b)
            if len(not_satisfied) >= 2:
                break

    # 确保至少2个无效值
    while len(not_satisfied) < 2:
        for bmi in [round(x * 0.1, 1) for x in range(100, 401)]:
            if bmi not in all_satisfied and bmi not in not_satisfied:
                not_satisfied.append(bmi)
                break

    return satisfied, not_satisfied


def parse_gender_expression(expr: str) -> Tuple[List[str], List[str]]:
    """
    解析性别表达式，返回有效值（1个）和无效值（1个）
    仅支持性别=男/女
    """
    expr = expr.strip()
    gender_match = re.match(r'性别=(男|女)', expr)
    if not gender_match:
        raise ValueError(f"不支持的性别表达式格式：{expr}，仅支持性别=男或性别=女")
    satisfied = [gender_match.group(1)]
    not_satisfied = ['女'] if satisfied[0] == '男' else ['男']
    return satisfied, not_satisfied


def generate_combinations(
        satisfied_ages: List[int],
        satisfied_bmis: List[float],
        satisfied_genders: List[str],
        not_satisfied_ages: List[int],
        not_satisfied_bmis: List[float],
        not_satisfied_genders: List[str]
) -> Dict[str, List[Dict[str, any]]]:
    """
    生成满足条件和不满足条件的组合（严格匹配输出格式）
    - satisfied：年龄、BMI、性别均为有效值的所有组合
    - notSatisfied：至少一项为无效值的所有组合（去重）
    """
    # 生成满足条件的组合
    satisfied = []
    for age in satisfied_ages:
        for bmi in satisfied_bmis:
            for gender in satisfied_genders:
                satisfied.append({
                    '年龄': age,
                    'BMI': bmi,
                    '性别': gender
                })

    # 生成不满足条件的组合（所有可能的无效组合，去重）
    not_satisfied = []
    # 收集所有可能的取值（有效+无效）
    all_ages = satisfied_ages + not_satisfied_ages
    all_bmis = satisfied_bmis + not_satisfied_bmis
    all_genders = satisfied_genders + not_satisfied_genders

    for age in all_ages:
        for bmi in all_bmis:
            for gender in all_genders:
                # 判断是否不满足（至少一项无效）
                age_valid = age in satisfied_ages
                bmi_valid = bmi in satisfied_bmis
                gender_valid = gender in satisfied_genders
                if not (age_valid and bmi_valid and gender_valid):
                    combo = {'年龄': age, 'BMI': bmi, '性别': gender}
                    if combo not in not_satisfied:
                        not_satisfied.append(combo)

    return {
        'satisfied': satisfied,
        'notSatisfied': not_satisfied
    }


def main(expressions: List[str]) -> Dict[str, List[Dict[str, any]]]:
    """
    主函数：解析输入表达式，生成最终结果
    """
    # 分类表达式（支持多个年龄/BMI表达式，单个性别表达式）
    age_exprs = [expr for expr in expressions if '年龄' in expr]
    bmi_exprs = [expr for expr in expressions if 'BMI' in expr]
    gender_exprs = [expr for expr in expressions if '性别' in expr]

    # 校验输入合法性
    if len(gender_exprs) != 1:
        raise ValueError("必须且只能包含一个性别表达式（性别=男 或 性别=女）")
    if len(age_exprs) == 0:
        raise ValueError("必须包含至少一个年龄表达式")
    if len(bmi_exprs) == 0:
        raise ValueError("必须包含至少一个BMI表达式")

    # 解析各字段的有效/无效值
    satisfied_ages, not_satisfied_ages = parse_age_expression(age_exprs)
    satisfied_bmis, not_satisfied_bmis = parse_bmi_expression(bmi_exprs)
    satisfied_genders, not_satisfied_genders = parse_gender_expression(gender_exprs[0])

    # 生成组合结果
    result = generate_combinations(
        satisfied_ages, satisfied_bmis, satisfied_genders,
        not_satisfied_ages, not_satisfied_bmis, not_satisfied_genders
    )

    return result


# ------------------- 测试示例（完全匹配需求格式） -------------------
if __name__ == "__main__":
    # 测试用例1：基础格式（年龄=6，BMI>=19.5，性别=男）
    print("测试用例1：['年龄=6', 'BMI>=19.5', '性别=男']")
    result1 = main(['年龄=6', 'BMI>=19.5', '性别=男'])
    import json

    print(json.dumps(result1, ensure_ascii=False, indent=2))
    print("\n" + "-" * 80 + "\n")

    # 测试用例2：范围格式（66<=年龄<69，BMI<12，性别=男）
    print("测试用例2：['66<=年龄<69', 'BMI<12', '性别=男']")
    result2 = main(['66<=年龄<69', 'BMI<12', '性别=男'])
    print(json.dumps(result2, ensure_ascii=False, indent=2))
    print("\n" + "-" * 80 + "\n")

    # 测试用例3：多个年龄表达式（BMI<18.5，年龄>=18，年龄<65，性别=女）
    print("测试用例3：['BMI<18.5', '年龄>=18', '年龄<65', '性别=女']")
    result3 = main(['BMI<18.5', '年龄>=18', '年龄<65', '性别=女'])
    print(json.dumps(result3, ensure_ascii=False, indent=2))
