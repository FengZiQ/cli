# coding=utf-8

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyLogoutInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify logout invalid option</b>")
    
    command = ['logout -x']
    
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        
        result = SendCmd(c, com)
        
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
            
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify logout invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
        
    return FailFlag

def verifyLogoutInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify logout invalid parameters</b>")
    
    result = SendCmd(c, 'logout test')
    
    if "Error (" not in result or "Invalid setting parameters" not in result:
         FailFlag = True
         tolog('\n<font color="red">Fail: logout </font>')
        
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify logout invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
        
    return FailFlag

def verifyLogout(c):
    FailFlag = False
    tolog("<b>Verify logout </b>")
    
    result = SendCmd(c, 'logout')
    
    if 'Error (' in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: logout </font>')
        
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify logout </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyLogoutInvalidOption(c)
    verifyLogoutInvalidParameters(c)
    verifyLogout(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped