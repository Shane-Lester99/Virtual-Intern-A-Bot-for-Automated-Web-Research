
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import json
import urllib.request
import requests

class Data_Retrieval(object):
	def __init__(self, reference_links, search_string):
		self.search_string = search_string
		self.reference_links = reference_links


class Reference_Links(object):
	def __init__(self, url, hit_links):
		self.url = url
		self.hit_links = hit_links


class Hit_Links(object):
	def __init__(self, url, hit_link_id, raw_content):
		self.url = url
		self.hit_link_id = hit_link_id
		self.raw_content = raw_content
		# Dont worry about below this line !!!!!!!!!!!!!
		self.run_object = None

	def enter_run_stage(self, run_object):
		self.run_object = run_object

class Run(object):
	def __init__(self, summary, sentimentAnalysis, questions):
		self.summary = summary
		self.sentimentAnalysis = sentimentAnalysis
		self.questions = questions


class Questions(object):
	def __init__(self, where, who, what):
		self.where = where
		self.who = who
		self.what = what

def search(search, link_num):
    service = build("customsearch", "v1",
            developerKey="AIzaSyBD9ZOK0SnCn_lzpLtSAezUI7yUVfUJ2pE")

    res = service.cse().list(q=search,
      cx='017225943151680571230:hr5srssdquy').execute()

    results = []
    page_content = []
    hits = []

    for x in range(link_num):
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
                    page_content = BeautifulSoup(page_response.content, "html.parser")
                    #print(page_content)

                    hits.append(Hit_Links(results[x], None, page_content))
                    #print("results[x] ", results[x])
    #print(page_content)
    #print("hits ", hits)
    #print("len(hits) ", len(hits))
    return hits

def put_in(site, hits):
    #print("len(hits) ", len(hits))
    #print("len(site) ", len(site))
    array_hits = []
    ref = []
    for i in range(0, len(hits), 1):
        if hits is not None:
            #array_hits.insert(len(array_hits), hits[i])
            array_hits.append(hits[i])
        ref.append(Reference_Links(site[i], array_hits))

    #print("len(array_hits) ", len(array_hits))
    #print("string ", string)
    return ref

def api_call(search_string, list_of_ref_links, num_of_hit_links):
    #string = search_string
    #site = list_of_ref_links
    #num_link = num_of_hit_links
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
   

    #for i in range(0, num_of_hit_links, 1):
    #    ready.append(put_in(store_hits, store_hits[i], string))
        #print("ready ", ready)

    #print("len(store_hits)", len(store_hits))
    #print("len(site) ", len(site))
    #print("site[0] ",site[0])
    #print("store_hits[0] ", store_hits[0])
    #for n in range(len(site)):
        #temp = site
        #ready = put_in(temp, store_hits[n])

    #print("len(ready) ", len(ready))
    
    #print("ready[0].search_string ", ready[0].search_string)
    #print("ready[1].search_string ", ready[1].search_string)
    
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

if __name__ == "__main__":

	# For web scraping use beautiful soup

	# ALL YOU HAVE TO WORRY ABOUT IS url and raw_content

	# These are our "hit links", these are what we retrieve from our reference
	# links
	#hitLink1 = Hit_Links("wiki/dogFunny.com", None, "web scraping text oreilly")
	#hitLink2 = Hit_Links("wiki/dogCrazy.com", None, "web scraping text oreilly")
	#arrayHLA = [hitLink1, hitLink2]
	#hitLink3 = Hit_Links("fb/dogBannaza.com", None, "web scraping text oreilly")
	#hitLink4 = Hit_Links("fb/dogTopia.com", None, "web scraping text oreilly")
	#arrayHLB = [hitLink3, hitLink4]

	#rlA = Reference_Links("wikipedia.com", arrayHLA)
	#rlB = Reference_Links("fb.com", arrayHLB)

	#referenceLinkArray = [rlA, rlB]

	#Data_Retrieval(referenceLinkArray, "dog")

	

    string = "apple"
    listx = ["cnn.com", "hamster.com", "http://wikipedia.org"]
    num_link = 1
    x = api_call(string, listx, num_link)

    #print("How many Data Retrieval Objects: ", len(x))
    #print("How many Reference Links: ", "Obkect 1: ", len(x[0].reference_links), "object 2: ",  len(x[1].reference_links))
    #print("How many hit links: ", "Object 1, rl1: ", len(x[0].reference_links[0].hit_links), "Object 1, rl2: ", len(x[0].reference_links[1].hit_links))
    #print("How many hit links: ", "Object 2, rl1: ", len(x[1].reference_links[0].hit_links), "Object 1, rl2: ", len(x[1].reference_links[1].hit_links))
     
    print("Search string:", x.search_string)
    print("Reference Link 1: ", x.reference_links[0].url)
    for i in range(0, len(x.reference_links), 1):
        for j in range(0, len(x.reference_links[i].hit_links), 1):
            print(x.reference_links[i].hit_links[j].url)
    #print(len(x.reference_links[0].hit_links))
    #print(len(x.reference_links[1].hit_links))
    #print(len(x.reference_links[2].hit_links))
    #for i in range(0, len(x.reference_links[0].hit_links), 1):
    #    print("Reference Link 1, Hit Link ", i, ":",  x.reference_links[0].hit_links[i].url)
    #print("Reference Link 2: ", x.reference_links[1].url)
    #for i in range(0, len(x.reference_links[1].hit_links), 1):
    #    print("Reference Link 2, Hit Link ", i, ":",  x.reference_links[1].hit_links[i].url)
    #for i in range(0, len(x.reference_links[2].hit_links), 1):
    #    print("Reference Link 3, Hit Link ", i, ":",  x.reference_links[2].hit_links[i].url)
   

    #print("\n")
    #print("data ", data)
    #print("data[0].search_string ", data[0].search_string)
   # print("data[0].reference_links[0].hit_links ", data[0].reference_links[0].hit_links)
   # for i in range(0, len(data[0].reference_links[0].hit_links)):
    #    print("Reference Link 1, Hit Link ", i, ":", data[0].reference_links[0].hit_links[i].url)
    #print("data.reference_links[0].url", data[0].reference_links[0].url)

    #print("data[1].reference_links[0].hit_links ", data[1].reference_links[0].hit_links)
    #for i in range(0, len(data[1].reference_links[0].hit_links)):
    #    print("Reference Link 2, Hit Link ", i, ":", data[1].reference_links[0].hit_links[i].url)
    #print("data[1].reference_links[0].url", data[1].reference_links[0].url)
