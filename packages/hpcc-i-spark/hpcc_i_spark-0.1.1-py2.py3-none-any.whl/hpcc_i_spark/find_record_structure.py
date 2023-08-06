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