from ssh_connect import *
from send_cmd import *


def install(c):

    file = open('/home/work/zach/clitest/target_release.txt', 'r')

    file_name = file.readline()

    print file_name

    SendCmd(c, 'ptiflash -y -t -s 10.84.2.99 -f ' + file_name)

    file.close()


if __name__ == "__main__":

    start = time.clock()
    c, ssh = ssh_conn()

    install(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped

