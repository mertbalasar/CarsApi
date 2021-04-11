import scrapy, json
from scrapy import Request, FormRequest
from ..items import CardataItem

class RenaultSpider(scrapy.Spider):
    name = 'renault'

    def start_requests(self):

        url = "https://best.renault.com.tr/wp-json/service/v1/CatFiyatData?cat=Binek"
        headers = {
            'authority': 'best.renault.com.tr',
            'accept': 'application/json, text/plain, */*',
            'referer': 'https://best.renault.com.tr/fiyat-listesi/?kat=Binek',
            'accept-language': 'tr,en;q=0.9',
        }
        yield Request(url, headers=headers, callback=self.parse)
    
    def parse(self, response):

        data = json.loads(response.body)
        for item in data["results"]:
            js = {}
            js["brand"] = "Renault"
            js["model"] = item["ModelAdi"].strip() if "ModelAdi" in item.keys() else None
            js["year"] = int(item["ModelYili"]) if "ModelYili" in item.keys() else None
            js["package"] = item["VersiyonAdi"].strip() if "VersiyonAdi" in item.keys() else None
            js["price"] = float(item["AntesFiyati"].replace(",", ".")) if "AntesFiyati" in item.keys() else None
            js["currency"] = item["ParaBirimi"].strip() if "ParaBirimi" in item.keys() else None
            yield js