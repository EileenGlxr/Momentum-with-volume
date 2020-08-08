import pandas as pd
import numpy as np
from momentum_calculation import momentum_calculation

df_cci30index = pd.read_csv('data/cci30.csv', index_col=0)
df_coin_pri = pd.read_csv('data/dailyprice_150.csv', index_col=0)
del df_coin_pri['infinitecoin']
del df_coin_pri['tether']
df_coin_vol = pd.read_csv('data/volume_150.csv', index_col=0)
del df_coin_vol['infinitecoin']
del df_coin_vol['tether']

df_mktret = df_cci30index['Close'].pct_change(1).dropna()
# df_rstk = df_coin_pri.pct_change(1).dropna()


'''
momentum with volume
'''
ks = [21, 55, 90]
max_days = [3, 5, 7, 14]

hs = [3, 6, 9, 12, 15, 18, 24]  # 传统的持有期，from 蔡显军
js = [3, 6, 12, 18, 24, 30]  # 传统的形成期
# hs = [10, 20, 30, 40, 50, 60, 70]  # 传统的持有期，from 蔡显军
# js = [20, 40, 60, 70]  # 传统的形成期
fee = 0.003
lb = 5
'''
traditional momentum
'''
df_t_stats_trad_jk = pd.DataFrame(
    columns=['j', 'h', 'winner_mon', 'winner_t', 'loser_t', 'loser_mon', 'mean', 't_com', 't_sim'])
# df_t_stats_trad_excessret = pd.DataFrame(
#     columns=['j', 'h', 'winner_mon', 'winner_t', 'loser_t', 'loser_mon', 'mean', 't_com', 't_sim'])
# df_t_stats_trad_mv = pd.DataFrame(
#     columns=['k', 'h', 'winner_mon', 'winner_t', 'loser_t', 'loser_mon', 'mean', 't_com', 't_sim'])
# df_t_stats_trad_mv2 = pd.DataFrame(
#     columns=['k', 'h', 'winner_mon', 'winner_t', 'loser_t', 'loser_mon', 'mean', 't_com', 't_sim'])

for j in js:
    for h in hs:
        # simple cumulated return
        df_momentum_trad = momentum_calculation.calculate_trad_momentum50(df_coin_pri, j)
        df_momentum = df_momentum_trad
        df_stkpri = df_coin_pri
        df_group_return_trad, df_coin_selected_trad, winner_ave, loser_ave, winner_t, loser_t, ave_trad, t_stats_trad_com, t_stats_trad_sim = momentum_calculation.portfolio_formation(
            df_momentum_trad, df_coin_pri, h, lb, fee)

        winner_mon = np.power(1 + winner_ave, 30 / h) - 1
        loser_mon = np.power(1 + loser_ave, 30 / h) - 1
        # ave_trad_mon = np.power(1 + ave_trad, 30 / h) - 1
        ave_trad_mon = winner_mon - loser_mon

        df_t_stats_trad_jk = df_t_stats_trad_jk.append(
            pd.Series(
                [h, j, winner_mon, loser_mon, winner_t, loser_t, ave_trad_mon, t_stats_trad_com, t_stats_trad_sim],
                index=['h', 'j', 'winner_mon', 'loser_mon', 'winner_t', 'loser_t', 'mean', 't_com', 't_sim']),
            ignore_index=True)
        df_group_return_trad.to_csv(
            'results/traditional_150/trad_cumulated_ret/df_group_return' + '_j_' + str(j) + '_h_' + str(
                h) + '_mean_' + str(
                np.round(ave_trad_mon, 4)) + '_t_' + str(np.round(t_stats_trad_com, 4)) + '.csv')
        df_coin_selected_trad.to_csv(
            'results/traditional_150/trad_cumulated_ret/df_stk_selected' + '_j_' + str(j) + '_h_' + str(
                h) + '_mean_' + str(
                np.round(ave_trad_mon, 4)) + '_t_' + str(np.round(t_stats_trad_com, 4)) + '.csv')

df_t_stats_trad_jk.to_csv('150_coins_trad_5groups_jk_lb_' + str(lb) + '_simplecumulated_mom(函数修改后).csv')
