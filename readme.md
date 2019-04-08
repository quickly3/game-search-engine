# Game Search Engine

> 这是一个自动收集游戏信息并提供搜索引擎搜索的项目

### 主要开源技术
>后端框架 Laravel 5.6   
前端框架 Angular 7.2.12  
爬虫框架 Scrapy 1.4  
搜索引擎 ElasticSearch 6.5  
关系数据库 mysql 5.7   

### 安装部署
>npm install  
composer install  
php artisan key:generate  
前端开发模式 npm run watch  
部署模式 npm run prod  

###  爬虫命令 
>  爬虫代码在scrapy 目录下   
scrapy crawl ali  
scrapy crawl ali2  
sudo php artisan MysqlToEs  
