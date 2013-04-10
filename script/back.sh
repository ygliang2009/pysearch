#!/bin/bash
#desc: backup the whole of the project

backspace='/home/chemical/workspace/backup/se'
pwdpath=$(pwd)
path=$pwdpath'/'$0
cd $(dirname $path)
now=`date +%Y%m%d%H%M`
filename='se_bak_'$now'.tar.gz'
tar -zcvf $filename '../../se/' --exclude 'log\/*'
if [ ! -d $backspace ]
then
	mkdir -p $backspace
fi
if [ -f $filename ]
then
	mv $filename $backspace
fi
echo 'back done!'
