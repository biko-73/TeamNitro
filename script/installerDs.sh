#!/bin/sh
#########################################################
version=3.0
description="add new basic skin !!!"
#########################################################

#########################################################
PACKAGE_DIR='TeamNitro/main/skins'
MY_FILE="DesertFHD_v-3.0.tar.gz"
#########################################################

##############################################################################################################
##
## Script Purpose: Download and install NitroTeam skin
##
## Command: wget https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerDs.sh -O - | /bin/sh
##
##############################################################################################################

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
        echo "#########################################################"
        echo "#   DesertFHD Skin $version INSTALLED SUCCESSFULLY      #"
        echo "#              BY NitroTeam - support on                #"
        echo "#  https://www.tunisia-sat.com/forums/threads/4334347/  #"
        echo "#########################################################"
        echo "#           your Device will RESTART Now                #"
        echo "#########################################################"		
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
