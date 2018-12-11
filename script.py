from bs4 import BeautifulSoup
from requests import get
import csv

rowsData = []

ufo_home_page = 'http://www.nuforc.org/webreports/ndxevent.html'

response = get(ufo_home_page)

if response.status_code == 200:
    parsedPage = BeautifulSoup(response.text, 'html.parser')

    date_links = parsedPage.findAll('a')

    for link in date_links:

        date = link.text.strip()
        month = date[:2]
        year = date[-4:]

        response = get('http://www.nuforc.org/webreports/ndxe' + year + month + '.html')

        if response.status_code == 200:
            page_html = BeautifulSoup(response.text, 'html.parser')
            table = page_html.find('table')

            headers = [header.text.strip() for header in table.findAll('th')]

            rows = []
            print rows

            for row in table.find_all('tr'):
                for a in row.findAll('a', href=True):
                    event_link = a['href']
                    response = get('http://www.nuforc.org/webreports/' + event_link)
                    if response.status_code == 200:    
                        parsedEventPage = BeautifulSoup(response.text, 'html.parser')
                        td = parsedEventPage.findAll('td')

                        infos = []
                        summaries = []

                        for single_td in td:
                            if single_td.text.startswith("Occurred"):
                                info = single_td.text.strip()
                                infos.append(info)
                            else:
                                summary = single_td.text.strip()
                                summaries.append(summary)

                        info_summaries = infos + summaries
                        combined_data = (list(info_summaries))

                        with open('missing_summaries.csv', 'a') as file:
                                writer = csv.writer(file)
                                writer.writerow(info_summaries)
                                # writer.writerows(info for info in infos if info)
                                # writer.writerows(summary for summary in summaries if summary)

                rows.append([val.text.encode('utf8') for val in row.find_all('td')])

            # with open('UFO_sightings.csv', 'a') as file:
            #     writer = csv.writer(file)
            #     writer.writerow(headers)
            #     writer.writerows(row for row in rows if row)


