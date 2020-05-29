#  Virtual Intern

Virtual intern automates the process of research and gives a storage interface to summarized documents. The ideal user is anyone who wants quick summaries of a large amount of documents from web links for personal or commercial use.

Using backend Python code, a SQL relational database, the google custom search API, and a simple Natural Language Processing library TextBlob, a large amount of links can be examined and summarized, automating the process of research. The experience is similar to having a personal research intern bot that can perform summaries of research for the user. 

The process goes like this: the user inputs a list of websites with a research keyword. Each link is automatically examined for the keyword. If the word is found the document is broken down by various natural language processing methods and stored as summary statistics for the user. This interface can then be cleared, saved, or added too depending on the users needs. 

Currently the interface is a command line application and the NLP layer is extremely simple. It can be easily extended using the TextBlob library to create a more sophisticated summary statistic interface. A frontend is also needed but would be extremely simple to implement. All the core logic is implemented.
