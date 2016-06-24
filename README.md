# Crawler

## 网易新闻

## 百度知道

## 百度贴吧
总的逻辑如下
1. 假设某贴吧有 10000 页，parse 就是把这 10000 页的 url 给爬下来，然后 response 交给 first_parse 处理
2. first_parse 爬取本页上的所有 post 的 url，然后 response 交给 second_parse
3. 假设每个 post 有 1-N 页内容，second_parse 就爬取该 post 的该页的内容，response 交给 third_parse
4. third_parse 获取最后的 item 并返回。

值得注意的是 scrapy 默认会根据 url 的 finger print 进行去重，所以在第 3 步的时候很危险的一件事就是对只有 1 页内容的 post，如果把原链接传到 third_parse，那就会发现返回的结果并不会有这些信息，因为链接重复了，因此对于这种 post，要做的是在原链接之后加上 "?pn=1"，形成新链接进行处理。
