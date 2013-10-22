#!/bin/bash
function usage(){
    echo "usage:fsdf"
}

while getopts "a:b:p:t:" opt;do
    case $opt in
        a) 
            app_repo="$OPTARG"
        ;;
        b)
            temp_repo="$OPTARG"
        ;;
        p)
            app_uuid="$OPTARG"
        ;;
		t)
            temp_uuid="$OPTARG"
        ;;
        h|\?)
            usage $0
            exit 0
        ;;
    esac
        
done
slp=0

#首先更新templates文件夹下的模板
echo -n "updating templates... "
git clone --depth 1 "$temp_repo" "$temp_uuid"
find "$temp_uuid/" -name '.*' -print0 | xargs -0 rm -rf

if [[ ! -d templates ]]; then  
    mkdir templates
fi 
sleep $slp
cp -rf "$temp_uuid"/* templates
rm -rf "$temp_uuid"
echo "done."

#更新整个程序文件
echo -n "updating application... "
git clone --depth 1 "$app_repo" ../"$app_uuid"
find "../$app_uuid/" -name '.*' -print0 | xargs -0 rm -rf
sleep $slp
cp -rf ../"$app_uuid"/* .
rm -rf ../"$app_uuid"
echo "done."