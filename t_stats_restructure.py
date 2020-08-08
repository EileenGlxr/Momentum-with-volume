import pandas as pd
import os
import numpy as np

import os


# os.walk方法获取当前路径下的root（所有路径）、dirs（所有子文件夹）、files（所有文件）

def file_name(path):
    F = []
    for root, dirs, files in os.walk(path):
        # print root
        # print dirs
        for file in files:
            # print file.decode('gbk')    #文件名中有中文字符时转码
            if os.path.splitext(file)[1] == '.csv':
                t = os.path.splitext(file)[0]
                print(t)  # 打印所有py格式的文件名
                F.append(t)  # 将所有的文件名添加到L列表中
    return F  # 返回L列表


path = 'results/t_stats/drop_out_abs/pess short'
csv_names = file_name(path)

for csv in csv_names:
    df = pd.read_csv(path + '/' + csv + '.csv')
    df_cols = df.columns

    if 'k' in df_cols:
        s = 'k'
    else:
        s = 'j'

    j_ks = df[s].unique().tolist()
    cols = df['h'].unique().tolist()

    df_mon_ret = pd.DataFrame(columns=cols + ['port'])
    df_t = pd.DataFrame(columns=cols + ['port'])

    win_los_mi = ['winner', 'loser', 'w_l']

    for j_k in j_ks:
        for row in win_los_mi:
            ser_ret = pd.Series(index=cols)
            ser_t = pd.Series(index=cols)
            for col in cols:
                ind = df.loc[(df[s] == j_k) & (df.h == col), df.columns[0]].values[0]
                ser_ret.loc['port'] = row
                ser_t.loc['port'] = row
                if row == 'winner':
                    for i in ser_ret.index:
                        ser_ret.loc[col] =np.round(df['winner_mon'].loc[ind],4)
                        ser_t.loc[col] = np.round(df['winner_t'].loc[ind],2)

                elif row == 'loser':
                    for i in ser_ret.index:
                        ser_ret.loc[col] = np.round(df['loser_mon'].loc[ind],4)
                        ser_t.loc[col] = np.round(df['loser_t'].loc[ind],2)
                else:
                    for i in ser_ret.index:
                        ser_ret.loc[col] = np.round(df['mean'].loc[ind],4)
                        ser_t.loc[col] = np.round(df['t_sim'].loc[ind],2)
            df_mon_ret = df_mon_ret.append(ser_ret, ignore_index=True)
            df_t=df_t.append(ser_t,ignore_index=True)
    df_mon_ret.to_csv(path + '/' + 'mon_ret_'+csv + '.csv')
    df_t.to_csv(path + '/' + 't_stats_'+csv + '.csv')
