# -*- encoding: utf-8 -*-

"""ERT EPG parser, add mapping to CHANELS"""

from __future__ import print_function
import datetime
from xml.sax.saxutils import escape
from bs4 import BeautifulSoup
import requests


def _channel(channel, name):
    """Channel Id and Name"""
    print('  <channel id="{}">'.format(channel))
    print('    <display-name lang="el">{}</display-name>'.format(escape(name)))
    print('  </channel>')


def _programme(start, channel, title, desc):
    """Channel Programm using only start, end should be calculated"""
    print('  <programme start="{} +0200" channel="{}">'.format(start, channel))
    print('    <title lang="el">{}</title>'.format(escape(title)))
    print('    <desc>{}</desc>'.format(escape(desc)))
    print('  </programme>')


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.program.ert.gr',
    'Connection': 'keep-alive',
    'Referer': 'https://program.ert.gr/search.asp',
}

CHANNELS = {
    '8': ('ert.vouli.gr', 'VOULI'),
    '9': ('ert.ert1.gr', 'ERT1'),
    '10': ('ert.ert3.gr', 'ERT3'),
    '11': ('ert.ertworld.gr', 'ERT WORLD'),
    '24': ('ert.ertsports.gr', 'ERT SPORTS'),
    '49': ('ert.ert2.gr', 'ERT2'),
}

EPG_URL = 'https://program.ert.gr/search.asp'

def get_data(day):
    """get data for a single day"""
    data = {
        'frmDates': day.strftime('%-j'),
        'frmChannels': '',
        'frmSearch': '',
        'x': '14',
        'y': '6'
    }
    res = requests.post(EPG_URL, headers=HEADERS, data=data)
    res.encoding = 'windows-1253'
    return res.text

def parse_html(html, day):
    """parse the html returned from get data"""
    soup = BeautifulSoup(html, 'lxml')
    channels = []
    _last_time = -1
    prevday = day
    nextday = day + datetime.timedelta(1)
    for ahr in soup.find_all('a', attrs={'class':'black'}):
        cid = ahr['href'].rsplit('=', 1)[-1]
        nci = CHANNELS.get(cid, None)
        if not nci:
            continue
        if nci not in channels:
            channels.append(nci)
            _channel(nci[0], nci[1])
            _last_time = -1
            day = prevday
        atr = ahr.find_parent('tr', attrs={'bgcolor': True})
        _time = atr.td.text.strip().replace(':', '')
        _title = " ".join(atr.table.tr.text.split())
        _desc = atr.font and atr.font.text.strip() or _title
        if _last_time > int(_time):
            day = nextday
        _last_time = int(_time)
        _start = '%s%s00' % (day.strftime('%Y%m%d'), _time)
        _programme(_start, nci[0], _title, _desc)

for d in (datetime.date.today() + datetime.timedelta(n) for n in range(11)):
    h = get_data(d)
    parse_html(h, d)
