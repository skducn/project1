# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2025.3.12
# Description: 10. 拼写检查与纠正
# 场景描述: 检测并纠正文本中的拼写错误。
# 应用: 分词后，可以对每个词元进行拼写检查。
# 工具: pyspellchecker、symspellpy。

# pip3 install setuptools-git
# pip3 install pbr
# pip3 install spellchecker
# pip3 install indexer

# pip3 install pyspellchecker
# ********************************************************************************************************************
from spellchecker import SpellChecker

# 创建一个 SpellChecker 对象
spell = SpellChecker()

# 示例文本，包含一些拼写错误
text = "Ths is a smple text with sme errors."

# 将文本分割成单词
words = text.split()

# 用于存储纠正后的单词列表
corrected_words = []

# 遍历每个单词
for word in words:
    # 检查单词是否拼写正确
    if word in spell:
        # 如果拼写正确，直接添加到纠正后的列表中
        corrected_words.append(word)
    else:
        # 如果拼写错误，找到最可能的正确拼写
        corrected_word = spell.correction(word)
        corrected_words.append(corrected_word)
        print(f"'{word}' 可能是拼写错误，建议纠正为 '{corrected_word}'")

# 将纠正后的单词列表重新组合成文本
corrected_text = " ".join(corrected_words)

# 输出原始文本和纠正后的文本
print("原始文本:", text)
print("纠正后的文本:", corrected_text)


# 'Ths' 可能是拼写错误，建议纠正为 'the'
# 'smple' 可能是拼写错误，建议纠正为 'simple'
# 'sme' 可能是拼写错误，建议纠正为 'me'
# 'errors.' 可能是拼写错误，建议纠正为 'errors'
# 原始文本: Ths is a smple text with sme errors.
# 纠正后的文本: the is a simple text with me errors