#!/usr/bin/python

import sys
from sets import Set
from svnlook import SvnLook
import assets

InvalidFiles = Set(["Thumbs.db"])

def EnforceMetadata(changes):
	ret = True

	files = Set()
	metas = Set()
	for change in changes:
		change = assets.RemoveTrailingSlash(change)
		if assets.IsAsset(change):
			if assets.IsMetaData(change):
				metas.add(change)
			else:
				files.add(change)
	
	for file in files:
		metaName = assets.GetMetaDataName(file)
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
				print fileName + " is not allowed, don't commit it!"
				ret = False

	return ret

def main(repo, txn):
	ret = True
	svnlook = SvnLook(repo, txn)
	if not svnlook.CheckBypass():
		added = svnlook.GetChanges(SvnLook.AddMarker)
		if not EnforceMetadata(added):
			ret = False
		if not ValidateFiles(added):
			ret = False

		deleted = svnlook.GetChanges(SvnLook.DeleteMarker)
		if not EnforceMetadata(deleted):
			ret = False

	if not ret:
		print "If you believe these are not real errors, add \"bypass-hook\" to the commit message."
		return 1

	return 0

if __name__ == "__main__":
	sys.stdout = sys.stderr
	if len(sys.argv) != 3:
		print "invalid args"
		sys.exit(1)
	
	sys.exit(main(sys.argv[1], sys.argv[2]))