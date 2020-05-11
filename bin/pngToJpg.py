# -* - coding: UTF-8 -* -

import sys
import os
from PIL import Image
from log import R, G, B

changeSize = 0
ignorePath = ['build',".idea",".DS_Store"]
ext = ['png','webP','jpg','jpeg']

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
            if needExtFilter and extension in ext:
                if needExtFilter:
                    allfiles.append(filepath)
    return allfiles

# 压缩目录下所有图片
def CompressPng(dir):
    global changeSize
    changeFiles = {}
    if os.path.isdir(dir):
        imgFiles = GetFileFromThisRootDir(dir, ext)
        for file in imgFiles:
            fileName = os.path.basename(file)
            fileName = fileName.split('.')[0]
            outPath = "{}/temp_webp/{}.jpg".format(dir,fileName)
            floder=os.path.dirname(outPath)
            if not os.path.exists(floder):
                os.makedirs(floder)
            originSize = float(os.path.getsize(file))
            isChange=changeImage(file,outPath)
            if isChange < 0 :   
            	R(outPath) 
            	afterSize = float(os.path.getsize(outPath))
            	if originSize > afterSize:
            	    size = originSize - afterSize
            	    changeSize = changeSize + size
            	    content ="changeFile: {} changeSize: {}".format(file, size)
            	    R(content)
            	    changeFiles[file] = outPath
            	else:
            	    os.remove(outPath)
    elif os.path.splitext(dir)[1][1:] == 'png':
        fileName = os.path.basename(file)
        cmd = "cwebp -q 75 {} -o {}.jpg".format(dir,fileName) 
        os.system(cmd)
    return changeFiles


def changeImage(file,outPath):
	filePath = file
	png = Image.open(filePath).convert('RGBA')
	alpha_index = png.getbands().index('A')
	if alpha_index < 0 :
		bg = Image.new('RGB', size = png.size, color = (255, 255, 255))
		bg.paste(png,png)
		bg.save(outPath)
		print(outPath)
		return alpha_index
	return alpha_index

if __name__ == '__main__':
	changeFiles=CompressPng(os.getcwd())