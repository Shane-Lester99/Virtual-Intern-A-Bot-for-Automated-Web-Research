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
        self.cursor.execute("SET @email= \"" + email + "\";")
        self.cursor.execute("SELECT @maxID := COUNT(*) FROM User WHERE Email = @email;")
        row = self.cursor.fetchone()
        if (row[0] == 1):
            return True
        else:
            return False
    # Given an email and a password, this method will check if there is a match
    def authenticate(self, email, password):
        self.cursor.execute("SET @email= \"" + email + "\";")
        self.cursor.execute("SET @password= \"" + password + "\";")
        self.cursor.execute("SELECT @maxID := COUNT(*) FROM User WHERE Email = @email and Password = @password;")
        row = self.cursor.fetchone()
        if (row[0] == 1):
            return True
        else:
            return False
    # This will enter a new user into our database
    def enterNewUser(self, email, password):
        if (self.doesAccountExist(email) is False):
            self.cursor.execute("SET @email= \"" + email + "\";")
            self.cursor.execute("SET @password= \"" + password + "\";")
            self.cursor.execute("INSERT INTO User (Email, Password) VALUES (@email, @password);");
            print("Account " + email + " has been sucessfully entered into db")
            return True
        else:
            print("Account " + email + " already exists.")

    # This will store a query from a data retrieval object
    def createNewQuery(self, dataObject):
        pass

    def __use(self):
        return "USE DATABASE " + self.__currentDB


if __name__ == "__main__":
    query = Query()
    Hit_links1 = Hit_links("wiki/dogFunny.com", None, "web scraping text oreilly")
    Hit_links2 = Hit_links("wiki/dogCrazy.com", None, "web scraping text oreilly")
    arrayHLA = [Hit_links1, Hit_links2]
    Hit_links3 = Hit_links("fb/dogBannaza.com", None, "web scraping text oreilly")
    Hit_links4 = Hit_links("fb/dogTopia.com", None, "web scraping text oreilly")
    arrayHLB = [Hit_links3, Hit_links4]

    rlA = Reference_Links("wikipedia.com", arrayHLA)
    rlB = Reference_Links("fb.com", arrayHLB)

    referenceLinkArray = [rlA, rlB]

    Data_Retrieval(refrenceLinkArray, "dog")

    
