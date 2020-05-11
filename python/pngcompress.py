# -* - coding: UTF-8 -* -
import os

changeSize = 0
ignorePath = ['build',".idea",".DS_Store"]


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
            if needExtFilter and extension == ext in ext:
                if needExtFilter:
                    allfiles.append(filepath)
    return allfiles


# 压缩目录下所有图片
def CompressPng(dir):
    global changeSize
    if os.path.isdir(dir):
        imgFiles = GetFileFromThisRootDir(dir, 'png')
        for file in imgFiles:
            originSize = float(os.path.getsize(file))
            cmd = "pngquant -f --skip-if-larger --strip --ext=.png " + file
            os.system(cmd)
            afterSize = float(os.path.getsize(file))
            if originSize > afterSize:
                size = originSize - afterSize
                changeSize = changeSize + size
                print "changeFile: " + file +" changeSize:"+size
                print  size
    elif os.path.splitext(dir)[1][1:] == 'png':
        cmd = "pngquant -f --skip-if-larger --strip --ext=.png " + dir
        os.system(cmd)


def size_format(b):
    if b < 1000:
              return '%i' % b + 'B'
    elif 1000 <= b < 1000000:
        return '%.1f' % float(b/1000) + 'KB'
    elif 1000000 <= b < 1000000000:
        return '%.1f' % float(b/1000000) + 'MB'
    elif 1000000000 <= b < 1000000000000:
        return '%.1f' % float(b/1000000000) + 'GB'
    elif 1000000000000 <= b:
        return '%.1f' % float(b/1000000000000) + 'TB'


# -------------------------------脚本入口点，以及执行逻辑----------------------------------
if __name__ == '__main__':
    # 检查是否安装了 pngquant
    checkCmd = "which pngquant"
    result = os.system(checkCmd)
    if result != 0:
        cmd = "brew install pngquant"
        os.system(cmd)
    compressDir = os.getcwd()
    # 压缩目录下所有图片
    CompressPng(compressDir)
    print  size_format(changeSize)
