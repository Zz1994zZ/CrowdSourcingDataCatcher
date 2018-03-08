# CrowdSourcingDataCatcher
### python实现爬虫抓取[https://www.proginn.com/users/](https://www.proginn.com/users/ "程序员客栈")中的程序员信息（作研究用途）
## 流程：
### 从数据库读取已经爬取过的程序员序号放入布隆过滤器完成初始化
### url收集线程：遍历每个页码收集程序员序号加入队列
### 信息抓取线程：从队列中取出一个序号，再从代理池（从[https://www.kuaidaili.com/free](https://www.kuaidaili.com/free)抓取代理）中取一个代理，抓取该序号对应程序员页面的数据存入数据库

### DOM处理使用BeautifulSoup
