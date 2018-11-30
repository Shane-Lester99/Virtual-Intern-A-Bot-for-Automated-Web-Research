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
        self.cursor = mydb.cursor()
    def doesAccountExist(self, email):    
        st = ("SELECT @maxID := COUNT(*) FROM User WHERE Email = %s;")
        self.cursor.execute(st, (email,))
        row = self.cursor.fetchone()
        if (row[0] == 1):
            return True
        else:
            return False
    # Given an email and a password, this method will check if there is a match
    def authenticate(self, email, password): 
        st = ("SELECT @maxID := COUNT(*) FROM User WHERE Email = %s and Password = %s;")
        self.cursor.execute(st, (email, password))
        row = self.cursor.fetchone()
        if (row[0] == 1):
            return True
        else:
            return False
    # This will enter a new user into our database
    def enterNewUser(self, email, password):
        if (self.doesAccountExist(email) is False):  
            st = ("INSERT INTO User (Email, Password) VALUES (%s, %s);");
            self.cursor.execute(st, (email, password))
            print("Account " + email + " has been sucessfully entered into db")
            return True
        else:
            print("Account " + email + " already exists.")

    # This will store a query from a data retrieval object
    def createNewQuery(self, email, dataObject):
        pass
        #searchString = dataobject.search_string
        #rl = dataObject.reference_links
        #if (searchString is None or rl is None):
        #    return
        #self.cursor.execute("SET @email = " + email + ";")
        #self.cursor.execute("SET @searchString = " + searchString + ";");
        # This will create a new query with the new search string. That will create a new 'highest' query id.
        #self.cursor.execute("INSERT INTO Query (SearchString) VALUES (@" + searchString");")
        #self.cursor.execute("SELECT @queryID :=  MAX(QueryID) FROM Query;")
        #self.cursor.execute("INSERT INTO QueryTable(Email, QueryID) VALUES (@email, @queryID);")
        #for i in range(0, len(rl), 1): 
            #self.cursor.execute("SET @rl = " + rl[i].url + ";")
            #self.cursor.execute("INSERT INTO ReferenceLink (Url) VALUES (@rl)");
            #self.cursor.execute("SELECT @referenceLinkID1 :=  MAX(ReferenceLinkID) FROM ReferenceLink;")
            #self.cursor.execute("INSERT INTO ReferenceLinkTable(QueryID, ReferenceLinkID) VALUES (@queryID, @referenceLinkID1);")
            #for j in range(0, len(rl[i].hit_links, 1):
             #   self.cursor.execute(

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

    
