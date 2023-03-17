import boto3
import paramiko
import io


s3 = boto3.resource('s3')

obj = s3.Object('bucket_name', 'metadata/pemfile')
data = io.BytesIO()
obj.download_fileobj(data)
key_stream = io.StringIO(data.getvalue().decode("utf-8"))


k = paramiko.RSAKey.from_private_key(
    key_stream)  # TODO replace env
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())


print("Connecting to Host")
host_ip = '123.33.33.33'
c.connect(hostname=host_ip, username="ubuntu", pkey=k)  # TODO replace env
print(f"connected to {host_ip}")

# TODO copy all commands in bash.sh in s3


# compile a bash script on the fly
query = "SELECT * FROM Table"
key_prefix = "members1"


start_process_commands = [f'''python3 main.py "{query}" "{key_prefix}"''']
stop_process_commands = ["sudo pkill -9 -f python"]


def execute_commands(c, commands, wait=False):

    for command in commands:
        print(f"Executing {command}")
        stdin, stdout, stderr = c.exec_command(command)
        if wait:
            print(stdout.read())
            print(stderr.read())
    print("Execution Done NOT waiting")


execute_commands(c, stop_process_commands)
# Return execution complete see cloud watch logs for complete output
