from bs4 import BeautifulSoup
import requests
hit_link_url = "https://stackoverflow.com/questions/40668390/mysql-connector-errors-programmingerror-failed-processing-format-parameters-py"
page_response = requests.get(hit_link_url)
page_content = str(BeautifulSoup(page_response.content, "html.parser"))
print(type(page_content))

