�����ʿز�������˵����
1������jar�����磺java -jar {D:\51\python\project\instance\zyjk\EHR\controlRuleNew1\config\healthRecordRules.jar}

2�����HrRuleRecord�����ݣ��磺DELETE HrRuleRecord

3���޸����ݿ��жϹ���sql1/sql2�� �磺{update HrCover set name=null}

4��ִ���ʿؽӿڣ��磺curl http://localhost:8080/healthRecordRules/rulesApi/execute/{�������}

5���鿴�ʿؽ�� ���磺SELECT t2.Comment,t2.Categories, t2.RuleSql FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId

6���ָ����ݿ��жϹ���sql1/sql2���磺{UPDATE  HrCover set name='����'}
===========================================================================

�����ʿز���������䡿
java -jar D:\51\python\project\instance\zyjk\EHR\controlRuleNew1\config\healthRecordRules.jar
DELETE HrRuleRecord
update HrCover set name=null
curl http://localhost:8080/healthRecordRules/rulesApi/execute/31011310200312009116
SELECT t2.Comment,t2.Categories, t2.RuleSql FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId
UPDATE  HrCover set name='����'

===========================================================================

�����ʿ��Զ���˵��֮config.ini��
ruleType�Ĺ����жϹ������ͣ���ѡ��淶�ԣ������ԣ�һ���ԣ���Ч�ԣ�׷���ԣ��ջ�����ֵ��
�磺ruleType = ������    //��ʾִֻ�й�������Ϊ�����Ե��������������������������ԡ�
ruleType =          //�ջ�����ֵ��ʾִ�����й������͡�

isRun�Ĺ����жϲ��Խ������ѡ�error��ok��empty���ջ�����ֵ��
�磺isRun = error   //��ʾִֻ�б���в��Խ��Ϊerror������
isRun = ok   //��ʾִֻ�б���в��Խ����Ϊok������
isRun = empty   //��ʾִֻ�б���в��Խ��Ϊ�յ�����
isRun =     //�ջ�����ֵ��ʾִ����������

caseFrom��caseTo�Ĺ�������������ʹ�ã���ʾִ��ĳ����������������Ĭ��������ʼ����� 2��caseFrom ����ʼ������ţ�caseTo  �ǽ���������š��磺
����ȡֵ��Χ����ʾִֻ�б���������2������4
caseFrom = 2
caseTo = 5
�� �� ��ʾִֻ�б���������2����������
caseFrom = 2
caseTo =
�� ��ʾִֻ�б���������2������50
caseFrom =
caseTo = 50

�����쳣ȡֵ��Χ����ʾִ����������
caseFrom = 0
caseTo = 0
��
caseFrom = 0
caseTo = -2
��
caseFrom = 36
caseTo = 2
��
caseFrom = 300     //������ֻ��100����������ʼ��ų�����������
caseTo = 2000

===========================================================================

�����ʿ��Զ���˵��ִ֮�нű���
test.py   //���������ļ�config.iniִ�б��������
testOk.py  //ִ�б������Խ��Ϊok������
testError.py  //ִ�б������Խ��Ϊerror������
testAll.py  //ִ�б������������




