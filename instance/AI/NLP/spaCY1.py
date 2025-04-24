# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2025.3.12
# Description: 3. spaCy + 中文模型
# 中文分词工具，广泛用于中文文本处理。
# 用途：spaCy 是一个通用的 NLP 库，支持中文处理（需要加载中文模型）。
# 获取与使用：
# 安装：pip install spacy
# 下载中文模型：python -m spacy download zh_core_web_sm
# ********************************************************************************************************************
import spacy
nlp = spacy.load("zh_core_web_sm")
text = "我喜欢自然语言处理"
doc = nlp(text)

for token in doc:
    print(token.text, token.pos_)

# 我 PRON
# 喜欢 VERB
# 自然 ADJ
# 语言 NOUN
# 处理 VERB



# nlp = spacy.load("en_core_web_sm")
# text = "Apple is looking at buying U.K. startup for $1 billion"
# doc = nlp(text)
# for ent in doc.ents:
#     print(ent.text, ent.label_)
# # 输出: Apple ORG
# #       U.K. GPE
# #       $1 billion MONEY


from rake_nltk import Rake

r = Rake()
text = "Natural language processing is a field of artificial intelligence."
r.extract_keywords_from_text(text)
print(r.get_ranked_phrases())
# 输出: ['natural language processing', 'field', 'artificial intelligence']