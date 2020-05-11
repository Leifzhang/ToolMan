# -* - coding: UTF-8 -* -
import os
ignorePath = ['build',".idea",".DS_Store"]
ext = ['kt','java']

# 获取指定路径下所有指定后缀的文件
def GetFileFromThisRootDir(dir, ext=None):
    allfiles = []
    needExtFilter = (ext != None)
    for root, dirs, files in os.walk(dir):
        for filespath in files:
            filepath = os.path.join(root, filespath)
            #if not ignorePath.__contains__(filepath):
            #print  filepath
            text = os.path.splitext(filepath)[0][1:]
            isIgnore = 0
            for ignoreText in ignorePath:
                if text.find(ignoreText)>=0:
                    isIgnore+= 1
            if isIgnore > 0:
                continue
            if text.find('.9')>=0:
                continue
            extension = os.path.splitext(filepath)[1][1:]
            fileName = os.path.basename(filepath)
            fileName = fileName.split('.')[0]
            if needExtFilter and extension in ext:
                print fileName
                if needExtFilter and fileName not in ignoreFileName :
                    allfiles.append(filepath)
    return allfiles

def checkClassAndRemove(dir):
	if os.path.isdir(dir):
		files=GetFileFromThisRootDir(dir,ext)
		for file in files:
			