#!/bin/bash

KIT_NAME="toolman"
INSTALL_PATH=`cd ~;pwd`/.$KIT_NAME/kit/bin
. $INSTALL_PATH/./log.sh

throttle=$1
if [[ -z "$throttle" ]]; then
	throttle=200
fi

command=$2
if [[ -z "$command" ]]; then
	command=3000
fi

bundle=$3
if [[ -z "$bundle" ]]; then
	bundle=com.jingyao.easybike
fi

R
R "***********************Moneky开始测试***********************";
P "参数1[200]：指令间隔为:$throttle";
P "参数2[3000]：指令总数为:$command";
P "参数3[com.wallstreetcn.news]：测试包名为:$bundle";
G "关闭Monkey的指令为，ps | grep monkey , kill [tid]"
R
G "adb shell monkey -p $bundle -v -v --throttle $throttle $command"
R
adb shell monkey -p $bundle -v -v --throttle $throttle $command
R "***********************Moneky测试结束***********************";
