#!/bin/bash

#file name
if [ x$1 != x ] && [ x$2 != x ] && [ x$3 != x ]
then
    folder=$1
    category=$2
    output=$3
else
    echo "please run the following command ./runSpider.sh Zhidao/Tieba category output"
    exit 12
fi


cd $folder

scrapy crawl $folder -a category=$category
cd ..
path=${folder}"/items.json"

cat $path >> $output
