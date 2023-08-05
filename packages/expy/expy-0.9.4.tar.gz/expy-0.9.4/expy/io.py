import numpy as np
import pandas as pd
import os
import re
import os

from expy import shared

'''IO class'''
# 读取配置文件
# 【参数】 path：文件路径
# 【返回值】配置变量
def readSetting(path='setting.txt'):
    setting = dict()
    with open(path) as f:
        try:
            for s in re.compile(r'[-]{2,}').split(f.read()):
                if len(s)>0:
                    if s[0]=='\n': s = s[1:]
                    if s[-1]=='\n': s = s[:-1]

                    name,*content = s.split('\n')
                    setting[name[1:-1]] = content

            if 'timingSet' in setting:
                # Set timing of each phase
                for dur in setting['timingSet']:
                    k,v = dur.replace(' ','').split(':')
                    if '-' in v:
                        limit = v.split('-')
                        shared.timing[k] = [int(limit[0]),int(limit[1])]
                    else:
                        shared.timing[k] = int(v)
        except:
            raise ValueError('Please check your setting.txt!')
    return setting

# get stimuli in a csv file
# 读取csv数据文件，得到实验刺激材料
# 【参数】 filepath：csv数据文件的路径
# 【返回值】Pandas数组，存储了csv数据文件的内容
def readStimuli(filepath,blockID=None,sheetname=0):
    if filepath.split('.')[-1]=='csv':
        stimuli = pd.read_csv(filepath,sep=',',encoding='gbk')
    elif filepath.split('.')[-1] in ['xls','xlsx']:
        stimuli = pd.read_excel(filepath,sep=',',sheetname=0)
    else:
        raise ValueError('Only support csv and Excel file')
    if blockID:
        # stimuli = stimuli[stimuli[blockID[0]]==blockID[1]]
        stimuli = stimuli[stimuli[blockID[0]]==blockID[1]].sample(n=4)
    stimuli.index = range(len(stimuli))
    return stimuli

# 读取一个文件夹下的文件
# 【参数】 dirpath：csv数据文件的路径
# 【返回值】文件列表
def readDir(dirpath,shuffle=True):
    files = [dirpath+f for f in os.listdir(dirpath)]
    if shuffle:
        np.random.shuffle(files)
    return files

# 将反应时数据叠加到原始刺激数据上，生成名为{subjID}_{blockID}_result的csv文件
# 【参数】 blockID：本block的序号, stimuli: 刺激信息, resp：反应数据的Pandas数组
# 【返回值】无
def saveResult(blockID, resp, columns=['respKey','RT'], stim=None, stim_columns=None):
    if not os.path.exists('result'):
        os.mkdir('result')
    result = pd.DataFrame(resp,columns=columns)
    if not stim is None:
        if type(stim) is list:
            stim = pd.DataFrame(stim,columns=stim_columns)
        result = stim.join(result)

    result.to_csv('result\\'+shared.subj+'_'+str(blockID)+'_result.csv',index=None)

# send trigger
def sendTrigger(data, mode='P'):
    try:
        if mode=='P':
            shared.Objdll.Out32(shared.setting['port'],0)
        elif mode=='S': 
            shared.ser.write(bytes(data,encoding='utf-8')) # send a string which might change
            # shared.ser.write(b'something') # send a string directly

            # n=int('0b00010001',2)
            # shared.ser.write(n.to_bytes((n.bit_length()+7)//8, 'big')) # send a binary code
        else:
            raise ValueError('Only support "S" or "P" (serial/parallel) mode!')
    except:
        print('The port might be closed.')

