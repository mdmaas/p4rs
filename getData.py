from datetime import datetime, date, timedelta
from lxml import etree
from io import StringIO
import requests
import time
import os
import pathlib

baseurls = ['https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGM.06/',
            'https://e4ftl01.cr.usgs.gov/MOLA/MYD13C1.006/', 
            'https://e4ftl01.cr.usgs.gov/MOLT/MOD13C1.006/',
            'https://n5eil01u.ecs.nsidc.org/SMAP/SPL3SMP.007/'] 

def getLinks(url):
    print("Getting links from: " + url)
    page = session.get(url)
    html = page.content.decode("utf-8")
    tree = etree.parse(StringIO(html), parser=etree.HTMLParser())
    refs = tree.xpath("//a")    
    return list(set([link.get('href', '') for link in refs]))

def isDate(l):
    isDate = False
    for fmt,substr in [('%Y.%m.%d',l[0:10]), ('%Y',l[0:4])]:
        try:
            d = datetime.strptime(substr,fmt).date()
            return True
        except ValueError:
            isDate = False
    return False

def isHDFFile(l):
    ext = ['.HDF5', '.H5', '.HDF']
    return any([l.lower().endswith(e.lower()) for e in ext])   

for url in baseurls:
    session = requests.Session()
    basedir = pathlib.PurePath(url).name 
    links = getLinks(url)
    ldates = [l for l in links if isDate(l)]
    for d in ldates:
        links_date = getLinks(url + d)
        l_hdf = [l for l in links_date if isHDFFile(l)]
        for f in l_hdf:
            folder = basedir + '/' + d
            filepath = folder + f
            if pathlib.Path(filepath).is_file():
                print ("File exists: " + filepath )
            else:
                print("File doesn't exist: " + filepath )
                print("Downloading... " + url + d + f)
                f = session.get(url + d + f)
                time.sleep(1)
                pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
                open(filepath, 'wb').write(f.content)
        
    
    


