import pandas as pd
import math
import numpy as np


def parrallel(df1, df2):
    index_set = set(df1.index) & set(df2.index)
    df1 = df1.reindex(index_set).sort_index()
    df2 = df2.reindex(index_set).sort_index()
    return df1, df2


def calculate_trad_momentum(df_mktret, df_stkpri, j):
    df_stkret = df_stkpri.pct_change(1).drop(df_stkpri.index[0])

    # 对齐三个数据框
    df_stkret, df_mktret = parrallel(df_stkret, df_mktret)

    df_excess_ret = df_stkret.sub(df_mktret, axis=0)
    df_momentum = pd.DataFrame(columns=df_stkpri.columns)

    for i in range(j, len(df_stkret)):
        df_excess_ret_use = df_excess_ret.iloc[i - j:i]
        cu_excess_ret = (df_excess_ret_use + 1).cumprod() - 1
        row = cu_excess_ret.iloc[-1]
        df_momentum = df_momentum.append(row, ignore_index=True)

    df_momentum.index = df_stkret.index[j:]
    return df_momentum


def calculate_trad_momentum50(df_pri, j):
    df_momentum = pd.DataFrame(columns=df_pri.columns)

    for i in range(j, len(df_pri)):
        df_pri_use = df_pri.iloc[i - j:i]
        cu_ret = df_pri_use.iloc[-1] / df_pri_use.iloc[0] - 1
        df_momentum = df_momentum.append(cu_ret, ignore_index=True)

    df_momentum.index = df_pri.index[j:]
    return df_momentum


def calculate_vol_mom(df_stkpri, df_stkvol, df_indexret, k, type):
    '''
    mv, mv_2
    '''
    df_stkret = df_stkpri.pct_change(1).drop(df_stkpri.index[0])

    # 对齐三个数据框
    df_stkret, df_mktret = parrallel(df_stkret, df_indexret)
    df_stkvol = df_stkvol.loc[df_stkret.index]

    df_momentum = pd.DataFrame(columns=df_stkret.columns)
    ser_sum_vol = df_stkvol.sum(axis=1)
    df_excess_ret = df_stkret.sub(df_mktret, axis=0)
    df_vol_weight = df_stkvol.div(ser_sum_vol, axis=0)

    if type == 'mv2':
        df_right = df_vol_weight * df_excess_ret ** 2
    elif type == 'mv':
        df_right = df_vol_weight * df_excess_ret

    for i in range(k, len(df_stkret)):
        df_right_use = df_right.iloc[i - k:i]
        row = df_right_use.sum(axis=0, skipna=False)
        df_momentum = df_momentum.append(row, ignore_index=True)

    #
    # for ind in df_stkret:
    #     df_vol_use = df_stkvol.iloc[i - k:i]
    #     ser_vol_sum = df_vol_use.sum(axis=0)
    #     vol_weight = df_stkvol.iloc[i - 1] / ser_vol_sum
    #
    #     df_stkret_use = df_stkret.iloc[i]
    #     ser_mktret_use = df_mktret.iloc[i]
    #     sum_ret = df_stkret_use.sub(ser_mktret_use, axis=0).sum(axis=0)
    #     vm_row = sum_ret * vol_weight
    #
    #     df_momentum = df_momentum.append(vm_row, ignore_index=True)
    df_momentum.index = df_stkret.index[k:]

    return df_momentum


def ts_max(df, ts_window):  # 用来计算MAX。第31天的所在行记录第1-30天的最大值。
    df_ts_max = pd.DataFrame(columns=df.columns)
    for i in range(ts_window - 1, len(df) - 1):
        df_use = df.iloc[i - ts_window + 1:i + 1]
        maximum = df_use.max()
        df_ts_max = df_ts_max.append(maximum, ignore_index=True)
    df_ts_max.index = df.index[ts_window:]
    return df_ts_max


def calculate_MAX(df_price, df_indexret, MAX_days):
    df_coinret = df_price.pct_change(1).drop(df_price.index[0])
    df_coinret, df_indexret = parrallel(df_coinret, df_indexret)  # 对齐

    df_excess_return = df_coinret.sub(df_indexret, axis=0)
    df_MAX = ts_max(df_excess_return, MAX_days)
    return df_MAX


