import scrapy
from housescraper.items import HouseItem
from urllib.parse import urljoin


class MubawabspiderSpider(scrapy.Spider):
    name = "mubawabspider"
    allowed_domains = ["www.mubawab.tn"]
    start_urls = ["https://www.mubawab.tn/en/cc/real-estate-for-sale"]

    def parse(self, response):
        houses = response.css("div.listingBox")

        for house in houses:

            link = house.css("h2.listingTit a::attr(href)").get()
            prix = house.css("div.priceBar span.priceTag::text").get()

            if link:
                full_link = urljoin(response.url, link)
                yield response.follow(
                    full_link,
                    callback=self.parse_detail,
                    meta={
                        "prix": prix,
                        }
                )

        # Pagination
        next_page = response.css("a#nextPage::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        house_item = HouseItem()
        house_item["titre"] = response.css("h1.searchTitle::text").get()
        house_item["type_bien"] = response.xpath("//p[contains(text(), 'Type of property')]/following-sibling::p/text()").get()
        house_item["prix"] = response.meta.get("prix")
        house_item["ville"] = ville = response.css("h3.greyTit::text").get()
        house_item["surface"] = response.css('.adDetailFeature .icon-triangle + span::text').get()
        house_item["chambres"] = response.css('.adDetailFeature .icon-bed + span::text').get()
        house_item["type_transaction"] = "À Vendre"
        house_item["source"] = "mubawab"
        
        yield house_item
