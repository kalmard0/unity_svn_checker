import os
import subprocess
import fnmatch

svnlook = "/usr/bin/svnlook"
BypassCommand = "bypass-hook"

class SvnLook:
	AddMarker = "A"
	DeleteMarker = "D"
	UpdateMarker = "U"

	def __init__(self, repo, txn = None, revision = None):
		self.repo = repo
		self.txn = txn
		self.revision = revision

	def Call(self, params):
		if self.txn is not None:
			command = [svnlook, params, "-t", self.txn, self.repo]
		else:
			command = [svnlook, params, "-r", self.revision, self.repo]
		return subprocess.check_output(command, universal_newlines = True)

	def GetChanges(self, changeType):
		changes = self.Call("changed")
		changed = []
		for line in changes.splitlines():
			line = line.decode().strip()
			text_mod = line[0:1]
			if text_mod == changeType:
				changed.append(line[4:])
		return changed

	def GetLog(self):
		return self.Call("log")
		
	def CheckBypass(self):
		return BypassCommand in self.GetLog()

