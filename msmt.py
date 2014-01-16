#!/usr/bin/python

import urllib, urllib2 
import json

import re

import requests

from lxml import etree

from datetime import datetime

def datestring(display_format="%a, %d %b %Y %H:%M:%S", datetitme_object=None):
    """Convert the datetime object (defaults to now, in utc) into a string, in the given display format"""
    datetime_object = datetime.utcnow()
    return datetime.strftime(datetime_object, display_format)
    
    
def get_access_token (client_id, client_secret):
    """Make an HTTP POST request to the token service, and return the access_token,
    as described in number 3, here: http://msdn.microsoft.com/en-us/library/hh454949.aspx
    """
 
    data = urllib.urlencode({
        'client_id' : client_id,
        'client_secret' : client_secret,
        'grant_type' : 'client_credentials',
        'scope' : 'http://api.microsofttranslator.com'
    })
 
    try:
 
        request = urllib2.Request('https://datamarket.accesscontrol.windows.net/v2/OAuth2-13')
        request.add_data(data)

        #request = urllib2.Request("https://datamarket.accesscontrol.windows.net/v2/OAuth2-13")
        #request = urllib2.Request("http://api.microsofttranslator.com/v2/Http.svc/Translate")
        #request = urllib2.Request("http://api.microsofttranslator.com/V2/Http.svc/Translate")
        #request = urllib2.Request("http://api.microsofttranslator.com/V2/Http.svc/Translate")
 
        response = urllib2.urlopen(request)
        response_data = json.loads(response.read())
 
        if response_data.has_key('access_token'):
            return response_data['access_token']
 
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
          print datestring(), 'Could not connect to the server:', e.reason
        elif hasattr(e, 'code'):
          print datestring(), 'Server error: ', e.code
    except TypeError:
        print datestring(), 'Bad data from server'
        
        
def to_bytestring(s):
    """Convert the given unicode string to a byetstring, using utf-8 encoding,
    unless it's already a bytestring"""
    if s:
        if isinstance(s, str):
            return s
        else:
            return s.encode("utf-8")
        

def translate (access_token, text, to_lang, from_lang=None):
    """Use the HTTP Interface to translate text, as described here:
    http://msdn.microsoft.com/en-us/library/ff512387.aspx
    and return an xml string if successful
    """
 
    if not access_token:
        print 'Sorry, the access token is invalid'
    else:
        data = { 'text' : to_bytestring(text), 'to' : to_lang }
 
        data['from'] = from_lang
 
        try:
            #request = urllib2.Request("http://api.microsofttranslator.com/v2/Http.svc/Translate?text=" + urllib.urlencode(text) + "&from=" + from_lang + "&to=" + to_lang)
            #print "request:", request.get_full_url()
            #request = urllib2.Request("http://api.microsofttranslator.com/V2/Http.svc/Translate?" + urllib.urlencode(data))
            
            request = urllib2.Request('http://api.microsofttranslator.com/v2/Http.svc/Translate?'+urllib.urlencode(data))
            request.add_header('Authorization', 'Bearer '+access_token)
            #request.add_header('Authorization', access_token)
            
            #print "Request:", request.get_full_url()
 
            response = urllib2.urlopen(request)
            xml = response.read()
            #return get_text_from_msmt_xml(xml)
            
            return xml
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print datestring(), 'Could not connect to the server:', e.reason
            elif hasattr(e, 'code'):
                print datestring(), 'Server error: ', e.code
                

