# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader.processors import MapCompose, TakeFirst


class DiscursoItem(scrapy.Item):
    """
    Item responsavel por receber os discursos do site da
    Camara dos Deputados, via raspagem no HTML.
    """
    session = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    created_at = scrapy.Field(
        output_processor=TakeFirst()
    )
    inserted_at = scrapy.Field()

    phase = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    summary = scrapy.Field(
        output_processor=TakeFirst()
    )
    speech = scrapy.Field()


class OradorItem(scrapy.Item):
    """
    Item responsavel por receber dados do
    orador do webservice
    """
    default_input_processor = MapCompose(str.strip)

    numero = scrapy.Field()
    nome = scrapy.Field()
    partido = scrapy.Field()
    uf = scrapy.Field()


class SpeechItem(scrapy.Item):
    """
    Item responsavel por receber dados do
    discurso do webservice
    """

    default_input_processor = MapCompose(str.strip)

    orador = scrapy.Field()
    hora = scrapy.Field()
    quarto = scrapy.Field()
    insercao = scrapy.Field()
    sumario = scrapy.Field()


class SessionPhaseItem(scrapy.Item):
    """
    Item responsavel por receber dados da
    fase da sessão do webservice
    """

    code = scrapy.Field()
    description = scrapy.Field()
    speechs = scrapy.Field(serializer=list)


class SessionItem(scrapy.Item):
    """
    Item responsavel por receber dados da
    sessão do webservice
    """

    default_input_processor = MapCompose(str.strip)

    code = scrapy.Field()
    type = scrapy.Field()
    date = scrapy.Field()
    number = scrapy.Field()
    phases = scrapy.Field(serializer=list)
    inserted_at = scrapy.Field()
