import re
import random
import itertools

class BmiAgePO():
    def parse_condition(self,condition_str):
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

        # 处理简单条件
        match = re.match(r'(\w+)\s*([<>=!]+)\s*([\d.]+)', condition_str)
        if not match:
            raise ValueError(f"无法解析条件: {condition_str}")

        var_name, operator, value_str = match.groups()
        value = float(value_str)

        # 生成对应的判断函数
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
        else:
            raise ValueError(f"不支持的运算符: {operator}")

    # 修改 generate_test_points 方法中的相关部分
    def generate_test_points(self, conditions, num_random=1):
        """根据条件动态生成测试点"""
        test_points = {}

        for cond in conditions:
            var_name, cond_func = self.parse_condition(cond)

            # 提取所有数值（兼容复合条件）
            if '<=' in cond and '<' in cond:  # 复合条件
                parts = re.split(r'(<=|<)', cond.replace(' ', ''))
                lower_bound = float(parts[0])
                upper_bound = float(parts[-1])

                # 对于年龄变量，生成整数测试点
                if var_name == '年龄':
                    points = [
                        int(lower_bound - 1),
                        int(lower_bound),  # 18
                        int(lower_bound + 1),
                        int(upper_bound - 1),  # 64
                        int(upper_bound),  # 65
                        int(upper_bound + 1)
                    ]
                else:
                    points = [
                        round(lower_bound - 0.1, 10),
                        round(lower_bound, 10),
                        round(lower_bound + 0.1, 10),
                        round(upper_bound - 0.1, 10),
                        round(upper_bound, 10),
                        round(upper_bound + 0.1, 10)
                    ]

            else:
                # 简单条件逻辑
                threshold = float(re.search(r'([<>=!]+)\s*([\d.]+)', cond).group(2))
                # 对于年龄变量，生成整数测试点
                if var_name == '年龄':
                    points = [int(threshold - 1), int(threshold), int(threshold + 1)]
                else:
                    points = [threshold - 0.1, threshold, threshold + 0.1]

            test_points[var_name] = list(set(points))  # 去重

        return test_points

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
        d_['notSatisfied'] = invalid

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


# 测试入口
if __name__ == "__main__":

    BmiAge_PO = BmiAgePO()

    print("\n测试条件: ['BMI<20', '年龄>=65']")
    print(BmiAge_PO.main(['BMI<20', '年龄>=65']))

    print("\n测试条件: ['BMI>=24', '年龄>=18', '年龄<65']")
    print(BmiAge_PO.main(['BMI>=24', '年龄>=18', '年龄<65']))

    print("\n测试条件: ['BMI<18.5', '年龄>=18', '年龄<65']")
    print(BmiAge_PO.main(['BMI<18.5', '年龄>=18', '年龄<65']))

    print("\n测试条件: ['BMI>=27', '年龄>=65']")
    print(BmiAge_PO.main(['BMI>=27', '年龄>=65']))

    print("\n测试条件: ['BMI<27', 'BMI>=20', '年龄>=65']")
    print(BmiAge_PO.main(['BMI<27', 'BMI>=20', '年龄>=65']))

