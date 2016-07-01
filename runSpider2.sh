#!/bin/bash
currentPath=`pwd`
usage ()
{
  echo 'Usage : '
  echo '-s <spider, with default all spiders>'
  echo '-c <categories split by "，"> '
  echo '-f <input file> '
  echo '-o <output file> '
  echo '-a <run all spiders, with default "output.json"> '
  echo '-h <help>'
  exit
}

runSpider_category ()
{
  echo $1
  cd $1
  scrapy crawl $1 -a category=${category}
  cd ..
}

runSpider_file ()
{
  echo $1
  cd $1
  scrapy crawl $1 -a file=${currentPath}'/'${file}
  cd ..
}

run ()
{
  if [ ! $category ] && [ ! $file ]; then
    echo 'Please identify the input'
    usage
  fi

  if [ ! $output ]; then
    output='output.json'
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
  else
    if [ $category ]; then
      runSpider_category 'Zhidao'
      runSpider_category 'Tieba'
      runSpider_category 'Wangyi'
    else
      runSpider_file 'Zhidao'
      runSpider_file 'Tieba'
      runSpider_file 'Wangyi'
    fi
  fi
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

run
