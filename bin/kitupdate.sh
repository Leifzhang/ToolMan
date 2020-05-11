#!/bin/sh

export LANG=en_US.UTF-8

KIT_NAME="kit"

MBULL_PATH=`cd ~;pwd`/.toolman
if [ ! -d $MBULL_PATH ]; then mkdir -p $MBULL_PATH; fi

INSTALL_PATH=$MBULL_PATH/kit
if [ ! -d $INSTALL_PATH ]; then mkdir -p $INSTALL_PATH; fi

WORK_PATH="$PWD"


timeout=10  # 10秒超时
while [[ -f $INSTALL_PATH/update.lock ]]; do
    sleep 1;
    timeout=$(($timeout-1));
    if [[ $timeout == 0 ]]; then
        echo "toolman kitupdate failed: timeout!"
        exit 0;
        break;
    fi
done

R(){
    echo "\033[31m"$1"\033[0m"
}
G(){
    echo "\033[32m"$1"\033[0m"
}
P(){
    echo "\033[35m"$1"\033[0m"
}

G "toolmankit install_path: $INSTALL_PATH"

args=`getopt nspfv $*`

function S_RM ()
{
    for i in `find $1 -depth 1 | grep -v "update.lock"`; do
        if [[ "`echo $i | grep $2`" != "" ]]; then
            echo " - delete $i"
            rm -rf $i
        fi
    done
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


# get new version
P " - get new version...."

TMP_DIR=/tmp/mbullkit-`date +%s`
mkdir $TMP_DIR
cd $TMP_DIR
curl -s -o v "https://gitlab.wallstcn.com/mopensource/MBull/raw/master/mbull/VERSION"
NEWEST_VERSION=$(cat ./v 2> /dev/null)
rm -rf $TMP_DIR


# download new kit version
P " - download new kit version...."
KIT_SOURCE="https://gitlab.wallstcn.com/mopensource/MBull/raw/master/mbull/tag/$NEWEST_VERSION.zip"
echo $KIT_SOURCE

TMP_DIR=/tmp/aptkit-`date +%s`
mkdir $TMP_DIR
cd $TMP_DIR
curl -o tmp.zip $KIT_SOURCE
unzip -q tmp.zip

if [ ! -d $INSTALL_PATH ]; then mkdir -p $INSTALL_PATH; fi
# remove old kit
P " - remove old kit ...."
S_RM $INSTALL_PATH $KIT_NAME
cp -a * $INSTALL_PATH/


P "\nupdated to $NEWEST_VERSION"

echo " - clean temp" 
rm -rf $TMP_DIR
rm $INSTALL_PATH/tmp.zip
rm -rf $INSTALL_PATH/__MACOSX

echo " - check permisions."
find $INSTALL_PATH/bin -exec chmod +x {} \;

INS_BIN "mbull"

rm -f $INSTALL_PATH/update.lock

P "\nupdate done."