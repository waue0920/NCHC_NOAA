

start=$1 #'2011/02/01'
end=$2 #'2011/05/31'

client_ip="140.110.141.141" #"165.124.158.52"
client_user="peggy"
video_folder="~/video/"


time=("00" "06" "12" "18")

cur="$start"
while [ "$cur" != "$end" ]; do

    for i in "${time[@]}"
    do
#        echo $cur"_"$i
	./convert.sh $cur $i
	sleep 2
	scp ${cur}_${i}/video/${cur}_${i}.mp4 ${client_user}@${client_ip}:${video_folder}
	
	rm -rf ${cur}_${i}	
    done
     cur=`date -d"$cur 1 day" "+%Y%m%d"`
#     rm -rf ${cur}_${i}
done


#rm -rf ${cur}_${i}



#time=("00" "06" "12" "18")
#for i in "${time[@]}"
#do
#	file_count=`ls $IMAGE_FOLDER/gfs.0p25.$DATE$i*.png|wc -l`
#	ffmpeg -r 1 -i $IMAGE_FOLDER/gfs.0p25.$DATE$TIME.f%*.png  -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -pix_fmt yuv420p -y  "$VIDEO_FOLDER/${DATE}_${TIME}.mp4"
#done



