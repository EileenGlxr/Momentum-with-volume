import pandas as pd
import numpy as np
from momentum_calculation import momentum_calculation

df_coin_pri = pd.read_csv('data/dailyprice_50.csv', index_col=0)

'''
momentum with volume
'''
js = [3,6,9, 12,15, 21,28,30]  # 形成期
hs = [6, 9, 12, 15, 18, 24]  # 持有期
ks = [21, 55, 90]
max_days = [3, 5, 7, 14]
fee = 0.003
'''
traditional momentum
'''
df_t_stats_trad = pd.DataFrame(columns=['j', 'h', 'winner_mon_ret', 'loser_mon_ret', 'mean', 't'])
lb = 5

for j in js:
    for h in hs:
        # trad
        df_momentum_trad = momentum_calculation.calculate_trad_momentum50(df_coin_pri, j)
        # df_group_return_trad, df_coin_selected_trad, winner, loser, diff_ave_trad, t_stats_trad = momentum_calculation.portfolio_formation50(
        #     df_momentum_trad, df_coin_pri, j, k,fee)
        df_group_return_trad, df_coin_selected_trad, winner, loser, diff_ave_trad, t_stats_trad = momentum_calculation.portfolio_formation50(
            df_momentum_trad, df_coin_pri, j, h, fee)
        winner_mon_ret = np.power(1 + winner, 30 / h) - 1
        loser_mon_ret = np.power(1 + loser, 30 / h) - 1

        df_t_stats_trad = df_t_stats_trad.append(
            pd.Series([j, h, winner_mon_ret, loser_mon_ret, diff_ave_trad, t_stats_trad],
                      index=['j', 'h', 'winner_mon_ret', 'loser_mon_ret', 'mean', 't']), ignore_index=True)

df_t_stats_trad.to_csv('50_coins_test_trad_j_k.csv')
# df_t_stats_trad_mv.to_csv('coins_test_trad_k_h_mv.csv')
# df_t_stats_trad_mv2.to_csv('coins_test_trad_k_h_mv2.csv')

'''
MAX related
'''

df_t_stats_MAX = pd.DataFrame(columns=['h', 'max_day', 'mean', 't'])
df_t_stats_MAX_mv = pd.DataFrame(columns=['k', 'h', 'max_day', 'mean', 't'])
df_t_stats_MAX_mv2 = pd.DataFrame(columns=['k', 'h', 'max_day', 'mean', 't'])

for k in ks:
    hs = range(1, k, 3)
    for h in hs:
        # df_momentum = momentum_calculation.calculate_vol_mom_mv2(df_coin_pri, df_coin_vol, df_mktret, k)
        for mday in max_days:
            # MAX
            df_MAX = momentum_calculation.calculate_MAX(df_coin_pri, df_mktret, mday)
            df_group_return_MAX, df_coin_selected_MAX, ave_MAX, t_stats_MAX = momentum_calculation.portfolio_formation(
                df_MAX, df_coin_pri, h)
            df_t_stats_MAX = df_t_stats_MAX.append(
                pd.Series([h, mday, ave_MAX, t_stats_MAX], index=['h', 'max_day', 'mean', 't']),
                ignore_index=True)

            # MAX_mv
            df_momentum_MAX_mv = momentum_calculation.calculate_MAX_with_volume(df_coin_pri, df_mktret, df_coin_vol,
                                                                                mday, k, 'mv')
            df_group_return_MAX_mv, df_coin_selected_MAX_mv, ave_MAX_mv, t_stats_MAX_mv = momentum_calculation.portfolio_formation(
                df_momentum_MAX_mv,
                df_coin_pri, h, k)
            df_t_stats_MAX_mv = df_t_stats_MAX_mv.append(
                pd.Series([k, h, mday, ave_MAX_mv, t_stats_MAX_mv], index=['k', 'h', 'max_day', 'mean', 't']),
                ignore_index=True)

            # MAX_mv2
            df_MAX_mv2 = momentum_calculation.calculate_MAX_with_volume(df_coin_pri, df_mktret, df_coin_vol,
                                                                        mday, k, 'mv2')
            df_group_return_MAX_mv2, df_coin_selected_MAX_mv2, ave_MAX_mv2, t_stats_MAX_mv2 = momentum_calculation.portfolio_formation(
                df_MAX_mv2, df_coin_pri, h, k)
            df_t_stats_MAX_mv2 = df_t_stats_MAX_mv2.append(
                pd.Series([k, h, mday, ave_MAX_mv2, t_stats_MAX_mv2], index=['k', 'h', 'max_day', 'mean', 't']),
                ignore_index=True)

df_t_stats_MAX_mv.to_csv('coins_test_MAX_k_h_mv.csv')
df_t_stats_MAX_mv2.to_csv('coins_test_MAX_k_h_mv2.csv')
df_t_stats_MAX.to_csv('coins_test_MAX_h.csv')
