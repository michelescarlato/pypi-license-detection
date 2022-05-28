import json
import re


def retrieveGitHubUrl(jsonResponse, packageName):
    response = json.dumps(jsonResponse)
    data = json.loads(response)
    #print("Type:", type(data))
    #print(data)
    #print("\nhome_page:", data['info']['home_page'])
    url = iterdict(data, packageName)
    print(url)
    return url

def iterdict (d,packageName):
    #print(packageName)
    for k,v in d.items():
        if k != "description":
            if isinstance(v, dict):
                iterdict(v,packageName)
            else:
                if "https://github.com/" in str(v):
                    if packageName in str(v):
                        #print(str(v))
                        url = str(v)
                        print(url)
                        return url

'''
    response = json.dumps(jsonResponse)
    response = list(response.split(" "))
    gitHubUrls = []
    #print(response)
    for element in response:
        if "github.com" in element:
            #print(element)
            if packageName in element:
                element
                gitHubUrls.append(element)                
    return gitHubUrls
'''



#def queryGitHubAPIs(gitHubURL):
