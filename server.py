import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import os
import sys
import subprocess


class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MyPythonServer"
    _svc_display_name_ = "My Python Server"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_alive = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False
    
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        self.main()

    def main(self):
        os.chdir(os.path.dirname(sys.argv[0]))
        subprocess.call("python C:\\python\\app.py", stdout=subprocess.PIPE, shell=True)
        # subprocess.call()

        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
    

if __name__ == '__main__':
    print("running")
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyService)