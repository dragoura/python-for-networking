from pprint import pprint

import pexpect


def send_show_command(sshname, password, enable, commands):
    with pexpect.spawn(f"ssh {sshname}", timeout=10, encoding="utf-8") as ssh:
        yes_or_password = ssh.expect(["[Pp]assword", "yes/no"])
        if yes_or_password == 1:
            ssh.sendline("yes")
            ssh.expect("[Pp]assword")
        ssh.sendline(password)
        enable_status = ssh.expect([">", "#"])
        if enable_status == 0:
            ssh.sendline("enable")
            ssh.expect("[Pp]assword")
            ssh.sendline(enable)
            ssh.expect("#")

        ssh.sendline("terminal length 0")
        ssh.expect("#")
        hostname = ssh.before.split("\n")[-1]
        host = f"{hostname}#"

        result = {}
        for command in commands:
            ssh.sendline(command)
            match = ssh.expect([host, pexpect.TIMEOUT, pexpect.EOF])
            if match == 0:
                output = ssh.before
                result[command] = output.replace("\r\n", "\n")
            elif match == 2:
                return result
            else:
                print("Ошибка: timeout")
        return result


if __name__ == "__main__":
    devices = ["gns3-r1", "gns3-r2", "gns3-r3"]
    commands = ["sh clock", "sh arp"]
    for sshname in devices:
        result = send_show_command(sshname, "cisco", "cisco", commands)
        pprint(result, width=120)
