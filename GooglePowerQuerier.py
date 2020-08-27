import requests
from bs4 import BeautifulSoup as bs
import random
from selenium import webdriver

class GooglePowerQuerier:
        """Generalized Module containing engine for getting results for queries using Google Power Queries. Main use in PersonalityProfileBuilder, PlagiarismChecker, GoogleQUestionQuerier, other use undefined for time being"""
        """
        Involved Attribute : text
        """
        headers = USER_AGENTS = [
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'),  # chrome
                ('Mozilla/5.0 (X11; Linux x86_64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/61.0.3163.79 '
                 'Safari/537.36'),  # chrome
                ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
                 'Gecko/20100101 '
                 'Firefox/55.0'),  # firefox
                ('Mozilla/5.0 (X11; Linux x86_64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/61.0.3163.91 '
                 'Safari/537.36'),  # chrome
                ('Mozilla/5.0 (X11; Linux x86_64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/62.0.3202.89 '
                 'Safari/537.36'),  # chrome
                ('Mozilla/5.0 (X11; Linux x86_64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/63.0.3239.108 '
                 'Safari/537.36'),  # chrome
        ]

        def __init__(self,text):
                self.text = text
                self.driver =None

        def query_exact_match(self,multiple=False,limit=1):
                data = []
                link = 'https://www.google.com/search?q="'+self.text+'"';
                data = self.get_online_results(link,data);
                if multiple:
                        if limit > 1:
                                for i in range(1,limit+1):
                                        link = 'https://www.google.com/search?q="'+self.text+'"&start='+str(limit)+'0';
                                        data = self.get_online_results(link,data)
                return data

        def query_norm(self,multiple=False,limit=1):
                data = []
                link = 'https://www.google.com/search?q='+self.text;
                data = self.get_online_results(link,data);
                if multiple:
                        if limit > 1:
                                for i in range(1,limit+1):
                                        link = 'https://www.google.com/search?q='+self.text+'&start='+str(limit)+'0';
                                        data = self.get_online_results(link,data)
                return data;

        def get_online_results(self,link,data):
                try:
                        soup = bs(requests.get(link.replace(" ","+"),headers={"User-agent" : self.headers[1],"Accept-Language":"en"}).content,"html.parser")
                except:
                        if self.driver == None:
                                options = webdriver.ChromeOptions()
                                options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images':2})
                                self.driver = webdriver.Chrome(executable_path="C://Users/Rojit/Downloads/chromedriver_win32/chromedriver.exe",service_args=['--load-images=no'],chrome_options = options)
                        self.driver.get(link)
                        soup = bs(self.driver.page_source,"html.parser")
                results = soup.find_all(lambda tag:tag.name=="div" and tag.get("class")!= None and "rc" in tag.get("class"));
                # if "No results found" in soup.text:
                #         return data
                for result in results:
                        idata = {}
                        link_element = result.find_all("a")[0]
                        link = link_element.get("href")
                        res_text = link_element.find_all("h3")[0].text.strip()
                        s_element = result.find_all(lambda tag:tag.name=="div" and tag.get("class")!=None and "s" in tag.get("class"))[0]
                        res_subscript = s_element.text.strip()
                        exact_matching = []
                        for em in s_element.find_all("em"):
                                exact_matching.append(em.text.strip().lower())
                        idata["link"] = link
                        idata["res_text"] = res_text
                        idata["subscript"] = res_subscript
                        idata["exact_matchings"] = exact_matching
                        data.append(idata)
                return data

        def query_exact_matches(self,texts,multiple=False,limit=1):
                data = []
                link = 'https://www.google.com/search?q=';
                params = "";
                for text in texts:
                        params += '"'+text+'" | '
                params = params[0:len(params)-3]
                link += params
                data = self.get_online_results(link,data)
                if multiple:
                        if limit > 1:
                                for i in range(1,limit+1):
                                        t_link = link+'&start='+str(limit)+'0';
                                        data = self.get_online_results(t_link,data)
                return data

#print(GooglePowerQuerier("rojit rajan george").query_exact_match(multiple=True,limit=4))