def translateArray(access_token, texts, to_lang, from_lang=None):
        translateArraySourceTexts = texts
        uri = "http://api.microsofttranslator.com/v2/Http.svc/TranslateArray2";
        body = ""
        body += "<TranslateArrayRequest>"
        body += "<AppId />"
        body += "<From>" + from_lang + "</From>"
        body += "<Options>"
        body += " <Category xmlns=\"http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2\" />"
        body += "<ContentType xmlns=\"http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2\">text/plain</ContentType>"
        body += "<ReservedFlags xmlns=\"http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2\" />"
        body += "<State xmlns=\"http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2\" />" 
        body += "<Uri xmlns=\"http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2\" />"
        body += "<User xmlns=\"http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2\" />"
        body += "</Options>"
        body += "<Texts>"
        for text in texts:
            body += "<string xmlns=\"http://schemas.microsoft.com/2003/10/Serialization/Arrays\">" + text + "</string>"
        #body += "<string xmlns=\"http://schemas.microsoft.com/2003/10/Serialization/Arrays\">{3}</string>"
        #body += "<string xmlns=\"http://schemas.microsoft.com/2003/10/Serialization/Arrays\">{4}</string>"
        body += "</Texts>"
        body += "<To>" + to_lang + "</To>"
        body += "</TranslateArrayRequest>"
        
        #print "from_lang:", from_lang
        #reqBody = body.format(body, from_lang, "text/plain", translateArraySourceTexts[0], to_lang);
        
        #print body
        
        #request.add_header
            
        headers = {'Authorization': 'Bearer '+access_token, "content-type": "text/xml"}
            
        response = requests.post(uri, data=body, headers=headers)
        xml = response.content
        
        return xml
                

def translateArray2(access_token, texts, to_lang, from_lang=None):
    """Use the HTTP Interface to translate text, as described here:
    http://msdn.microsoft.com/en-us/library/ff512387.aspx
    and return an xml string if successful
    """
 
    if not access_token:
        print 'Sorry, the access token is invalid'
    else:
        #data = { 'texts' : texts, 'to' : to_lang }
        #data['from'] = from_lang
        
        headers = {'Authorization': 'Bearer '+access_token, "content-type": "application/json" }
        
        options = {
            'Category': "general",
            'Contenttype': "text/plain",
            'Uri': '',
            'User': 'default',
            'State': ''
        }
        
        params = {
            'texts': json.dumps(texts),
            'to': to_lang,
            'from': from_lang,
            'options': json.dumps(options),
        }
        
        try:
            #translate_array_url = "http://api.microsofttranslator.com/V2/Ajax.svc/TranslateArray"
            translate_array_url = "http://api.microsofttranslator.com/v2/Http.svc/TranslateArray"
            #url = translation_url = translate_array_url + "?" + urllib.urlencode(params)
            response = requests.post(url=translate_array_url, data=params, headers=headers)
            
            
            #request = urllib2.Request(translate_array_url, data=urllib.urlencode(data), headers=headers)
            
            #print "Request:", request.get_full_url()
 
            #response = urllib2.urlopen(request)
            #xml = response.read()
            return response.content
            #return get_text_from_msmt_xml(xml)
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print datestring(), 'Could not connect to the server:', e.reason
            elif hasattr(e, 'code'):
                print datestring(), 'Server error: ', e.code
 
def get_tr(xml):
    translations = []
    doc = etree.fromstring(xml)
    respArray = doc.findall("{http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2}TranslateArray2Response")
    print "len(respArray):", len(respArray)
    for resp in respArray:
        translatedText = resp.find("{http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2}TranslatedText")
        try:
            translations.append(translatedText.xpath("./text()")[0])
        except IndexError:
            translations.append("")
    return translations
    #return re.findall("<TranslatedText>(.*?)</TranslatedText>", xml)

    
def get_alignment(xml):
    alignments = []
    doc = etree.fromstring(xml)
    respArray = doc.findall("{http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2}TranslateArray2Response")
    for resp in respArray:
        alignment = resp.find("{http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2}Alignment")
        #print alignment
        try:
            alignments.append(alignment.xpath("./text()")[0])
        except IndexError:
            alignments.append("")
    return alignments
    #return re.findall("<Alignment>(.*?)</Alignment>", xml)
    
"""
translateArrayResponse.find("{http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2}Alignment")
alignments = translateArrayResponse.findall("{http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2}Alignment")
alignments[0].xpath('./text()')

"""

 
def get_text_from_msmt_xml (xml):
    """Parse the xml string returned by the MS machine translation API, and return just the text"""
 
    text = []
    doc = etree.fromstring(xml)
    #for elem in doc.xpath('/foo:string', namespaces={'foo': 'http://schemas.microsoft.com/2003/10/Serialization/'}):
    for elem in doc.xpath('/TranslatedText'):
        if elem.text:
            elem_text = ' '.join(elem.text.split())
            if len(elem_text) > 0:
                text.append(elem_text)
    return ' '.join(text)
