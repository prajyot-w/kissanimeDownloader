#!/usr/bin/env python
import gtk, webkit

def go_btn(widget):
    add = addressbar.get_text()
    if add.startswith('http://'):
        pass
    else:
        add = 'http://' + add
        addressbar.set_text(add)
    web.open(add)

win = gtk.Window()
win.connect('destroy', lambda w: gtk.main_quit())

box1 = gtk.VBox()   # Vertical container inside Window
win.add(box1)

box2 = gtk.HBox()   # Horizontal container inside Vertical container
box1.pack_start(box2, False)

addressbar = gtk.Entry()    # text box in H container
box2.pack_start(addressbar)
gobtn = gtk.Button("Go")    # button in H container
box2.pack_start(gobtn, False)
gobtn.connect('clicked', go_btn)

scroller = gtk.ScrolledWindow() # Scroller in V container
box1.pack_start(scroller)

web = webkit.WebView() # Area where web pages loads
scroller.add(web)   # Added to Scroller container

win.show_all()
gtk.main()
