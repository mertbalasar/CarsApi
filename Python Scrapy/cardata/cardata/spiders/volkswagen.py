import scrapy, json
from scrapy import Request, FormRequest
from ..items import CardataItem

class VolkswagenSpider(scrapy.Spider):
    name = 'volkswagen'

    def start_requests(self):

        url = "https://binekarac2.vw.com.tr/fiyatlardata/fiyatlar.json"
        yield Request(url, callback=self.parse)
    
    def parse(self, response):

        data = json.loads(response.body)
        for item in data["Data"]["FiyatBilgisi"]:
            year = int(item["-YIL"]) if "-YIL" in item.keys() else ""
            for car in item["Arac"]:
                car_data = car["AracXML"]["PriceData"]
                model = car_data["-ModelName"].strip() if "-ModelName" in car_data.keys() else None
                for packages in car_data["SubList"]["Item"]:
                    js = {}

                    js["brand"] = "Volkswagen"

                    js["model"] = model if model else None

                    js["year"] = year if year else None

                    gear = None
                    hardware = None
                    price = None
                    currency = None
                    try:
                        for i in packages["SubItem"]:
                            if i["-Title"] == "Şanzıman": gear = i["-Value"].strip() if i["-Value"] else " "
                            if i["-Title"] == "Donanım": hardware = i["-Value"].strip() if i["-Value"] else " "
                            if i["-Title"] == "Fiyat (*1-2-3-8)": price = float(i["-Value"].replace("₺", "").replace(".", "").replace(",", ".")) if i["-Value"] else None
                            if i["-Title"] == "Fiyat (*1-2-3-8)": currency = i["-Currency"].strip() if i["-Currency"] else None
                    except:
                        continue

                    package_name = packages["-Value"] + " " + gear + " " + hardware
                    js["package"] = package_name.strip() if package_name else None

                    js["price"] = price if price else None

                    js["currency"] = currency.replace("TL", "TRY") if currency else None

                    yield js