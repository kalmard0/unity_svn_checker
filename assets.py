AssetDir = "Assets/"
MetaDataExtension = ".meta"

def IsDirectory(path):
	return path[-1] == "/"

def RemoveTrailingSlash(path):
	if IsDirectory(path):
		path = path[0:-1]
	return path

def IsAsset(path):
	index = path.find(AssetDir)
	return index == 0 or path[index - 1] == "/"

def IsMetaData(path):
	return path.endswith(MetaDataExtension)

def GetMetaDataName(path):
	return path + MetaDataExtension

def GetFileName(path):
	slashIdx = path.rfind("/")
	fileName = path
	if slashIdx >= 0:
		fileName = path[slashIdx + 1:]
	return fileName