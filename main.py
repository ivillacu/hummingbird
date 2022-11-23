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
        if host_inventory[iteration]['servername'] in exclude_hosts:
            print("Worker not opened...")
            continue

        params = {
            "hostname": host_inventory[iteration]["hostname"],
            "username": "root",
            "commands": [
                "df -Th | grep ext4",
                # "docker ps",
                # "reboot",
                "systemctl stop docker.socket",
                "systemctl status docker | grep Active",
                "service docker status | grep Active",
                # "sleep 5",
                "rm -rf /var/lib/docker",
                # "sleep 1",
                "df -Th | grep ext4",
                "reboot",
                # "rm -rf /home/jobs.txt",
                # "rm -rf /home/cronjob.log",
                # "crontab -r",
                # "crontab -l",
                # "echo '0 14 */2 * * echo Prune system -- $(date) >> /home/cronjob.log' >> /home/jobs.txt",
                # "echo '1 14 */2 * * /usr/bin/docker system prune -a -f >> /home/cronjob.log' >> /home/jobs.txt",
                # "echo '0 15 */15 * * echo Prune volume -- $(date) >> /home/cronjob.log' >> /home/jobs.txt",
                # "echo '1 15 */15 * * /usr/bin/docker volume prune -f >> /home/cronjob.log' >> /home/jobs.txt",
                # "crontab /home/jobs.txt",
                # "crontab -l",
                # "df -h | grep '/dev/vda1 '",
                # "systemctl restart docker",
                # "sleep 3",
                # "docker image prune -a -f",
                # "sleep 3",
                # "systemctl restart nomad",
                # "df -h | grep '/dev/vda1 '",
                # "reboot"
            ],
        }
        execute_in_server(params)

    print("END")
