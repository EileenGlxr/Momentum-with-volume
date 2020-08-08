import pandas as pd
import numpy as np
from momentum_calculation import momentum_calculation

df_cci30index = pd.read_csv('data/cci30.csv', index_col=0)
df_coin_pri = pd.read_csv('data/dailyprice_150.csv', index_col=0)
df_coin_pri = df_coin_pri[df_coin_pri.index >= 20170901]
df_coin_pri = df_coin_pri[df_coin_pri.index <= 20181231]
del df_coin_pri['infinitecoin']
del df_coin_pri['tether']

df_coin_vol = pd.read_csv('data/volume_150.csv', index_col=0)
df_coin_vol = df_coin_vol[df_coin_vol.index >= 20170901]
df_coin_vol = df_coin_vol[df_coin_vol.index <= 20181231]
del df_coin_vol['infinitecoin']
del df_coin_vol['tether']

df_mktret = df_cci30index['Close'].pct_change(1).dropna()
df_mktret = df_mktret[df_mktret.index >= 20170901]
df_mktret = df_mktret[df_mktret.index <= 20181231]
# df_rstk = df_coin_pri.pct_change(1).dropna()

'''
悲观期
'''
df_mktret = df_mktret[df_mktret.index >= 20180401]
df_coin_pri = df_coin_pri[df_coin_pri.index >= 20180401]
df_coin_vol = df_coin_vol[df_coin_vol.index >= 20180401]

# '''
# 乐观期
# '''
# df_mktret = df_mktret[df_mktret.index < 20180401]
# df_coin_pri = df_coin_pri[df_coin_pri.index < 20180401]
# df_coin_vol = df_coin_vol[df_coin_vol.index < 20180401]

'''
momentum with volume
'''
ks = [3, 7, 13]
# max_days = [3, 5, 7, 14]

# hs = [3, 6, 9, 12, 15, 18, 24]  # 传统的持有期，from 蔡显军
# js = [3, 6, 12, 18, 24, 30]  # 传统的形成期
# 还没用过
hs = [10,20,30,40,50,60,70]  # 传统的持有期，from 蔡显军
js = [20, 40, 60, 70]  # 传统的形成期
fee = 0.003
lb = 5
'''
traditional momentum
'''
df_t_stats_trad_jk = pd.DataFrame(
    columns=['j', 'h', 'winner_mon', 'winner_t', 'loser_t', 'loser_mon', 'mean', 't_com', 't_sim'])
# df_t_stats_trad_excessret = pd.DataFrame(
#     columns=['j', 'h', 'winner_mon', 'winner_t', 'loser_t', 'loser_mon', 'mean', 't_com', 't_sim'])
df_t_stats_trad_mv = pd.DataFrame(
    columns=['k', 'h', 'winner_mon', 'winner_t', 'loser_t', 'loser_mon', 'mean', 't_com', 't_sim'])
df_t_stats_trad_mv2 = pd.DataFrame(
    columns=['k', 'h', 'winner_mon', 'winner_t', 'loser_t', 'loser_mon', 'mean', 't_com', 't_sim'])

for j in js:
    for h in hs:
        # simple cumulated return
        df_momentum_trad = momentum_calculation.calculate_trad_momentum50(df_coin_pri, j)
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
            'results/traditional_150/inv_sent/trad_cumulated_ret/df_group_return' + '_j_' + str(j) + '_h_' + str(
                h) + '_mean_' + str(
                np.round(ave_trad_mon, 4)) + '_t_' + str(np.round(t_stats_trad_com, 4)) + '.csv')
        df_coin_selected_trad.to_csv(
            'results/traditional_150/inv_sent/trad_cumulated_ret/df_stk_selected' + '_j_' + str(j) + '_h_' + str(
                h) + '_mean_' + str(
                np.round(ave_trad_mon, 4)) + '_t_' + str(np.round(t_stats_trad_com, 4)) + '.csv')

df_t_stats_trad_jk.to_csv('invsent_150_coins_trad_5groups_jk_lb_' + str(lb) + '_simplecumulated_mom(去除异常收益率).csv')

