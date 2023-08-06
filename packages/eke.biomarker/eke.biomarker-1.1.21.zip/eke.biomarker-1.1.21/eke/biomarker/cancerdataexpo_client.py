import urllib2, json, requests, re
from base64 import encodestring

IDSEARCH_API = "http://edrn-dev.jpl.nasa.gov/cancerdataexpo/idsearch"

def getBiomarkerLinks(biomarker, idDataSource):
    if not idDataSource:
        idDataSource = IDSEARCH_API
    if idDataSource.strip() == "":
        idDataSource = IDSEARCH_API
        
    r = requests.get(idDataSource+"/"+biomarker, headers={'Accept': 'application/json'})

    j= r.text
    j=j.replace("'", '"')
    j=j.replace('u"', '"')
    j=j.strip()
    
    jsonresults = None
    if j != "":
        try:
            jsonresults = json.loads(j)
        except ValueError:
            pass
    return jsonresults
