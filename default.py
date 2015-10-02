# -*- coding: utf-8 -*-
import sys
import os
import urllib
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
from BeautifulSoup import BeautifulSoup

import requests

__addon__ = xbmcaddon.Addon(id='script.entremachacasybecarios')
__addonid__ = __addon__.getAddonInfo('id')
__fanart__ = __addon__.getAddonInfo('fanart')
__cwd__ = __addon__.getAddonInfo('path').decode("utf-8")
__profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile')).decode("utf-8")
__resource__ = xbmc.translatePath(os.path.join(__cwd__, 'resources').encode("utf-8")).decode("utf-8")
__lib__ = xbmc.translatePath(os.path.join(__resource__, 'lib').encode("utf-8")).decode("utf-8")


sys.path.append(__resource__)
sys.path.append(__lib__)

if __name__ == '__main__':
    # Get all the arguments
    base_url = sys.argv[0]
    print base_url
    print "Hello world"
    addon_handle = int(sys.argv[1])
    args = urlparse.parse_qs(sys.argv[2][1:])
    xbmcplugin.setContent(addon_handle, 'movies')
    def build_url(query):
        return base_url + '?' + urllib.urlencode(query)

    NumberPagination = 3
    mode = args.get('mode', None) 

    Url = 'http://www.machacas.com/'
    r = requests.get(Url)
    data = r.text
    soup = BeautifulSoup(data)
    DivPagination = soup.body.findAll("div",{"class": "pagination"})
    last = DivPagination[0].findAll('a')
    MaxPage = last[len(last)-1].attrs[0][1].split('/')[len(last[len(last)-1].attrs[0][1].split('/')) -1]
    def AddVideo(IdYoutube,EndDirectory):
                url = build_url({'mode': 'playYoutube', 'idYoutube': IdYoutube,'value':"123"})
                #url = 'plugin://plugin.image.mongolfridayphotos?foldername=mongol-friday-photos-vol-352&mode=slideshow&value=http://www.machacas.com/mongol-friday-photos-vol-352/'

                li = xbmcgui.ListItem("Video", iconImage='http://img.youtube.com/vi/'+IdYoutube+'/default.jpg')
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)
                if (EndDirectory):
                    print "EndDirectory"
                    xbmcplugin.endOfDirectory(addon_handle)

    def KindOfVideo(video):
        for attribs in video.attrs:
            if attribs[0].find('src') != -1:
                url = attribs[1]
                if url.find('youtube') != -1:
                    print "Youtube video!!"
                    idYoutube = url.split('/')[4].split('?')[0]
                    xbmc.executebuiltin( "XBMC.PlayMedia(plugin://plugin.video.youtube/play/?video_id="+idYoutube+")")
                if url.find('vimeo') != -1:
                    idVimeo = url.split('/')[4]
                    xbmc.executebuiltin( "XBMC.PlayMedia(plugin://plugin.video.vimeo/play/?video_id="+idVimeo+")")
                    print "Vimeo Video"

    def AddItems(Url,currentPage,EndDirectory):
        #print Url
        r = requests.get(Url)
        data = r.text
        soup = BeautifulSoup(data)

        for link in soup.body.findAll("div",{ "class" : "blog-item-wrap" }):
            href = link.find('a').attrs[0][1]
            VolName = href.split('/')[3]
            print VolName
            if VolName.find("mongol-friday") != -1:
                print "Play Script ..."
                url = build_url({'mode': 'playMongol', 'foldername': VolName,'value':href})
                #url = 'plugin://plugin.image.mongolfridayphotos?foldername=mongol-friday-photos-vol-352&mode=slideshow&value=http://www.machacas.com/mongol-friday-photos-vol-352/'
                li = xbmcgui.ListItem(VolName, iconImage='DefaultFolder.png')
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)
            else:
                url = build_url({'mode': 'folder', 'foldername': VolName,'value':href})
                li = xbmcgui.ListItem(VolName, iconImage='DefaultFolder.png')
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)

        if (EndDirectory):
            if (currentPage +1) <= MaxPage:
                currentPage = currentPage +1
                NextPage = 'http://www.machacas.com/page/' + str(currentPage)
                url1 = build_url({'mode': 'next', 'foldername': 'Next','value':NextPage})
                li1 = xbmcgui.ListItem('Next' , iconImage='DefaultFolder.png')
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url1,listitem=li1, isFolder=True)

            xbmcplugin.endOfDirectory(addon_handle)
    if mode is None:
        AddItems('http://www.machacas.com/',1,False)
        for Page in range(2,NumberPagination):
            if Page+1 == NumberPagination:
                AddItems('http://www.machacas.com/page/'+str(Page),Page,True)
            else:
                AddItems('http://www.machacas.com/page/'+str(Page),Page,False)
    elif mode[0] == 'next':
        print 'Enter on next'
        valors = args['value'][0]
        print valors
        currentPage = int(valors.split('/')[len(valors.split('/'))-1])
        for Page in range(currentPage,currentPage+NumberPagination):
            if (Page +1 == currentPage+NumberPagination):
                AddItems('http://www.machacas.com/page/'+str(Page),int(Page),True)
            else:
                AddItems('http://www.machacas.com/page/'+str(Page),int(Page),False)
    elif mode[0] == 'playMongol':
        print args
        foldername = args['foldername'][0]
        url = args['value'][0]
        xbmc.executebuiltin( "SlideShow(plugin://plugin.image.mongolfridayphotos/?foldername="+foldername+"&mode=slideshow&value="+url+",,notrandom)" )
    elif mode[0] == 'playYoutube':
        print args
        idYoutube = args['idYoutube'][0]
        xbmc.executebuiltin( "XBMC.PlayMedia(plugin://plugin.video.youtube/play/?video_id="+idYoutube+")")
        #XBMC.PlayMedia('plugin://plugin.video.youtube/play/?video_id='+idYoutube+')'
    elif mode[0] == 'playVimeo':
        print args
        idVimeo = args['idVimeo'][0]
        xbmc.executebuiltin( "XBMC.PlayMedia(plugin://plugin.video.vimeo/play/?video_id="+idVimeo+")")

    elif mode[0] == 'playMongol':
        picture = ""
        XBMC.ShowPicture(picture)

    elif mode[0] == 'folder':
        print args
        print "Analyze this post and find images or videos"
        url = args['value'][0]
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data)
        link = soup.body.find("article")
        paragrahp = link.find('p')
        QuantityVideos = len(paragrahp.findAll('iframe'))
        QuantityImages = len(paragrahp.findAll('img'))
        if QuantityVideos > 1:
            print QuantityVideos
            NumVideos = 1
            EndDirectory = False
            for video in paragrahp.findAll('iframe'):
                print video
                print NumVideos
                idYoutube = video.attrs[2][1]
                idYoutube = idYoutube.split('/')[4].split('?')[0]
                if NumVideos >= QuantityVideos:
                    EndDirectory = True
                else:
                    NumVideos = NumVideos + 1

                AddVideo(idYoutube,EndDirectory)
        else:
            video = paragrahp.find('iframe')
            KindOfVideo(video)
            #idYoutube = video.attrs[2][1]
            #idYoutube = idYoutube.split('/')[4].split('?')[0]
            #xbmc.executebuiltin( "XBMC.PlayMedia(plugin://plugin.video.youtube/play/?video_id="+idYoutube+")")


        #if QuantityImages > 1:
        #    print paragrahp.prettify()
        #    for image in paragrahp.findAll('img'):                
        #        print len(image.attrs)
        #        print paragrahp.find('src')
        #else:
        #    image = paragrahp.find('img')            
        #    print len(image.attrs)
        #    print paragrahp.find('src')

        #print QuantityVideos
        #print QuantityImages
        #for link in soup.body.findAll("article"):
        #    href = link.find('a').attrs[0][1]
        #    valor = link.find('a').attrs[1][1]
        #    if link.find('iframe'):
        #        idYoutube = link.find('iframe').attrs[2][1]
        #        idYoutube = idYoutube.split('/')[4].split('?')[0]
        #    print idYoutube
        #    print valor.encode('utf-8')

        #    VolName = link.find('a').attrs[1][1].encode('utf-8')
        #    url = build_url({'mode': 'folder', 'foldername': VolName,'value':href})
        #    commands = []
        #    commands.append(( 'runme', 'XBMC.RunPlugin(plugin://video/myplugin)', ))
        #    print "PlayId on youtube:"+idYoutube
        #    commands.append(( 'runyoutube_'+idYoutube, 'XBMC.PlayMedia(plugin://plugin.video.youtube/play/?video_id='+idYoutube+')', ))

        #    li = xbmcgui.ListItem(VolName, iconImage='http://img.youtube.com/vi/'+idYoutube+'/default.jpg')
        #    li.addContextMenuItems( commands ) 
        #    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)
            
        #xbmcplugin.endOfDirectory(addon_handle)

