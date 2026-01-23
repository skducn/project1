# 预构建 XPath 模板
xpath_templates = {
    'code': '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[{i}]/td[3]/a',
    'name': '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[{i}]/td[4]/a',
    'chg': '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[{i}]/td[7]/span',
    'mcni': '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[{i}]/td[8]/span',
    'chaoda': '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[{i}]/td[10]/span',
    'da': '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[{i}]/td[11]/span',
    'zhong': '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[{i}]/td[12]/span',
    'xiao': '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[{i}]/td[13]/span'
}

# 批量获取所有数据
all_codes = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[3]/a")
all_names = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[4]/a")
all_chgs = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[7]/span")
all_mcnis = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[8]/span")
all_chaodas = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[10]/span")
all_das = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[11]/span")
all_zhongs = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[12]/span")
all_xiaos = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[13]/span")

# 组合数据并过滤 BK 板块
l_all = []
for i in range(i_rowCount):
    s_code = all_codes[i]
    if "BK" in s_code:
        l_ = [
            s_code,
            all_names[i],
            all_chgs[i],
            all_mcnis[i],
            all_chaodas[i],
            all_das[i],
            all_zhongs[i],
            all_xiaos[i]
        ]
        l_all.append(l_)
