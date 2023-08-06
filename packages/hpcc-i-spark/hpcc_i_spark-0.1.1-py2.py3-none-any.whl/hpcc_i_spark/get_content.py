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