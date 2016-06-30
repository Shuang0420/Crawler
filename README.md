# Crawler

根据关键词爬取 **[网易新闻](https://github.com/Shuang0420/Crawler/tree/master/wangyi)、[百度知道](https://github.com/Shuang0420/Crawler/tree/master/zhidao)、[百度贴吧](https://github.com/Shuang0420/Crawler/tree/master/tieba)** 的内容。
## 网易新闻
### 今日热点
[news.py](https://github.com/Shuang0420/Crawler/blob/master/news.py) 是直接用 python 实现的爬虫，并没有用到 scrapy，output 是 html 文件； [wynews](https://github.com/Shuang0420/Crawler/tree/master/wynews) 用到了 scrapy，ouput 是 json 文件。
仅爬取 "1小时前点击排行" 新闻。

- html 版
一个类别一个文件，标题 "\t" url（超链接太丑，所以分开写）
![](http://7xu83c.com1.z0.glb.clouddn.com/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202016-06-24%20%E4%B8%8B%E5%8D%888.44.48.png)

![](http://7xu83c.com1.z0.glb.clouddn.com/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202016-06-24%20%E4%B8%8B%E5%8D%888.42.29.png)

- json 版
<pre>{"category": "校园", "url": "http://news.163.com/special/0001386F/rank_campus.html", "secondary_title": "星海校花身材修长 曾被爆为陈学冬女友", "secondary_url": "http://daxue.163.com/15/0126/17/AGTCQNPI00913J5O.html"}</pre>

### 关键词搜索
[wangyi](https://github.com/Shuang0420/Crawler/tree/master/wangyi) 实现利用关键词爬取网易新闻。输出格式是 json。
<pre>{"url":"http://elite.youth.cn/channel/201606/t20160627_8195089.htm","text":"2016-06-2717:29:00  来源：中华儿女报刊社  编辑：安吉　　2016年6月25日,国窖1573日照公司总经理许加东、山东周智律师事务所行政副主任王建英一行来国美酒业四川有限公司考察交流。国美酒业集团董事长武玉杰、国美酒业四川有限公司副总经理柳加润陪同来宾参观了国美酒业四川有限公司包装车间、酿酒车间、国美酒窖及范曾著《锦文掇英—学研习近平用典心得》书法作品四川展览馆。　　在参观中,武玉杰董事长向许加东总经理一行介绍了国美酒业四川有限公司的生产规模和品牌建设等情况,特别是国美酒业集团创新营销,与京东集团达成战略合作伙伴,开创了白酒营销新格局,以及公司与北京科研机构开展保健酒、生物工程的合作,和酱香酒车间在重阳节期间投料备产,这一些都彰显了公司迅猛发展的态势。　　许加东总经理一行在具体了解国美酒业四川有限公司的发展规划、品牌建设、文化底蕴等各方面情况并品评国美美酒后,对国美酒业集团的综合实力十分赞赏。　　双方并对产品销售渠道建设等方面进行了深入沟通和交流。我要说两句没有可显示评论！！旗下样刊","title":"国窖1573日照公司总经理许加东来国美酒业考察交流_中华儿女"}</pre>

## 百度知道
### 输出格式
一个问答是一条记录，多个回答间用 "##" 分隔。
<pre>
{"url":"http://zhidao.baidu.com/question/1691515616122360188.html?fr=iks&word=%E6%BB%B4%E6%BB%B4&ie=gbk","answer":"滴滴快车一块五一公里，比出租车便宜。##你输入目的地就能出来大致钱##差不多 25块钱吧。","question":"滴滴打车去目的地有20公里外的地方要多少车费","title":"滴滴打车去目的地有20公里外的地方要多少车费"}
</pre>

## 百度贴吧
### 输出格式
一个 post 的一页是一条记录，楼与楼之间用 "##" 分隔。
<pre>{"url": "http://tieba.baidu.com/p/4619660649", "text": "##什么情况啊##亲，抱歉给您带来不便，麻烦您提供下订单号码，方便及时查询处理您的问题。##正在出库还是小事，我的快递还被签收了，他们厉害吧##解决了，这家店居然周末不看订单##我也也是没收到货，确签收了，太坑人。解决事情太慢，", "pageUrl": "http://tieba.baidu.com/p/4619660649?pn=1", "title": "怎么两天了还正在出库？？？"}</pre>

## 使用方法
### 简洁版（必须指定 spider, category, output）
<pre>./runSpider.sh spider(Zhidao/Tieba/Wynews/Wangyi) category output</pre>

注：
Wynews 中的 category 指新闻类别，包括 新闻/娱乐/体育/财经/科技/汽车/女人/房产/读书/游戏/旅游/教育/公益/校园/传媒/视频/移动/全站/图集排行榜；Wangyi Tieba Zhidao 的 category 即搜索关键词

eg. 爬取百度知道有关 iphone 的信息并保存为 iphone.json
<pre>./runSpider.sh Zhidao iphone iphone.zhidao.json</pre>

### 复杂版（可选参数）
<pre> ./runSpider2.sh -s (Zhidao/Tieba/Wynews/Wangyi) -f input</pre>
Usage :
-s <spider, with default all spiders>
-c <categories split by "，">
-f <input file>
-o <output>
-a <run all spiders, with default "output.json">
-h <help>
</pre>

eg. 爬取 **百度知道** 有关 iphone 的信息并保存为 iphone.json
<pre>./runSpider2.sh -s Zhidao -c iphone -o iphone.zhidao.json</pre>

eg. 爬取 **百度知道、百度贴吧、网易新闻** 所有有关 iphone 的信息并保存为默认 output.json
<pre>./runSpider2.sh -c iphone</pre>

## 数据后续处理
[convertJson.py](https://github.com/Shuang0420/Crawler/blob/master/convertJson.py) 文件用于处理 json 文件，去除标点符号和其他特殊符号，输出较为“干净”的 txt 文件，用于之后的分词等工作。
filename 必须以 zhidao.json, tieba.json, wangyi.json 结尾。
<pre>python convertJson.py filename</pre>
