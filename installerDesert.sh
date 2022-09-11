#!/bin/sh
#########################################################
version=1.0
description="DesertFHD" !!!

#########################################################

#########################################################
PACKAGE_DIR='TeamNitro/main/'
MY_FILE="DesertFHD.tar.gz"
#########################################################
MY_MAIN_URL="https://raw.githubusercontent.com/biko-73/"
MY_URL=$MY_MAIN_URL$PACKAGE_DIR'/'$MY_FILE
MY_TMP_FILE="/tmp/"$MY_FILE

rm -f $MY_TMP_FILE > /dev/null 2>&1

MY_SEP='============================================================='
echo $MY_SEP
echo 'Downloading '$MY_FILE' ...'
echo $MY_SEP
echo ''
wget -T 2 $MY_URL -P "/tmp/"

if [ -f $MY_TMP_FILE ]; then

	echo ''
	echo $MY_SEP
	echo 'Extracting ...'
	echo $MY_SEP
	echo ''
	tar -xf $MY_TMP_FILE -C /
	MY_RESULT=$?

	rm -f $MY_TMP_FILE > /dev/null 2>&1


	echo ''
	echo ''
	if [ $MY_RESULT -eq 0 ]; then
        echo "#####################################################################"
        echo "#  	TeamNitro Skin $descriptio $version INSTALLED SUCCESSFULLY   #"
        echo "#                			BY BIKO - support on                      #"
        echo "#      		 https://www.tunisia-sat.com/forums/forums            #"
        echo "#####################################################################"
        echo "#             	your Device will RESTART Now             	      #"
        echo "#####################################################################"		
		if which systemctl > /dev/null 2>&1; then
			sleep 2; systemctl restart enigma2
		else
			init 4; sleep 4; init 3;
		fi
	else
		echo "   >>>>   INSTALLATION FAILED !   <<<<"
	fi;
	echo ''
	echo '**************************************************'
	echo '**                   FINISHED                   **'
	echo '**************************************************'
	echo ''
	exit 0
else
	echo ''
	echo "Download failed !"
	exit 1
fi
# ------------------------------------------------------------------------------------------------------------