version= 1.1
description= AL_AYAM_FHD V1.1\n Presenting the new skin by TeamNitro\n Ready to Download... Lets Fun !!!
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
initializeANSI
cat << EOF
${boldon}${redfbright}■■■■■■■■ ${boldon}${greenfbright}  ■■■■■■■■ ${boldon}${yellowfbright}        ■  ${boldon}${bluefbright}      ■■■        ■■■ ${boldon}${redfbright}  ■■■■      ■■ ${boldon}${greenfbright}  ■■■■ ${boldon}${yellowfbright}  ■■■■■■■■ ${boldon}${bluefbright}  ■■■■■■ ${boldon}${purplefbright}      ■■■■ ${reset}
${boldon}${redfbright}■  ■■  ■ ${boldon}${greenfbright}   ■■      ${boldon}${yellowfbright}       ■■■ ${boldon}${bluefbright}         ■■    ■■    ${boldon}${redfbright}     ■■     ■■ ${boldon}${greenfbright}   ■■  ${boldon}${yellowfbright}  ■  ■■  ■ ${boldon}${bluefbright}   ■■   ■■ ${boldon}${purplefbright}  ■■    ■■ ${reset}
${boldon}${redfbright}   ■■    ${boldon}${greenfbright}   ■■      ${boldon}${yellowfbright}      ■■■■■${boldon}${bluefbright}       ■■  ■■■■  ■■  ${boldon}${redfbright}   ■■ ■■    ■■ ${boldon}${greenfbright}   ■■  ${boldon}${yellowfbright}     ■■    ${boldon}${bluefbright}   ■■    ■■ ${boldon}${purplefbright} ■■    ■■ ${reset}
${boldon}${redfbright}   ■■    ${greenf}   ■■■■■■ ${yellowf}      ■(   )■   ${bluef}   ■■   ■■   ■■ ${redf}    ■■  ■■   ■■ ${greenf}   ■■ ${yellowf}      ■■ ${bluef}      ■■   ■■ ${purplef}  ■■    ■■ ${reset}
${boldon}${redfbright}   ■■    ${greenf}   ■■     ${yellowf}     ■■■■ ■■■■  ${bluef}   ■■        ■■ ${redf}    ■■   ■■  ■■ ${greenf}   ■■ ${yellowf}      ■■ ${bluef}      ■■ ■■   ${purplef}  ■■    ■■ ${reset}
${boldon}${redfbright}   ■■    ${greenf}   ■■     ${yellowf}    ■■       ■■ ${bluef}   ■■        ■■ ${redf}    ■■    ■■    ${greenf}   ■■ ${yellowf}      ■■ ${bluef}      ■■   ■■ ${purplef}  ■■    ■■ ${reset}
${boldon}${redfbright}  ■■■■   ${greenf}  ■■■■■■■■${yellowf}   ■■         ■■${bluef}   ■■        ■■ ${redf}    ■■     ■■■■ ${greenf}  ■■■■${yellowf}     ■■■■${bluef}     ■■■■   ■■${purplef}    ■■■■ ${reset}
${boldon}${yellowfbright}				    TeamNitro Skin BoHLALA V2.3 ${reset}
EOF
MY_FILE="TeamNitro.tar.gz"
MY_TMP_FILE="/var/volatile/tmp/"$MY_FILE
MY_FILE1="AL_AYAM_FHD_v-1.1.tar.gz"
MY_TMP_FILE1="/var/volatile/tmp/"$MY_FILE1
MY_SEP='============================================================='
echo $MY_SEP
echo 'Downloading '$MY_FILE' ...'
echo $MY_SEP
echo 'Downloading '$MY_FILE1' ...'
echo $MY_SEP
echo ''
rm -rf "/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro"
rm -rf "/usr/share/enigma2/AL_AYAM_FHD"
rm -rf "/usr/lib/enigma2/python/Components/Converter/TN_Bitrate3.pyc"
rm -rf "/usr/lib/enigma2/python/Components/Converter/DRNextEvents.pyc"
wget -O /var/volatile/tmp/TeamNitro.tar.gz --no-check-certificate "https://github.com/biko-73/TeamNitro/raw/main/skins/TeamNitro.tar.gz"
wget -O /var/volatile/tmp/AL_AYAM_FHD_v-1.1.tar.gz --no-check-certificate "https://github.com/biko-73/TeamNitro/raw/main/skins/AL_AYAM_FHD_v-1.1.tar.gz"
if [ -f $MY_TMP_FILE ]; [ -f $MY_TMP_FILE1 ]; then
echo ''
echo $MY_SEP
echo 'Extracting ...'
echo $MY_SEP
echo ''
tar -xzvf $MY_TMP_FILE; $MY_TMP_FILE1  -C /
chmod 755 /usr/bin/opbitrate
MY_RESULT=$?
rm -f $MY_TMP_FILE > /dev/null 2>&1
rm -f $MY_TMP_FILE1 > /dev/null 2>&1
echo ''
if [ $MY_RESULT -eq 0 ]; then
echo "########################################################################"
echo "#            AL_AYAM_FHD by TeamNitro INSTALLED SUCCESSFULLY          s#"
echo "#                      BY TeamNitro - support on                       #"
echo "#              https://www.tunisia-sat.com/forums/forums               #"
echo "########################################################################"
echo "#        Sucessfully Download Please apply from skin selection         #"
echo "########################################################################"
if which systemctl > /dev/null 2>&1; then
sleep 2; systemctl restart enigma2
else
init 4
sleep 4 > /dev/null 2>&1
init 3
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
