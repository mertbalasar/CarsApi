# API KULLANIMI
API Taban Adresi: [https://mertbalasar.azurewebsites.net/](https://mertbalasar.azurewebsites.net/)
| Yöntem | Adres | Açıklama
|--|--|--|
| `GET` | `.api/CarData` | Tüm araçların listesini döndürür |
| `GET` | `.api/CarData/id=4` | ID numarası 4 olan aracı döndürür |
| `GET` | `.api/CarData/brand=bmw` | Markası BMW olan araçların listesini döndürür |
| `GET` | `.api/CarData/yearUpLimit=2021` | Üretim yılı 2021'e eşit veya az olan araçların listesini döndürür |
| `GET` | `.api/CarData/yearDownLimit=2020` | Üretim yılı 2020'ye eşit veya fazla olan araçların listesini döndürür |
| `GET` | `.api/CarData/priceUpLimit=350000` | Fiyatı 350000'e eşit veya az olan araçların listesini döndürür |
| `GET` | `.api/CarData/priceDownLimit=350000` | Fiyatı 350000'e eşit veya fazla olan araçların listesini döndürür |

Geri Dönüş Değeri

   

    {
	    "id":1,
	    "brand":"BMW",
	    "model":"118i",
	    "year":2020,
	    "package":"Sport Line",
	    "price":424100,
	    "currency":"TRY"
	}

 - id: Her aracın kendine özgü kimlik numarası
 - brand: Aracın markası
 - model: Aracın modeli
 - year: Aracın üretim yılı
 - package: Aracın donanım paketi
 - price: Aracın Türkiye'de bayi satış fiyatı
 - currency: Aracın satıldığı fiyatın para birimi
