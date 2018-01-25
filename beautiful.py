import bs4 as bs
import urllib.request
import pandas as pd
import numpy as np
import os
import string
def network_infobox(urls, parent, their_network = False):
    for row in urls:
        for u in row:
            if "http" not in u and "/wiki/" in u:
                url = 'https://en.wikipedia.org' + u
                # print(str(url))
                sauce = urllib.request.urlopen(str(url)).read()
                soup = bs.BeautifulSoup(sauce, 'lxml')
                table = soup.table
                if soup.find('table', class_='infobox vcard') is not None:
                    table = soup.find('table', class_='infobox vcard')
                elif soup.find('table', class_='infobox biography vcard'):
                    table = soup.find('table', class_='infobox biography vcard')
                if table is not None:
                    table_rows = table.find_all('tr')

                    counter = 1
                    data = pd.DataFrame()

                    for tr in table_rows:
                        th = tr.find('th')
                        if th is not None:
                            title = th.text.strip()
                            title = title.replace('\n', ' - ')
                        else:
                            title = ''
                        data.at[counter, 'title'] = title
                        td = tr.find('td')
                        if td is not None:
                            info = td.text.strip()
                            info = info.replace('\n', ' - ')
                        else:
                            info = ''
                        data.at[counter, 'info'] = info
                        if title != '' or info != '':
                            counter += 1
                    counter = 1
                    if their_network is True:
                        table_rows = table.find_all('td')
                        for td in table_rows:
                            links = td.find_all('a', href=True)
                            linked = []
                            for i in links:
                                if links is not None:
                                    linked.append(i['href'])
                            data.at[counter, 'linked'] = linked
                            # linked = link['href']
                            # linked = np.asarray(link)
                            # data.at[counter, 'linked'] = linked
                            counter += 1
                    # print(data)

                    if (len(data['info'])) > 1 and (len(data['title'])) > 1:
                        url = url.replace('https://en.wikipedia.org/wiki/', '')
                        file_name = 'C:/stat420/Baseball_graph/' + parent + '/' + url + '.csv'
                        data.to_csv(file_name)
def infobox_data(url, initial):
    url = 'https://en.wikipedia.org' + url
    # print (url)
    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    table = soup.table
    if soup.find('table', class_='infobox vcard') is not None:
        table = soup.find('table', class_='infobox vcard')
    elif soup.find('table', class_='infobox biography vcard'):
        table = soup.find('table', class_='infobox biography vcard')
    table_rows = table.find_all('tr')

    counter = 1
    data = pd.DataFrame()

    for tr in table_rows:
        th = tr.find('th')
        if th is not None:
            title = th.text.strip()
            title = title.replace('\n', ' - ')
        else:
            title = ''
        data.at[counter, 'title'] = title
        td = tr.find('td')
        if td is not None:
            info = td.text.strip()
            info = info.replace('\n', ' - ')
        else:
            info = ''
        data.at[counter, 'info'] = info
        if title != '' or info != '':
            counter += 1
    counter = 1
    table_rows = table.find_all('td')
        links = td.find_all('a', href=True)
        linked = []
        for i in links:
            if links is not None:
                linked.append(i['href'])
                # print (i['href'])
        data.at[counter, 'linked'] = linked
            # linked = link['href']
            # linked = np.asarray(link)
        # data.at[counter, 'linked'] = linked
        counter += 1

    # counter = 1
    # table_rows = table.find_all('th')
    # for th in table_rows:
    #     links = th.find_all('a', href=True)
    #     linked2 = []
    #     for i in links:
    #         if links is not None:
    #             linked2.append(i['href'])
    #     data.at[counter, 'linked2'] = linked2
    #     # linked = link['href']
    #     # linked = np.asarray(link)
    #     # data.at[counter, 'linked'] = linked
    #     counter += 1
    # print (data)
    #
    linked = data['linked']
    # print (linked)
    url = url.replace('https://en.wikipedia.org/wiki/','')
    if os.path.exists('C:/stat420/Baseball_graph/'+url) is False:
        os.makedirs('C:/stat420/Baseball_graph/'+url)
    file_name = 'C:/stat420/Baseball_graph/'+url+'/'+url+'.csv'
    data.to_csv(file_name)
    return linked, url


infobox_data('/wiki/Donald_Trump', True)
network_links, parent = infobox_data('/wiki/Donald_Trump', True)
network_infobox(network_links, parent)