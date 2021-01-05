#!/usr/bin/python3
# -*- encoding: utf-8 -*-

"""CYTA EPG parser, add mapping to CHANELS"""

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
    'Origin': '',
    'Connection': 'keep-alive',
    'Referer': 'https://www.cyta.com.cy/tv-guide',
}

CHANNELS = {
    'ch27': ('cyta.rik1.cy', 'RIK1'),
    'ch28': ('cyta.rik2.cy', 'RIK2'),
    'ch29': ('cyta.megaone.cy', 'MEGAONE'),
    'ch26': ('cyta.ant1.cy', 'ANT1'),
    'ch30': ('cyta.sigma.cy', 'SIGMA'),
    'ch151': ('cyta.alfagr.cy', 'ALFAGR'),
    'ch39': ('cyta.cncp.cy', 'CNCP'),
    'ch54': ('cyta.capitaltv.cy', 'CAPITAL TV'),
    'ch32': ('cyta.extra.cy', 'EXTRA'),
    'ch83': ('cyta.ertw.cy', 'ERTW'),
    'ch84': ('cyta.ve.cy', 'VE'),
    'ch82': ('cyta.4e.cy', '4E'),
    'ch152': ('cyta.tvmall.cy', 'TVMALL'),
    'ch178': ('cyta.action24.cy', 'ACTION24'),
    'ch22': ('cyta.babytv.cy', 'BABYTV'),
    'ch33': ('cyta.boomerang.cy', 'BOOMERANG'),
    'ch300': ('cyta.cartoonnetwork.cy', 'CARTOON NETWORK'),
    'ch80': ('cyta.dsnch.cy', 'DSNCH'),
    'ch124': ('cyta.dsnxd.cy', 'DSNXD'),
    'ch125': ('cyta.dsnjr.cy', 'DSNJR'),
    'ch139': ('cyta.nckd.cy', 'NCKD'),
    'ch166': ('cyta.smile.cy', 'SMILE'),
    'ch90': ('cyta.novacinema1.cy', 'NOVACINEMA1'),
    'ch91': ('cyta.novacinema2.cy', 'NOVACINEMA2'),
    'ch92': ('cyta.novacinema3.cy', 'NOVACINEMA3'),
    'ch93': ('cyta.novacinema4.cy', 'NOVACINEMA4'),
    'ch176': ('cyta.nvlife.cy', 'NVLIFE'),
    'ch145': ('cyta.nvch.cy', 'NVCH'),
    'ch121': ('cyta.foxlf.cy', 'FOXLF'),
    'ch69': ('cyta.fox.cy', 'FOX'),
    'ch182': ('cyta.otevil.cy', 'OTEVIL'),
    'ch173': ('cyta.mvbesthd.cy', 'MVBESTHD'),
    'ch19': ('cyta.tcm.cy', 'TCM'),
    'ch133': ('cyta.grcine.cy', 'GRCINE'),
    'ch12': ('cyta.discovery.cy', 'DISCOVERY'),
    'ch15': ('cyta.discoveryscience.cy', 'DISCOVERY SCIENCE'),
    'ch102': ('cyta.anipl.cy', 'ANIPL'),
    'ch5': ('cyta.ng.cy', 'NG'),
    'ch61': ('cyta.natgeowild.cy', 'NATGEOWILD'),
    'ch184': ('cyta.bbceth.cy', 'BBCETH'),
    'ch188': ('cyta.cosmhis.cy', 'COSMHIS'),
    'ch156': ('cyta.viasat.cy', 'VIASAT'),
    'ch119': ('cyta.hstr.cy', 'HSTR'),
    'ch101': ('cyta.idisc.cy', 'IDISC'),
    'ch8': ('cyta.reality.cy', 'REALITY'),
    'ch100': ('cyta.tlc.cy', 'TLC'),
    'ch150': ('cyta.travel.cy', 'TRAVEL'),
    'ch73': ('cyta.foodnet.cy', 'FOODNET'),
    'ch20': ('cyta.Eentert.cy', 'EENTERT'),
    'ch167': ('cyta.fshtv.cy', 'FSHTV'),
    'ch141': ('cyta.chapec.cy', 'CHAPEC'),
    'ch138': ('cyta.vh1cl.cy', 'VH1CL'),
    'ch313': ('cyta.mtvlive.cy', 'MTVLIVE'),
    'ch88': ('cyta.madcy.cy', 'MADCY'),
    'ch62': ('cyta.madviral.cy', 'MADVIRAL'),
    'ch112': ('cyta.madgrkz.cy', 'MADGRKZ'),
    'ch312': ('cyta.mezzo.cy', 'MEZZO'),
    'ch17': ('cyta.cnnv2.cy', 'CNN V2'),
    'ch1': ('cyta.bbc.cy', 'BBC'),
    'ch123': ('cyta.skynews.cy', 'SKYNEWS'),
    'ch171': ('cyta.euronews.cy', 'EURONEWS'),
    'ch40': ('cyta.euronews.cy', 'EURONEWS'),
    'ch57': ('cyta.aljazeera.cy', 'ALJAZEERA'),
    'ch16': ('cyta.bloomberg.cy', 'BLOOMBERG'),
    'ch52': ('cyta.france24.cy', 'FRANCE24'),
    'ch56': ('cyta.tv5monde.cy', 'TV5MONDE'),
    'ch147': ('cyta.dewe.cy', 'DEWE'),
    'ch170': ('cyta.rusone.cy', 'RUSONE'),
    'ch49': ('cyta.vesti.cy', 'VESTI'),
    'ch50': ('cyta.planeta.cy', 'PLANETA'),
    'ch172': ('cyta.euronews.cy', 'EURONEWS'),
    'ch44': ('cyta.cvsp1hd.cy', 'CVSP1HD'),
    'ch38': ('cyta.cvsp2hd.cy', 'CVSP2HD'),
    'ch36': ('cyta.cvsp3hd.cy', 'CVSP3HD'),
    'ch66': ('cyta.cvsp4hd.cy', 'CVSP4HD'),
    'ch67': ('cyta.cvsp5hd.cy', 'CVSP5HD'),
    'ch34': ('cyta.cvsp6hd.cy', 'CVSP6HD'),
    'ch324': ('cyta.cvsp7hd.cy', 'CVSP7HD'),
    'ch327': ('cyta.cablenet1.cy', 'CABLENET1'),
    'ch328': ('cyta.cablenet2.cy', 'CABLENET2'),
    'ch333': ('cyta.primetel1new.cy', 'PRIMETEL1 NEW'),
    'ch334': ('cyta.primetel2new.cy', 'PRIMETEL2 NEW'),
    'ch335': ('cyta.primetel3new.cy', 'PRIMETEL3 NEW'),
    'ch94': ('cyta.novasports1.cy', 'NOVASPORTS1'),
    'ch95': ('cyta.novasports2.cy', 'NOVASPORTS2'),
    'ch96': ('cyta.novasports3.cy', 'NOVASPORTS3'),
    'ch97': ('cyta.novasports4.cy', 'NOVASPORTS4'),
    'ch99': ('cyta.nvsprt5.cy', 'NVSPRT5'),
    'ch2': ('cyta.ese1.2015.cy', 'ESE1.2015'),
    'ch23': ('cyta.ese2.2015.cy', 'ESE2.2015'),
    'ch135': ('cyta.nbatv.cy', 'NBATV'),
    'ch148': ('cyta.motovs.cy', 'MOTOVS'),
    'ch185': ('cyta.cvsp1hd.cy', 'CVSP1HD'),
    'ch111': ('cyta.rikhd.cy', 'RIKHD'),
    'ch316': ('cyta.boomerang.cy', 'BOOMERANG'),
    'ch162': ('cyta.nvc1hd.cy', 'NVC1HD'),
    'ch163': ('cyta.nvc2hd.cy', 'NVC2HD'),
    'ch301': ('cyta.novacinema3hd.cy', 'NOVACINEMA3HD'),
    'ch302': ('cyta.novacinema4hd.cy', 'NOVACINEMA4HD'),
    'ch310': ('cyta.nvlife.cy', 'NVLIFE'),
    'ch179': ('cyta.nvch.cy', 'NVCH'),
    'ch160': ('cyta.foxlf.cy', 'FOXLF'),
    'ch161': ('cyta.fox.cy', 'FOX'),
    'ch183': ('cyta.otevil.cy', 'OTEVIL'),
    'ch174': ('cyta.mvbesthd.cy', 'MVBESTHD'),
    'ch303': ('cyta.tcmhd.cy', 'TCMHD'),
    'ch108': ('cyta.nghd.cy', 'NGHD'),
    'ch107': ('cyta.ngwlhd.cy', 'NGWLHD'),
    'ch186': ('cyta.bbcethhd.cy', 'BBCETHHD'),
    'ch189': ('cyta.cosmhis.cy', 'COSMHIS'),
    'ch120': ('cyta.hstrhd.cy', 'HSTRHD'),
    'ch169': ('cyta.travelhd.cy', 'TRAVELHD'),
    'ch315': ('cyta.foodnethd.cy', 'FOODNETHD'),
    'ch304': ('cyta.Eenterthd.cy', 'EENTERTHD'),
    'ch198': ('cyta.ftvuhd.cy', 'FTVUHD'),
    'ch106': ('cyta.cvsp1hd.cy', 'CVSP1HD'),
    'ch192': ('cyta.cvsp2hd.cy', 'CVSP2HD'),
    'ch193': ('cyta.cvsp3hd.cy', 'CVSP3HD'),
    'ch194': ('cyta.cvsp4hd.cy', 'CVSP4HD'),
    'ch195': ('cyta.cvsp5hd.cy', 'CVSP5HD'),
    'ch196': ('cyta.cvsp6hd.cy', 'CVSP6HD'),
    'ch325': ('cyta.cvsp7hd.cy', 'CVSP7HD'),
    'ch331': ('cyta.cablenet1.cy', 'CABLENET1'),
    'ch332': ('cyta.cablenet2.cy', 'CABLENET2'),
    'ch326': ('cyta.primetel1new.cy', 'PRIMETEL1 NEW'),
    'ch329': ('cyta.primetel2new.cy', 'PRIMETEL2 NEW'),
    'ch330': ('cyta.primetel3new.cy', 'PRIMETEL3 NEW'),
    'ch164': ('cyta.nvs1hd.cy', 'NVS1HD'),
    'ch165': ('cyta.nvs2hd.cy', 'NVS2HD'),
    'ch307': ('cyta.novasports3hd.cy', 'NOVASPORTS3HD'),
    'ch308': ('cyta.novasports4hd.cy', 'NOVASPORTS4HD'),
    'ch309': ('cyta.novasports5hd.cy', 'NOVASPORTS5HD'),
    'ch190': ('cyta.ese1.2015.cy', 'ESE1.2015'),
    'ch191': ('cyta.ese2.2015.cy', 'ESE2.2015'),
    'ch318': ('cyta.ppv1.cy', 'PPV1'),
    'ch319': ('cyta.ppv2.cy', 'PPV2'),
    'ch320': ('cyta.ppv3.cy', 'PPV3'),
    'ch87': ('cyta.hstb.cy', 'HSTB'),
    'ch154': ('cyta.sirina.cy', 'SIRINA'),
    'ch153': ('cyta.hstlhd.cy', 'HSTLHD'),
    'ch155': ('cyta.redlt.cy', 'REDLT'),
    'ch86': ('cyta.drng.cy', 'DRNG'),
}

