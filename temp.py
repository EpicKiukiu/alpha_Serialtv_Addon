# -*- coding: utf-8 -*-
from core import httptools
from core import scrapertools
from core import servertools
from core.item import Item
from platformcode import logger

def mainlist(item):
   logger.info()
   itemlist = []
   itemlist.append(Item(channel = item.channel,
                          title = "Novedades",
                         action = "peliculas",
                            url = "https://serialgo.tv/home"
                     ))
   #itemlist.append(Item(channel = item.channel,
    #                      title = "Series",
     #                    action = "series",
      #                      url = "https://serialgo.tv/tv-show"
       #               ))
   return itemlist


def peliculas(item):
   logger.info()
   itemlist = []
   data = httptools.downloadpage(item.url).data
   patron = r'https://serialgo.tv' + r'<a\s+[^>]*href="([^"]+)"'
   patron += r'<img data-src="(https://[^"]+\.(jpg|png|webp))"'
   patron += r'<a[^>]+title="([^"]+)"'
   matches = scrapertools.find_multiple_matches(data, patron)
   for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
          itemlist.append(Item(action = "findvideos",
                               channel = item.channel,
                               title = scrapedtitle,
                               thumbnail = scrapedthumbnail,
                               url = scrapedurl
                               ))
   return itemlist
