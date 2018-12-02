import mysql.connector
import data_collector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Shanelester1",
  database="CollectiveConscience"
)

mydb.autocommit = True

class Query(object):
    def __init__(self):
        self.__currentDB = "CollectiveConscience"
        self.__use()
        self.cursor = mydb.cursor(buffered = True)
    def doesAccountExist(self, email):    
        query = ("SELECT @maxID := COUNT(*) FROM User WHERE Email = %s;")
        self.cursor.execute(query, (email,))
        row = self.cursor.fetchone()
        if (row[0] == 1):
            return True
        else:
            return False
    # Given an email and a password, this method will check if there is a match
    def authenticate(self, email, password): 
        query = ("SELECT @maxID := COUNT(*) FROM User WHERE Email = %s and Password = %s;")
        self.cursor.execute(query, (email, password))
        row = self.cursor.fetchone()
        if (row[0] == 1):
            return True
        else:
            return False
    # This will enter a new user into our database
    def createAccount(self, email, password, authKey):
        if (self.doesAccountExist(email) is False):  
            query = ("INSERT INTO User (Email, Password, authKey) VALUES (%s, %s, %s);");
            self.cursor.execute(query, (email, password, authKey))
            print("Account " + email + " has been sucessfully entered into db")
            return True
        else:
            print("Account " + email + " already exists.")

    # This will store a query from a data retrieval object
    def createNewQuery(self, email, dataObject):  
        if (dataObject.search_string is None or dataObject.reference_links is None):
            return
        # This will create a new query with the new search string. That will create a new 'highest' query id.
        query = "INSERT INTO Query (SearchString) VALUES (%s);"
        self.cursor.execute(query, (dataObject.search_string,))
        self.cursor.execute("SELECT @queryID :=  MAX(QueryID) FROM Query;")
        query = ("INSERT INTO QueryTable(Email, QueryID) VALUES (%s, @queryID);")
        self.cursor.execute(query, (email,))
        rl = dataObject.reference_links
        for i in range(0, len(rl), 1):
            query = "INSERT INTO ReferenceLink (Url) VALUES (%s)";
            self.cursor.execute(query, (rl[i].url,))
            self.cursor.execute("SELECT @referenceLinkId :=  MAX(ReferenceLinkID) FROM ReferenceLink;")
            self.cursor.execute("INSERT INTO ReferenceLinkTable(QueryID, ReferenceLinkID) VALUES (@queryID, @referenceLinkId);")
            for j in range(0, len(rl[i].hit_links), 1):
                query = "INSERT INTO HitLink (Url, RawContent, RunSentiment, RunWhere, RunWho, RunWhat, RunSummary) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                data = dataObject.reference_links[i].hit_links[j]
                para = (data.url,  data.raw_content, data.run_object.sentiment_analysis, data.run_object.questions.where, data.run_object.questions.who, data.run_object.questions.what, data.run_object.summary)
                self.cursor.execute(query, para)
                self.cursor.execute("SELECT @hitLinkId :=  MAX(HitLinkID) FROM HitLink;")
                self.cursor.execute("INSERT INTO HitLinkTable (HitLinkID, ReferenceLinkID) VALUES (@hitLinkId, @referenceLinkId)")
                
    def retrieveAllSummaries(self, email):
        query = """SELECT OtherStuffAndHitLinkId.QueryID, OtherStuffAndHitLinkId.SearchString, OtherStuffAndHitLinkId.ReferenceLinkID, OtherStuffAndHitLinkId.url, OtherStuffAndHitLinkId.HitLinkID, HitLink.url, HitLink.runSummary FROM
	(SELECT QueryIDAndStringAndRefLinkIDAndRefUrl.QueryID, QueryIDAndStringAndRefLinkIDAndRefUrl.SearchString, QueryIDAndStringAndRefLinkIDAndRefUrl.ReferenceLinkID, QueryIDAndStringAndRefLinkIDAndRefUrl.Url, HitLinkTable.HitLinkID FROM
	(SELECT QueryIDAndStringAndRefLinkID.QueryID, QueryIDAndStringAndRefLinkID.SearchString, QueryIDAndStringAndRefLinkID.ReferenceLinkID, ReferenceLink.Url FROM
    (SELECT EmailAndIDAndString.QueryID, EmailAndIDAndString.SearchString, ReferenceLinkTable.ReferenceLinkID FROM
	(SELECT Query.QueryID, Query.SearchString, EmailAndID.Email FROM 
	(SELECT User.Email, QueryTable.QueryID 
	FROM QueryTable JOIN User ON QueryTable.Email=User.Email where User.email = %s) 
	as EmailAndID 
	JOIN Query ON EmailAndID.QueryID=Query.QueryID) 
	as EmailAndIDAndString
	JOIN ReferenceLinkTable ON EmailAndIDAndString.QueryID = ReferenceLinkTable.QueryID)
	as QueryIDAndStringAndRefLinkID
	JOIN ReferenceLink ON QueryIDAndStringAndRefLinkID.ReferenceLinkID=ReferenceLink.ReferenceLinkID)
	as QueryIDAndStringAndRefLinkIDAndRefUrl
	JOIN HitLinkTable ON QueryIDAndStringAndRefLinkIDAndRefUrl.ReferenceLinkID=HitLinkTable.ReferenceLinkID)
	as OtherStuffAndHitLinkId
	JOIN HitLink on OtherStuffAndHitLinkId.HitLinkID = HitLink.HitLinkID;"""
        self.cursor.execute(query, (email,))
        results = []
        i = 0
        for row in self.cursor.fetchall():
            results.append({"Query Values: " : [row[0], row[2], row[4]], "Search String: " : row[1], "Reference Link URL: " : row[3], "Hit Link URL: " : row[5], "Summary: " : row[6]})
            print(results[i])
            i += 1 

    def retrieveSpecificAnalysis(self, email, queryID, rlID, hlID):
        query = """SELECT MasterTable.searchString, MasterTable.RLURL, MasterTable.HLURL, MasterTable.RunSummary, HitLink.RunSentiment, HitLink.RunWho, HitLink.RunWhat, HitLink.RunWhere  FROM
	(SELECT OtherStuffAndHitLinkId.QueryID, OtherStuffAndHitLinkId.SearchString, OtherStuffAndHitLinkId.ReferenceLinkID, OtherStuffAndHitLinkId.Url as RLURL, OtherStuffAndHitLinkId.HitLinkID, HitLink.Url as HLURL, HitLink.runSummary FROM
	(SELECT QueryIDAndStringAndRefLinkIDAndRefUrl.QueryID, QueryIDAndStringAndRefLinkIDAndRefUrl.SearchString, QueryIDAndStringAndRefLinkIDAndRefUrl.ReferenceLinkID, QueryIDAndStringAndRefLinkIDAndRefUrl.Url, HitLinkTable.HitLinkID FROM
	(SELECT QueryIDAndStringAndRefLinkID.QueryID, QueryIDAndStringAndRefLinkID.SearchString, QueryIDAndStringAndRefLinkID.ReferenceLinkID, ReferenceLink.Url FROM
    (SELECT EmailAndIDAndString.QueryID, EmailAndIDAndString.SearchString, ReferenceLinkTable.ReferenceLinkID FROM
	(SELECT Query.QueryID, Query.SearchString, EmailAndID.Email FROM 
	(SELECT User.Email, QueryTable.QueryID 
	FROM QueryTable JOIN User ON QueryTable.Email=User.Email WHERE User.email = %s AND QueryTable.QueryID = %s) 
	as EmailAndID 
	JOIN Query ON EmailAndID.QueryID=Query.QueryID) 
	as EmailAndIDAndString
	JOIN ReferenceLinkTable ON EmailAndIDAndString.QueryID = ReferenceLinkTable.QueryID WHERE ReferenceLinkTable.ReferenceLinkID = %s)
	as QueryIDAndStringAndRefLinkID
	JOIN ReferenceLink ON QueryIDAndStringAndRefLinkID.ReferenceLinkID=ReferenceLink.ReferenceLinkID)
	as QueryIDAndStringAndRefLinkIDAndRefUrl
	JOIN HitLinkTable ON QueryIDAndStringAndRefLinkIDAndRefUrl.ReferenceLinkID=HitLinkTable.ReferenceLinkID WHERE HitLinkTable.HitLinkID = %s)
	as OtherStuffAndHitLinkId
	JOIN HitLink on OtherStuffAndHitLinkId.HitLinkID = HitLink.HitLinkID)
	as MasterTable
	JOIN HitLink on MasterTable.HitLinkID = HitLink.HitLinkID"""
        self.cursor.execute(query, (email, queryID, rlID, hlID))
        results = []
        i = 0
        for row in self.cursor.fetchall():
            print(row)
            #results.append({"Query Values: " : [row[0], row[2], row[4]], "Search String: " : row[1], "Reference Link URL: " : row[3], "Hit Link URL: " : row[5], "Summary: " : row[6]})
            #print(results[i])
            #i += 1 



    def __use(self):
        return "USE DATABASE " + self.__currentDB


if __name__ == "__main__":
    query = Query()
    query.enterNewUser("shanejlester@gmail.com", "p")
    print(query.authenticate("shanejlester@gmail.com", "p"))
    #Hit_links1 = Hit_links("wiki/dogFunny.com", None, "web scraping text oreilly")
    #Hit_links2 = Hit_links("wiki/dogCrazy.com", None, "web scraping text oreilly")
    #arrayHLA = [Hit_links1, Hit_links2]
    #Hit_links3 = Hit_links("fb/dogBannaza.com", None, "web scraping text oreilly")
    #Hit_links4 = Hit_links("fb/dogTopia.com", None, "web scraping text oreilly")
    #arrayHLB = [Hit_links3, Hit_links4]

    #rlA = Reference_Links("wikipedia.com", arrayHLA)
    #rlB = Reference_Links("fb.com", arrayHLB)

    #referenceLinkArray = [rlA, rlB]

    #Data_Retrieval(refrenceLinkArray, "dog")

    
