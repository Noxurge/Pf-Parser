import os
import argparse
from datetime import datetime
import pyscca
import sys
import time

# Argument Parser
parsing = argparse.ArgumentParser(description="Parser for Windows Prefetch Files using libscca library.")
parsing.add_argument('-f', '--file', type=str, help="Prefetch file to parse", required=True)
parsing.add_argument('-i', '--info', action='store_true', help="Show files information")
parsing.add_argument('-o', help="Save the output to a file", metavar="output")

if len(sys.argv) == 1:
    parsing.print_help()
    sys.exit(1)

args = parsing.parse_args()

if not pyscca.check_file_signature(args.file):
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

print("\n\n")
scca = pyscca.open(args.file)
metadata = os.stat(args.file)

# Last Run Time Function
def search():
    x = 0
    last_run = scca.get_last_run_time_as_integer(x)
    if last_run > 0:
        date = scca.get_last_run_time(x).strftime("%Y-%m-%d %H:%M:%S")
        return f"Last run: \033[93m{date}\033[0m\n"

# Device Name Function
def volume_info():
    vol = []
    for i in range(scca.number_of_volumes):
        name = scca.get_volume_information(i).device_path
        creation_time = scca.get_volume_information(i).creation_time.strftime('%Y-%m-%d %H:%M:%S')
        file_count = scca.number_of_filenames
        serial = format(scca.get_volume_information(i).serial_number,'x').upper()
        volume = f"Volume Information:\n\nName: {name} Serial: {serial} Created: {creation_time} Number Files: {file_count}"
        vol.append(volume)
    return vol

# Function of Filenames
def files_func():
    print("Files: \n")
    files = scca.filenames
    result = ""
    num_digits = len(str(len(files) - 1))
    format_str = "{:0" + str(num_digits) + "d}: {}"
    for number, file in enumerate(files):
        result += format_str.format(number, file) + "\n"
    return result.strip()

# Information about the file
def file_info():
    win_version = scca.get_format_version()
    version = ''
    executable = f"Executable name: {scca.executable_filename}"
    hash_file = f"Hash: {format(scca.prefetch_hash, 'x').upper()}"
    if win_version == 30:
        version = 'Windows 10 or Windows 11'
    elif win_version == 26:
        version = 'Windows 8.1'
    elif win_version == 23:
        version = 'Windows Vista or Windows 7'
    elif win_version == 17:
        version = 'Windows XP or Windows 2003'
    else:
        version = 'Not possible view version information!'
    return f"{executable}\n{hash_file}\nWindows Version: {version}"

def main():
    # File Metadata
    creation_date = datetime.fromtimestamp(metadata.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    modify_date = datetime.fromtimestamp(metadata.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    last_access_date = datetime.fromtimestamp(metadata.st_atime).strftime('%Y-%m-%d %H:%M:%S')
    date_message = f"Created on: {creation_date}\nModified on: {modify_date}\nLast accessed on: {last_access_date}\n"
    print(date_message)
    file_info_str = file_info()
    search_str = search()
    volume_info_list = volume_info()
    print(f"{file_info_str}\n{search_str}")
    for volumes in volume_info_list:
        print(volumes)
    if args.info:
        files_func_str = files_func()
        print(files_func_str)
    if args.o:
        with open(args.o, 'w') as f:
            f.write(date_message + "\n")
            f.write(file_info_str + "\n")
            f.write(search_str + "\n")
            for volume in volume_info_list:
                f.write(volume + "\n")
            if args.info:
                f.write(files_func_str + "\n\n")
        print(f"\nDatas saved in {args.o}")

# Initializing the main function
main()