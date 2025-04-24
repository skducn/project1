import pandas as pd
from req_parser import RequirementParser  # 假设已导入解析模块
from typing import List, Dict

class TestCaseGenerator:
    def __init__(self, structured_reqs: List[Dict]):
        self.reqs = structured_reqs
        self.testcases = []
        
    def _generate_testcase(self, req: Dict, scenario_suffix: str = "") -> Dict:
        """生成单个测试用例"""
        return {
            "用例ID": f"TC-{len(self.testcases)+1}",
            "测试标题": f"{req['title']} - {scenario_suffix or '正常场景'}",
            "模块": req['module'],
            "前置条件": "; ".join(req['input_conditions']),
            "操作步骤": req['operation_steps'],
            "预期结果": req['expected_results'],
            # "优先级": "P0" if "正常" in scenario_suffix else "P1"
            "优先级": "P0" if not scenario_suffix else "P1"
        }
    
    def generate_all(self) -> List[Dict]:
        """生成所有测试用例（包含异常场景扩展）"""
        for req in self.reqs:
            # 正常场景
            self.testcases.append(self._generate_testcase(req))
            print(req['input_conditions'])
            # 自动扩展异常场景（示例：密码错误）
            if len(req['input_conditions']) > 1:
                if "密码" in req['input_conditions'][1]:
                    error_req = req.copy()
                    error_req['input_conditions'][1] = "密码：654321（错误密码）"
                    error_req['expected_results'] = "显示密码错误提示"
                    self.testcases.append(self._generate_testcase(error_req, "密码错误"))
        return self.testcases

# 完整流程示例
if __name__ == "__main__":
    # 1. 解析需求文档（假设从文件读取）
    with open("requirements.txt", "r", encoding="utf-8") as f:
        req_text = f.read()
    structured_reqs = RequirementParser(req_text).parse()
    
    # 2. 生成测试用例
    generator = TestCaseGenerator(structured_reqs)
    testcases = generator.generate_all()
    
    # 3. 输出到Excel
    df = pd.DataFrame(testcases)
    df.to_excel("test_cases.xlsx", index=False)
    print("已生成测试用例文件：test_cases.xlsx")
