#!/usr/bin/python
import requests
import re
from BeautifulSoup import BeautifulSoup
import sys

class TvParser():
  def parse(self, html):
    channels = []
    soup = BeautifulSoup(html)
    
    channelHtml = soup.findAll("div", {"class" : re.compile(r"tabla_container")})
    for ch in channelHtml:
      channel = Channel()
      channel.name = ch.div.p.a.text

      rows = ch.findAll("li")

      for sh in rows:
        show = Show()
        show.time = sh.contents[1].strip()
        rowType = self.getRowType(sh)
        show.showType = rowType["type"]
        show.timeType = rowType["timeType"]
        show.name = sh.contents[2].text
        channel.shows.append(show)
 
      channels.append(channel)
    return channels


  def getRowType(self,row):
    rowType = {}
    if row["class"][0] == "p":
      rowType["type"] = "program"
    elif row["class"][0] == "m":
      rowType["type"] = "movie"

    if row["class"][1] == "g":
      rowType["timeType"] = "past"
    elif row["class"][1] == "o":
      rowType["timeType"] = "present"
    else:
      rowType["timeType"] = "future"

    return rowType

class Show():
  pass

class Channel():
  def __init__(self):
    self.shows = []


def main():
  parser = TvParser()
  r = requests.get("http://www.tv.nu/")
  parsed = parser.parse(r.content)
  
  if len(sys.argv) > 1: 
    for channel in parsed:
      for show in channel.shows:
        if (show.timeType == "present" and "-c" in sys.argv) or (show.timeType == "past" and "-p" in sys.argv) or (show.timeType == "future" and "-f" in sys.argv):
          print channel.name,
          print show.time,
          print show.name.encode('ISO-8859-1')
  else:
    for channel in parsed:
      for show in channel.shows:
        print channel.name,
        print show.time,
        print show.name.encode('ISO-8859-1')



if __name__ == "__main__":
  main()