for k in ks:  # 上溯天数
    # for j in js:
    for h in hs:
        # '''
        # # trad , excess return
        # # '''
        # df_momentum_trad = momentum_calculation.calculate_trad_momentum(df_mktret, df_coin_pri, j)
        # df_group_return_trad, df_coin_selected_trad, winner_ave_trad, loser_ave_trad, winner_t_trad, loser_t_trad, ave_trad, t_trad_com, t_trad_sim = momentum_calculation.portfolio_formation(
        #     df_momentum_trad, df_coin_pri, h, lb, fee)
        #
        # winner_mon_trad = np.power(1 + winner_ave_trad, 30 / h) - 1
        # loser_mon_trad = np.power(1 + loser_ave_trad, 30 / h) - 1
        # ave_mon_trad = np.power(1 + ave_trad, 30 / h) - 1
        #
        # df_t_stats_trad_excessret = df_t_stats_trad_excessret.append(
        #     pd.Series([h, j, winner_mon_trad, loser_mon_trad, winner_t_trad, loser_t_trad, ave_mon_trad, t_trad_com,
        #                t_trad_sim],
        #               index=['h', 'j', 'winner_mon', 'loser_mon', 'winner_t', 'loser_t', 'mean', 't_com', 't_sim']),
        #     ignore_index=True)
        # df_group_return_trad.to_csv(
        #     'results/traditional_150/trad_excess_ret/df_group_return_k_' + str(k) + '_h_' + str(h) + '_mean_' + str(
        #         np.round(ave_mon_trad, 4)) + '_t_' + str(np.round(t_trad_com, 4)) + '.csv')
        # df_coin_selected_trad.to_csv(
        #     'results/traditional_150/trad_excess_ret/df_stk_selected_k_' + str(k) + '_h_' + str(h) + '_mean_' + str(
        #         np.round(ave_mon_trad, 4)) + '_t_' + str(np.round(t_trad_com, 4)) + '.csv')

        '''
        不需要j
        '''

        # trad_mv
        df_momentum_trad_mv = momentum_calculation.calculate_vol_mom(df_coin_pri, df_coin_vol, df_mktret, k,
                                                                     'mv')
        df_group_return_trad_mv, df_coin_selected_trad_mv, winner_ave_mv, loser_ave_mv, winner_t_mv, loser_t_mv, ave_trad_mv, t_trad_com_mv, t_trad_sim_mv = momentum_calculation.portfolio_formation(
            df_momentum_trad_mv, df_coin_pri, h, lb, fee)
        winner_mon_trad_mv = np.power(1 + winner_ave_mv, 30 / h) - 1
        loser_mon_trad_mv = np.power(1 + loser_ave_mv, 30 / h) - 1
        # ave_mon_trad_mv = np.power(1 + ave_trad_mv, 30 / h) - 1
        ave_mon_trad_mv = winner_mon_trad_mv - loser_mon_trad_mv

        df_t_stats_trad_mv = df_t_stats_trad_mv.append(
            pd.Series([h, k, winner_mon_trad_mv, loser_mon_trad_mv, winner_t_mv, loser_t_mv, ave_mon_trad_mv,
                       t_trad_com_mv, t_trad_sim_mv],
                      index=['h', 'k', 'winner_mon', 'loser_mon', 'winner_t', 'loser_t', 'mean', 't_com', 't_sim']),
            ignore_index=True)
        df_group_return_trad_mv.to_csv(
            'results/traditional_150/inv_sent/mv/df_group_return_k_' + str(k) + '_h_' + str(h) + '_mean_' + str(
                np.round(ave_mon_trad_mv, 4)) + '_t_' + str(np.round(t_trad_com_mv, 4)) + '.csv')
        df_coin_selected_trad_mv.to_csv(
            'results/traditional_150/inv_sent/mv/df_stk_selected_k_' + str(k) + '_h_' + str(h) + '_mean_' + str(
                np.round(ave_mon_trad_mv, 4)) + '_t_' + str(np.round(t_trad_com_mv, 4)) + '.csv')

        # trad_mv2
        df_momentum_trad_mv2 = momentum_calculation.calculate_vol_mom(df_coin_pri, df_coin_vol, df_mktret, k,
                                                                      'mv2')
        df_group_return_trad_mv2, df_coin_selected_trad_mv2, winner_ave_mv2, loser_ave_mv2, winner_t_mv2, loser_t_mv2, ave_trad_mv2, t_trad_com_mv2, t_trad_sim_mv2 = momentum_calculation.portfolio_formation(
            df_momentum_trad_mv2, df_coin_pri, h, lb, fee)

        winner_mon_trad_mv2 = np.power(1 + winner_ave_mv2, 30 / h) - 1
        loser_mon_trad_mv2 = np.power(1 + loser_ave_mv2, 30 / h) - 1
        # ave_mon_trad_mv2 = np.power(1 + ave_trad_mv2, 30 / h) - 1
        ave_mon_trad_mv2 = winner_mon_trad_mv2 - loser_mon_trad_mv2

        df_t_stats_trad_mv2 = df_t_stats_trad_mv2.append(
            pd.Series([h, k, winner_mon_trad_mv2, loser_mon_trad_mv2, winner_t_mv2, loser_t_mv2, ave_mon_trad_mv2,
                       t_trad_com_mv2, t_trad_sim_mv2],
                      index=['h', 'k', 'winner_mon', 'loser_mon', 'winner_t', 'loser_t', 'mean', 't_com', 't_sim']),
            ignore_index=True)
        df_group_return_trad_mv2.to_csv(
            'results/traditional_150/inv_sent/mv2/df_group_return_k_' + str(k) + '_h_' + str(h) + '_mean_' + str(
                np.round(ave_mon_trad_mv2, 4)) + '_t_' + str(np.round(t_trad_com_mv2, 4)) + '.csv')
        df_coin_selected_trad_mv2.to_csv(
            'results/traditional_150/inv_sent/mv2/df_stk_selected_k_' + str(k) + '_h_' + str(h) + '_mean_' + str(
                np.round(ave_mon_trad_mv2, 4)) + '_t_' + str(np.round(t_trad_com_mv2, 4)) + '.csv')

