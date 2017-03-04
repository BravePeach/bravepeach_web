import os
from collections import OrderedDict

import paramiko
from bravepeach.settings.staging import APT_PACKAGE_LIST

home = os.path.expanduser("~")

with paramiko.SSHClient() as client:
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #client.connect(hostname="54.199.224.189", username="ubuntu", key_filename=os.path.join(home, ".ssh", "id_rsa"))
    client.connect(hostname="54.199.224.189", username="ubuntu", key_filename=os.path.join(home, "ulismoon_bravepeach.pem"))

    cmd_dict = OrderedDict()
    cmd_dict["Install Dependency Packages"] = ["sudo apt install -y " + " ".join(APT_PACKAGE_LIST),
                                               "sudo pip3 install virtualenv"]
    cmd_dict["Pull Latest Source"] = ["cd bravepeach_web", "git pull"]
    cmd_dict["Setup Python Environment"] = ["cd bravepeach_web", "virtualenv -p python3 .venv",
                                            "source .venv/bin/activate", "pip install -r requirements.txt"]
    #cmd_dict["Reload Service"] = ["sudo systemd service uwsgi reload"]

    for k, v in cmd_dict.items():
        print("[Paramiko] {}".format(k))
        cmd = ";".join(v)
        stdin, stdout, stderr = client.exec_command(cmd)
        stdin.flush()
        o = stdout.read().splitlines()
        e = stderr.read().splitlines()

        for l in o:
            print(l.decode())
        print("")

        for l in e:
            print(l.decode())
        print("")
