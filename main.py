import os
import re
from datetime import datetime
import time

#--------------------------------------------------------------------#
# this code will automatically get the server ip if it is being ran #
# ip with port will be printed, and exported to server_ips.txt 
# serverhops will also be logged automatically 
#--------------------------------------------------------------------#

#console colors
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

username = os.getenv('username')
log_path = os.path.join(os.environ['LOCALAPPDATA'], 'Roblox', 'logs')
previous_max_create_time = 0

while True:
    try:
        log_files = [
            os.path.join(log_path, file) for file in os.listdir(log_path)
            if os.path.isfile(os.path.join(log_path, file))
        ]
        current_max_create_time = max([os.path.getctime(file) for file in log_files])
        if current_max_create_time > previous_max_create_time:
            latest_file = max(log_files, key=os.path.getctime)
            latest_file_name = os.path.basename(latest_file)
            print(f"{GREEN}[-] GAME FOUND \n[-] Found latest log file: {latest_file_name} ({datetime.fromtimestamp(os.path.getctime(latest_file)).strftime('%Y-%m-%d %H:%M:%S')}){ENDC}")
            try:
                with open(latest_file, 'r') as roblox_log:
                    print(f"{GREEN}[-] Processing log file: {latest_file_name}{ENDC}")
                    print(f"{GREEN}[-] Waiting for [FLog:Network]")
                    time.sleep(3) #xdd
                    for line in roblox_log:
                        if 'Connection accepted from' in line:
                            line = line.replace('Connection accepted from', '')
                            line2 = line.replace('|', ':')
                            line3 = re.search(r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', line2)
                            if line3:
                                print(f"{RED}[+] Server IP: {line3.group(0)}{ENDC}\n")
                                try:
                                    with open('server_ips.txt', 'a+') as ip_history:
                                        ip_history.write(line3.group(0) + "\n")
                                except Exception as e:
                                    print(f"{RED}Error occurred while writing to server_ips.txt: {e}{ENDC}")
            except IOError:
                print(f"{RED}Unable to open file: {latest_file_name}{ENDC}")
            except Exception as e:
                print(f"{RED}Error occurred while processing log file: {e}{ENDC}")
            previous_max_create_time = current_max_create_time
        time.sleep(1) 
    except KeyboardInterrupt:
        break
