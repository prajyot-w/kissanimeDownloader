#!/usr/bin/env python
import gtk, webkit, time
from bs4 import BeautifulSoup

# defining function
def spit(view, frame):
    title = web.get_title()
    web.execute_script("oldtitle = document.title; document.title = document.documentElement.innerHTML;")
    data = web.get_title()
    web.execute_script("document.title = oldtitle;")
    soup = BeautifulSoup(data, 'lxml')
    vid = soup.findAll("video")
    if len(vid) > 0:
        print("Inside Condition:")
        web.stop_loading()
        #web.stop_emission()
        link = soup.findAll('img',{'id':'btnNext'})[0].parent['href']
        print("Next Buttons : "+ str(len(link)))
        vidlnk = vid[0]['src']
        #nxtlnk = link[14]['href']
        fp=open('sample.html','w')
        fp.write(str(title)+"\n")
        fp.write(str(vidlnk)+"\n")
        fp.write(str(link)+"\n")
        fp.close()
        gtk.main_quit()



# defineing all variables ....
win = gtk.Window()
win.connect('destroy', lambda w:gtk.main_quit())
box1 = gtk.VBox()
scrol = gtk.ScrolledWindow()
web = webkit.WebView()
web.connect('load-finished',spit)
# adding all elements together
scrol.add(web)
box1.pack_start(scrol)
win.add(box1)

# Opening a page
#web.open('https://kissanime.to/Anime/Naruto-Dub/Episode-213-Vanished-Memories?id=104080')
web.open('http://kissanime.to/Anime/Rock-Lee-no-Seishun-Full-Power-Ninden-Dub/Episode-001?id=82858')
# showing it all
win.show_all()
gtk.main()
