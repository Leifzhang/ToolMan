#!/bin/bash
KIT_NAME="toolman"
INSTALL_PATH=`cd ~;pwd`/.$KIT_NAME/kit/bin
WORK_PATH="$PWD"
. $INSTALL_PATH/./log.sh

R "***********************图片压缩开始***********************";
python $INSTALL_PATH/pngToWebp.py $WORK_PATH/
R "***********************图片压缩结束***********************";