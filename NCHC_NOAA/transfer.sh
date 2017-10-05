#!/bin/bash

bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
cd $bin;

#start=$1 #'20110201'
#end=$2 #'20110531'

export PATH=/sbin:/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/usr/lib/jvm/java-8-oracle/bin:/usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin

client_ip="140.110.141.141" #"165.124.158.52"
#client_ip="10.7.50.205" #"165.124.158.52"
client_user="peggy"
video_folder="/home/peggy/video/"
grib_folder="/home/peggy/origin"

datetime=$(date +%s)

function run_command()
{

	cmd=$1
	$cmd
	ret=$?
	if [ "$ret" == "0" ];then 
		echo "[${cur}_${hour}] $cmd" >> $bin/run_transfer.log; 
	fi

}

if [ "$2" != ""  ]
then
        cur=$1
	hour=$2
else
	cur=$(date --date="yesterday" +%Y%m%d)
	#hour=$(date +%H)
	hour="00"
fi

grib_dst_folder=${grib_folder}"/"${cur}"_"${hour}

run_command "echo $(date +%y%m%d_%H%M%S) start..."

run_command "$bin/convert.sh $cur $hour"

sleep 2

run_command "scp $bin/NCHC_NOAA/${cur}_${hour}/video/${cur}_${hour}.mp4 ${client_user}@${client_ip}:${video_folder}"

run_command "ssh ${client_user}@${client_ip} mkdir -p $grib_dst_folder"

run_command "scp -r $bin/NCHC_NOAA/${cur}_${hour}/grib2 ${client_user}@${client_ip}:${grib_dst_folder}"


#run_command "rm -rf $bin/NCHC_NOAA/${cur}_${hour}"

run_command "echo $(date +%y%m%d_%H%M%S) finish"

