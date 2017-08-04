
# initial version
# March 20, 2017

buildserverurl="http://192.168.208.5/release/hyperion_ds/daily/"
fcsserverurl="http://192.168.208.5/release/hyperion_ds/fcs/"
tftpserver="root@10.84.2.99:/work/tftpboot/"
serv = "MjExLjE1MC42NS44MQ=="
u = "amFja3kubGlAY24ucHJvbWlzZS5jb20="
p = "NzcwMjE0WHA="

import requests
from bs4 import BeautifulSoup

import os
import glob
import time
def getnewbuild():


    download=False
    # get the current build folder

    files=glob.glob("/work/tftpboot/d5k-multi*.ptif")
    tftpbuildnumber120=0
    tftpbuildnumber121=0
    tftpbuildnumber122 = 0
    tftpbuildnumber13 = 0

    tmp120=tmp121=tmp122=tmp13=0
    for file in files:
        try:
            if int(file[25:27])==12 and int(file[28])==2:
                tmp122=int(file[-7:-5])

            elif int(file[25:27])==12 and int(file[28])==1:
                tmp121=int(file[-7:-5])

            elif int(file[25:27])==12 and int(file[28])==0:
                tmp120 = int(file[-7:-5])

            elif int(file[25:27]) == 13:
                tmp13 = int(file[-7:-5])
        except:
            tmp120=0
            tmp121 = 0
            tmp122 = 0
            tmp13=0

        if tmp120>tftpbuildnumber120:
           tftpbuildnumber120=tmp120
        if tmp121>tftpbuildnumber121:
           tftpbuildnumber121=tmp121
        if tmp122>tftpbuildnumber122:
           tftpbuildnumber122=tmp122
        if tmp13>tftpbuildnumber13:
           tftpbuildnumber13=tmp13

    # print "current build is %d" %tftpbuildnumber
    # to get the full directory list
    soup = BeautifulSoup(requests.get(buildserverurl).text)
    fcssoup=BeautifulSoup(requests.get(fcsserverurl).text)
    buildnumber120 = list()
    buildnumber121 = list()
    buildnumber122 = list()
    buildnumber13 = list()
    for link in soup.find_all('a'):
        tmp = link.get('href')
        if "13." in tmp:
            buildnumber13.append(tmp)
        if "12.00" in tmp:
            buildnumber120.append(tmp)
        if "12.01" in tmp:
            buildnumber121.append(tmp)
        if "12.02" in tmp:
            buildnumber122.append(tmp)

    for link in fcssoup.find_all('a'):
        print link
        tmp = link.get('href')
        print tmp
        if "13_" in tmp:
            buildnumber13.append(tmp)


    try:

        webupdatedbuild120=int((buildnumber120[-1].replace("/","").split(".")[-1]))
        webupdatedbuild121 = int((buildnumber121[-1].replace("/", "").split(".")[-1]))
        webupdatedbuild122 = int((buildnumber122[-1].replace("/", "").split(".")[-1]))

        webupdatedbuild13 = int((buildnumber13[-1].replace("/", "").split("_")[-1]))
    except:
        webupdatedbuild120=0
        webupdatedbuild121=0
        webupdatedbuild122 = 0
        webupdatedbuild13 = 0

    #print "webupdatedbuildnumbers are %d,%d" %(webupdatedbuild12,webupdatedbuild13)
