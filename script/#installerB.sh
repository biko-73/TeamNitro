#!/bin/sh
#########################################################
version=2.0
description="BoHLALA_FHD" !!!

#########################################################

#########################################################
PACKAGE_DIR='TeamNitro/main/skins'
PACKAGE_DIR2='TeamNitro/main/'

MY_FILE="BoHLALA_FHD.tar.gz"
MY_PLUGIN="TeamNitro.tar.gz"
#########################################################
MY_MAIN_URL="https://raw.githubusercontent.com/biko-73/"

MY_URL=$MY_MAIN_URL$PACKAGE_DIR'/'$MY_FILE
MY_TMP_FILE="/tmp/"$MY_FILE

MY_URL_PLUGIN=$MY_MAIN_URL$PACKAGE_DIR2'/'$MY_PLUGIN
MY_TMP_PLUGIN="/tmp/"$MY_PLUGIN

MY_SEP='============================================================='
echo $MY_SEP
echo 'Downloading '$MY_FILE' ...'
echo $MY_SEP
echo 'Downloading '$MY_PLUGIN' ...'
echo $MY_SEP
echo ''
wget -T 2 $MY_URL_PLUGIN -P "/tmp/"
wget -T 2 $MY_URL -P "/tmp/"

rm -rf "/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro"
rm -rf "/usr/share/enigma2/BoHLALA_FHD"

if [ -f $MY_TMP_FILE ]; [ -f $MY_TMP_PLUGIN ]; then

	echo ''
	echo $MY_SEP
	echo 'Extracting ...'
	echo $MY_SEP
	echo ''
	tar -xf $MY_TMP_FILE -C /
	tar -xf $MY_TMP_PLUGIN -C /
	MY_RESULT=$?

	rm -f $MY_TMP_FILE > /dev/null 2>&1
	rm -f $MY_TMP_PLUGIN > /dev/null 2>&1

	echo ''
	echo ''
	if [ $MY_RESULT -eq 0 ]; then
         echo "#####################################################################"
         echo "#  	TeamNitro Skin $version INSTALLED SUCCESSFULLY   	   #"
         echo "#                	BY BIKO - support on                       #"
         echo "#           https://www.tunisia-sat.com/forums/forums               #"
         echo "#####################################################################"
         echo "#             	  your Device will RESTART Now                     #"
         echo "#####################################################################"		
		if which systemctl > /dev/null 2>&1; then
			sleep 2; systemctl restart enigma2
		else
			init 4; sleep 4; init 3;
		fi
	else
		echo "   >>>>   INSTALLATION FAILED !   <<<<"
	fi;
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
