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
# import jieba
# import pycorrector
#
# # 示例中文文本，包含一些拼写错误
# text = "这是一个用Python进行分词的例子，其中有几个拼写错误。"
#
# # 使用 jieba 进行分词
# words = jieba.lcut(text)
#
# # 使用 pycorrector 进行拼写纠正
# # corrected_text, details = pycorrector.correct(text)
# corrected_text, details = pycorrector.corrector(text)
# # corrected_text, details = pycorrector.corrector.correct(text)
#
# # 输出原始文本和纠正后的文本
# print("原始文本:", text)
# print("纠正后的文本:", corrected_text)
# print("错误详情:", details)


import sys

sys.path.append("../")
# from pycorrector.bert import bert_corrector
# from pycorrector.electra import electra_corrector
# from pycorrector.ernie import ernie_corrector
# from pycorrector.corrector import Corrector
# from pycorrector.macbert import macbert_corrector

# from pycorrector.bert import BertCorrector
# from pycorrector.electra import ElectraCorrector
# from pycorrector.ernie import ErnieCorrector
from pycorrector.corrector import Corrector
# from pycorrector.macbert import MacBertCorrector

error_sentences = [
    '真麻烦你了。希望你们好好的跳无',
    '少先队员因该为老人让坐',
    '少 先  队 员 因 该 为 老人让坐'
]


def main():
    m_rule = Corrector()
    for line in error_sentences:
        correct_sent, err = m_rule.correct(line)
        print("rule: {} => {}, err:{}".format(line, correct_sent, err))
        print()
    # # m_rule = Corrector()
    # # m_bert = bert_corrector.BertCorrector()
    # # m_electra = electra_corrector.ElectraCorrector()
    # # m_ernie = ernie_corrector.ErnieCorrector()
    # # m_macbert = macbert_corrector.MacBertCorrector()
    # m_rule = Corrector()
    # m_bert = BertCorrector()
    # m_electra = ElectraCorrector()
    # m_ernie = ErnieCorrector()
    # m_macbert = MacBertCorrector()
    # for line in error_sentences:
    #     correct_sent, err = m_rule.correct(line)
    #     print("rule: {} => {}, err:{}".format(line, correct_sent, err))
    #     correct_sent, err = m_bert.bert_correct(line)
    #     print("bert: {} => {}, err:{}".format(line, correct_sent, err))
    #     corrected_sent, err = m_electra.electra_correct(line)
    #     print("electra: {} => {}, err:{}".format(line, correct_sent, err))
    #     corrected_sent, err = m_ernie.ernie_correct(line)
    #     print("ernie: {} => {}, err:{}".format(line, correct_sent, err))
    #     corrected_sent, err = m_macbert.macbert_correct(line)
    #     print("macbert: {} => {}, err:{}".format(line, correct_sent, err))
    #     print()


if __name__ == '__main__':
    main()