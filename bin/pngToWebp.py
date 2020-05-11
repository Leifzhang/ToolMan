# -* - coding: UTF-8 -* -
import os
import shutil
from log import R, G, B
changeSize = 0
ignorePath = ['build',".idea",".DS_Store"]
ext = ['png','webP','jpg']
ignoreFileName = ['yw_1222_0670',"yw_1222_0c33","hello_bike_ic_launcher"]

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


# 压缩目录下所有图片
def CompressPng(dir):
    global changeSize
    changeFiles = {}
    if os.path.isdir(dir):
        imgFiles = GetFileFromThisRootDir(dir, ext)
        for file in imgFiles:
            fileName = os.path.basename(file)
            fileName = fileName.split('.')[0]
            outPath = "{}/temp_webp/{}.webp".format(dir,fileName)
            floder=os.path.dirname(outPath)
            if not os.path.exists(floder):
                os.makedirs(floder)
            print outPath
            originSize = float(os.path.getsize(file))
            cmd = "cwebp -q 75 {} -o {} -quiet".format(file,outPath) 
            result = os.system(cmd)      
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
        cmd = "cwebp -q 75 {} -o {}.webp -quiet".format(dir,fileName) 
        os.system(cmd)
    return changeFiles


def size_format(b):
    if b < 1023:
        return '%i' % b + 'B'
    elif 1024 <= b < 1024*1024:
        return '%.1f' % float(b/1024) + 'KB'
    elif 1024*1024 <= b < 1024*1024*1024:
        return '%.1f' % float(b/(1024*1024)) + 'MB'
    elif 1024*1024*1024 <= b < 1024*1024*1024*1024:
        return '%.1f' % float(b/(1024*1024*1024)) + 'GB'
    elif 1024*1024*1024*1024 <= b:
        return '%.1f' % float(b/(1024*1024*1024*1024)) + 'TB'

def replace(changeFiles):
    for key in changeFiles:
        try:
            imgFloder= os.path.dirname(key)
            webPFile = changeFiles[key]
            shutil.copy(webPFile,imgFloder)
            print key
            os.remove(key)
            os.remove(webPFile)
        except Exception as e:
            R('出现异常')
        finally:
            R("替换下一个文件")



# -------------------------------脚本入口点，以及执行逻辑----------------------------------
if __name__ == '__main__':
    # 检查是否安装了 pngquant
    checkCmd = "which cwebp"
    result = os.system(checkCmd)
    if result != 0:
        cmd = "brew install webp"
        os.system(cmd)
    compressDir = os.getcwd()
    # 压缩目录下所有图片
    changeFiles=CompressPng(compressDir)
    B(size_format(changeSize))
    
    str = raw_input('是否替换所有图片：Y/N\n').strip();
    if str == "Y":
        replace(changeFiles)
        os.removedirs("{}/temp_webp/".format(compressDir))
    else:
        for key in changeFiles:
            os.remove(changeFiles[key])
        os.removedirs("{}/temp_webp".format(compressDir))
        R("忽略")
