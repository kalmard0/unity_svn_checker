import os
import subprocess
import fnmatch

svnlook = "/usr/bin/svnlook"
BypassCommand = "bypass-hook"

class SvnLook:
	def __init__(self, repo, txn):
		self.repo = repo
		self.txn = txn

	def Call(self, params):
		command = [svnlook, params, "-t", self.txn, self.repo]
		return subprocess.check_output(command, universal_newlines = True)

	def FindChange(self, changeType):
		changes = self.Call("changed")
		changed = []
		for line in changes.splitlines():
			line = line.decode().strip()
			text_mod = line[0:1]
			if text_mod == changeType:
				changed.append(line[4:])
		return changed

	def CheckBypass(self):
		log = self.Call("log")
		return BypassCommand in log

