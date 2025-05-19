import re
import random
import itertools

class BmiAgeSexPO():
    def parse_condition(self, condition_str):
        """解析条件字符串为变量名、运算符和值"""
        # 处理复合条件，如 "18.0<=年龄<65.0"
        if '<=' in condition_str and '<' in condition_str:
            # 移除所有空格以简化解析
            clean_cond = condition_str.replace(' ', '')
            # 分割条件字符串
            parts = re.split(r'(<=|<)', clean_cond)

            # 提取变量名和上下限
            lower_part = parts[0]
            operator1 = parts[1]
            var_part = parts[2]
            operator2 = parts[3]
            upper_part = parts[4]

            var_name = var_part
            lower_bound = float(lower_part)
            upper_bound = float(upper_part)

            return var_name, lambda x: lower_bound <= x < upper_bound

        # 处理简单条件（保留已有逻辑）
        match = re.match(r'(\w+)\s*(!=|==|<=|>=|<|>|=)\s*([\d.]+|男|女)', condition_str)
        if not match:
            raise ValueError(f"无法解析条件: {condition_str}")

        var_name, operator, value_str = match.groups()

        # 判断是否为性别字段（中文或数字）
        gender_map = {'男': 1, '女': 2}
        if value_str in gender_map:
            value = gender_map[value_str]
        else:
            value = float(value_str) if '.' in value_str else int(value_str)

        if operator == '>':
            return var_name, lambda x: x > value
        elif operator == '<':
            return var_name, lambda x: x < value
        elif operator == '>=':
            return var_name, lambda x: x >= value
        elif operator == '<=':
            return var_name, lambda x: x <= value
        elif operator == '==':
            return var_name, lambda x: x == value
        elif operator == '!=':
            return var_name, lambda x: x != value
        elif operator == '=':  # 支持单个等号
            return var_name, lambda x: x == value
        else:
            raise ValueError(f"不支持的运算符: {operator}")

    def generate_test_points(self, conditions, num_random=1):
        test_points = {}

        for cond in conditions:
            var_name, cond_func = self.parse_condition(cond)

            if var_name == '性别':
                # 性别只取两个值：男/女 → 内部用 1 / 2 表示
                test_points[var_name] = [1, 2]
                continue

            # 原有 BMI、年龄等连续变量逻辑保持不变
            if '<=' in cond and '<' in cond:
                parts = re.split(r'(<=|<)', cond.replace(' ', ''))
                lower_bound = float(parts[0])
                upper_bound = float(parts[-1])

                points = [
                    round(lower_bound - 0.1, 10),
                    round(lower_bound, 10),
                    round(lower_bound + 0.1, 10),
                    round(upper_bound, 10),
                    round(upper_bound + 0.1, 10)
                ]
            else:
                threshold = float(re.search(r'([<>=!]+)\s*([\d.]+)', cond).group(2))
                points = [threshold - 10.1, threshold, threshold + 10.1]

            test_points[var_name] = list(set(points))

        return test_points

    def format_output(self, data):
        result = []
        for item in data:
            formatted = {}
            for var, val in item.items():
                if var == '性别':
                    formatted[var] = '男' if val == 1 else '女'
                else:
                    formatted[var] = round(float(val), 1)
            result.append(formatted)
        return result

    def combinations(self,conditions, test_points):
        """测试所有组合并分类为有效和无效"""
        # 按变量名组织条件
        var_conditions = {}
        for cond in conditions:
            var_name, cond_func = self.parse_condition(cond)
            var_conditions.setdefault(var_name, []).append(cond_func)

        # 生成所有可能的组合
        variables = list(test_points.keys())
        value_combinations = itertools.product(*[test_points[var] for var in variables])

        valid = []
        invalid = []

        for values in value_combinations:
            value_dict = dict(zip(variables, values))
            is_valid = True

            # 检查所有条件
            for var, conds in var_conditions.items():
                if not all(cond(value_dict[var]) for cond in conds):
                    is_valid = False
                    break

            if is_valid:
                valid.append(value_dict)
            else:
                invalid.append(value_dict)

        return valid, invalid

    def merge_conditions(self,conditions):
        """合并关于同一个变量的条件"""
        var_conditions = {}
        for cond in conditions:
            var_name, _ = self.parse_condition(cond)
            var_conditions.setdefault(var_name, []).append(cond)

        merged_conditions = []
        for var, conds in var_conditions.items():
            if len(conds) == 1:
                merged_conditions.append(conds[0])
            else:
                lower_bound = None
                upper_bound = None
                for cond in conds:
                    operator = re.search(r'([<>=!]+)', cond).group(1)
                    value = float(re.search(r'([<>=!]+)\s*([\d.]+)', cond).group(2))
                    if '>=' in operator or '>' in operator:
                        if lower_bound is None or value > lower_bound:
                            lower_bound = value
                    elif '<=' in operator or '<' in operator:
                        if upper_bound is None or value < upper_bound:
                            upper_bound = value
                # 确保合并后的条件格式一致（无多余空格）
                merged_conditions.append(f"{lower_bound:.1f}<={var}<{upper_bound:.1f}")

        return merged_conditions

    def main(self, conditions):
        merged_conditions = self.merge_conditions(conditions)
        test_points = self.generate_test_points(merged_conditions)
        valid, invalid = self.combinations(merged_conditions, test_points)

        return {
            'satisfied': self.format_output(valid),
            'notSatisfied': self.format_output(invalid)
        }


    def main2(self, conditions):
        # 可配置的条件列表
        # conditions = ['BMI>=24', '年龄>=18', '年龄<65']
        # conditions = ['BMI<24', 'BMI>=18.5','年龄>=18', '年龄<65']
        # conditions = ['BMI<18.5', '年龄>=18', '年龄<65']
        # conditions = ['BMI>=27', '年龄>=65']
        # conditions = ['BMI<27', 'BMI>=20', '年龄>=65']
        # conditions = ['BMI<20', '年龄>=65']


        # 合并条件（特别是关于同一个变量的多个条件）
        merged_conditions = self.merge_conditions(conditions)
        # print("合并后的条件:", merged_conditions)

        # 生成测试点
        test_points = self.generate_test_points(merged_conditions)

        # 测试所有组合
        d_ = {}
        valid, invalid = self.combinations(merged_conditions, test_points)
        d_['satisfied'] = valid
        d_['not1'] = invalid

        # print(d_)
        return d_


        # # 输出结果
        # print(f"有效组合 ({len(valid)}):")
        # for case in valid:
        #     s = (', '.join([f"{var}={val:.1f}" for var, val in case.items()]))
        #     print(s)
        #
        # print(f"\n无效组合 ({len(invalid)}):")
        # for case in invalid:
        #     print(', '.join([f"{var}={val:.1f}" for var, val in case.items()]))

    def splitMode(self, condition):
        """
        将形如 '6<=年龄<6.5' 或 '14.7<BMI<18.8' 的复合条件拆分为两个标准条件
        :param condition: 条件字符串
        :return: 拆分后的简单条件列表
        """

        cond = condition.strip().replace(" ", "")

        # 匹配形如：6<=年龄<6.5 或 14.7<BMI<18.8
        match = re.match(r'^(\d+(?:\.\d+)?)(<=|<|>=|>)(年龄|BMI)(<=|<|>=|>)(\d+(?:\.\d+)?)$', cond)

        if not match:
            return [condition]  # 不符合格式，返回原始条件

        left_val, op1, field, op2, right_val = match.groups()

        # 判断是否是合法组合（如：a < x < b）
        if (op1 in ('<', '<=') and op2 in ('<', '<=')) or (op1 in ('>', '>=') and op2 in ('>', '><')):
            # 如果是 a < x < b 类型，转换成 x > a 且 x < b
            cond1 = f"{field}{op1}{left_val}"
            cond2 = f"{field}{op2}{right_val}"

            # 修复方向错误：例如 6<=年龄<6.5 → 年龄>=6 and 年龄<6.5
            if op1 == '<=' and op2 == '<':
                cond1 = f"{field}>={left_val}"
            elif op1 == '<' and op2 == '<=':
                cond1 = f"{field}>{left_val}"
                cond2 = f"{field}<={right_val}"
            elif op1 == '<' and op2 == '<':
                cond1 = f"{field}>{left_val}"
            elif op1 == '<=' and op2 == '<=':
                cond1 = f"{field}>={left_val}"
                cond2 = f"{field}<={right_val}"

            return [cond1, cond2]

        else:
            return [condition]

    def interconvertMode(self, condition):
        """
        互换
        将形如 '18.5>BMI' 转换为 'BMI<18.5'
        :param condition: 条件字符串
        :return: 拆分或转换后的条件列表
        """
        cond = condition.strip().replace(" ", "")

        # 匹配类似 18.5>BMI 或 24<BMI 这样的逆序写法
        match = re.match(r'^(\d+(?:\.\d+)?)(>|>=|<|<=)(BMI|年龄)$', cond)

        if match:
            value, op, field = match.groups()

            # 反转操作符方向
            if op == '>':
                return [f"{field}<{value}"]
            elif op == '>=':
                return [f"{field}<={value}"]
            elif op == '<':
                return [f"{field}>{value}"]
            elif op == '<=':
                return [f"{field}>={value}"]

        # 默认返回原条件
        return [condition]



# 测试入口
if __name__ == "__main__":

    BmiAgeSex_PO = BmiAgeSexPO()

    print("\n测试条件: ['年龄>=66', '年龄<69', '13.1>BMI', '性别=男']")
    print(BmiAgeSex_PO.main(['年龄>=69', '年龄<=72', 'BMI<13.1', '性别=男']))

    # print("\n测试条件: ['BMI>=24', '年龄>=18', '年龄<65', '性别=男']")
    # print(BmiAgeSex_PO.main(['BMI>=24', '年龄>=18', '年龄<65', '性别=男']))
    #
    # print("\n测试条件: ['BMI<18.5', '年龄>=18', '年龄<65', '性别=女']")
    # print(BmiAgeSex_PO.main(['BMI<18.5', '年龄>=18', '年龄<65', '性别=女']))
    #
    # print("\n测试条件: ['BMI>=27', '年龄>=65', '性别=男']")
    # print(BmiAgeSex_PO.main(['BMI>=27', '年龄>=65', '性别=男']))
    #
    # print("\n测试条件: ['BMI<27', 'BMI>=20', '年龄>=65', '性别=女']")
    # print(BmiAgeSex_PO.main(['BMI<27', 'BMI>=20', '年龄>=65', '性别=女']))

