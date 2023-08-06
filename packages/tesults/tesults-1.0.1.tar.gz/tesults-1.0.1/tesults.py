import ast
import json
import urllib2

def results(data):
    if type(data) != dict:
        print "Results data must be a dictionary."
        return
    
    postData = json.dumps(data)
    
    req = urllib2.Request('https://www.tesults.com/results', postData)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Content-Length', len(postData.encode('utf-8')))
    
    ret = {}
    success = True
    jsonResponse = {}
    messageResponse = ''
    
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        success = False
        jsonResponse = ast.literal_eval(e.read())
    except:
        return {'success': False, 'message': 'Unable to make request, check network.'}
        
    if success:
        jsonResponse = ast.literal_eval(response.read())
        successData = jsonResponse['data']
        codeResponse =  successData['code']
        messageResponse = successData['message']
    else:
        failData =  jsonResponse['error']
        codeResponse =  failData['code']
        messageResponse = failData['message']
    
    return {'success': success, 'message': messageResponse}