#!/bin/bash
currentPath=`pwd`
usage ()
{
  echo 'Usage : '
  echo '-s <spider, with default all spiders>'
  echo '-c <categories split by "，"> '
  echo '-f <input file> '
  echo '-o <output> '
  echo '-a <run all spiders, with default "output.json"> '
  echo '-h <help>'
  exit
}


while getopts ":c:f:o:s:h" opt
do
        case $opt in
                c ) category=$OPTARG;;
                f ) file=$OPTARG;;
                o ) output=$OPTARG;;
                h ) usage;;
                s ) spider=$OPTARG;;
                ? ) echo "error"
                    exit 1;;
        esac
done

if [ ! $category ] && [ ! $file ]; then
  echo 'Please identify the input'
  usage
fi

if [ ! $output ]; then
  output='output.json'
  echo $output
fi

if [ $spider ]; then
  cd $spider
  if [ $category ]; then
    scrapy crawl $spider -a category=$category
  else
    scrapy crawl $spider -a file=${currentPath}'/'${file}
  fi
  cd ..
  path=${spider}"/items.json"
  cat $path >> $output
  echo '[output]: ' $output
fi
