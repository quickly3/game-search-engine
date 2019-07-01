# Game Search Engine

> 这是一个自动收集游戏信息并提供搜索引擎服务的项目

### 网站地址
<http://www.zhouhongbin.com>

### 主要开源技术
>后端框架 Laravel 5.6   
前端框架 Angular 7.2.12  
爬虫框架 Scrapy 1.4  
搜索引擎 ElasticSearch 6.5  
关系数据库 mysql 5.7   

### 爬虫数据源
>游侠网 


### 安装部署
>npm install  
composer install  
php artisan key:generate  
前端开发 监听模式 npm run watch  
部署模式 npm run prod  

###  爬虫命令 
>  爬虫代码在scrapy 目录下 

游侠网 
>scrapy crawl ali  
scrapy crawl ali2  

Elasticsearch日报
>scrapy crawl escn  
scrapy crawl escn2
scrapy crawl nba_player

B站弹幕
>scrapy crawl fanju
scrapy crawl episode
scrapy crawl danmu

scrapy crawl episode -a ssid=*
scrapy crawl danmu -a ssid=*

### 数据挖掘
>???有么

### 数据转换
>sudo php artisan MysqlToEs  
>sudo php artisan EscnToEs  


###  更多数据源和功能
>挤时间中...

### 理论模型
> 喵喵喵？