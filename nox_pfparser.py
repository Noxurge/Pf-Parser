import os
from datetime import datetime
import pyscca
import sys
import time

if len(sys.argv) != 2:
    sys.exit()

file = sys.argv[1]
if pyscca.check_file_signature(file) == False:
    print("\n\033[31mThe file is not a Prefetch File! Exiting the program...\033[0m\n")
    sys.exit(1)

banner = ('''\033[95m
██████╗ ███████╗    ██████╗  █████╗ ██████╗ ███████╗███████╗██████╗ 
██╔══██╗██╔════╝    ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
██████╔╝█████╗█████╗██████╔╝███████║██████╔╝███████╗█████╗  ██████╔╝
██╔═══╝ ██╔══╝╚════╝██╔═══╝ ██╔══██║██╔══██╗╚════██║██╔══╝  ██╔══██╗
██║     ██║         ██║     ██║  ██║██║  ██║███████║███████╗██║  ██║
╚═╝     ╚═╝         ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝\033[0m''')

for char in banner:
    print(f'{char}', end='', flush=True)
    time.sleep(0.006)

scca = pyscca.open(file)
metadata = os.stat(file)

# Last Run Time Function
def search():
    x = 0
    last_run = scca.get_last_run_time_as_integer(x)
    if last_run > 0:
        date = scca.get_last_run_time(x).strftime("%Y-%m-%d %H:%M:%S")
        print(f"Last run: \033[93m{date}\033[0m\n")

# Device Name Function
def volume_info():
    for i in range(scca.number_of_volumes):
        name = scca.get_volume_information(i).device_path
        creation_time = scca.get_volume_information(i).creation_time.strftime('%Y-%m-%d %H:%M:%S')
        file_count = scca.number_of_filenames
        serial = format(scca.get_volume_information(i).serial_number,'x').upper()
        print("Volume Information:\n")
        return print(f"Name: {name} Serial: {serial} Created: {creation_time} Number Files: {file_count}\n")

# Function of Filenames
def files_func():
    print("Files: \n")
    files = scca.filenames
    result = ""
    num_digits = len(str(len(files) - 1))
    format_str = "{:0" + str(num_digits) + "d}: {}"
    for number, file in enumerate(files):
        result += format_str.format(number, file) + "\n"
    print(result.strip())

# Information about the file
def file_info():
    win_version = scca.get_format_version()
    version = ''
    print(f"Executable name: {scca.executable_filename}")
    print(f"Hash: {format(scca.prefetch_hash, 'x').upper()}")
    if win_version == 30:
        version = 'Windows 10 or Windows 11'
    elif win_version == 26:
        version = 'Windows 8.1'
    elif win_version == 23:
        version = 'Windows Vista or Windows 7'
    elif win_version == 17:
        version = 'Windows Version: Windows XP or Windows 2003'
    else:
        version = 'Not possible view version information!'
    print(f"Windows Version: {version}")

def main():
    # File Metadata
    data_de_criacao = datetime.fromtimestamp(metadata.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    data_de_modificacao = datetime.fromtimestamp(metadata.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    data_de_ultimo_acesso = datetime.fromtimestamp(metadata.st_atime).strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n\nCreated on: {data_de_criacao}\nModified on: {data_de_modificacao}\nLast accessed on: {data_de_ultimo_acesso}\n")
    # Calling Functions
    file_info()
    search()
    volume_info()
    files_func()

# Initializing the main function
main()