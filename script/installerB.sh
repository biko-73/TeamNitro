#!/bin/sh
initializeANSI()
{
  esc=""

  redf="${esc}[31m";     greenf="${esc}[32m"
  yellowf="${esc}[33m"   bluef="${esc}[34m";   
  cyanf="${esc}[36m";    purplef="${esc}[35m"   
  
  redfbright="${esc}[91m";     greenfbright="${esc}[92m"
  yellowfbright="${esc}[93m"   bluefbright="${esc}[94m";   
  cyanfbright="${esc}[96m";    purplefbright="${esc}[95m"   
                      
  boldon="${esc}[1m";    
  reset="${esc}[0m"
}

# note in this first use that switching colors doesn't require a reset
# first - the new color overrides the old one.

initializeANSI

cat << EOF 

${boldon}${redfbright}■■■■■■■■ ${boldon}${greenfbright}  ■■■■■■■■ ${boldon}${yellowfbright}        ■  ${boldon}${bluefbright}      ■■■        ■■■ ${boldon}${redfbright}  ■■■■      ■■ ${boldon}${greenfbright}  ■■■■ ${boldon}${yellowfbright}  ■■■■■■■■ ${boldon}${bluefbright}  ■■■■■■ ${boldon}${purplefbright}      ■■■■ ${reset}
${boldon}${redfbright}■  ■■  ■ ${boldon}${greenfbright}   ■■      ${boldon}${yellowfbright}       ■■■ ${boldon}${bluefbright}         ■■    ■■    ${boldon}${redfbright}     ■■     ■■ ${boldon}${greenfbright}   ■■  ${boldon}${yellowfbright}  ■  ■■  ■ ${boldon}${bluefbright}   ■■   ■■ ${boldon}${purplefbright}  ■■    ■■ ${reset}
${boldon}${redfbright}   ■■    ${boldon}${greenfbright}   ■■      ${boldon}${yellowfbright}      ■■■■■${boldon}${bluefbright}       ■■  ■■■■  ■■  ${boldon}${redfbright}   ■■ ■■    ■■ ${boldon}${greenfbright}   ■■  ${boldon}${yellowfbright}     ■■    ${boldon}${bluefbright}   ■■    ■■ ${boldon}${purplefbright} ■■    ■■ ${reset}
${boldon}${redfbright}   ■■    ${greenf}   ■■■■■■ ${yellowf}      ■(   )■   ${bluef}   ■■   ■■   ■■ ${redf}    ■■  ■■   ■■ ${greenf}   ■■ ${yellowf}      ■■ ${bluef}      ■■   ■■ ${purplef}  ■■    ■■ ${reset}
${boldon}${redfbright}   ■■    ${greenf}   ■■     ${yellowf}     ■■■■ ■■■■  ${bluef}   ■■        ■■ ${redf}    ■■   ■■  ■■ ${greenf}   ■■ ${yellowf}      ■■ ${bluef}      ■■ ■■   ${purplef}  ■■    ■■ ${reset}
${boldon}${redfbright}   ■■    ${greenf}   ■■     ${yellowf}    ■■       ■■ ${bluef}   ■■        ■■ ${redf}    ■■    ■■    ${greenf}   ■■ ${yellowf}      ■■ ${bluef}      ■■   ■■ ${purplef}  ■■    ■■ ${reset}
${boldon}${redfbright}  ■■■■   ${greenf}  ■■■■■■■■${yellowf}   ■■         ■■${bluef}   ■■        ■■ ${redf}    ■■     ■■■■ ${greenf}  ■■■■${yellowf}     ■■■■${bluef}     ■■■■   ■■${purplef}    ■■■■ ${reset}

${boldon}${yellowfbright}				    TeamNitro By BoHLALA V1.0 Version 3.0 BY KIMOO1987 ${reset}

EOF
##########################################################
version=2.1
description="*** TEAMNITRO by BoHlala V1.0 ***\n Fix some issues related to xml to work skin faster\n Fix renders and converters\n Upgrade to latest python version\n add new PosterX and Extraevent skins !!!"
#########################################################

#########################################################
MY_FILE="TeamNitro.tar.gz"
MY_TMP_FILE="/var/volatile/tmp/"$MY_FILE
MY_FILE1="Team_Nitro-by_BoHlala-V_1.0.tar.gz"
MY_TMP_FILE1="/var/volatile/tmp/"$MY_FILE1
#########################################################

MY_SEP='============================================================='
echo $MY_SEP
echo 'Downloading '$MY_FILE' ...'
echo $MY_SEP
echo 'Downloading '$MY_FILE1' ...'
echo $MY_SEP
echo ''


wget -O /var/volatile/tmp/TeamNitro.tar.gz --no-check-certificate "https://github.com/biko-73/TeamNitro/raw/main/skins/TeamNitro.tar.gz"
wget -O /var/volatile/tmp/Team_Nitro-by_BoHlala-V_1.0.tar.gz --no-check-certificate "https://github.com/biko-73/TeamNitro/raw/main/skins/Team_Nitro-by_BoHlala-V_1.0.tar.gz.tar.gz"

rm -rf "/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro"
rm -rf "/usr/share/enigma2/BoHLALA_FHD"


if [ -f $MY_TMP_FILE ]; [ -f $MY_TMP_FILE1 ]; then

	echo ''
	echo $MY_SEP
	echo 'Extracting ...'
	echo $MY_SEP
	echo ''
	tar -xf $MY_TMP_FILE -C /
	tar -xf $MY_TMP_FILE1 -C /
	MY_RESULT=$?

	rm -f $MY_TMP_FILE > /dev/null 2>&1
	rm -f $MY_TMP_FILE1 > /dev/null 2>&1

	echo ''
	if [ $MY_RESULT -eq 0 ]; then
         echo "########################################################################"
         echo "#          TeamNitro By BoHLALA V1.0 INSTALLED SUCCESSFULLY            s#"
         echo "#                      BY TeamNitro - support on                       #"
         echo "#              https://www.tunisia-sat.com/forums/forums               #"
         echo "########################################################################"
         echo "#        Sucessfully Download Please apply from skin selection         #"
         echo "########################################################################"
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
# ----------------------------------------------------------------------------------------------------------
