#!/usr/bin/env python3

import random
import string
import requests
import json
from itertools import groupby
from datetime import datetime

def icon_g(group):
    return{
    	"Nuevo en Pluto TV":    "https://helmerluzo.github.io/PlutoTV_HL/icons/ES/Nuevo_live.png",
        "Películas":            "https://helmerluzo.github.io/PlutoTV_HL/icons/ES/Peliculas.png",
        "Navidad":	        "https://helmerluzo.github.io/PlutoTV_HL/icons/ES/Navidad.png",        
        "Series":               "https://helmerluzo.github.io/PlutoTV_HL/icons/ES/Series.png",
        "Noticias":             "https://helmerluzo.github.io/PlutoTV_HL/icons/ES/Noticias.png",
        "MTV en Pluto TV":      "https://helmerluzo.github.io/PlutoTV_HL/icons/ES/MTV.png",
        "Entretenimiento":      "https://helmerluzo.github.io/PlutoTV_HL/icons/ES/Entretenimiento.png",
        "Comedia":              "https://helmerluzo.github.io/PlutoTV_HL/icons/ES/Comedia.png",
        "Crimen y misterio":    "https://helmerluzo.github.io/PlutoTV_HL/icons/ES/Crimen.png",
        "Estilo de Vida":       "https://helmerluzo.github.io/PlutoTV_HL/icons/ES/Estilo.png",
        "Música":		"https://helmerluzo.github.io/PlutoTV_HL/icons/ES/Musica.png",
        "Deportes":             "https://helmerluzo.github.io/PlutoTV_HL/icons/ES/Deportes.png",
        "Infantil":             "https://helmerluzo.github.io/PlutoTV_HL/icons/ES/Infantil.png",
	"LOL":			"https://helmerluzo.github.io/PlutoTV_HL/icons/ES/lol.png",	
        "Animación + Gaming":   "https://helmerluzo.github.io/PlutoTV_HL/icons/ES/AnimeBR.png",
        "Última oportunidad":	"https://helmerluzo.github.io/PlutoTV_HL/icons/ES/Ultima.png"
    }.get(group, "https://helmerluzo.github.io/PlutoTV_HL/icons/pluto.png")


novedades = {"name": "30/05/2021", "image": "https://helmerluzo.github.io/PlutoTV_HL/icons/news.gif", "stations": [\
                {"name": "Enlaces","image": "https://helmerluzo.github.io/PlutoTV_HL/icons/pluto.png",\
                     "url": "https://helmerluzo.github.io/PlutoTV_HL/enlaces.html", "embed": "True"}]}

acerca = {"name": "Acerca de","image": "https://cdn.pixabay.com/photo/2016/04/21/13/28/info-symbol-1343394_960_720.png","stations": [\
            {"name": "Importante", "image": "https://cdn.pixabay.com/photo/2012/04/12/22/25/warning-sign-30915__340.png",\
                "url": "https://helmerluzo.github.io/PlutoTV_HL/alert.html", "embed": "True"}, \
            {"name": "Disclaimer", "image": "https://cdn.pixabay.com/photo/2012/04/12/22/25/warning-sign-30915__340.png",\
                "url": "https://helmerluzo.github.io/PlutoTV_HL/disclaimer.html", "embed": "True"}]} 
  
clientId = "".join(random.choice(string.ascii_lowercase) for i in range(6))

temp = json.loads(open("channels_DK.json", "r").read())
temp = sorted(temp, key=lambda i: i['number'])
temp = groupby(temp, lambda temp: temp["category"])

sid = json.loads(requests.get('https://boot.pluto.tv/v4/start?appname=web&appversion=1&clientId=' + clientId + 'spencer&clientModelNumber=na').text)['session']["sessionID"]

m3u = "#EXTM3U url-tvg=\"https://i.mjh.nz/PlutoTV/dk.xml.gz\"\n"
groups = []
#groups.append(novedades)
#groups.append(acerca)
for category, group in temp:
    stations = []
    for content in group:
        stations.append({"name" : content["name"], "image" : content["colorLogoPNG"]["path"], \
            "url" : "https://stitcher.pluto.tv/stitch/hls/channel/" + content["_id"] + "/master.m3u8?deviceType=web&servertSideAds=false&deviceMake=safari&deviceVersion=1&deviceId=spencer&appVersion=1&deviceDNT=0&deviceModel=web&sid={}".format(sid), \
            "epgId" : content["_id"]})
        
        
        m3u = m3u + "#EXTINF:-1 tvg-id=\"" +  content["_id"] + "\" tvg-name=\"" + content["name"] + "\" tvg-logo=\"" + content["colorLogoPNG"]["path"] + "\" group-title=\"" + category + \
            "\" tvg-chno=\"" + str(content["number"]) + "\", " + content["name"] + "\n" + "https://stitcher.pluto.tv/stitch/hls/channel/" + content["_id"] + "/master.m3u8?deviceType=web&servertSideAds=false&deviceMake=safari&deviceVersion=1&deviceId=spencer&appVersion=1&deviceDNT=0&deviceModel=web&sid={}\n".format(sid)
         
    groups.append({"name" : category, "image" : icon_g(category), "stations" : stations})

fecha = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M")
tv = {"name": "PlutoTV - TV 🇩🇰", "author": "Actualizada " + fecha, "epg": "https://i.mjh.nz/PlutoTV/dk.xml.gz",\
        "image": "https://helmerluzo.github.io/PlutoTV_HL/icons/pluto.png","url": "https://w3ubin.com/GHi43tZ0I.w3u", "groups": groups} 

data = open("PlutoTV_TV_DK.json", "w")
data.write(json.dumps(tv, ensure_ascii=False))
data.close()

url = 'http://w3ubin.com/save'
params = {'content': json.dumps(tv, indent = 4), 'id': 'GHi43tZ0I', 'password' : '5a60e500-e1a4-46f0-8f02-bff691e6b2b0'}
resultado = requests.post(url, data = params)

data = open("PlutoTV_TV_DK.m3u", "w")
data.write(m3u)
data.close()
