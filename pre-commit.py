#!/usr/bin/python

import sys
from sets import Set
import svnlook

AssetDir = "Assets/"
MetaDataExtension = ".meta"
InvalidFiles = Set(["Thumbs.db"])

def enforce_metadata(changes):
	ret = True

	files = Set()
	metas = Set()
	for change in changes:
		inAsset = False
		if change[-1] == "/":
			change = change[0:-1]
		index = change.find(AssetDir)
		if (index == 0 or change[index - 1] == "/"):
			metaIndex = change.find(MetaDataExtension)
			if (metaIndex >= 0 and metaIndex == len(change) - len(MetaDataExtension)):
				metas.add(change)
			else:
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

def validate_files(changes):
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
	if not svnlook.svnlook_checkbypass(repo, txn):
		added = svnlook.svnlook_find(repo, txn, "A")
		if not enforce_metadata(added):
			ret = False
		if not validate_files(added):
			ret = False

		deleted = svnlook.svnlook_find(repo, txn, "D")
		if not enforce_metadata(deleted):
			ret = False
	return 1
	

if __name__ == "__main__":
	if len(sys.argv) != 3:
		sys.stderr.write("invalid args\n")
		sys.exit(1)
	sys.stdout = sys.stderr
	sys.exit(main(sys.argv[1], sys.argv[2]))