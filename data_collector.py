class Collect_Data(object):
    def __init__(self, ref_link_urls, search_string, hit_link_num):
        self.data_retrieval = Data_Retrieval(None, search_string)
        ref_links_data = []
        for i in range(0, len(ref_link_urls), 1):
            # This will store all the data from our API call in a list to be added to our Data_Retrieval object
            ref_links_data.append(self.call_api_and_fill_data(ref_link_urls[i], hit_link_num))
        self.data_retrieval.reference_links = ref_links_data

    # Returns all the data given by an API call to the reference link
    def call_api_and_fill_data(self, ref_link_url, hit_link_num):
        # This will be where we will store the data to be stored in Data_Retrieval class
        hit_links = []
        for i in range(0, hit_link_num, 1):
            # get the hit links
            hit_link_url = input("Please enter fake hit link for " + ref_link_url + ": ")
            raw_content =  hit_link_url + " This is raw content!"
            hit_link_obj = Hit_Links(hit_link_url, raw_content)
            # perform our run analysis on the link
            summary = hit_link_url + " This is the summary!"
            sentiment_analysis = True
            
            where = hit_link_url + " what!"
            who = hit_link_url + " who!"
            what = hit_link_url + " what!"
            
            questions = Questions(where, who, what)

            run_obj = Run(summary, sentiment_analysis, questions)
            # create and store objects properly for retrieval
            hit_link_obj.run_object = run_obj
            hit_links.append(hit_link_obj)
        return Reference_Links(ref_link_url, hit_links)
            
         
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
    pass
    #x = Collect_Data(["facebook.com", "Flickr.com"], "dog", 2)
    #print(x.data_retrieval.reference_links[0].hit_links[0].raw_content)  


