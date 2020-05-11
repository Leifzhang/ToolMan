#!bin/bash

KIT_NAME="toolman"
INSTALL_PATH=`cd ~;pwd`/.$KIT_NAME/kit/bin
WORK_PATH="$PWD"
. $INSTALL_PATH/./log.sh

P "**************************************************************"
G "**************开始对当前文件夹下的PNG图片进行转化*********************"
P "**************************************************************\n"
python $INSTALL_PATH/pngToJpg.py $WORK_PATH/
P "\n**************************************************************\n"
