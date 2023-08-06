from __future__ import print_function

# dummy
def hello():
    """ Returns a Hello, World! """
    return("Hello, Python")

# dummy
def say_hello():
    """ Prints Hello, World message """
    print(hello())
    

def find_record_structure(logical_filename, thor_ip):
    import urllib2
    import ujson
    ''' get record structure '''
    records = []
    
    # Building the url which can be used extract the file layout of the logical filename
    url = "http://" + str(thor_ip) + ":8002/WsEcl/submit/query/thor/getfilelayout/json?"
    url += "esp_server=" + str(thor_ip) + "&username=&password=&logical_filename="
    url += logical_filename
    
    # Download the content of the page
    response = urllib2.urlopen(url)
    html = response.read()
    
    # Extract the record set from the json downloaded from the url
    j = ujson.loads(html)
    xml_string = j['getfilelayoutResponse']['Results']['FileLayout']['Row'][-1]
    xml_string = str(xml_string['FileLayout'])
    
    # get breaks
    breaks = xml_string.split("<br>")
    
    # removing exports and end
    breaks = breaks[1:-1]
    for break_tag in breaks:
        records.append(break_tag.strip())
    return '{' + "".join(records) + '}'


def get_content(logical_filename, thor_ip, no_sample):
    import urllib2
    import ujson
    import xmltodict

    # Find the record structure of the logical filename
    record_string = find_record_structure(logical_filename, thor_ip)
    url = "http://" + thor_ip + ":8002/WsEcl/submit/query/thor/runprogram/json?"
    url += "recordds=\'" + record_string + "\'&"
    url += "filename=\'" + logical_filename + "\'&"
    url += "sample_no=" + str(no_sample)
    
    # Replacing the whitespace in the url with %20
    url = url.replace(' ', '%20')
    
    # Download the content of the page
    response = urllib2.urlopen(url)
    html = response.read()
    
    # Parsing the response
    j = ujson.loads(html)
    xml_string = '<root>' + str(j["runprogramResponse"]["Results"]["op_GetWorkunitResult"]["Row"][-1]["Result"]) + '</root>'

    o = xmltodict.parse(xml_string)
    rows = o["root"]["Dataset"]["Row"]
    content = [[row[key] for key in row.keys()] for row in rows]
    return content
