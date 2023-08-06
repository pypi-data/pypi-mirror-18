#!/usr/bin/env python

# test url http://nptel.ac.in/courses/101104063/
import httplib
import urllib2, urllib
from bs4 import BeautifulSoup
import re
import os
import sys


def progress(i, size, tot):
    percent = i*size*100/tot
    bar = '[' + '#' * (percent/2) + '-'*(50-percent/2) + '] ' + str(percent) + '%  '
    sys.stdout.write("\r%s" % bar)
    sys.stdout.flush()

try:
    os.system('clear')
except:
    pass

print "This script will download all videos of the course you specify\n"
while True:
    url = raw_input("Enter the course url: ")
    url = "http://nptel.ac.in/courses" + re.search(r'/[0-9]{9}/', url).group(0)
    folder = raw_input("Enter the download folder: ") + '/'
    if not os.path.exists(folder):
        print "\nFolder not found!\n Creating Folder...\n"
        os.makedirs(folder)

    print "Loading Url ...\n\t(This might take a while)\n"
    try:
        page = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print e, "\nFailed Loading url...\n"
        continue
    except urllib2.URLError, e:
        print e, "\nFailed Loading url...\n"
        continue
    except httplib.HTTPException, e:
        print e, "\nFailed Loading url...\n"
        continue
    except Exception:
        print "Unknown Error!\nFailed Loading url...\n"
        continue

    soup = BeautifulSoup(page, "html.parser")
    soup = BeautifulSoup(str(soup.find("div", id="div_lm")), "html.parser")
    sources = soup.findAll('a', {"onclick": True})

    for src in sources:
        lec_url = src['onclick'][15:-1]
        lec_url = "http://nptel.ac.in"+lec_url
        try:
            lec_page = urllib2.urlopen(lec_url)
        except urllib2.HTTPError, e:
            print e, "\nFailed Loading url...\n"
            continue
        except urllib2.URLError, e:
            print e, "\nFailed Loading url...\n"
            continue
        except httplib.HTTPException, e:
            print e, "\nFailed Loading url...\n"
            continue
        except Exception:
            print "Unknown Error!\nFailed Loading url...\n"
            continue
        lec = BeautifulSoup(lec_page, "html.parser")
        lec = BeautifulSoup(str(lec.find("div", id="download")), "html.parser")
        try:
            mirror = lec.find('a', {"onclick": True})
            print "Mirror1: ", mirror['href']
            print "Downloading ..."
            testfile = urllib.URLopener()
            testfile.retrieve(mirror['href'], folder+mirror['href'][-9:], reporthook=progress)
            print "\nDownloaded Successful !\n"
        except (urllib2.HTTPError, httplib.HTTPException,  httplib.HTTPException) as e:
            try:
                print e, "\nMirror1 Download Failed!\nTrying Mirror2"
                mirror = lec.findAll('a', {"onclick": True})[1]
                print "Mirror2: ", mirror['href']
                print "Downloading ... \n"
                testfile = urllib.URLopener()
                testfile.retrieve(mirror['href'], folder + mirror['href'][-9:], reporthook=progress)
                print " Downloaded Successful !\n"
            except (urllib2.HTTPError, httplib.HTTPException, httplib.HTTPException) as e:
                print e, "\nFailed Downloading ", mirror['href'][-9:]

    print "Download Complete.\nStopping Script.\n"
    break

