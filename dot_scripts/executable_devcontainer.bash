#!/usr/bin/env bash
#https://superuser.com/questions/333388/gnu-dialog-and-utf-8-characters
export NCURSES_NO_UTF8_ACS=1

workspaceFolder=/home/admin/.scripts
devcontainerFolder=/home/admin/.scripts/.devcontainer

count=0
options=
directories=

if [ ! -d $workspaceFolder ]; then
	echo $workspaceFolder not found.
	exit
fi

if [ ! -d $devcontainerFolder ]; then
	echo $devcontainerFolder not found.
	exit
fi

for directory in `ls $devcontainerFolder`; do
	count=$[count+1]
	options="$options $count $directory off "
	directories="$directories $directory "
done

options=($options)
directories=($directories)

# https://stackoverflow.com/questions/4889187/dynamic-dialog-menu-box-in-bash
choice=$(dialog --radiolist 'Select devcontainer:' 0 0 0 "${options[@]}" 2>&1 >/dev/tty)

if [ -z "$choice" ]; then
	echo no choice.
	exit
fi

echo $choice

i=$[choice-1]

echo $i
directory=${directories[$i]}

cp -r $devcontainerFolder/$directory $workspaceFolder \
	&& rm -rf $devcontainerFolder \
	&& cp -r $workspaceFolder/$directory/. $workspaceFolder/ \
	&& rm -rf $workspaceFolder/$directory \
	&& clear

