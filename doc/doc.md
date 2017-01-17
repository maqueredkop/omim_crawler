

####note:

1 脚本文件为 omim_crawler.py, python 版本为python3, 需要两个额外的包 requests, bs4

2 运行脚本文件，无需其他参数，会在当前文件夹内生成两个结果文件，
  其中， alzheimer_search_result.txt 为脚本在 OMIM 网站上自动查询结果文件
         mutation_output.txt 为根据上面的查询结果文件进行 mutation 信息的抓取的结果。

3 爬虫的正常运行依赖于稳定的网络，脚本测试表明可以正常运行，大约需要 5 min, 如果等待时间过长，建议重新运行或者更换其他网络。
