# --coding = utf-8--
from ssh_connect import check_ping
import time
from to_log import tolog


def SendCmd(c, cmdstr):

    data = ''

    if cmdstr.endswith('\n'):
        c.send(cmdstr)
    else:
        c.send(cmdstr + '\n')
    # time.sleep(1)

    while not c.exit_status_ready():

        if c.recv_ready():

            data += c.recv(2000)

        # add code for password in user
        # data=data.replace("[32D[32C[0m[?12l[?25h","").replace("[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m","")

        while data.endswith('?25h'):

                c.send("Local#123" + "\n")
                data += c.recv(2000)
                if data.endswith('@cli> '):
                    break
        if data.endswith('@cli> '):
            break

    while c.recv_ready():
        data += c.recv(2000)

        if data.endswith('@cli> '):
            break

    # removing the following chars to avoid
    # <Fault -32700: 'parse error. not well formed'>
    # when updating to TestLink

    data = data.replace(
        "\x1b[D \x1b[D", ""
    ).replace(
        '[?12l[?25h[?25l[32D[0m[J[0m', ''
    ).replace(
        "[32D[32C[0m[?12l[?25h", ''
    ).replace(
        "[?7h[0m[?12l[?25h[?2004l[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m", ''
    )

    tolog(data)

    return data


def SendCmdRestart(c, cmdstr):

    data = ''

    if cmdstr.endswith('\n'):
        c.send(cmdstr)
    else:
        c.send(cmdstr + '\n')
    # time.sleep(1)

    while not c.exit_status_ready():

        a = check_ping()
        if a == 0:
            if c.recv_ready():

                data += c.recv(2000)

            while data.endswith('?25h'):

                c.send("Local#123" + "\n")
                data += c.recv(2000)

                if data.endswith('@cli> '):
                    break

            if data.endswith('@cli> '):
                break

        else:
            tolog("Network connection lost.")
            break

    while c.recv_ready():
        data += c.recv(2000)

        if data.endswith('@cli> '):
            break

    data = data.replace(
        "\x1b[D \x1b[D", ""
    ).replace(
        '[?12l[?25h[?25l[32D[0m[J[0m', ''
    ).replace(
        "[32D[32C[0m[?12l[?25h", ''
    ).replace(
        "[?7h[0m[?12l[?25h[?2004l[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m", ''
    )

    tolog(data)

    return data


def SendCmdconfirm(c, cmdstr):

    data = ''

    ytrue = False

    if cmdstr.endswith('\n'):

        c.send(cmdstr)

    else:
        c.send(cmdstr + '\n')

    while not c.exit_status_ready():

        if c.recv_ready():

            data += c.recv(2000)

        while data.endswith('?25h'):

            if ytrue==False:

                c.send("y" + "\n")

                ytrue=True

                time.sleep(1)

                data += c.recv(2000)

                break

            if data.endswith('@cli> '):
                break

        if data.endswith('@cli> '):
            break

    while c.recv_ready():
        data += c.recv(2000)

        if data.endswith('@cli> '):
            break

    data = data.replace(
        "\x1b[D \x1b[D", ""
    ).replace(
        '[?12l[?25h[?25l[32D[0m[J[0m', ''
    ).replace(
        '[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[44D[0m', ''
    ).replace(
        "[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m", ''
    ).replace(
        "[32D[32C[0m[?12l[?25h", ''
    ).replace(
        "[?7h[0m[?12l[?25h[?2004l[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m", ''
    )

    tolog(data)

    return data


def SendCmdpassword(c, cmdstr,password):

    data = ''
    ytrue = False

    if cmdstr.endswith('\n'):
        c.send(cmdstr)

    else:
        c.send(cmdstr + '\n')

    while not c.exit_status_ready():

        if c.recv_ready():

            data += c.recv(2000)

        while data.endswith('?25h'):

            if ytrue == False:

                c.send(password + "\n")
                time.sleep(1)
                c.send(password + "\n")
                ytrue = True
                time.sleep(1)
                data += c.recv(2000)
                break

            if data.endswith('@cli> '):
                break

        if data.endswith('@cli> '):
            break

    while c.recv_ready():
        data += c.recv(2000)

        if data.endswith('@cli> '):
            break

    data = data.replace(
        "\x1b[D \x1b[D", ""
    ).replace(
        "[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m", ''
    ).replace(
        "[32D[32C[0m[?12l[?25h", ''
    ).replace(
        "[?7h[0m[?12l[?25h[?2004l[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m", ''
    ).replace(
        '[33D[33C[0m[?12l[?25h[?25l[33D[0m[J[0m', '\r\n'
    ).replace(
        "[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[45D[0m", ''
    ).replace(
        '[?7h[0m[?12l[?25h[?2004l', '\r\n'
    ).replace(
        '[?12l[?25h[?25l[32D[0m[J[0m', ''
    ).replace(
        '[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[44D[0m', ''
    ).replace(
        '[?25l[32D[0m[J[0m', '\r\n'
    ).replace(
        '[17D[17C[0m[?12l[?25h[?25l[17D[0m[J[0m', '\r\n'
    ).replace(
        '[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[29D[0m', ''
    ).replace(
        '[J', ''
    )

    tolog(data)

    return data


def SendCmdDoublepassword(c, cmdstr, password):

    data = ''
    ytrue = False

    if cmdstr.endswith('\n'):
        c.send(cmdstr)

    else:
        c.send(cmdstr + '\n')

    while not c.exit_status_ready():

        if c.recv_ready():

            data += c.recv(2000)

        while data.endswith('?25h'):

            if ytrue == False:

                c.send(password + "\n")
                time.sleep(1)
                c.send(password + "\n")
                time.sleep(1)
                c.send(password + "\n")
                time.sleep(1)
                c.send(password + "\n")
                ytrue = True
                time.sleep(1)
                data += c.recv(2000)
                break

            if data.endswith('@cli> '):
                break

        if data.endswith('@cli> '):
            break

    while c.recv_ready():
        data += c.recv(2000)

        if data.endswith('@cli> '):
            break

    data = data.replace(
        "\x1b[D \x1b[D", ""
    ).replace(
        "[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m", ''
    ).replace(
        "[32D[32C[0m[?12l[?25h", ''
    ).replace(
        "[?7h[0m[?12l[?25h[?2004l[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m", ''
    ).replace(
        '[33D[33C[0m[?12l[?25h[?25l[33D[0m[J[0m', '\r\n'
    ).replace(
        "[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[45D[0m", ''
    ).replace(
        '[?7h[0m[?12l[?25h[?2004l', '\r\n'
    ).replace(
        '[?12l[?25h[?25l[32D[0m[J[0m', ''
    ).replace(
        '[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[44D[0m', ''
    ).replace(
        '[?25l[32D[0m[J[0m', '\r\n'
    ).replace(
        '[?12l[?25h[?25l[20D[0m[J[0m', '\r\n'
    ).replace(
        '[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[30D[0m', ''
    ).replace(
        '[?12l[?25h[?25l[16D[0m[J[0m', '\r\n'
    ).replace(
        '[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[26D[0m', ''
    ).replace(
        '[?12l[?25h[?25l[16D[0m[J[0m', '\r\n'
    ).replace(
        '[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[0m*[26D[0m', ''
    )

    tolog(data)

    return data