#!/bin/bash

bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
cd $bin;

#d=`date +%Y%m%d`
DATE=$1 #`date +%Y%m%d -d "$d - 2 day"`
TIME=$2

FOLDER="/home/peggy/NCHC_NOAA/NCHC_NOAA"
OUTPUT_FOLDER=$FOLDER"/${DATE}_${TIME}"
ORIGIN_FOLDER=$OUTPUT_FOLDER"/grib2"
NETCDF_FOLDER=$OUTPUT_FOLDER"/nc"
IMAGE_FOLDER=$OUTPUT_FOLDER"/image"
VIDEO_FOLDER=$OUTPUT_FOLDER"/video"

PWD="1234"
#TH=1 #350
COMPLETENUM=372
BAND=277
#mkdir -p $FOLDER
mkdir -p $ORIGIN_FOLDER
mkdir -p $NETCDF_FOLDER
mkdir -p $IMAGE_FOLDER
mkdir -p $VIDEO_FOLDER


#convert grib2 to netCDF
file_count_grib=`ls $ORIGIN_FOLDER|wc -l`
file_count_nc=`ls $NETCDF_FOLDER|wc -l`
file_count_img=`ls $IMAGE_FOLDER|wc -l`

#if [ $file_count_grib -ne $COMPLETENUM ]
if [ $file_count_grib -lt 2  ]
then
	/usr/bin/python $bin/download.py  $DATE $TIME $FOLDER 
#       perl download3.pl $PWD $DATE $ORIGIN_FOLDER
fi

#download again
#if [ $file_count_grib -ne $COMPLETENUM ]
#then
#	perl download3.pl $PWD $DATE $ORIGIN_FOLDER
#fi


#if [[ ( "$file_count_grib" -ge "$TH" )  &&  ( $file_count_grib -ne $file_count_nc ) ]]
#then
	for path in $ORIGIN_FOLDER/* 
	do
        echo $path
	if [[ "$path" == *grib2 ]]
	then
		filename=$(basename "$path" ".grib2")
		echo "converting $filename to netCDF..."
		#echo "gdal_translate  -b 3 -of netCDF  $path $NETCDF_FOLDER/$filename.nc"
 		/usr/bin/gdal_translate  -b $BAND -of netCDF  $path $NETCDF_FOLDER/$filename.nc 
	fi
	done
#fi


#convert netCDF to png
echo $file_count_nc
echo $file_count_img
#if [[ ( $file_count_nc -ge $TH ) && ( $file_count_nc -ne $file_count_img ) ]]
#then
	for path in $NETCDF_FOLDER/* 
	do
	if [[ "$path" == *nc ]]
	then
		filename=$(basename "$path" ".nc")
		echo "converting $filename to image...."
		#echo "python plot.py -i $NETCDF_FOLDER/$filename.nc -o $IMAGE_FOLDER/$filename.png"
		/usr/bin/python $bin/plot.py -i $NETCDF_FOLDER/$filename.nc -o $IMAGE_FOLDER/$filename.png
	fi
	done
#fi
#video_num=$(( TH / 4 ))
#convert png to video
#time=("00" "06" "12" "18")
#for i in "${time[@]}"
#do
	file_count=`ls $IMAGE_FOLDER/gfs.0p25.$DATE$i*.png|wc -l`
#	if [ $file_count -ge $video_num ]
#	then
#	echo "ffmpeg -r 1 -i $IMAGE_FOLDER/gfs.0p25.$DATE$i.f%*.png  -vcodec mpeg4 -y $VIDEO_FOLDER/${DATE}_$i.mp4"
	/usr/bin/ffmpeg -r 1 -i $IMAGE_FOLDER/gfs.0p25.$DATE$TIME.f%*.png  -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -pix_fmt yuv420p -y  "$VIDEO_FOLDER/${DATE}_${TIME}.mp4"
#	fi
#done





