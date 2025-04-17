import datetime
import json
import random
import re
import requests



def download_subtitle_for_date_19h(day, month, year, proxies = None):
    captions_api_response = "not found"
    url = ""
    i = 1
    while "not found" in captions_api_response and i <= 10:
        url = f'https://utstreaming.zdf.de/mtt/zdf/{year}/{month:02d}/{year}{month:02d}{day:02d}_1900_sendung_h19/{i}/19_Uhr_{day:02d}{month:02d}{year}.xml'
        x = requests.get(url, headers= {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
                "Accept": "application/vnd.de.zdf.v1.0+json",
                "Accept-Language": "en-US,en;q=0.5",
                "Api-Auth": "Bearer aa3noh4ohz9eeboo8shiesheec9ciequ9Quah7el",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Priority": "u=4"
            }, proxies = proxies
            )
        i += 1
        captions_api_response = x.text
    if "not found" not in captions_api_response:
        path = f"./downloads/19h/{year}{month:02d}{day:02d}.xml"
        with open(path, "w") as output:
            output.write(captions_api_response)




def get_subtitle_for_date(day, month, year):
    months = ["januar", "februar", "maerz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember"]
    

    heute_seite_html = requests.get(f'https://www.zdf.de/nachrichten/heute-journal/heute-journal-vom-{day}-{months[month-1]}-20{year}-100.html', headers= {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/136.0",
                "Accept": "application/vnd.de.zdf.v1.0+json",
                "Accept-Language": "en-US,en;q=0.5",
                "Api-Auth": "Bearer aa3noh4ohz9eeboo8shiesheec9ciequ9Quah7el",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Priority": "u=4"
            })
    regex_string = f"{year}-{month:02d}-{day:02d}T[0-2][0-9]:[0-5][0-9]"
    date_string_list = re.findall(regex_string, heute_seite_html.text)
    air_time = date_string_list[0].split("T")[1]
    date_api_string = f"{year}{month:02d}{day:02d}_{air_time.replace(":","")}"
    x = "not found"
    i = 1
    while "not found" in x:
        x = requests.get(f'https://api.zdf.de/tmd/2/ngplayer_2_5/vod/ptmd/mediathek/{date_api_string}_sendung_hjo_dgs/{i}', headers= {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
                "Accept": "application/vnd.de.zdf.v1.0+json",
                "Accept-Language": "en-US,en;q=0.5",
                "Api-Auth": "Bearer aa3noh4ohz9eeboo8shiesheec9ciequ9Quah7el",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Priority": "u=4"
            }
            )
        i += 1
    xml_url = None
    captions = json.loads(x.text)["captions"]
    for caption in captions:
        if caption["format"] == "ebu-tt-d-basic-de":
            xml_url = caption["uri"]
    print(xml_url)
    return xml_url


def get_proxy_list():
    list_request = requests.get("https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=http&proxy_format=protocolipport&format=json&anonymity=Elite&timeout=100", headers= {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/136.0",
                "Accept": "application/vnd.de.zdf.v1.0+json",
                "Accept-Language": "en-US,en;q=0.5",
                "Api-Auth": "Bearer aa3noh4ohz9eeboo8shiesheec9ciequ9Quah7el",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Priority": "u=4"
            })
    print(list_request.text)
    proxy_request_json = json.loads(list_request.text)
    proxy_list = []
    for proxy in proxy_request_json["proxies"]:
        try:
            proxies = { 
                        "https" : proxy["proxy"]
                        }
            url = "https://google.com"
            requests.get(url, headers= {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
                "Accept": "application/vnd.de.zdf.v1.0+json",
                "Accept-Language": "en-US,en;q=0.5",
                "Api-Auth": "Bearer aa3noh4ohz9eeboo8shiesheec9ciequ9Quah7el",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Priority": "u=4"
            }, proxies = proxies
            )
            proxy_list.append(proxy["proxy"])
        except:
            pass
    print(len(proxy_list))
    return proxy_list

def download_starting_from_until(start_date, end_date, proxy_list = None):
    proxies = None
    while start_date < end_date:
        print(start_date)
        try:
            if proxy_list != None:
                random_number = random.randrange(len(proxy_list))
                proxies = { 
                    "https" : proxy_list[random_number]
                    }
            url = download_subtitle_for_date_19h(start_date.day, start_date.month, start_date.year - 2000, proxies=proxies)
            # download_file(url, f"./downloads/19h/{start_date.year-2000}{start_date.month:02d}{start_date.day:02d}.xml",proxies=proxies)
        except:
            print("not found")
        start_date += datetime.timedelta(days=1)

def main():
    # start_date = datetime.datetime(year, month, day)
    #proxy_list = get_proxy_list()
    
    proxy_list = ["http://localhost:8118"]
    proxies = { 
                        "https" : "http://localhost:8118"
                        }
    url = "https://check.torproject.org/api/ip"
    try:
        test = requests.get(url, proxies = proxies)
        response = json.loads(test.text)
        if response["IsTor"]:
            print("Connected to the tor network")
        else:
            exit(1)
    except:
        exit(1)
    start_date = datetime.datetime.now() - datetime.timedelta(days=20)
    end_date = datetime.datetime.now() - datetime.timedelta(days=1)
    download_starting_from_until(start_date, end_date, proxy_list)

    

def download_file(url, path, proxies = None):
    page = requests.get(url, headers= {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/136.0",
                "Accept": "application/vnd.de.zdf.v1.0+json",
                "Accept-Language": "en-US,en;q=0.5",
                "Api-Auth": "Bearer aa3noh4ohz9eeboo8shiesheec9ciequ9Quah7el",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Priority": "u=4"
            }, proxies = proxies)

    with open(path, "w") as output:
        output.write(page.text)


if __name__ == '__main__':
    main()