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

if __name__== "__main__":
    pass   


