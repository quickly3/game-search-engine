import scrapy


class ImgData(scrapy.Item):
    # other fields...
    images = scrapy.Field()
    image_urls = scrapy.Field()


class QuotesSpider(scrapy.Spider):
    name = "ali_fuli1"

    # start_urls = [
    #     'https://www.ali213.net/news/zl/bxgif/',
    # ]
    start_urls = [
        'https://www.ali213.net/news/zl/bxgif/',
    ]

    image_urls = []

    # def start_requests(self):
    #     url = 'https://www.ali213.net/news/html/2019-8/444957.html'
    #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pages = response.xpath('//div[@class="subscribe-li"]/a/@href').getall()
        for page in pages:
            page = page.replace("http://", "https://")
            yield scrapy.Request(page, callback=self.item_parse, meta={'page': page})

    def item_parse(self, response):

        images1 = response.selector.xpath(
            '//*[@id="Content"]/p/img/@src').getall()

        images2 = response.selector.xpath(
            '//*[@id="Content"]/p/a/img/@src').getall()

        image_urls = images1+images2

        yield ImgData(image_urls=image_urls)

        next_page_url = response.selector.xpath(
            '//*[@id="after_this_page"]/@href').get()

        print(next_page_url)
        # item_parse
