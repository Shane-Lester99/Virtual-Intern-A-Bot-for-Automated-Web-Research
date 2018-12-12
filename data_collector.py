from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import json
import urllib.request
import requests
import httplib2
def collect(ref_link_urls, search_string, hit_link_num):
        data_retrieval = api_call(search_string, ref_link_urls, hit_link_num)
        if data_retrieval is None:
            print("No matching links found. No analysis created")
            return None
        data_retrieval = run_analysis_on_data_object(data_retrieval)
        return data_retrieval

def api_call(search_string, list_of_ref_links, num_of_hit_links):
    #string = search_string
    #site = list_of_ref_links
    #num_link = num_of_hit_links
    print("Retrieving web content. Please wait.")
    ref_link_obj_storage = []
    #data = Data_Retrieval(search_string, list_of_ref_links)
    #readiy = []
    #print("len(site) ", len(site))
    for i in range(0, len(list_of_ref_links), 1):
        query = search_string + " site:" + list_of_ref_links[i]
        r = Reference_Links(search_string, search(query, num_of_hit_links))
        if r.hit_links is not None:
            ref_link_obj_storage.append(Reference_Links(list_of_ref_links[i], search(query, num_of_hit_links)))
    if len(ref_link_obj_storage) is 0:
        return None
    return Data_Retrieval(ref_link_obj_storage, search_string)
  

def run_analysis_on_data_object(data_object):
    print("Creating analysis. Please wait")
    if data_object.reference_links is not None:
        for i in range(0, len(data_object.reference_links), 1):
            for j in range(0, len(data_object.reference_links[i].hit_links), 1):
                run_object = run_analysis(data_object.reference_links[i].hit_links[j])
                data_object.reference_links[i].hit_links[j].run_object = run_object 
 
    return data_object
   
  
def run_analysis(hit_link_obj):
    #perform our run analysis on the link
    summary = hit_link_obj.url + " This is the summary!"
    sentiment_analysis = True        
    where = hit_link_obj.url + " where!"
    who = hit_link_obj.url + " who!"
    what = hit_link_obj.url + " what!"        
    questions = Questions(where, who, what)
    return Run(summary, sentiment_analysis, questions)

# This is a method to return one Data_Retrieval object given one ref link and one hit_link    
def recall_one_hit_link(search_string,  ref_link_url, hit_link_url):
    # We need to create an array of one hit link to store in our Reference_Links object
    checked = check_url(hit_link_url)
                #print(results[x])
                #print(checked)
    if checked is 0:
        page_response = requests.get(hit_link_url)
        page_content = str(BeautifulSoup(page_response.content, "html.parser"))
    else:
        print("Error retrieving web content. Terminating update.")
        return None;
    
    hit_links = [Hit_Links(hit_link_url, page_content)]
    # Now we will recreate the the run stage
    run_analysis
    questions = Questions(hit_link_url + " where!", hit_link_url + " who!", hit_link_url + " what!")
    run_obj = Run(hit_link_url + " summary!", 1, questions)
    hit_links[0].run_object = run_obj
    # We then create an array of one reference_links to pass to our Data_Retrieval object
    reference_links = [Reference_Links(ref_link_url, hit_links)]
    return Data_Retrieval(reference_links, search_string)



def check_url(results_url):
    try:
        page_response = requests.get(results_url,timeout=5)
        page_response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:",errh)
        return 1
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:",errc)
        return 2
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:",errt)
        return 3
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else",err)
        return 4

    return 0

def search(search, link_num):
    try:
        service = build("customsearch", "v1",
            developerKey= getKeys()[0])
        res = service.cse().list(q=search,
      cx=getKeys()[1]).execute()
    except httplib2.ServerNotFoundError as err:
        print("Error: ", err, "Consider checking network connection.")
        return None

    results = []
    page_content = []
    hits = []
    
    if (len(res) < link_num):
        print("Only", len(res), " links found.")
        link_num = len(res)

    for x in range(0, link_num, 1):
        if "items" not in res:
            return
        results.append(json.dumps(res['items'][x]['link']))
    
    for x in range(link_num):
        results[x] = results[x].replace('"', '')

    for x in range(link_num):
        if "items" not in res:
            return 
        else: 
            if results != '':
                results[x] = results[x].replace('"', '')
                checked = check_url(results[x])
                #print(results[x])
                #print(checked)
                if checked is 0:
                    page_response = requests.get(results[x])
                    page_content = str(BeautifulSoup(page_response.content, "html.parser"))
                    #print(page_content)

                    hits.append(Hit_Links(results[x], page_content))
                    #print("results[x] ", results[x])
    #print(page_content)
    #print("hits ", hits)
    #print("len(hits) ", len(hits))
    return hits

def getKeys():
    x = []
    file = open("keys.txt", "r")
    for line in file:
        x.append(line)
    return x

def put_in(site, hits):
    #print("len(hits) ", len(hits))
    #print("len(site) ", len(site))
    array_hits = []
    ref = []
    for i in range(0, len(hits), 1):
        if hits is not None:
            #array_hits.insert(len(array_hits), hits[i])
            array_hits.append(hits[i])

class Data_Retrieval(object):
	def __init__(self, reference_links, search_string):
		self.search_string = search_string
		self.reference_links = reference_links


class Reference_Links(object):
	def __init__(self, url, hit_links):
		self.url = url
		self.hit_links = hit_links


class Hit_Links(object):
	def __init__(self, url, raw_content):
		self.url = url
		self.raw_content = raw_content
		self.run_object = None

class Run(object):
	def __init__(self, summary, sentiment_analysis, questions):
		self.summary = summary
		self.sentiment_analysis = sentiment_analysis
		self.questions = questions


class Questions(object):
	def __init__(self, where, who, what):
		self.where = where
		self.who = who
		self.what = what

if __name__== "__main__":
    
    x = collect(["facebook.com", "Flickr.com"], "dog", 2)
    #print(x.reference_links[0].hit_links[0].raw_content)  
    print("Done:)")

