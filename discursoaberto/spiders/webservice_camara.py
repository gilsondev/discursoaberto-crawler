# -*- coding: utf-8 -*-
import scrapy

from scrapy.http import FormRequest
from scrapy.loader import ItemLoader

from discursoaberto.items import (
    SessionItem, SessionPhaseItem, SpeechItem, OradorItem
)


class CamaraSpider(scrapy.Spider):
    name = "camara"
    allowed_domains = ["camara.gov.br", "www.camara.gov.br"]
    start_urls = ['http://www.camara.gov.br/SitCamaraWS\SessoesReunioes.asmx?wsdl']

    def parse(self, response):
        result = [FormRequest(
            url="http://www.camara.gov.br/SitCamaraWS/SessoesReunioes.asmx/ListarDiscursosPlenario",
            formdata={
                "dataIni": "03/05/2016",
                "dataFim": "03/05/2016",
                "codigoSessao": "",
                "parteNomeParlamentar": "",
                "siglaPartido": "",
                "siglaUF": "",
            },
            callback=self.parse_discurso
        )]
        return result

    def parse_discurso(self, response):
        session = ItemLoader(item=SessionItem(), response=response)
        phases = []
        speech_requests = []

        # Session
        session.add_xpath('code', '//sessao/codigo/text()')
        session.add_xpath('date', '//sessao/data/text()')
        session.add_xpath('number', '//sessao/number/text()')
        session.add_xpath('type', '//sessao/tipo/text()')

        # Session phase
        for phase_session in response.xpath('//sessao/fasesSessao//faseSessao'):
            phase = SessionPhaseItem()
            phase['code'] = phase_session.xpath('./codigo/text()').extract_first()
            phase['description'] = phase_session.xpath('./descricao/text()').extract_first()

            for speech_item in phase_session.xpath('./discursos//discurso'):
                speech = SpeechItem()
                orador = OradorItem()

                orador['numero'] = speech_item.xpath('./orador/numero/text()').extract_first()
                orador['nome'] = speech_item.xpath('./orador/nome/text()').extract_first()
                orador['partido'] = speech_item.xpath('./orador/partido/text()').extract_first()
                orador['uf'] = speech_item.xpath('./orador/uf/text()').extract_first()

                speech['orador'] = orador
                speech['hora'] = speech_item.xpath('./horaInicioDiscurso/text()').extract_first()
                speech['quarto'] = speech_item.xpath('./numeroQuarto/text()').extract_first()
                speech['insercao'] = speech_item.xpath('./numeroInsercao/text()').extract_first()
                speech['sumario'] = speech_item.xpath('./sumario/text()').extract_first()

                request = FormRequest(
                    url="http://www.camara.gov.br/SitCamaraWS/SessoesReunioes.asmx/obterInteiroTeorDiscursosPlenario",
                    formdata={
                        "codSessao": response.xpath('//sessao/codigo/text()').extract_first().strip(),
                        "numOrador": orador['numero'],
                        "numQuarto": speech['quarto'],
                        "numInsercao": speech['insercao']
                    },
                    callback=self.parse_teor
                )
                request.meta['speech'] = speech
                request.meta['phase'] = phase
                request.meta['session'] = session
                speech_requests.append(request)

        return speech_requests

    def parse_teor(self, response):
        speech = response.meta['speech']
        phase = response.meta['phase']
        session = response.meta['session']

        import ipdb; ipdb.set_trace()