EPG_URL = 'https://data.cytavision.com.cy/epg/index.php'

def get_data(day):
    """get data for a single day"""
    params = {
        'site': 'cyprus',
        'day': day,
        'lang': 'el',
        'package': 'all',
        'category': 'all',
    }
    res = requests.get(EPG_URL, headers=HEADERS, params=params)
    res.encoding = 'utf-8'
    return res.text

def parse_html(html, day):
    """parse the html returned from get data"""
    soup = BeautifulSoup(html, 'lxml')
    ahr = soup.find_all('a', attrs={'class':'channel_link'})
    div = soup.find_all('div', attrs={'class':'epgrow clearfix'})
    for idx, val in enumerate(ahr):
        cid = val['data-reveal-id']
        nci = CHANNELS.get(cid, None)
        if not nci:
            continue
        _channel(nci[0], nci[1])
        for epgrow in div[idx].find_all("div", attrs={'class': 'data'}):
            _time, _title = epgrow.h4.text.split(" ", 1)
            _desc = epgrow.h4.next_sibling.strip()
            _start = '%s%s00' % (day.strftime('%Y%m%d'), _time.replace(':', '').zfill(4)[:4])
            _programme(_start, nci[0], _title, _desc)

for d, n in ((datetime.date.today() + datetime.timedelta(n), n) for n in range(8)):
    h = get_data(n)
    parse_html(h, d)