# df_t_stats_trad_excessret.to_csv('invsent_150_coins_test_trad_excessret_lb_' + str(lb) + '_k_short_h.csv')
df_t_stats_trad_mv.to_csv('invsent_150_coins_test_trad_lb_' + str(lb) + 'k_short_h_mv（去除异常收益率）.csv')
df_t_stats_trad_mv2.to_csv('invsent_150_coins_test_trad_lb_' + str(lb) + 'k_short_h_mv2（去除异常收益率）.csv')

# '''
# MAX related
# '''
#
# df_t_stats_MAX = pd.DataFrame(columns=['h', 'max_day','winner_mon', 'loser_mon','winner_t', 'loser_t', 'mean', 't_com','t_sim'])
# df_t_stats_MAX_mv = pd.DataFrame(columns=['k', 'h', 'max_day','winner_mon', 'loser_mon', 'winner_t', 'loser_t','mean', 't_com','t_sim'])
# df_t_stats_MAX_mv2 = pd.DataFrame(columns=['k', 'h', 'max_day','winner_mon', 'loser_mon', 'winner_t', 'loser_t','mean', 't_com','t_sim'])
#
# for h in hs:
#     for mday in max_days:
#         # MAX
#         df_MAX = momentum_calculation.calculate_MAX(df_coin_pri, df_mktret, mday)
#         df_group_return_MAX, df_coin_selected_MAX, winner_ave_MAX, loser_ave_MAX, winner_t_MAX, loser_t_MAX, ave_MAX, t_com_MAX, t_sim_MAX = momentum_calculation.portfolio_formation(
#             df_MAX, df_coin_pri, h, lb, fee)
#
#         winner_mon_MAX = np.power(1 + winner_ave_MAX, 30 / h) - 1
#         loser_mon_MAX = np.power(1 + loser_ave_MAX, 30 / h) - 1
#         ave_mon_MAX = np.power(1 + ave_MAX, 30 / h) - 1
#
#         df_t_stats_MAX = df_t_stats_MAX.append(
#             pd.Series([h, mday, winner_mon_MAX, loser_mon_MAX, winner_t_MAX, loser_t_MAX, ave_mon_MAX,
#                             t_com_MAX, t_sim_MAX],
#                       index=['h', 'max_day','winner_mon', 'loser_mon','winner_t', 'loser_t', 'mean', 't_com','t_sim']),
#             ignore_index=True)
#         df_group_return_MAX.to_csv(
#                     'results/MAX_150/MAX/df_group_return_' + '_h_' + str(h) + '_mday_'+str(mday)+'_mean_' + str(
#                         np.round(ave_mon_MAX, 4)) + '_t_' + str(np.round(t_com_MAX, 4)) + '.csv')
#         df_coin_selected_MAX.to_csv(
#                     'results/MAX_150/MAX/df_stk_selected_' + '_h_' + str(h) +'_mday_'+str(mday)+ '_mean_' + str(
#                         np.round(ave_mon_MAX, 4)) + '_t_' + str(np.round(t_com_MAX, 4)) + '.csv')
#
#
# df_t_stats_MAX.to_csv('150_coins_test_MAX_h.csv')
#
# for k in ks:
#     for h in hs:
#         for mday in max_days:
#             # MAX_mv
#             df_momentum_MAX_mv = momentum_calculation.calculate_MAX_with_volume(df_coin_pri, df_mktret, df_coin_vol,
#                                                                                 mday, k, 'mv')
#             df_group_return_MAX_mv, df_coin_selected_MAX_mv, winner_ave_MAX_mv, loser_ave_MAX_mv, winner_t_MAX_mv, loser_t_MAX_mv, ave_MAX_mv, t_com_MAX_mv, t_sim_MAX_mv  = momentum_calculation.portfolio_formation(
#                 df_momentum_MAX_mv, df_coin_pri,h,lb, fee)
#
#             winner_mon_MAX_mv = np.power(1 + winner_ave_MAX_mv, 30 / h) - 1
#             loser_mon_MAX_mv = np.power(1 + loser_ave_MAX_mv, 30 / h) - 1
#             ave_mon_MAX_mv = np.power(1 + ave_MAX_mv, 30 / h) - 1
#
#             df_t_stats_MAX_mv = df_t_stats_MAX_mv.append(
#                 pd.Series([k,h, mday, winner_mon_MAX_mv, loser_mon_MAX_mv, winner_t_MAX_mv, loser_t_MAX_mv, ave_mon_MAX_mv,
#                             t_com_MAX_mv, t_sim_MAX_mv],
#                       index=['k','h', 'max_day','winner_mon', 'loser_mon','winner_t', 'loser_t', 'mean', 't_com','t_sim']),
#             ignore_index=True)
#
#             df_group_return_MAX_mv.to_csv(
#                 'results/MAX_150/MAX_mv/df_group_return_k_'+str(k) + '_h_' + str(h) + '_mday_' + str(mday) + '_mean_' + str(
#                     np.round(ave_mon_MAX_mv, 4)) + '_t_' + str(np.round(t_com_MAX_mv, 4)) + '.csv')
#             df_coin_selected_MAX_mv.to_csv(
#                 'results/MAX_150/MAX_mv/df_stk_selected_k_'+str(k)  + '_h_' + str(h) + '_mday_' + str(
#                     mday) + '_mean_' + str(
#                     np.round(ave_mon_MAX_mv, 4)) + '_t_' + str(np.round(t_com_MAX_mv, 4)) + '.csv')
#
#             # MAX_mv2
#             df_momentum_MAX_mv2 = momentum_calculation.calculate_MAX_with_volume(df_coin_pri, df_mktret, df_coin_vol,
#                                                                         mday, k, 'mv2')
#             df_group_return_MAX_mv2, df_coin_selected_MAX_mv2, winner_ave_MAX_mv2, loser_ave_MAX_mv2, winner_t_MAX_mv2, loser_t_MAX_mv2, ave_MAX_mv2, t_com_MAX_mv2, t_sim_MAX_mv2 = momentum_calculation.portfolio_formation(
#                 df_momentum_MAX_mv2, df_coin_pri, h, lb, fee)
#
#             winner_mon_MAX_mv2 = np.power(1 + winner_ave_MAX_mv2, 30 / h) - 1
#             loser_mon_MAX_mv2 = np.power(1 + loser_ave_MAX_mv2, 30 / h) - 1
#             ave_mon_MAX_mv2 = np.power(1 + ave_MAX_mv2, 30 / h) - 1
#
#             df_t_stats_MAX_mv2 = df_t_stats_MAX_mv.append(
#                 pd.Series(
#                     [k, h, mday, winner_mon_MAX_mv2, loser_mon_MAX_mv2, winner_t_MAX_mv2, loser_t_MAX_mv2, ave_mon_MAX_mv2,
#                      t_com_MAX_mv2, t_sim_MAX_mv2],
#                     index=['k', 'h', 'max_day', 'winner_mon', 'loser_mon', 'winner_t', 'loser_t', 'mean', 't_com',
#                            't_sim']),
#                 ignore_index=True)
#
#             df_group_return_MAX_mv2.to_csv(
#                 'results/MAX_150/MAX_mv2/df_group_return_k_' + str(k) + '_h_' + str(h) + '_mday_' + str(
#                     mday) + '_mean_' + str(
#                     np.round(ave_mon_MAX_mv2, 4)) + '_t_' + str(np.round(t_com_MAX_mv2, 4)) + '.csv')
#             df_coin_selected_MAX_mv2.to_csv(
#                 'results/MAX_150/MAX_mv2/df_stk_selected_k_' + str(k) + '_h_' + str(h) + '_mday_' + str(
#                     mday) + '_mean_' + str(
#                     np.round(ave_mon_MAX_mv2, 4)) + '_t_' + str(np.round(t_com_MAX_mv2, 4)) + '.csv')
#
# df_t_stats_MAX_mv.to_csv('150_coins_test_MAX_k_h_mv.csv')
# df_t_stats_MAX_mv2.to_csv('150_coins_test_MAX_k_h_mv2.csv')