#   if the webupdated build is newer than the installed one, download the new build
#   file list contains the filename to be updated on the host
    filelist=list()
    print "webupdatebuild120,webupdatedbuild121,tftpbuildnumber120,tftpbuildnumber121,tftpbuildnumber122",webupdatedbuild120,webupdatedbuild121,tftpbuildnumber120,tftpbuildnumber121,webupdatedbuild122
    print "webupdatebuild13,tptpbuildnumber13", webupdatedbuild13, tftpbuildnumber13
    if webupdatedbuild13 >tftpbuildnumber13:
        download=True
        Pfile = open('downloadedfiles', 'w')
        Pfile.close()
        #for filetype in ("conf", "multi"):
        for filetype in ("conf", "multi", "bios", "fw", "lib", "oem", "sw", "usr", "base"):

            if filetype=="base":
                filename="d5k-"+filetype+"-"+(buildnumber13[-1].replace("/","")).replace(".","_").replace("13_00","13_0")+".raw.gz"

            else:
                filename="d5k-"+filetype+"-"+(buildnumber13[-1].replace("/","")).replace(".","_").replace("13_00","13_0")+".ptif"
            os.system("wget "+fcsserverurl+buildnumber13[-1]+filename)
            # os.system("scp "+ filename +" "+tftpserver)
            # filename="d5k-"+filetype+"-"+webupdatedbuild.replace(".","_").replace("00","0")+".ptif"
            #
            #os.system("wget " + buildserverurl + buildnumber[-1] + "/" + filename)

            timestr=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            os.system("echo " + timestr +" downloaded %s" % filename +" >> downloadedfiles")
            os.system("mv /root/d5k* /work/tftpboot/")

            os.system("mv ./d5k* /work/tftpboot/")

    if webupdatedbuild120 > tftpbuildnumber120:
        download = True
        Pfile = open('downloadedfiles', 'w')
        Pfile.close()
        # for filetype in ("conf", "multi"):
        for filetype in ("conf", "multi", "bios", "fw", "lib", "oem", "sw", "usr", "base"):

            if filetype == "base":
                filename = "d5k-" + filetype + "-" + (buildnumber120[-1].replace("/", "")).replace(".", "_").replace(
                    "12_00", "12_0") + ".raw.gz"

            else:
                filename = "d5k-" + filetype + "-" + (buildnumber120[-1].replace("/", "")).replace(".", "_").replace(
                    "12_00", "12_0") + ".ptif"
            os.system("wget " + buildserverurl + buildnumber120[-1] + filename)
            # os.system("scp "+ filename +" "+tftpserver)
            # filename="d5k-"+filetype+"-"+webupdatedbuild.replace(".","_").replace("00","0")+".ptif"
            #
            # os.system("wget " + buildserverurl + buildnumber[-1] + "/" + filename)

            timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            os.system("echo " + timestr + " downloaded %s" % filename + " >> downloadedfiles")
            os.system("mv /root/d5k* /work/tftpboot/")

            os.system("mv ./d5k* /work/tftpboot/")
    if webupdatedbuild121 > tftpbuildnumber121:
        download = True
        Pfile = open('downloadedfiles', 'w')
        Pfile.close()
        # for filetype in ("conf", "multi"):
        for filetype in ("conf", "multi", "bios", "fw", "lib", "oem", "sw", "usr", "base"):

            if filetype == "base":
                filename = "d5k-" + filetype + "-" + (buildnumber121[-1].replace("/", "")).replace(".", "_").replace(
                    "12_01", "12_1") + ".raw.gz"

            else:
                filename = "d5k-" + filetype + "-" + (buildnumber121[-1].replace("/", "")).replace(".", "_").replace(
                    "12_01", "12_1") + ".ptif"
            os.system("wget " + buildserverurl + buildnumber121[-1] + filename)
            # os.system("scp "+ filename +" "+tftpserver)
            # filename="d5k-"+filetype+"-"+webupdatedbuild.replace(".","_").replace("00","0")+".ptif"
            #
            # os.system("wget " + buildserverurl + buildnumber[-1] + "/" + filename)

            timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            os.system("echo " + timestr + " downloaded %s" % filename + " >> downloadedfiles")
            os.system("mv /root/d5k* /work/tftpboot/")

            os.system("mv ./d5k* /work/tftpboot/")

    if webupdatedbuild122 > tftpbuildnumber122:
        download = True
        Pfile = open('downloadedfiles', 'w')
        Pfile.close()
        # for filetype in ("conf", "multi"):
        for filetype in ("conf", "multi", "bios", "fw", "lib", "oem", "sw", "usr", "base"):

            if filetype == "base":
                filename = "d5k-" + filetype + "-" + (buildnumber122[-1].replace("/", "")).replace(".", "_").replace(
                    "12_02", "12_2") + ".raw.gz"

            else:
                filename = "d5k-" + filetype + "-" + (buildnumber122[-1].replace("/", "")).replace(".", "_").replace(
                    "12_02", "12_2") + ".ptif"
            os.system("wget " + buildserverurl + buildnumber122[-1] + filename)
            # os.system("scp "+ filename +" "+tftpserver)
            # filename="d5k-"+filetype+"-"+webupdatedbuild.replace(".","_").replace("00","0")+".ptif"
            #
            # os.system("wget " + buildserverurl + buildnumber[-1] + "/" + filename)

            timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            os.system("echo " + timestr + " downloaded %s" % filename + " >> downloadedfiles")
            os.system("mv /root/d5k* /work/tftpboot/")

            os.system("mv ./d5k* /work/tftpboot/")

    return download

if __name__ == "__main__":

    timestr=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    os.system("echo %s \" Trying to download files\" >> downloadedfiles" %timestr )
    download=getnewbuild()
    if download==True:
        import smtplib

        # Import the email modules we'll need
        from email.mime.text import MIMEText

        # Open a plain text file for reading.  For this example, assume that
        # the text file contains only ASCII characters.
        textfile="downloadedfiles"
        fp = open(textfile, 'rb')
        buildversion=fp.readline()[-18:-6]
        tofile=open("buildnum","w")
        tofile.write(buildversion.replace("_","."))
        tofile.close()
        # os.system("scp /root/buildnum root@192.168.252.106:/opt/testlink-1.9.16-0/apache2/htdocs/srvpool/")
        # os.system("scp /work/jackyl/buildnum root@192.168.252.106:/opt/testlink-1.9.16-0/apache2/htdocs/srvpool/")
        time.sleep(1)
        os.system("scp /root/buildnum root@10.84.2.66:/home/work/jackyl/Scripts/clitest/")
        # os.system("scp /work/jackyl/buildnum root@10.84.2.66:/home/work/jackyl/Scripts/clitest/")
        time.sleep(1)
        # Create a text/plain message
        msg = MIMEText(fp.read())
        fp.close()

        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = 'New build is available at 10.84.2.99:/work/tftpboot/, please see the %s for detail' % textfile
        msg['From'] = 'jacky.li@cn.promise.com'
        msg['To'] = 'jacky.li@cn.promise.com'
        # Send the message via our own SMTP server, but don't include the
        rec = ['ken.hou@cn.promise.com','tracy.you@cn.promise.com','travis.tang@cn.promise.com','xin.wang@cn.promise.com','lily.zhao@cn.promise.com','lisa.xu@cn.promise.com','jacky.li@cn.promise.com','zach.feng@cn.promise.com','socrates.su@cn.promise.com','paul.diao@cn.promise.com','hulda.zhao@cn.promise.com']
        #rec = ['zach.feng@cn.promise.com','jacky.li@cn.promise.com','hulda.zhao@cn.promise.com']
        # Send the message via our own SMTP server, but don't include the
        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        u=u.decode('base64')
        serv=serv.decode('base64')
        p=p.decode('base64')


        s = smtplib.SMTP(serv)
        s.login(u,p)
        s.sendmail(msg['From'], rec, msg.as_string())
        s.quit()
