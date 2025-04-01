import re
from typing import List, Dict
import pandas as pd


class RequirementParser:
    def __init__(self, req_file: str):
        self.req_text = self._load_file(req_file)
        self.test_cases = []
        self.rtm = []
        self.document_mode = self.detect_document_mode(self.req_text)

    @staticmethod
    def _load_file(file_path: str) -> str:
        """安全加载文件（支持txt/docx/pdf）"""
        try:
            if file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            elif file_path.endswith('.docx'):
                from docx import Document
                doc = Document(file_path)
                return '\n'.join([para.text for para in doc.paragraphs])
            elif file_path.endswith('.pdf'):
                from PyPDF2 import PdfReader
                reader = PdfReader(file_path)
                return '\n'.join([page.extract_text() for page in reader.pages])
            else:
                raise ValueError("不支持的文件格式")
        except Exception as e:
            print(f"文件加载失败: {str(e)}")
            return ""

    @staticmethod
    def detect_document_mode(text: str) -> str:
        """自动检测文档格式模式"""
        if re.search(r"^\d+\.\s+【", text, re.MULTILINE):
            return "standard"  # 标准模式（带【】）
        elif re.search(r"^\d+\.\s+\w+:\s+", text, re.MULTILINE):
            return "agile"  # 敏捷模式（功能: 标题）
        else:
            return "custom"  # 自定义模式

    def _extract_requirements(self) -> List[Dict]:
        """根据文档模式提取需求"""
        if self.document_mode == "standard":
            return self._parse_standard_mode()
        elif self.document_mode == "agile":
            return self._parse_agile_mode()
        else:
            return self.interactive_annotation()

    def _parse_standard_mode(self) -> List[Dict]:
        """解析标准格式需求"""
        pattern = r"""
            ^\s*(\d+)\.\s+                          # 需求编号
            【([^】]+)】                            # 标题（带【】）
            \s*(验收标准|测试点|场景|条件):\s*      # 分隔符
            ((?:\n\s*[*-]\s*.+?)+)                  # 验收标准（支持-/*列表）
        """
        return self._parse_common(pattern)

    def _parse_agile_mode(self) -> List[Dict]:
        """解析敏捷格式需求"""
        pattern = r"""
            ^\s*(\d+)\.\s+                          # 需求编号
            (\w+):\s+([^\n]+?)                     # 功能类型+标题
            \s*(验收标准|测试点|场景|条件):\s*      # 分隔符
            ((?:\n\s*[*-]\s*.+?)+)                  # 验收标准
        """
        return self._parse_common(pattern)

    def _parse_common(self, pattern: str) -> List[Dict]:
        """通用解析逻辑"""
        reqs = re.findall(pattern, self.req_text, re.MULTILINE | re.VERBOSE)
        parsed = []
        for req in reqs:
            req_id = req[0]
            title = req[1] if self.document_mode == "standard" else req[2]
            criteria = [c.strip() for c in req[-1].split('\n') if c.strip()]
            parsed.append({
                "req_id": req_id,
                "title": title,
                "criteria": criteria
            })
        return parsed

    def interactive_annotation(self) -> List[Dict]:
        """交互式标注自定义格式需求"""
        print("\n检测到自定义文档格式，请手动标注需求：")
        reqs = []
        while True:
            req_id = input("\n输入需求编号（按回车结束）: ")
            if not req_id:
                break
            title = input("输入需求标题: ")
            print("输入验收标准（每行一个，按空行结束）:")
            criteria = []
            while True:
                line = input()
                if not line:
                    break
                criteria.append(line.strip())
            reqs.append({
                "req_id": req_id,
                "title": title,
                "criteria": criteria
            })
        return reqs

    def generate_test_cases(self) -> None:
        """生成测试用例主逻辑"""
        requirements = self._extract_requirements()
        if not requirements:
            print("未发现有效需求，请检查文档内容")
            return

        for req in requirements:
            for criterion in req["criteria"]:
                test_case = self._criterion_to_testcase(req, criterion)
                if test_case:
                    self.test_cases.append(test_case)
                    self.rtm.append({
                        "req_id": req["req_id"],
                        "test_case_id": test_case["test_case_id"],
                        "coverage": "full"
                    })

    def _criterion_to_testcase(self, req: Dict, criterion: str) -> Dict:
        """验收标准转测试用例核心逻辑"""
        # 密码复杂度测试
        if "需包含" in criterion and "长度" in criterion:
            return self._handle_password_complexity(req, criterion)
        # 账号锁定测试
        if "连续" in criterion and "锁定" in criterion:
            return self._handle_account_lock(req, criterion)
        # 通用场景
        return {
            "test_case_id": f"TC-{len(self.test_cases) + 1}",
            "req_id": req["req_id"],
            "title": f"验证{criterion}",
            "steps": ["待补充具体步骤"],
            "expected_result": "待补充预期结果",
            "priority": "medium"
        }

    def _handle_password_complexity(self, req: Dict, criterion: str) -> Dict:
        """密码复杂度测试用例生成（含等价类/边界值）"""
        return {
            "test_case_id": f"TC-{len(self.test_cases) + 1}",
            "req_id": req["req_id"],
            "title": "密码复杂度验证",
            "steps": [
                "输入符合规范的8位密码（如Abc@1234）",
                "输入7位密码（如Abc@123）",
                "输入17位密码（如Abcdefgh123456789）"
            ],
            "expected_result": "1. 登录成功；2. 提示长度错误；3. 提示长度错误",
            "priority": "high",
            "design_method": "等价类划分+边界值分析"
        }

    def _handle_account_lock(self, req: Dict, criterion: str) -> Dict:
        """账号锁定测试用例（场景法）"""
        return {
            "test_case_id": f"TC-{len(self.test_cases) + 1}",
            "req_id": req["req_id"],
            "title": "连续输错密码锁定机制验证",
            "steps": [
                "输入错误密码并登录（1/3）",
                "重复操作2次（2/3，3/3）",
                "第4次输入正确密码"
            ],
            "expected_result": "第3次提示剩余1次；第4次提示账号锁定",
            "priority": "high",
            "design_method": "场景法"
        }

    def export_to_excel(self, output_file: str = "test_cases.xlsx") -> None:
        """导出测试用例和RTM到Excel"""
        df_cases = pd.DataFrame(self.test_cases)
        df_rtm = pd.DataFrame(self.rtm)

        with pd.ExcelWriter(output_file) as writer:
            df_cases.to_excel(writer, sheet_name="测试用例", index=False)
            df_rtm.to_excel(writer, sheet_name="需求跟踪矩阵", index=False)
        print(f"\n成功生成测试用例：{len(self.test_cases)}条")
        print(f"需求跟踪矩阵：{len(self.rtm)}条")
        print(f"结果已保存到：{output_file}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("使用方法：python req_parser.py [需求文档路径]")
        sys.exit(1)

    parser = RequirementParser(sys.argv[1])
    parser.generate_test_cases()
    parser.export_to_excel()