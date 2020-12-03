import scrapy


class ThepaperSpider(scrapy.Spider):
    name = 'thepaper'
    allowed_domains = ['m.thepaper.cn']
    start_urls = ['http://m.thepaper.cn/list_page.jsp?nodeid=25600&isList=1&pageidx=1']
    page_number = 2
    find_exist_data_flag = False

    def parse(self, response):
        list_item = response.xpath("//div[@class='list_item']")
        for item in list_item:
            # 标题
            title = item.xpath(".//span/a/text()").extract_first()
            # 文章超链接
            title_url = item.xpath(".//span/a/@href").extract_first()
            # 图片
            img_url = item.xpath(".//a/img/@src").extract_first()

            # print("---------------------------------------", title, title_url, img_url)
            yield {
                "type": "text",
                "title": title,
                "title_url": title_url
            }
            # print("===================================", img_url)
            yield scrapy.Request(url=img_url, callback=self.parse_img, cb_kwargs={"img_name": title}, dont_filter=True)
        if not self.find_exist_data_flag:
            self.page_number += 1
            if self.page_number <= 5:
                next_page_url = "https://m.thepaper.cn/list_page.jsp?nodeid=25600&isList=1&pageidx=%s" % self.page_number
                yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_img(self, response, img_name):

        # print("--------------------------------=================", response.body)
        yield {
            "type": "img",
            "img_name": "./images/" + img_name + ".jpg",
            "img": response.body
        }
