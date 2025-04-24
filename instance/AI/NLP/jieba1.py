# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2025.3.12
# Description: 1. jieba（结巴分词）
# 中文分词工具，广泛用于中文文本处理。
# pip install jieba
# ********************************************************************************************************************
# import jieba
# text = "我喜欢自然语言处理"
# words = jieba.lcut(text)
# print(words)  # 输出: ['我', '喜欢', '自然语言', '处理']


from whoosh.analysis import StandardAnalyzer
analyzer = StandardAnalyzer()
text = "This is a sample text for information retrieval."
tokens = [token.text for token in analyzer(text)]
print(tokens)
# 输出: ['sample', 'text', 'information', 'retrieval']


from transformers import GPT2Tokenizer, GPT2LMHeadModel
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')
text = "Once upon a time"
input_ids = tokenizer.encode(text, return_tensors='pt')
output = model.generate(input_ids, max_length=50)
print(tokenizer.decode(output[0], skip_special_tokens=True))