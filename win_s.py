import win32serviceutil
import psutil
import os,sys,inspect

def all_win_service():
    list_service=[]
    for i in psutil.win_service_iter():    #лист всех служб win
        list_service.append(i)
    return list_service
    
def wr_to_file_list_service(list_service):
    path=os.path.dirname(os.path.abspath(__file__))
    path=os.path.join(path,'s_win.txt')
    with  open (path,'w',encoding='utf8',newline='') as fw:
        fw.write(str(list_service))
        fw.close()
    return str(list_service)

def service_running(service, machine):
    status = (win32serviceutil.QueryServiceStatus(service)[1] == 4)
    if not status:
        import time
        time.sleep(3)
        status = (win32serviceutil.QueryServiceStatus(service)[1] == 4)
    return status



def service_info(action, machine, service):
    running = service_running(service, machine)
    servnam = 'service (%s) on machine(%s)'%(service, machine)
    action = action.lower(  )
    if action == 'stop':
        if not running:
            print ("Can't stop, %s not running"%servnam)
            return 0
        win32serviceutil.StopService(service, machine)
        running = service_running(service, machine)
        if running:
            print ("Can't stop %s (???)"%servnam)
            return 0
        print ('%s stopped successfully' % servnam)
    elif action == 'start':
        if running:
            print ("Can't start, %s already running"%servnam)
            return 0
        try:
            win32serviceutil.StartService(service, machine)
        except Exception:
            print( 'Не удалось запустить дочернюю службу.')
        running = service_running(service, machine)
        if not running:
            print ("Can't start %s (???)"%servnam)
            return 0
        print ('%s started successfully' % servnam)
    elif action == 'restart':
        if not running:
            print ("Can't restart, %s not running"%servnam)
            return 0
        win32serviceutil.RestartService(service, machine)
        running = service_running(service, machine)
        if not running:
            print ("Can't restart %s (???)"%servnam)
            return 0
        print ('%s restarted successfully' % servnam)
    elif action == 'status':
        if running:
            print ("%s is running" % servnam)
        else:
            print ("%s is not running" % servnam)
    else:
        print ("Unknown action (%s) requested on %s"%(action, servnam))


if __name__ == '__main__':
    machine = None
    service= 'AdobeARMservice'       
    print(win32serviceutil.QueryServiceStatus(service),(win32serviceutil.QueryServiceStatus(service)[1] == 4))
    service = 'AdobeARMservice'
    action = 'start'
    #action = 'stop'
    service_info(action, machine, service)
