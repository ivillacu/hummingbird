from paramiko import SSHClient, AutoAddPolicy
from hosts import host_inventory, exclude_hosts


def execute_in_server(params):
    try:
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(hostname=params["hostname"], username=params["username"])

        for command in params["commands"]:
            stdin, stdout, stderr = client.exec_command(command)
            print(stdout.read().decode("UTF-8"))
        client.close()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    workers_amount = 0
    for iteration in range(0, len(host_inventory)):
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
                "df -Th | grep ext4",
                "docker ps",
                "reboot",
            ],
        }
        execute_in_server(params)

    print("END")
