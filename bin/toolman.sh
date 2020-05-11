#!/bin/bash

export LANG=en_US.UTF-8
INSTALL_PATH=`cd ~;pwd`/.toolman/kit
CONFIG_PATH=`cd ~;pwd`/.toolman_config

# 清屏
clear

function echo_help () {
	echo "***********************mbull帮助**********************"
	echo "1、[u|update]			更新Kit"
	echo "2、[png|pngquant]		使用 pngquant 进行png格式的压缩"
	echo "3、[m|monkey]			Android Monkey测试"
	echo "4、[w|webP]			使用 cwebp 进行png格式webP的转化"
	echo "5、[j|jpg]				使用 py 进行png格式jpg的转化"
	echo "*****************************************************"
}

action=$1
if [[ -z "$action" ]]; then
	echo_help
	read -p '指定一个操作:' action
	if [[ -z "$action" ]]; then
		echo "ERROR: action is not valid.";
		exit 1;
	fi
fi

if [ $action == "update" ]||[ $action == "u" ]; then
	sh $INSTALL_PATH/bin/kitupdate.sh
elif [ $action == "png" ]||[ $action == "pngquant" ]; then
	sh $INSTALL_PATH/bin/pngquant.sh $2
elif [ $action == "monkey" ]||[ $action == "m" ]; then
	sh $INSTALL_PATH/bin/monkey.sh $*
elif [ $action == "webp" ]||[ $action == "w" ]; then
	sh $INSTALL_PATH/bin/pngToWebp.sh $*
elif [ $action == "jpg" ]||[ $action == "j" ]; then
	sh $INSTALL_PATH/bin/pngToJpg.sh $*
else
	echo "ERROR: Currently supported actions: "
	echo_help 
fi
