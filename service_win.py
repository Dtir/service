import os,sys,inspect,json
from win_s import *

d_stop_list=['TermService','Browser']  #отказано в доступе, только ручное редактирование
#print(all_win_service())    #лист всех служб win
s1=(wr_to_file_list_service(all_win_service()))[2:-2]
sp=s1.split('WindowsService')
d={}
d_disp_name={}
for i in range(len(sp)):
# for i in range(5):
    si=sp[i].split(',')
    s_n=si[0].split('=')
    if len (si)>=2 and len (s_n)>=2:
        st=service_running(s_n[1][1:-1],None)
        print('name service  ',s_n[1][1:-1],st)
        d[s_n[1][1:-1]]=st
        d_disp_name[(si[1].split('=')[1][:-14])]=d
        d={}

for m in d_disp_name.keys():
    for k in d_disp_name[m].values():
        if k:
            print(m,k)          
path=os.path.dirname(os.path.abspath(__file__))
path=os.path.join(path,'s_win.json')
path_r=os.path.join(os.path.dirname(os.path.abspath(__file__)),'set_win_serv.json')
print('write  ',path)
print('read  ',path_r)
with  open (path,'w',encoding='utf8',newline='') as fw:
    ser_d=json.dumps(d_disp_name,indent=4,ensure_ascii=False)
    fw.write(ser_d)
fw.close()
k_set=input('файл set_win_serv.json сформирован? 1 - true')
service='TermService'
if k_set=='1':
    print('Процесс start/stop win service')
    with open(path_r,'r',encoding='utf8') as fr:
        data = fr.read()
        z = json.loads(data)
    for n_s in d_disp_name.keys():
        p_r=list(iter(d_disp_name[n_s].values()))[0]
        if n_s in z.keys():
            p_s=list(iter(z[n_s].values()))[0]
            service=list(iter(z[n_s].keys()))[0]
        else:
            p_s=p_r
        if service not in d_stop_list and p_r!=p_s:
            print('изменяется состояние ',service)
            if p_s:
                print('старт')
                service_info('start', None, service)
            else:
                print('стоп')
                service_info('stop', None, service)
        else:
            print('состояние службы не изменялось')
else:
    pr='''
  доступен для просмотра файл s_win.json
  состояние служб не изменено 
  нужно сформировать файл set_win_serv.json для запуска/останова служб        
        '''
    print(pr)
cl=10
while cl>0:
    # print(cl)
    cl=int(input('0 - выход'))
