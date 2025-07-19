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
                            url = "https://serialgo.tv/movie"
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
   logger.info("=== INICIO DEL HTML ===")
   logger.info(data[:1000])  # Muestra solo los primeros 1000 caracteres para no saturar el log
   logger.info("=== FIN DEL HTML ===")
   # patron = r'https://serialgo.tv' + r'<a\s+[^>]*href="([^"]+)"'
   patron = r'<a\s+[^>]*href="([^"]+)"'
   patron_href = r'<div class="film-poster">[\s\S]*?<a href="(/movie/[^"]+)"[^>]*class="[^"]*film-poster-ahref[^"]*"'
   matches_href = scrapertools.find_multiple_matches(data, patron_href)
   logger.info(f"Encontrados {len(matches_href)} enlaces: {matches_href[:5]}")
   # patron += r'<img data-src="(https://[^"]+\.(jpg|png|webp))"'
   patron += r'<img[^>]+data-src="(https:\/\/[^"]+\.jpg)"'
   patron_img = r'<img[^>]+data-src="(https:\/\/[^"]+\.jpg)"'
   matches_img = scrapertools.find_multiple_matches(data, patron_img)
   logger.info(f"Encontradas {len(matches_img)} imágenes: {matches_img[:5]}")
   # patron += r'<a[^>]+title="([^"]+)"'
   patron += r'<h3 class="film-name">.*?<a[^>]*>([^<]+)</a>'
   patron_title = r'<h2 class="film-name">\s*<a[^>]+title="[^"]*"[^>]*>([^<]+)</a>'
   matches_title = scrapertools.find_multiple_matches(data, patron_title)
   logger.info(f"Encontrados {len(matches_title)} títulos: {matches_title[:5]}")
   matches = scrapertools.find_multiple_matches(data, patron)
   logger.info("Loooooool:")
   logger.info("Coincidencias encontradas: %d" % len(matches))

   for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
          itemlist.append(Item(action = "findvideos",
                               channel = item.channel,
                               title = scrapedtitle,
                               thumbnail = scrapedthumbnail,
                               url = "https://serialgo.tv" + scrapedurl
                               ))
   return itemlist
