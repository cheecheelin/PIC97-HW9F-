import scrapy
from tutorial.items import CraigslistItem
import re 


class RoomSpider(scrapy.Spider):
    name = "rooms"
    allowed_domains = ["sfbay.craigslist.org"]
    start_urls = [
        "https://sfbay.craigslist.org/search/sfc/sub"
    ]

    # for i in range(1,24):
    #     start_urls.append(base_url+"s="+str(i)+"00&")
            
    def __init__(self):
        self.i = 0 # counter to limit number of results
    
    def parse(self,response):
        url = response.url
        titlebar = response.xpath('//*[@id="pagecontainer"]/section/h2/text()').extract()
        title = ''.join(titlebar)
        price = response.xpath('//*[@class="price"]/text()').extract()
        price = int(re.search(r'\$(\d+)', price[0]).group(1))
        content = response.xpath('//*[@id="postingbody"]').extract()[0]
        maplink = response.xpath('//*[@id="pagecontainer"]/section/section[2]/div[1]/div/p/small/a[1]').extract()

        longitude = None
        latitude = None
        mapdata = response.xpath('//*[@id="map"]')
      
        if len(mapdata) != 0:
            longitude = float(mapdata.xpath("@data-longitude").extract()[0])
            latitude = float(mapdata.xpath("@data-latitude").extract()[0])

        attributes = response.xpath('//*[@id="pagecontainer"]/section/section[2]/div[1]/p').extract()[0]

        image_links = response.xpath('//*[@id="picview"]/a/@href').extract()
        #changed from thumbs to picview 
        time = response.xpath('//*[@id="display-date"]/time/@datetime').extract()[0]


        item = CraigslistItem(
          url=url,
          size=None,
          price=price,
          title=title,
          content=content,
          maplink=maplink,
          longitude=longitude,
          latitude=latitude,
          attributes=attributes,
          image_links=image_links,
          time=time)

        return item

#         if self.i < 10:
#             for sel in response.xpath("//li[@class='regular-search-result']"):
#                 item = YelpItem()
#                 item["name"] = sel.xpath(".//a[@class='biz-name']/span/text()").extract()
#                 item["stars"]= sel.xpath(".//i[contains(@class,'star-img')]/img/@alt").extract()
#                 item["reviews"]= sel.xpath(".//span[@class='review-count rating-qualifier']/text()").extract()[0].strip()
#                 item["street_address1"]= sel.xpath(".//address/text()[1]").extract()[0].strip()
#                 item["street_address2"]= sel.xpath(".//address/text()[2]").extract()[0].strip()
#                 link = sel.xpath(".//a[@class='biz-name']/@href")
#                 if link:
#                     url = response.urljoin(link[0].extract())
#                     request = scrapy.Request(url, self.parse_quote)
#                     request.meta['item'] = item
#                     yield request
# #                yield item # we don't want the item to be returned until we get the top-quoted item
                
#             next_page = response.xpath("//a[@class='u-decoration-none next pagination-links_anchor']/@href")
#             if next_page:
#                 url = response.urljoin(next_page[0].extract())
#                 yield scrapy.Request(url, self.parse)
#         self.i +=1
        
    # def parse_quote(self,response):
    #     x = response.xpath("//a[@class='ngram']/text()")
    #     item = response.meta['item']
    #     item["top_item"] = x[0].extract()
    #     return item
    #     