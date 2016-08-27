#!/usr/bin/env python
import webkit, re, os, gtk, urllib, sys
from bs4 import BeautifulSoup

downList = []

class Logger:
    # file that keeps record of all the files downloaded or
    # to be downloaded

    def __init__(self):
        self.logFile = os.path.abspath(os.path.curdir)+"/download.log"
        print("Data logger file is located at : "+ self.logFile)

    def check(self):
        if os.path.exists(self.logFile) and os.path.isfile(self.logFile):
            return True
        else:
            return False

    def logRead(self):
        global downList
        # function that reads download.log
        # and stores it in downList global variables
        if os.path.exists(self.logFile) and os.path.isfile(self.logFile):
            # open file and read it
            try:
                fp=open(self.logFile,"r")
                records = fp.read().strip().split("\n")
                for record in records:
                    field = record.split(" ")
                    downList.append({'title':field[0],'url':field[1],'status':field[2]})
            except (KeyboardInterrupt, SystemExit, Exception):
                print("Something went wrong while opening log file in read mode.")
                exit()
            # now make script download files here ...
        else:
            # print error message and exit
            print("Log file does not exist. Please provide proper url and offset.")
        return

    def logWrite(self):
        global downList
        # function that writes contents in
        # global downList variables into download.log
        try:
            fp = open(self.logFile,"w")
            for i in downList:
                line = i['title'] + " " + i['url']  + " " + i['status'] + " " + "\n";
                fp.write(line)

            fp.close()
            del(fp)
            del(line)
        except (KeyboardInterrupt, SystemExit, Exception):
            print("Error occured while opening log file in write mode.")
            #fp.close()
            #del(fp)
            #del(line)
            exit()


class Extractor:
    def __init__(self,url,offset):
        self.url = url
        self.offset = int(offset)

    def recordExist(self,title):
        global downList
        if len(downList) == 0:
            return False
        for i in downList:
            if i['title'] == title:
                return True
            else:
                continue
        return False

    def addRecord(self, title, lnk):
        global downList
        downList.append({'title':title, 'url':lnk, 'status':'pending'})
        print("Record Added ...")

    def start(self):
        # create UI
        web = webkit.WebView()
        scroller = gtk.ScrolledWindow()
        win = gtk.Window()
        # bind UI
        scroller.add(web)
        win.add(scroller)
        # Link webkit to load-finished
        web.connect('load-finished',self.extract)
        # Link window to destroy
        win.connect('destroy', lambda w: gtk.main_quit())
        # Activate windows ...
        try:
            web.open(self.url)
        except:
            print("Error opening the link. Please check your network connection.")
        win.show_all()
        gtk.main()

    def extract(self, view, frame):
        # extract title
        title = view.get_title()
        try:
            title = re.sub(" ","_",title.strip())
        except:
            print("Exception: value of title is : "+str(title))
        print(title)
        #extract body
        view.execute_script("oldtitle=document.title;document.title = document.documentElement.innerHTML;")
        htmlData = view.get_title()
        view.execute_script("document.title = oldtitle;")
        # apply beautifulsoup to htmlData
        soup = BeautifulSoup(htmlData,'lxml')
        vidlnk = soup.findAll('video')
        if len(vidlnk) > 0:
            print("Video Link Found.")
            # check offset
            if self.offset > 0:
                print("OFFSET not Zero")
                # check if record exists
                if not self.recordExist(title):
                    print("Record Does not exist")
                    self.addRecord(title, vidlnk[0]['src'])
                    self.offset -= 1
                try:
                    anclnk = soup.findAll('img',{'id':'btnNext'})[0].parent
                    view.open(anclnk['href'])
                except IndexError:
                    print("Reached End of available videos")
                    gtk.main_quit()
                    return None
            else:
                # Extraction completed
                gtk.main_quit()
                print("Extraction Completed ... ")


def helpFunc():
    print """
    USAGE: kissanime [OPTIONS] URL OFFSET

    OPTIONS:
    ----------

    -h : prints this help page.
    -v : prints the version number.
    -c : continue last download in current folder

    ARGUMENTS:
    ----------

    URL    : accepts the url from which download needs to begin.
    OFFSET : accepts an integer number that tells how many
             episodes are required to be downloaded.
    """

# Added for version 1.1
def dlProgress(count, blockSize, totalSize):
    # Shows the progress of the Download.
    # Use it with reporthook handler for urlretrieve.
    try:
        percentage = int(count*blockSize*100/totalSize)
        sys.stdout.write("\rDownloaded %d%%" % percentage)
        sys.stdout.flush()
    except:
        print("dlProgress Exception")

def downloadFiles():
    global downList
    l = Logger()
    count = 0
    try:
        for i in downList:
            if i['status'] != 'done':
                url = i['url']
                filename = i['title']+'.mp4'
                print("Downloading : "+filename)
                download = urllib.urlretrieve(url, filename, dlProgress)
                i['status'] = 'done'
                count += 1
            if count >= 5:  # Added for version 1.1
                l.logWrite()
                count = 0
    except (KeyboardInterrupt, SystemExit, Exception):
        print("Something went wrong while downloading files.")
        l.logWrite()
        exit()
    finally:
        print("\nFinished Downloading Files.\n")

if __name__ == '__main__':
    l = Logger()
    if len(sys.argv) > 1:
        if sys.argv[1] == '-h':
            # print help
            helpFunc()
        elif sys.argv[1] == '-v':
            print("kissanime downloader version 1.1")
        elif sys.argv[1] == '-c':
            print("Prepareing to continue previous operation.")
            # code to continue previous operations
            # read data from download.log
            # resume download process
            l.logRead()
            downloadFiles()

        elif len(sys.argv) == 3:
            if bool(re.compile("http://kissanime.to/Anime/").match(sys.argv[1])) and int(sys.argv[2]):
                print(sys.argv[1]+ " " + sys.argv[2])
                # All arguments received successfully here
                # start operating on it here ....
                e = Extractor(sys.argv[1],sys.argv[2])
                print("Extracting Data.")
                e.start()
                del(e)
                l.logWrite()
                downloadFiles()
            else:
                print("Invalid URL")
                helpFunc()
        elif bool(re.compile("http://kissanime.to/Anime/").match(sys.argv[1])) and len(sys.argv) == 2:
            print("Please provide an appropriate offset.")
            helpFunc()
        else:
            # proceed with another operations
            print("Invalid Option or Argument : " + sys.argv[1])
            helpFunc()
    else:
        if l.check():
            l.logRead()
            downloadFiles()
        else:
            helpFunc()
    del(l)
    print("Proceeding to exit.")
