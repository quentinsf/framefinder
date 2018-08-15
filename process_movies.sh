#! /bin/bash

for i in movies/*.mp4
do 
    echo $i
    BASE=`echo $i|sed -e 's/.mp4//'`
    ffmpeg -i $i -codec copy -y $BASE.mov
    # exiftool -rotation=180 $BASE.mov
done

