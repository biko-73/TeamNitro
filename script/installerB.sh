#!/bin/sh

##########################################################
version=2.1
description="*** TEAMNITRO by BoHlala V1.0 ***\n Fix some issues related to xml to work skin faster\n Fix renders and converters\n Upgrade to latest python version\n add new PosterX and Extraevent skins !!!"
#########################################################

#########################################################
PACKAGE_DIR='TeamNitro/skins/main'
MY_FILE="Team_Nitro-by_BoHlala-V_1.0.tar.gz"
MY_FILE1="TeamNitro.tar.gz"
#########################################################
MY_MAIN_URL="https://raw.githubusercontent.com/biko-73/"
MY_URL=$MY_MAIN_URL$PACKAGE_DIR'/'$MY_FILE $MY_FILE1
MY_TMP_FILE="/tmp/"$MY_FILE $MY_FILE1

rm -f $MY_TMP_FILE $MY_FILE1 > /dev/null 2>&1

MY_SEP='============================================================='
echo $MY_SEP
echo 'Downloading '$MY_FILE $MY_FILE1' ...'
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
        echo "###########################################################"
        echo "#    Skin.BO-HLALA.FHD $version INSTALLED SUCCESSFULLY       #"
        echo "#                BY BIKO - support on                     #"
        echo "#    https://www.tunisia-sat.com/forums/threads/4236239/  #"
        echo "###########################################################"
        echo "#           your Device will RESTART Now                  #"
        echo "###########################################################"		
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
