# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2025.3.12
# Description: HanLP
# 用途：一个功能强大的中文自然语言处理工具，支持分词、词性标注、命名实体识别、依存句法分析等。
# pip install hanlp
# Downloading https://file.hankcs.com/hanlp/mtl/close_tok_pos_ner_srl_dep_sdp_con_electra_small_20210111_124159.zip to /Users/linghuchong/.hanlp/mtl/close_tok_pos_ner_srl_dep_sdp_con_electra_small_20210111_124159.zip
# 100% 114.3 MiB   1.4 MiB/s ETA:  0 s [=========================================]
# Decompressing /Users/linghuchong/.hanlp/mtl/close_tok_pos_ner_srl_dep_sdp_con_electra_small_20210111_124159.zip to /Users/linghuchong/.hanlp/mtl
# Downloading https://file.hankcs.com/hanlp/transformers/electra_zh_small_20210706_125427.zip to /Users/linghuchong/.hanlp/transformers/electra_zh_small_20210706_125427.zip
# 100%  41.2 KiB  41.2 KiB/s ETA:  0 s [=========================================]
# Decompressing /Users/linghuchong/.hanlp/transformers/electra_zh_small_20210706_125427.zip to /Users/linghuchong/.hanlp/transformers
# /Users/linghuchong/miniconda3/envs/py310/lib/python3.10/site-packages/transformers/tokenization_utils_base.py:1601: FutureWarning: `clean_up_tokenization_spaces` was not set. It will be set to `True` by default. This behavior will be depracted in transformers v4.45, and will be then set to `False` by default. For more details check this issue: https://github.com/huggingface/transformers/issues/31884
#   warnings.warn(
# Downloading https://file.hankcs.com/corpus/char_table.json.zip to /Users/linghuchong/.hanlp/thirdparty/file.hankcs.com/corpus/char_table.json.zip
# 100%  19.4 KiB   1.9 KiB/s ETA:  0 s [=========================================]
# Decompressing /Users/linghuchong/.hanlp/thirdparty/file.hankcs.com/corpus/char_table.json.zip to /Users/linghuchong/.hanlp/thirdparty/file.hankcs.com/corpus
# ********************************************************************************************************************
import hanlp
HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
text = "我爱自然语言处理"
result = HanLP(text)
print(result)

# {
#   "tok/fine": [
#     "我",
#     "爱",
#     "自然",
#     "语言",
#     "处理"
#   ],
#   "tok/coarse": [
#     "我",
#     "爱",
#     "自然语言处理"
#   ],
#   "pos/ctb": [
#     "PN",
#     "VV",
#     "NN",
#     "NN",
#     "VV"
#   ],
#   "pos/pku": [
#     "r",
#     "v",
#     "n",
#     "n",
#     "v"
#   ],
#   "pos/863": [
#     "r",
#     "v",
#     "a",
#     "n",
#     "v"
#   ],
#   "ner/msra": [],
#   "ner/pku": [],
#   "ner/ontonotes": [],
#   "srl": [
#     [["我", "ARG0", 0, 1], ["爱", "PRED", 1, 2], ["自然语言处理", "ARG1", 2, 5]],
#     [["自然语言", "ARGM-ADV", 2, 4], ["处理", "PRED", 4, 5]]
#   ],
#   "dep": [
#     [2, "nsubj"],
#     [0, "root"],
#     [4, "nn"],
#     [5, "dep"],
#     [2, "ccomp"]
#   ],
#   "sdp": [
#     [[2, "Aft"]],
#     [[0, "Root"]],
#     [[4, "Desc"]],
#     [[5, "Mann"]],
#     [[2, "dCont"]]
#   ],
#   "con": [
#     "TOP",
#     [["IP", [["NP", [["PN", ["我"]]]], ["VP", [["VV", ["爱"]], ["IP", [["VP", [["NN", ["自然"]], ["NN", ["语言"]], ["VP", [["VV", ["处理"]]]]]]]]]]]]]
#   ]
# }
#
# Process finished with exit code 0