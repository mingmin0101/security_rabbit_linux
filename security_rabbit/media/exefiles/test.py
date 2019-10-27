import subprocess


args = ["wine", "\mnt\security_rabbit\security_rabbit\media\exefiles\sigcheck.exe", "-i", "-l", "-nobanner", "\mnt\security_rabbit\security_rabbit\media//file_upload\javaw.exe"]
#args = ["wine", "--help" , "&"]
pipe = subprocess.Popen(args, stdout=subprocess.PIPE)
sigcheck_output = pipe.communicate()[0]

print(sigcheck_output)
