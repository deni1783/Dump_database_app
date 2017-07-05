from subprocess import Popen, PIPE


# Запускает команду и  возвращает (returncode, stdout_data, stderr_data)
#  Если returncode != 0 - Error!!
def run_cmd(cmd):
    start = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout_data, stderr_data = start.communicate()
    return_code = start.returncode

    return return_code, stdout_data.decode('utf-8'), stderr_data.decode('utf-8')