def calculate_MAX_with_volume(df_pri, df_indexret, df_vol, MAX_days, k, type):
    df_MAX = calculate_MAX(df_pri, df_indexret, MAX_days)
    df_MAX, df_indexret = parrallel(df_MAX, df_indexret)
    df_vol = df_vol.reindex(df_MAX.index)

    df_momentum = pd.DataFrame(columns=df_MAX.columns)
    ser_sum_vol = df_vol.sum(axis=1)
    df_vol_weight = df_vol.div(ser_sum_vol, axis=0)
    '''
    mv or mv2
    '''
    if type == 'mv':
        df_right = df_vol_weight * df_MAX
    elif type == 'mv2':
        df_right = df_vol_weight * df_MAX ** 2

    for i in range(k, len(df_MAX)):
        df_right_use = df_right.iloc[i - k:i]
        row = df_right_use.sum(axis=0, skipna=False)
        df_momentum = df_momentum.append(row, ignore_index=True)

    # for ind in df_stkret:
    #     df_vol_use = df_stkvol.iloc[i - k:i]
    #     ser_vol_sum = df_vol_use.sum(axis=0)
    #     vol_weight = df_stkvol.iloc[i - 1] / ser_vol_sum
    #
    #     df_stkret_use = df_stkret.iloc[i]
    #     ser_mktret_use = df_mktret.iloc[i]
    #     sum_ret = df_stkret_use.sub(ser_mktret_use, axis=0).sum(axis=0)
    #     vm_row = sum_ret * vol_weight
    #
    #     df_momentum = df_momentum.append(vm_row, ignore_index=True)
    df_momentum.index = df_MAX.index[k:]
    return df_momentum


def portfolio_formation(df_momentum, df_stkpri, h, lb, fee=0.003):
    '''

    :param df_momentum:
    :param df_stkpri:
    :param k: 上溯期
    :param h: 持有期
    :param lb: 每组最少的数字货币个数
    :param fee:
    :return:
    '''
    df_momentum, df_stkpri = parrallel(df_momentum, df_stkpri)

    # 构建投资组合,持有h天.每隔h天换仓，取momentum
    df_momentum_use = df_momentum.loc[df_momentum.index[range(0, len(df_momentum), h)]]  # 记录t时刻之前的历史信息
    df_group_return = pd.DataFrame(index=df_momentum_use.index,
                                   columns=['Port1', 'Port2', 'Port3', 'Port4', 'Port5'])
    df_stk_selected = pd.DataFrame(index=df_momentum_use.index,
                                   columns=['Port1', 'Port2', 'Port3', 'Port4', 'Port5'])

    for ind in df_momentum_use.index:
        row_mom = df_momentum_use.loc[ind].dropna()  # 去除有mom值的coin

        # 计算持有期收益率
        iid = df_stkpri.index.tolist().index(ind)
        price_buy = df_stkpri.loc[ind]
        if (iid + h) <= (len(df_stkpri) - 1):
            price_sell = df_stkpri.iloc[iid + h]
        else:
            continue
        row_ret = (price_sell - price_buy) / price_buy
        row_ret = row_ret.dropna()  # 去除无法持有完整k天的货币

        coin_avail = set(row_ret.index) & set(row_mom.index)
        stk_each_group = len(coin_avail) / 5
        if stk_each_group < lb:
            continue

        stk_sorted = row_mom[coin_avail].sort_values(ascending=False)  # 降序排列，只包含有效货币
        stk_Port = dict()  # 记录每一期每个组合里的stk

        # port5 最高的momentum 记录coin group return
        # port1 最低的momentum 记录coin group return
        for i in range(1, 6):
            stk_Port[6 - i] = stk_sorted.index[
                              math.floor(stk_each_group * (i - 1)):math.floor(stk_each_group * i)]
            df_stk_selected['Port' + str(6 - i)].loc[ind] = stk_Port[6 - i]

            group_ret = row_ret.loc[stk_Port[6 - i]].mean()
            group_ret = group_ret * (1 - fee * 2)  # 扣除手续费
            # group_ret_mon = np.power(1 + group_ret, 30 / h) - 1 #月化收益率

            df_group_return['Port' + str(6 - i)].loc[ind] = group_ret

    df_group_return.dropna(inplace=True)

    ind = df_group_return > 30 #去除异常值
    sum = ind.sum(axis=1)
    drop_index = sum.index[sum > 0]

    df_group_return.drop(index=drop_index,inplace=True)

    df_stk_selected, df_group_return = parrallel(df_stk_selected, df_group_return)
    # df_stk_selected.dropna(inplace=True)

    port5_ave = np.round(df_group_return['Port5'].mean(), 4)  # 买入
    port5_t = port5_ave * len(df_group_return) / df_group_return['Port5'].std()

    port1_ave = np.round(df_group_return['Port1'].mean(), 4)  # 卖出
    port1_t = port1_ave * len(df_group_return) / df_group_return['Port1'].std()

    diff = df_group_return['Port5'] - df_group_return['Port1']
    mean = diff.mean()
    print('mean:' + str(diff.mean()))
    std = math.sqrt((df_group_return['Port5'].var() + df_group_return['Port1'].var()) / len(diff))
    t_stats_com = diff.mean() / std
    t_stats_sim = diff.mean() * len(diff) / diff.std()
    print('t_com:' + str(t_stats_com))
    print('t_sim:' + str(t_stats_sim))

    return df_group_return, df_stk_selected, port5_ave, port1_ave, port5_t, port1_t, np.round(diff.mean(), 4), np.round(
        t_stats_com, 4), np.round(t_stats_sim, 4)


