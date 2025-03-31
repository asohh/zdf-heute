import json
import re
import requests

def get_subtitle_for_date(day, month, year):
    months = ["januar", "februar", "maerz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember"]



    

    print(f'https://www.zdf.de/nachrichten/heute-journal/heute-journal-vom-{day:02d}-{months[month-1]}-20{year}-100.html')
    heute_seite_html = requests.get(f'https://www.zdf.de/nachrichten/heute-journal/heute-journal-vom-{day:02d}-{months[month-1]}-20{year}-100.html', headers= {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/136.0",
                "Accept": "application/vnd.de.zdf.v1.0+json",
                "Accept-Language": "en-US,en;q=0.5",
                "Api-Auth": "Bearer aa3noh4ohz9eeboo8shiesheec9ciequ9Quah7el",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Priority": "u=4"
            })
    print(heute_seite_html)
    regex_string = f"{year}-{month:02d}-{day:02d}T[0-2][0-9]:[0-5][0-9]"
    print(regex_string)
    date_string_list = re.findall(regex_string, heute_seite_html.text)
    air_time = date_string_list[0].split("T")[1]
    print(air_time)
    date_api_string = f"{year}{month:02d}{day:02d}_{air_time.replace(":","")}"
    print(date_api_string)
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

def main():
    day = 27
    month = 8
    year = 24
    get_subtitle_for_date(day, month, year)

if __name__ == '__main__':
    main()
