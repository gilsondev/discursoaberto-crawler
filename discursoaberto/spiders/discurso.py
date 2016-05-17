# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.http import FormRequest, Request

from discursoaberto.items import DiscursoItem


class DiscursoSpider(CrawlSpider):
    """
    Spider responsável por raspar discursos do site da Camara dos
    Deputados.
    """
    name = 'discurso'
    allowed_domains = ['camara.leg.br', 'camara.gov.br']
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@title="Próxima Página"]')),
        Rule(LinkExtractor(
            restrict_xpaths='//*[@id="content"]/div/table/tbody'
            '//tr/td[4]/a',
            process_value=lambda url: url.replace('\r\n', '')),
            callback='parse_item'),
    )

    def __init__(self, *args, **kwargs):
        self.data_inicial = kwargs.get('data_inicial', '01/01/2015')
        self.data_final = kwargs.get('data_final', '31/12/2015')
        super(DiscursoSpider, self).__init__(*args, **kwargs)

    def _parse_date(self, response):
        date = response.xpath(
            '//table[@align="center"]/tr[3]/td[2]/text()'
        ).re('\d{2}\/\d{2}\/\d{4}')[0]

        time = response.xpath(
            '//table[@align="center"]/tr[2]/td[2]/text()'
        ).re('(\d{2})\h(\d{2}|\d{1})')
        time = ':'.join(time)

        return "{0} {1}".format(date, time)

    # Start with search
    def start_requests(self):
        return [
            Request(
                "http://www2.camara.leg.br"
                "/deputados/discursos-e-notas-taquigraficas",
                callback=self.parse_search
            )
        ]

    def parse_search(self, response):
        return FormRequest.from_response(
            response,
            formname="PesqDiscursos",
            formdata={
                "dtInicio": self.data_inicial,
                "dtFim": self.data_final,
                "basePesq": "plenario",
                "CampoOrdenacao": "dtSessao",
                "PageSize": "50",
                "TipoOrdenacao": "DESC",
                "btnPesq": "Pesquisar"
            }
        )

    def parse_item(self, response):
        item = ItemLoader(item=DiscursoItem(), response=response)
        item.add_xpath('session',
                       '//table[@align="center"]/tr[2]/td[1]/text()',
                       re='\d{3}\.\d{1}\.\d{2}\.[A-Z]{1}')

        created_at = self._parse_date(response)
        item.add_value('created_at', created_at)
        item.add_xpath('phase', '//table[@align="center"]/tr[2]/td[3]/text()',
                       re='\s\w{2}')
        item.add_xpath('summary', '//*[@id="txSumarioID"]/text()')
        item.add_xpath('speech', '//p[@align="justify"]//font/text()')

        return item.load_item()
