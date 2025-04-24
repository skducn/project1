# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2025.3.12
# Description: spacy
# 关键功能解析：
# 1. **分词处理**：SpaCy自动将连续文本分割为有意义的词语单位
# 2. **词性标注**：识别每个词的语法角色（名词、动词等）
# 3. **依存分析**：揭示词语间的语法关系（主语、宾语等）
# 4. **实体识别**：自动检测组织机构、时间、地点等关键信息
#
# 应用场景建议：
# - 客户咨询分析：自动提取产品名称、价格等关键信息
# - 舆情监控：识别品牌提及和情感倾向
# - 知识图谱构建：提取实体关系
# - 智能客服：理解用户查询的语义结构
#
# 注意：中文处理需使用专门的中文模型（如zh_core_web_sm），其分词逻辑与英文不同。对于专业领域（如医疗、法律），建议使用领域特定模型或自定义词典进行增强。

# ********************************************************************************************************************
# 请用NLP工具如SpaCy解析需求，给出一个实例。
# 以下是一个使用SpaCy进行中文文本分析的实例演示，包含分词、词性标注、依存句法分析和命名实体识别等核心功能：

# ```python
# 安装SpaCy和中文模型（需先执行）
# pip install spacy
# python -m spacy download zh_core_web_sm

import spacy

# 加载中文模型
nlp = spacy.load("zh_core_web_sm")

# 示例文本（客户服务场景）
text = "苹果公司将于2024年6月在北京发布新款iPhone，预计售价5999元起。"

# 处理文本
doc = nlp(text)

# 1. 分词与词性标注
print("=== 分词与词性标注 ===")
for token in doc:
    print(f"{token.text:<8} | {token.pos_:<6} | {token.dep_:<12} | {spacy.explain(token.pos_)}")

# 2. 命名实体识别
print("\n=== 命名实体 ===")
for ent in doc.ents:
    print(f"{ent.text:<12} | {ent.label_:<8} | {spacy.explain(ent.label_)}")

# 3. 依存关系可视化
from spacy import displacy
print("\n依存关系可视化：")
displacy.render(doc, style="dep", jupyter=True)

'''
输出示例：
=== 分词与词性标注 ===
苹果     | PROPN  | nmod       | proper noun
公司     | NOUN   | nsubj      | noun
将       | AUX    | aux        | auxiliary
于       | ADP    | prep       | adposition
2024     | NUM    | nummod     | numeral
年       | NOUN   | npadvmod   | noun
6        | NUM    | nummod     | numeral
月       | NOUN   | npadvmod   | noun
在       | ADP    | prep       | adposition
北京     | PROPN  | pobj       | proper noun
发布     | VERB   | ROOT       | verb
新款     | ADJ    | amod       | adjective
iPhone   | PROPN  | dobj       | proper noun
，       | PUNCT  | punct      | punctuation
预计     | VERB   | advcl      | verb
售价     | NOUN   | nsubj      | noun
5999     | NUM    | nummod     | numeral
元       | NOUN   | clf        | noun
起       | VERB   | ccomp      | verb
。       | PUNCT  | punct      | punctuation

=== 命名实体 ===
苹果公司     | ORG     | Companies, agencies, institutions, etc.
2024年6月  | DATE    | Absolute or relative dates or periods
北京       | GPE     | Countries, cities, states
新款iPhone | PRODUCT | Objects, vehicles, foods, etc. (not services)
5999元     | MONEY   | Monetary values, including unit
'''




