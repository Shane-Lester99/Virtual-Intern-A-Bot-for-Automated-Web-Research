import data_collector
import query

if __name__ == "__main__":
    # Create Query object. 

    # In API, user entered email address

    # Email Does not exist, enter it, enter password 

    # Email exists, Authenticate password or else be kicked out in 3 attempts

    #They are in! Now allow email alone to query information.

    # HELP
    # User asks for help: they get a list of possible commands

    # CreateAnalysis
    # User asks to create sentiment analysis. Inputs 1...3 reference links, search string, and 1...10 return requests
    # Returns RetrievePossibleAnalysis

    # RetrievePossibleAnalysis
    # Returns the list with a queryID, search strings, reference links, and a summary of each analysis
    
    # RetreieveSpecificAnalsis
    # With that list of querID, referenceLinkID, and hitLinkID, retrieve a detailed sentiment analysis on each 

    # Delete:
    # Can delete an analysis given queryID, referenceLinkID, and hitLinkID

    # Delete Account:
    # Can delete all their queries, account, and id. Exits out of the API. 

    # Update Analysis
    # Given a queryID, update the contents of the sentiment analysis and re-run it with more up to date websites 
