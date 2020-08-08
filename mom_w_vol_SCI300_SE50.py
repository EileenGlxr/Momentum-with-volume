import pandas as pd
import numpy as np
from momentum_calculation import momentum_calculation

df_csi300 = pd.read_csv('data/CSI300_index.csv', index_col=0)
df_se50stk_pri = pd.read_csv('data/SE50_stks_price.csv', index_col=0)
df_se50stk_vol = pd.read_csv('data/SE50_stks_volume.csv', index_col=0)

df_se50stk_pri.fillna(method='ffill', axis=0, inplace=True)
df_se50stk_vol.fillna(method='ffill', axis=0, inplace=True)

df_mktret = df_csi300['close'].pct_change(1).dropna()
df_rstk = df_se50stk_pri.pct_change(1).dropna()

'''
traditional momentum(only check the price)
'''

'''
momentum with volume
'''
ks = [21, 55, 90]
hs = [3,5,10,14,15,20,21,22,30]
df_t_stats = pd.DataFrame(columns=['k', 'h', 'mean', 't'])
for k in ks:
    for h in hs:
        if h <= k:
            df_group_return,df_stk_selected, ave, t_stats = momentum_calculation.vol_momentum(df_se50stk_pri, df_se50stk_vol, df_mktret, k, h)
            df_group_return.to_csv('data/sci300_se50/df_group_return_k_'+str(k)+'_h_'+str(h)+'_mean_'+str(ave)+'_t_'+str(t_stats)+'.csv')
            df_stk_selected.to_csv('data/sci300_se50/df_coin_selected_k_'+str(k)+'_h_'+str(h)+'_mean_'+str(ave)+'_t_'+str(t_stats)+'.csv')
            df_t_stats = df_t_stats.append(pd.Series([k, h, ave, t_stats], index=['k', 'h', 'mean', 't']),
                                       ignore_index=True)

df_t_stats.to_csv('stk_test_k_h.csv')