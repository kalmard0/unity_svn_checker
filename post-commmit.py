#!/usr/bin/python

import sys
from svnlook import SvnLook
from sets import Set
import tempfile
import subprocess
import assets
import os

CutOffLimit = 10

def AddToLog(newLog, changes, changeName):
	if len(changes) > 0:
		newLog = newLog + changeName + ": "

		if len(changes) < CutOffLimit:
			for file in changes:
				newLog = newLog + file + " "
		else:
			newLog = newLog + len(changes) + " files"
		newLog = newLog + "\n"
	return newLog

def AddFiles(marker, changes, look):
	for change in look.GetChanges(marker):
		if not assets.IsAsset(change) or not assets.IsMetaData(change):
			if assets.IsDirectory(change):
				changes.add(change)
			else:
				changes.add(assets.GetFileName(change))

def FixCommitMessage(look):
	newLog = look.GetLog()
	if len(newLog) == 0 or newLog == "\n":
		updates = Set()
		adds = Set()
		deletes = Set()
		
		AddFiles(SvnLook.AddMarker, adds, look)
		AddFiles(SvnLook.UpdateMarker, updates, look)
		AddFiles(SvnLook.DeleteMarker, deletes, look)

		moves = Set()

		for file in adds:
			if file in deletes:
				adds.remove(file)
				deletes.remove(file)
				moves.add(file)

		newLog = ""
		
		newLog = AddToLog(newLog, updates, "Updated")
		newLog = AddToLog(newLog, adds, "Added")
		newLog = AddToLog(newLog, deletes, "Deleted")
		newLog = AddToLog(newLog, moves, "Moved")
		
	return newLog

def main(repo, revision):
	svnlook = SvnLook(repo, revision = revision)
	if not svnlook.CheckBypass():
		log = FixCommitMessage(svnlook)
		temp = tempfile.NamedTemporaryFile()
		temp.write(log)
		temp.flush()
		subprocess.call(["svnadmin", "setlog", repo, "-r", revision, "--bypass-hooks", temp.name], universal_newlines = True)
		temp.close()
	
	return 0

if __name__ == "__main__":
	sys.stdout = sys.stderr
	if len(sys.argv) != 3:
		print "invalid args"
		sys.exit(1)
	
	sys.exit(main(sys.argv[1], sys.argv[2]))