def portfolio_formation50(df_momentum, df_stkpri, j, h, fee):
    '''
    :param df_momentum: 计算好的动量dataframe
    :param df_stkpri: 数字货币价格
    :param j: 动量形成期/天
    :param h: 持有期/天
    :param fee: 考虑手续费
    :return:
    '''

    df_momentum, df_stkpri = parrallel(df_momentum, df_stkpri)

    # 构建投资组合,持有k天，取momentum
    df_momentum_use = df_momentum.loc[df_momentum.index[range(0, len(df_momentum), h)]]  # 记录t时刻之前的历史信息
    df_group_return = pd.DataFrame(index=df_momentum_use.index, columns=['winner', 'loser'])
    df_stk_selected = pd.DataFrame(index=df_momentum_use.index, columns=['winner', 'loser'])

    for ind in df_momentum_use.index:
        row_mom = df_momentum_use.loc[ind].dropna()  # 去除有mom值的coin

        # 计算持有期收益率
        iid = df_stkpri.index.tolist().index(ind)
        price_buy = df_stkpri.loc[ind]
        if (iid + h) <= (len(df_stkpri) - 1):
            price_sell = df_stkpri.iloc[iid + h]
        else:
            continue
        row_ret = (price_sell - price_buy) / price_buy
        row_ret = row_ret.dropna()  # 去除无法持有完整k天的货币

        coin_avail = set(row_ret.index) & set(row_mom.index)  # y有mom且可以持有k期的coin

        stk_sorted = row_mom[coin_avail].sort_values(ascending=False)  # 降序排列，只包含有效数字货币

        if len(stk_sorted) < 20:  # 如果不到10个币就跳过
            continue
        stk_Port = dict()  # 记录每一期每个组合里的stk

        # winner 最高的momentum 记录coin group return
        # loser 最低的momentum 记录coin group return

        stk_Port['winner'] = stk_sorted.index[:10]
        stk_Port['loser'] = stk_sorted.index[-10:]
        df_stk_selected['winner'].loc[ind] = stk_Port['winner']
        winner_ret = row_ret.loc[stk_Port['winner']].mean()
        winner_ret = winner_ret * (1 - fee * 2)  # 扣除手续费
        # winner_ret_mon = np.power(1 + winner_ret, 30 / h) - 1 #月化收益率
        df_group_return['winner'].loc[ind] = winner_ret

        df_stk_selected['loser'].loc[ind] = stk_Port['loser']
        loser_ret = row_ret.loc[stk_Port['loser']].mean()
        loser_ret = loser_ret * (1 - fee * 2)  # 扣除手续费
        # loser_ret_mon = np.power(1 + loser_ret, 30 / h) - 1 #月化收益率
        df_group_return['loser'].loc[ind] = loser_ret

    df_group_return.dropna(inplace=True)
    df_stk_selected.dropna(inplace=True)

    df_group_return
    winner_ave = np.round(df_group_return['winner'].mean(), 4)  # 买入
    loser_ave = np.round(df_group_return['loser'].mean(), 4)  # 卖出
    diff = df_group_return['winner'] - df_group_return['loser']

    mean = diff.mean()
    print('mean:' + str(diff.mean()))
    std = math.sqrt((df_group_return['winner'].var() + df_group_return['loser'].var()) / len(diff))
    t_stats = diff.mean() / std
    print('t:' + str(t_stats))

    # df_group_return.to_csv('data/MAX_results/df_group_return_k_' + str(k) + '_h_' + str(h) + '_mean_' +str(np.round(mean,4))+'_t_'+str(np.round(t_stats,4))+'.csv')
    # df_stk_selected.to_csv('data/MAX_results/df_stk_selected_k_' + str(k) + '_h_' + str(h) + '_mean_' +str(np.round(mean,4))+'_t_'+str(np.round(t_stats,4))+'.csv')

    return df_group_return, df_stk_selected, winner_ave, loser_ave, np.round(diff.mean(), 4), np.round(t_stats, 4)
