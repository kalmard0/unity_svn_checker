import os
import subprocess
import fnmatch

svnlook = "/usr/bin/svnlook"
BypassCommand = "bypass-hook"

def svnlook_find(repo, txn, changeType):
	
	cmd = "'%s' changed -t '%s' '%s'" % (svnlook, txn, repo)
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	changed = []
	while True:
		line = p.stdout.readline()
		if not line:
			break
		line = line.decode().strip()
		text_mod = line[0:1]
		if text_mod == changeType:
			changed.append(line[4:])

	data = p.communicate()
	if p.returncode != 0:
		sys.stderr.write(data[1].decode())
		sys.exit(2)

	return changed

def svnlook_checkbypass(repo, txn):
	bypass = False
	cmd = "'%s' log -t '%s' '%s'" % (svnlook, txn, repo)
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	while True:
		line = p.stdout.readline()
		if not line:
			break
		if BypassCommand in line:
			bypass = True

	data = p.communicate()
	if p.returncode != 0:
		sys.stderr.write(data[1].decode())
		sys.exit(2)

	return bypass

