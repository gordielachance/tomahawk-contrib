#!/usr/bin/env python2
import urllib
import oauth2 as oauth
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
import json
import shove
import sys
sys.path.append('../scrapers')
import settings
from items import ChartItem, SingleItem, slugify

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': settings.GLOBAL_SETTINGS['OUTPUT_DIR']+'/cache/data',
    'cache.lock_dir': settings.GLOBAL_SETTINGS['OUTPUT_DIR']+'/cache/lock'
}

methodcache = CacheManager(**parse_cache_config_options(cache_opts))
storage = shove.Shove('file://'+settings.GLOBAL_SETTINGS['OUTPUT_DIR']+'/sources')

@methodcache.cache('parse', expire=settings.GLOBAL_SETTINGS['EXPIRE'])
def parse():
  url = "http://api.rdio.com/1/"
  consumer = oauth.Consumer('gk8zmyzj5xztt8aj48csaart', 'yt35kakDyW')
  client = oauth.Client(consumer)
  music_data = []
    
  # We are gonna skip playlist here, cuz its crazy, and returns one playlist, like iTunes Top 200 U.S. 11-01-11 for instance. Baaad
  for c in ["Artist", "Album", "Track"]:
    #Additional key 'extras' = 'tracks', but in tomahawk chart, we actually want artist, albums and tracks seperated! 
    response, contents = client.request(url, 'POST', urllib.urlencode({'method': 'getTopCharts', 'type': c})) 
    content = contents.decode('utf-8')
    j = json.loads(content)
    id = "top"+c
    music_data.append( { "type":c, "charts": id } )
    
    source = "rdio"
    chart_id = source+id
    print("Saving %s - %s" %(source, chart_id))

    list = storage.get(source, {})
    
    chart_list = []
    chart_name = "Top Overall"
    chart_type = c.title() 

    chart = ChartItem()
    chart['name'] = chart_name
    chart['source'] = "rdio"
    chart['type'] = chart_type
    chart['id'] = slugify(chart_name)

    x = []
    i = 1
    for items in j['result']:
       t = {}
       rank = i
       i += 1
       if( c == "Artist"):
          t["artist"] = items.pop("name")
       else:
	  t['artist'] = items.pop("artist")
       if( c == "Track"):
          t["track"] = items.pop("name")
       if( c == "Album"):
          t["album"] = items.pop("name")
         
       t["rank"] = rank
       x.append(t)
             
    chart['list'] = x
    
    # metadata is the chart item minus the actual list plus a size
    metadata_keys = filter(lambda k: k != 'result', j.keys())
    metadata = { key: j[key] for key in metadata_keys }
    metadata['id'] = id
    metadata['name'] = "Top Overall"
    metadata['type'] = c
    metadata['source'] = "rdio"
    if( c == "Track"):
      metadata['default'] = 1
      
    metadata['size'] = len(j['result'])
    list[chart_id] = metadata
    storage[source] = list
    storage[chart_id] = dict(chart)

parse()