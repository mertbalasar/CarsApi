import scrapy, json
from scrapy import Request, FormRequest
from ..items import CardataItem

class FiatSpider(scrapy.Spider):
    name = 'fiat'

    def start_requests(self):

        url = "https://alfa.digitalpanorama.com.tr/fiat/pricelist/backend/api/defaults?type=binek"
        yield Request(url, callback=self.get_year)
    
    def get_year(self, response):

        data = json.loads(response.body)
        for item in data["YearList"]:
            year = int("".join(filter(str.isnumeric, item["Title"]))) if "".join(filter(str.isnumeric, item["Title"])) else None
            query = item["Year"].strip().replace(" ", "+")
            follow_url = f"https://alfa.digitalpanorama.com.tr/fiat/pricelist/backend/api/vehicles?year={query}&type=0"
            yield Request(follow_url, callback=self.jump_body, meta={"year": year})
    
    def jump_body(self, response):
        
        data = json.loads(response.body)
        for item in data["Data"]:
            id_ = item["Id"] if "Id" in item.keys() else ""
            follow_url = f"https://alfa.digitalpanorama.com.tr/fiat/pricelist/backend/api/bodys?vehicle={id_}"
            model = item["Title"].replace("Yeni", "").strip() if "Title" in item.keys() else ""
            yield Request(follow_url, callback=self.jump_model, meta={"year": response.meta["year"], "model": model})
    
    def jump_model(self, response):

        data = json.loads(response.body)
        for item in data["Data"]:
            id_ = item["Id"] if "Id" in item.keys() else ""
            follow_url = f"https://alfa.digitalpanorama.com.tr/fiat/pricelist/backend/api/models?body={id_}"
            yield Request(follow_url, callback=self.jump_price, meta={"year": response.meta["year"], "model": response.meta["model"]})
    
    def jump_price(self, response):

        data = json.loads(response.body)
        for item in data["Data"]:
            id_ = item["Id"] if "Id" in item.keys() else ""
            follow_url = f"https://alfa.digitalpanorama.com.tr/fiat/pricelist/backend/api/prices?model={id_}"
            yield Request(follow_url, callback=self.get_details, meta={"year": response.meta["year"], "model": response.meta["model"]})
    
    def get_details(self, response):

        data = json.loads(response.body)
        for item in data["PriceValues"]:
            js = {}
            js["brand"] = "Fiat"
            js["model"] = response.meta["model"]
            js["year"] = response.meta["year"]

            package = None
            price = None
            for other_item in item["Prices"]:
                if other_item["Title"] == "Donanım": package = item["Title"].strip() + " " + other_item["Value"].strip()
                if "Fiyat" in other_item["Title"]: price = float(other_item["Value"].lower().replace("tl", "").replace(".", "").replace(",", ".")) 

            js["package"] = package if package else None
            js["price"] = price if price else None
            js["currency"] = "TRY" if "price" in js.keys() and js["price"] else None
            yield js