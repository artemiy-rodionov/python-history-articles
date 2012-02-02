# -*- coding: utf-8 -*-

import urllib2
import sys
from lxml import etree
from pdf_gen import *
from datetime import date

content = ''
headpage = 'http://python-history.blogspot.com/'

try:
    headhtml = urllib2.urlopen(headpage).read()
except:
    print "Could not load head page:" + headpage
    sys.exit(1)


content += '<br /><h2 align="center"><a href="%s">' % (headpage,)
content += 'The History of Python blog articles</a></h2><br />'
content += '<div><pdf:toc /></div>'
content += '<div><pdf:nextpage /></div>'

headet = etree.HTML(headhtml)
postlinks = headet.xpath("//ul[@class='posts']/li/a/@href")
postlinks.reverse()

for postlink in postlinks:
    try:
        posthtml = urllib2.urlopen(postlink).read()
    except:
        print "Can`t get page %s" % (postlink,)
        continue
    postet = etree.HTML(posthtml)

    titleraw = postet.xpath("//h3[@class='post-title entry-title']/text()")
    bodyraw = postet.xpath("//div[@class='post-body entry-content']")
    authorraw = postet.xpath("//a[@rel='author']/text()")
    dateraw = postet.xpath("//h2[@class='date-header']/*/text()")
    try:
        title = titleraw[0]
    except IndexError:
        print "No title for %s" % postlink
    try:
        body = etree.tostring(bodyraw[0])
    except:
        print "No body for %s" % postlink
        continue
    try:
        author = authorraw[0]
    except IndexError:
        print "No author for %s" % postlink
    try:
        date = dateraw[0]
    except IndexError:
        print "No date for %s" % postlink

    topic = ''

    topic += '<h3><a href="%s">%s</a></h3> by %s<br /> %s <br />' % (postlink, title, author, date)
    topic += body
    topic += '<div><pdf:nextpage /></div>'
    content += '<div>' + topic + '</div>'


go(content, 'pyton-history.pdf')
