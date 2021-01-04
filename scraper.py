import cloudscraper, requests, json
from scraper_api import ScraperAPIClient


API_SB = SCRAPINGBEE_API_KEY
API_SA = SCRAPERAPI_API_KEY
API_WI = WINTR_API_KEY

client = ScraperAPIClient(API_SA)
scraper = cloudscraper.create_scraper()



class Scraper:
    def __init__(self):
        self.credits = {"self.scraperAPI('{}')": self.scraperAPICount(), "self.scrapingbee('{}')": self.scrapingbeeCount(), "self.wintrAPI('{}')": self.wintrCount()}

    def get(self, url):
        r = scraper.get(url)
        if r.status_code != 429 and r.status_code != 403: #Scraper-APIs nur verwenden, wenn Statuscode 429 ("too many requests") ist, um Credits nicht unnötig zu verschwenden
            return r
        else:
            scraper_to_use = max(self.credits, key = self.credits.get) #prüft, welcher Scraper noch am meisten Credits hat und wählt diesen aus
            return eval(scraper_to_use.format(url))

    def scraperAPICount(self):
        sa_usage = client.account()
        return sa_usage['requestLimit'] - sa_usage['requestCount']

    def wintrCount(self):
        r = requests.get("https://api.wintr.com/accountdata?data=info&apikey={api_key}".format(api_key = API_WI))
        return json.loads(r.text)['apicredits']

    def scrapingbeeCount(self):
        r = requests.get(url="https://app.scrapingbee.com/api/v1/usage", params={"api_key": API_SB})
        sb_data = json.loads(r.text)
        return sb_data['max_api_credit'] - sb_data['used_api_credit']

    def scraperAPI(self, url):
        r = client.get(url=url)
        if r.status_code == 200 or r.status_code == 400:
            self.credits["self.scraperAPI('{}')"] -= 1
        return r

    def scrapingbee(self, url):
        r = requests.get(url="https://app.scrapingbee.com/api/v1/", params={"api_key": API_SB, "url": url, "render_js": "false"})
        if r.status_code == 200 or r.status_code == 404:
            self.credits["self.scrapingbee('{}')"] -= 1
        return r

    def wintrAPI(self, url):
        class Helper():
            def __init__(self, url, status_code, text):
                self.url = url
                self.status_code = status_code
                self.text = text

        data = {"url": url, "apikey": API_WI}
        r = requests.post(url="https://api.wintr.com/fetch", params=data)
        url = "https://api.wintr.com/fetch"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        status = json.loads(r.content)['info']['status']
        url = json.loads(r.content)['info']['url']
        text = json.loads(r.content)['content']
        r_helper = Helper(url, status, text)
        return r_helper
