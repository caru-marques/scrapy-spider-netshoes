import scrapy
from bs4 import BeautifulSoup

class TesteSpider(scrapy.Spider):
    name = 'teste'
    # allowed_domains = ['teste.com.br']
    start_urls = ['https://www.netshoes.com.br/lst/tenis-calcado-infantil?genero=menino&genero=menina&genero=bebe-menino&genero=bebe-menina&mi=hm_ger_mntop_CR-CAL-tenis&psn=Menu_Top']

    def parse(self, response):
        lista_produtos = response.css('.wrapper > a')
        
        for produto in lista_produtos:
            # soup = BeautifulSoup(produto.css("div.item-card__description").get(), 'html')
            # nome_produto = produto.css('.item-card__description__product-name').css("span::text").get()    
            # codigo_sku   = produto.css('a::attr(parent-sku)').get()
            detail_page = produto.css('a::attr(href)').get()
            yield scrapy.Request('http:'+detail_page, callback=self.parseDetails)
            # yield {
            #     "produto": nome_produto,
            #     "sku": codigo_sku,
            #     "detail_url": detail_page
            # }
        
        yield scrapy.Request('http:'+response.css('a.next::attr(href)').get(), callback=self.parse)

    def parseDetails(self, response):
        valor_preco = response.xpath('//div[@class="default-price"]/span/strong/text()').get()
        nome_produto = response.xpath("//h1[contains(@data-productname, '')]/text()").get()
        codigo_sku = response.xpath("//span[@qa-automation='product-sku']/text()").get()
        yield {
            "produto": nome_produto,
            "sku": codigo_sku,
            "preco": valor_preco
        }