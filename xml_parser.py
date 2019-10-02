#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 00:36:55 2019

@author: kevin
"""
import xml.etree.ElementTree as ET

def parseXML(xmlfile): 
  
    # create element tree object 
    tree = ET.parse(xmlfile) 
  
    # get root element 
    root = tree.getroot() 
    return root
#    # create empty list for news items 
#    items = [] 
#  
#    # iterate news items 
#    for item in root.findall('./channel/item'): 
#  
#        # empty news dictionary 
#        news = {} 
#  
#        # iterate child elements of item 
#        for child in item: 
#  
#            # special checking for namespace object content:media 
#            if child.tag == '{http://search.yahoo.com/mrss/}content': 
#                news['media'] = child.attrib['url'] 
#            else: 
#                news[child.tag] = child.text.encode('utf8') 
#  
#        # append news dictionary to news items list 
#        newsitems.append(news) 
#      
#    # return news items list 
#    return newsitems 

xmlfile = r'epc660_settings_default.xml'

root = parseXML(xmlfile)
for item in root.findall("."):
    for items in item:
        print(items.tag, items.find('.'))
