import requests
from bs4 import BeautifulSoup
import os
import datetime

build_server_url = "http://192.168.208.5/release/hyperion_ds/daily/"


def download():
    build_name = ''

    soup1 = BeautifulSoup(requests.get(build_server_url).text, 'html.parser', from_encoding='utf-8').text
    temp1 = soup1.split('\n')
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')

    temp2 = ''
    for t1 in temp1:
        if now_time + '-' in t1:
            temp2 = temp2 + t1.split('/')[0]

    if temp2:
        soup2 = BeautifulSoup(requests.get(build_server_url + temp2).text, 'html.parser', from_encoding='utf-8').text
        temp3 = soup2.split('\n')

        for t2 in temp3:
            if 'd5k-multi-' in t2:
                build_name = build_name + t2.split()[0]

        os.system('rm -f /home/tftpboot/' + build_name)
        os.system('wget -P /home/tftpboot/ ' + build_server_url + temp2 + '/' + build_name)

    os.system('echo ' + build_name + '>/home/zach/target_release.txt')
    os.system('scp /home/zach/target_release.txt root@10.84.2.66:/home/work/zach/clitest/')

if __name__ == "__main__":
    download()

