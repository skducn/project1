# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2026-1-6
# Description: 17.2.6 年会抽奖程序 376页
# https://gairuo.com/p/pandas-book-dataset
# 需求：分层抽奖：按等级顺序依次抽奖
# 去重机制：已中奖者不再参与后续抽奖
# 灵活配置：可调整各等级中奖人数
# 数据完整性：保证数据结构一致性
# ********************************************************************************************************************
import pandas as pd
import faker


def lottery_system():
      """
      年会抽奖程序 - 优化版本
      一等奖1名，二等奖2名，三等奖3名，一人只能中一次奖
      """
      # 生成参与者名单
      f = faker.Faker('zh_CN')
      df = pd.DataFrame([f.name() for _ in range(10)], columns=['name'])
      df['等级'] = None  # 使用None表示未中奖

      # 定义奖项配置
      prizes = [
            (1, '一等奖'),  # 1名一等奖
            (2, '二等奖'),  # 2名二等奖
            (3, '三等奖')  # 3名三等奖
      ]

      # 按等级依次抽奖
      for num_winners, prize_name in prizes:
            # 获取未中奖的参与者（等级为 None 的记录）
            # 每次抽奖前重新筛选，确保已中奖者不再参与后续抽奖
            # 去重机制：保证一人只能中一次奖的核心实现
            # 状态管理：通过等级列的 None 值标识未中奖状态
            # 安全边界：避免重复中奖的逻辑保障
            available_participants = df[df['等级'].isna()]  # 检测等级列中为 None 的记录
            # print(34,available_participants)

            # 如果可抽奖人数不足，调整中奖人数
            # 计算实际可抽取的中奖人数（避免人数不足的情况
            # num_winners - 计划抽取的中奖人数（如一等奖1名）
            # len(available_participants) - 当前可抽奖的参与者数量
            # actual_winners - 实际抽取的中奖人数，取两者最小值
            actual_winners = min(num_winners, len(available_participants))
            print(38,actual_winners)

            if actual_winners > 0:
                  # 随机抽取中奖者
                  # sample() - pandas 的随机抽样方法
                  # n=actual_winners - 指定抽取样本数量
                  # 无放回抽样 - 默认情况下不会重复抽取同一参与者
                  winners = available_participants.sample(n=actual_winners)

                  # 更新中奖信息
                  df.loc[winners.index, '等级'] = prize_name

      return df


# 执行抽奖
result = lottery_system()
print(result)

# 统计中奖情况
print("\n中奖统计:")
print(result.groupby('等级').size())
