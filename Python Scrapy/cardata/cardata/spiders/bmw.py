import scrapy, json
from datetime import datetime
from scrapy import Request, FormRequest
from ..items import CardataItem

class BmwSpider(scrapy.Spider):
    name = 'bmw'
    custom_settings = {
        "ROBOTSTXT_OBEY" : False
    }

    def start_requests(self):

        url = "https://www.borusanotomotiv.com/bmw/stage2/fiyat-listesi/static-fiyat-listesi-v2.aspx"
        headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'https://www.bmw.com.tr/',
            'Accept-Language': 'tr,en;q=0.9'
        }
        yield Request(url, headers=headers, callback=self.parse)
    
    def parse(self, response):

        model = None
        for car in response.xpath("//div[@class='SeriesDetail']/div[contains(@id,'seri')]/div[contains(@class,'Detail')]/div[position()>1]"):
            model_xpath = car.xpath("./div[1]/p/text()").get()
            if model_xpath: model = model_xpath.strip()
            
            js = {}
            js["brand"] = "BMW"
            js["model"] = model.replace("BMW", "").strip() if model else None

            year = car.xpath("./div[3]/p/text()").get()
            if year:
                js["year"] = int(year) 
            elif js["model"] and "yeni" in js["model"].lower():
                js["year"] = datetime.today().year
            else:
                js["year"] = datetime.today().year - 1

            js["package"] = car.xpath("./div[2]/p/text()").get().strip() if car.xpath("./div[2]/p/text()").get() else None
            js["price"] = float(car.xpath("./div[10]/p/text()").get().replace(".", "")) if car.xpath("./div[10]/p/text()").get() else None
            js["currency"] = "TRY" if "price" in js.keys() and js["price"] else None
            yield js