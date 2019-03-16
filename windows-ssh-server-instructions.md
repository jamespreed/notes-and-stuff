# Install server and client
Settings > Apps > Apps & features > Manage optional features

- Locate "OpenSSH server" > select Install
- Locate "OpenSSH client" > select Install
	
# Enable access through firewall
Open up port 22 to TCP traffic.
Either:

* Powershell as Admin > New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH SSH Server' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
Or:
* Control Panel > System and Security > Windows Defender Firewall > Advanced Settings > Inbound Rules > [Actions] New Rule...
- Rule Type: Port > TCP : Specific local ports = 22 > Allow the connection > [All] > Name and description
- (OR) Rule Type: Predefined > OpenSSH Server
	
# Start service
Control Panel > System and Security > Administrative Tools > run Services
* Locate OpenSSH SSH Server > [right click] Properties
- Startup Type: Automatic
- Start
		
# Key generation for remote login
Each user needs a key public and private key pair to SSH into the server.  
This can be done on the server or the remove computer, but both files need to be on the remote computer; 
while the server will only need the public key.

After installing the ssh client, `ssh-keygen` should now be located at C:\Windows\System32\OpenSSH\ssh-keygen.exe 
and it should be on your system's PATH.  The following command will create a public/private key pair with RSA 4096 bit encryption


```
C:\Users\user>ssh-keygen -t rsa -b 4096

Enter file in which to save the key (C:\Users\user/.ssh/id_rsa):  [hit enter]
Enter passphrase (empty for no passphrase):  [enter password]
Enter same passphrase again:                 [enter same password]

Your identification has been saved in C:\Users\user/.ssh/id_rsa.
Your public key has been saved in C:\Users\user/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:2EWy8ARPYEjvru/dCA9GTPkRXgLV3rlomER1RVljj2Q user@computer-name
The key's randomart image is:
+---[RSA 4096]----+
|   ...*=Bo+ .oE=.|
|    .o O.B.. oo.o|
|      +.*... .. .|
|     + +.o. o    |
|      =.So . .   |
|     o  o o .    |
|      =  .       |
|     o = o       |
|    .oo + .      |
+----[SHA256]-----+
```

Windows checks the public keys contained in the file `C:\Users\<username>\.ssh\authorized_keys` (no extension).  It also checks that no one
other than the user, Administrator, and System can access that file.  First, copy the public key file to authorized_keys, then open the
file explorer.

```
C:\Users\user>cd .ssh
C:\Users\user\.ssh>copy id_rsa.pub authorized_keys
C:\Users\user\.ssh>start . 
```

[right click] authorized_keys > Properties > Security > Advanced
- remove any user that is not "Administrator" or "SYSTEM"
	
Copy both `id_rsa.pub` and `id_rsa` to a thumbdrive (don't email them).  Copy them from the thumbdrive to remote computer, typically in 
`C:\Users\<username>\.ssh\`
	
# Securing the SSH server
Change the settings in Only allow access via public key exchange.  The file `C:\ProgramData\ssh\sshd_config` holds the configuration options
for the Windows SSH server.  Look through them to see which you care about, but you absolutely should change

```
#PasswordAuthentication yes
```

which is the default value that allows users to login using ONLY their user password.  Change it to:

```
PasswordAuthentication no
```

This removes the comment (#) and sets the value to false, forcing PKI authentication.
