# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
# Description: #
# ***************************************************************u**

import sys
print(sys.path)

from instance.zyjk.CHC.swagger.ConfigparserPO import *
Configparser_PO = ConfigparserPO("./instance/zyjk/CHC/swagger/config.ini")
print(Configparser_PO.HTTP("url"))