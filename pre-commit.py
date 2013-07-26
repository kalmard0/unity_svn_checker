#!/usr/bin/python

import sys
from sets import Set
from svnlook import SvnLook

AssetDir = "Assets/"
MetaDataExtension = ".meta"
MetaDataExtensionExceptions = Set()
InvalidFiles = Set(["Thumbs.db"])

def EnforceMetadata(changes):
	ret = True

	files = Set()
	metas = Set()
	for change in changes:
		if change[-1] == "/":
			change = change[0:-1]
		index = change.find(AssetDir)
		if (index == 0 or change[index - 1] == "/"):
			metaIndex = change.find(MetaDataExtension)
			if (metaIndex >= 0 and metaIndex == len(change) - len(MetaDataExtension)):
				metas.add(change)
			elif not change in MetaDataExtensionExceptions:
				files.add(change)
	
	for file in files:
		metaName = file + MetaDataExtension
		if (not metaName in metas):
			print "Change for " + file + " commited but .meta missing!"
			ret = False
		else:
			metas.remove(metaName)
	
	for meta in metas:
		ret = False
		print "Change for " + meta + " commited but file missing!"

	return ret

def ValidateFiles(changes):
	ret = True
	for change in changes:
		slashIdx = change.rfind("/")
		if slashIdx >= 0:
			fileName = change[slashIdx + 1:]
			if fileName in InvalidFiles:
				print fileName + " is invalid, don't commit it!"
				ret = False

	return ret

def main(repo, txn):
	ret = True
	svnlook = SvnLook(repo, txn)
	if not svnlook.CheckBypass():
		added = svnlook.FindChange("A")
		if not EnforceMetadata(added):
			ret = False
		if not ValidateFiles(added):
			ret = False

		deleted = svnlook.FindChange("D")
		if not EnforceMetadata(deleted):
			ret = False

	if not ret:
		print "If you believe these are not real errors, add \"bypass-hook\" to the commit message."
		return 1

	return 0

if __name__ == "__main__":
	if len(sys.argv) != 3:
		sys.stderr.write("invalid args\n")
		sys.exit(1)
	sys.stdout = sys.stderr
	sys.exit(main(sys.argv[1], sys.argv[2]))