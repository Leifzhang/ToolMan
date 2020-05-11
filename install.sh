#!/bin/sh

export LANG=en_US.UTF-8

KIT_NAME="kit"

MBULL_PATH=`cd ~;pwd`/.toolman
if [ ! -d $MBULL_PATH ]; then mkdir -p $MBULL_PATH; fi

INSTALL_PATH=$MBULL_PATH/kit
if [ ! -d $INSTALL_PATH ]; then mkdir -p $INSTALL_PATH; fi

WORK_PATH="$PWD"

R(){
    echo "\033[31m"$1"\033[0m"
}
G(){
    echo "\033[32m"$1"\033[0m"
}
P(){
    echo "\033[35m"$1"\033[0m"
}

function INS_BIN ()
{
    [[ -z $SILENT_MODE ]] && {
        if [[ "$(readlink `which $1`)" == "$INSTALL_PATH/bin/$1.sh" ]]; then
            echo " - already installed '$1.sh'"
        else
            R "[sudo] Require your sudo PASSWORD."
            if [[ -f /usr/sbin/$1 ]]; then
                echo " - remove old link: $(readlink `which $1`)"
                sudo rm /usr/sbin/$1
            fi
            sudo ln -s $INSTALL_PATH/bin/$1.sh /usr/local/bin/$1
            echo " - install '$1.sh' done"
        fi
    }
}


G "toolmankit install_path: $INSTALL_PATH"

if [ ! -d $INSTALL_PATH ]; then mkdir -p $INSTALL_PATH; fi
# remove old kit
P " - replace old kit ...."
cp -a * $INSTALL_PATH/

INS_BIN "toolman"
