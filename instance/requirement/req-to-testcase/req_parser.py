import re
from typing import List, Dict

class RequirementParser:
    def __init__(self, req_text: str):
        self.req_text = req_text
        self.structured_data = []
        
    def _extract_sections(self) -> List[str]:
        """按需求块分割文档（假设以### 功能开头）"""
        return re.split(r'###\s+\d+\.\d+\s+', self.req_text)[1:]  # 示例分割符
    
    def _parse_single_req(self, req_block: str) -> Dict:
        """解析单个需求块"""
        title = re.search(r'(.+?)\n', req_block).group(1).strip()
        module = re.search(r'模块：(.+?)(?=前置条件：)', req_block, re.DOTALL)

        # input_conditions = re.findall(r'输入条件：(.+?)\n', req_block, re.DOTALL)
        input_conditions = re.findall(r'前置条件：(.*?)(?=操作步骤：)', req_block, re.DOTALL)
        input_conditions = [item.strip() for item in input_conditions[0].split('\n') if item.strip()]
        # print(input_conditions)
        # operation = re.findall(r'操作步骤：(.+?)\n', req_block, re.DOTALL)
        operation = re.findall(r'操作步骤：(.*?)(?=预期结果：)', req_block, re.DOTALL)
        operation = [item.strip() for item in operation[0].split('\n') if item.strip()]
        # print(operation)
        # operation = re.search(r'操作步骤：(.+?)\n', req_block, re.DOTALL)
        expected = re.search(r'预期结果：(.+?)$', req_block, re.DOTALL)
        
        return {
            "title": title,
            "module": module.group(1).strip() if expected else "",
            "input_conditions": [c.strip() for c in input_conditions],
            "operation_steps": [c.strip() for c in operation],
            # "operation_steps": operation.group(1).strip() if operation else "",
            "expected_results": expected.group(1).strip() if expected else ""
        }
    
    def parse(self) -> List[Dict]:
        """主解析方法"""
        for block in self._extract_sections():
            if block:
                self.structured_data.append(self._parse_single_req(block))
        return self.structured_data

# 示例用法
if __name__ == "__main__":
    sample_req = """
### 1.1 用户登录
模块：
登录模块 - 首页模块
前置条件：
- 正确用户名
- 正确密码
操作步骤：
1. 打开登录页面
2. 输入用户名test和密码123456
3. 点击登录按钮
预期结果：
跳转至用户主页，显示欢迎信息
"""
    parser = RequirementParser(sample_req)
    print(parser.parse())  # 输出结构化需求数据
