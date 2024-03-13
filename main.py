from paramiko import AutoAddPolicy, SSHClient

from hosts import exclude_hosts, host_inventory


def execute_in_server(params):
    try:
        stdlog = ""
        version = ""
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(hostname=params["hostname"], username=params["username"])

        for command in params["commands"]:
            print(f"-*-*-*-*- Executing - {command} -*-*-*-*-")
            stdin, stdout, stderr = client.exec_command(command)
            stdlog = stdout.read().decode("UTF-8")
            print(stdlog)
            if "Docker version" in stdlog:
                version = stdlog
        client.close()
        return version
    except Exception as e:
        print(e)


if __name__ == "__main__":
    workers_amount = 0
    for iteration in range(0, len(host_inventory)):
        version = ""
        print("-" * 150)
        print(
            f"Executing in server: {host_inventory[iteration]['servername']} --- Iteration: {iteration}"
        )
        if host_inventory[iteration]["servername"] in exclude_hosts:
            print("Worker not opened...")
            continue

        params = {
            "hostname": host_inventory[iteration]["hostname"],
            "username": "root",
            "commands": [
                # exaples of commands
                # "dpkg --configure -a",
                # "sleep 1",
                # "apt -y --fix-broken install",
                # "sleep 3",
                # "apt update",
                # "sleep 3",
                # "apt-get install --only-upgrade -y docker-ce docker-ce-cli",
                # "sleep 3",
                # "dpkg --configure -a && apt -y --fix-broken install && apt update && apt-get install --only-upgrade -y docker-ce docker-ce-cli && docker --version",
                # f"echo '{string}' > /etc/squid/squid.conf",
                # "systemctl restart squid",
                # "systemctl status squid",
                # "sleep 2",
                # "rm /opt/nomad/client/client-id",
                # "docker --version",
                # "sleep 1",
                # "reboot",
                "systemctl stop docker.socket",
                "systemctl status docker | grep Active",
                "rm -rf /var/lib/docker",
                "df -Th | grep ext4",
                "reboot",
            ],
        }

        version = execute_in_server(params)
        # with open("host_ready_full.txt", "a") as archivo:
        #     # Escribir el nuevo contenido
        #     archivo.write(
        #         f"{host_inventory[iteration]['servername']},{host_inventory[iteration]['hostname']},{version}"
        #     )

    print("END")
