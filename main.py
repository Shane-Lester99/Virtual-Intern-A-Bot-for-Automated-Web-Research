import data_collector
import query
# TODO: Validate email. Decide if there are password rules. Decide how user retrieves password if they lose it.
# Decide how this will be done how far I will go
def is_valid_email(email):
    if email == "":
        return False
    return True

def main():
    # Create Query object. 
    queryMaster = query.Query()
    # In API, user entered email address
    email = input("Please enter your email address or any unique username.")
    while is_valid_email(email) is False:
        email = input("Invalid email, please try again.")
    # Email Does exist, enter it, enter password 
    if queryMaster.doesAccountExist(email):
        password = input("Account exists, please enter your password.") 
        i = 0
        while (queryMaster.authenticate(email, password) is False):
            if i == 2:
                print("Three invalid log in attempt. Exiting program. Goodbye.")
                return
            password = input("Please enter your password.")
            i += 1
    else:
        ans = input("Account does not exist. Would you like to create an account? (Y/N).")
        if ans is "Y" or ans is "y":
            # Allow user to create an account
            password = input("Please enter password.")
            queryMaster.createAccount(email, password)
        elif ans is "N" or ans is "n":
            print("Answer was no. Exiting program. Goodbye.")
            return
        else:
            print("Invalid answer. Exiting program. Goodbye.")
    #They are in! Now allow email alone to query information.

    #They can now query data with their email and password
    userData = [email, password]

    while True:
        command = input("Please enter a command.")
        if (command == 'Help'):
            print("Possible commands: \nHelp, \nCreateAnalysis, \nRetrievePossibleAnalysis, \nRetreieveSpecificAnalysis, \nDeleteSpecificAnalysis, \nDeleteAccount, \nUpdateAnalysis, \nQuit.")
        elif (command == "CreateAnalysis"):
            print("create analysis presses")
        elif (command == "RetrievePossibleAnalysis"):
            print("retreive possible analyisis pressed")
        elif (command == "RetrieveSpecificAnalysis"):
            print("retrieve specific analyisis pressed")
        elif (command == "DeleteSpecificAnalysis"):
            print("delete specific analysis pressed")
        elif (command == "DeleteAccount"):
            print("delete account pressed")
        elif (command == "UpdateAnalysis"):
            print("update analysis pressed")
        elif (command == "Quit"):
            print("Exiting program. Goodbye.")
            return
        else:
            print("invalid command. Please press Help to see menu.")

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

if __name__ == "__main__":
    main()
