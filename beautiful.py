import bs4 as bs
import urllib.request
import pandas as pd
import os
import wikipedia

def network_infobox(urls, parent, their_network = False):

    if their_network is True:
        all_links = []
        all_network = pd.DataFrame()

    #Scrape every url fed into function
    for u in urls:
        if "http" not in u and "/wiki/" in u:

            #Create URL to scrape
            url = 'https://en.wikipedia.org' + u
            # print(str(url))
            sauce = urllib.request.urlopen(str(url)).read()
            soup = bs.BeautifulSoup(sauce, 'lxml')
            table = soup.table

            #Narrow down to URL
            if soup.find('table', class_='infobox vcard') is not None:
                table = soup.find('table', class_='infobox vcard')
            elif soup.find('table', class_='infobox biography vcard'):
                table = soup.find('table', class_='infobox biography vcard')
            if table is not None:
                table_rows = table.find_all('tr')

                counter = 1
                data = pd.DataFrame()

                #Scrape Title and Info
                for tr in table_rows:

                    #Scrape Title
                    th = tr.find('th')
                    if th is not None:
                        title = th.text.strip()
                        title = title.replace('\n', ' - ')
                    else:
                        title = ''
                    data.at[counter, 'title'] = title

                    #Scrape Info
                    td = tr.find('td')
                    if td is not None:
                        info = td.text.strip()
                        info = info.replace('\n', ' - ')
                    else:
                        info = ''
                    data.at[counter, 'info'] = info
                    if title != '' and info != '':
                        counter += 1

                url = url.replace('https://en.wikipedia.org/wiki/', '')
                url = url.replace('/', '-')


                #Scrape everyone's network and write to CSV if True
                if their_network is True:

                    #Scrape all links in infocard
                    links = table.find_all('a', href=True)
                    linked = []
                    for i in links:
                        if links is not None:
                            linked.append(i['href'])
                            all_links.append(i['href'])
                    network = pd.DataFrame()
                    network['links'] = linked
                    # backlinks = 0
                    # for l in len(linked):
                    #     if ('/wiki/' + parent) in page:
                    #         backlinks += 1
                    #         l += 1
                    # network['backlinks'] = backlinks
                    # print(network)
                    file_name2 = 'C:/stat420/Baseball_graph/' + parent + '/' + url + '_network.csv'
                    network.to_csv(file_name2)

                #If info or title aren't empty, write to CSV
                if (len(data['info'])) > 1 or (len(data['title'])) > 1:
                    file_name = 'C:/stat420/Baseball_graph/' + parent + '/' + url + '.csv'
                    data.to_csv(file_name)

    #Write all network connections to CSV and return
    if their_network is True:
        all_network['links'] = all_links
        network_file = 'C:/stat420/Baseball_graph/' + parent + '/full_network.csv'
        all_network.to_csv(network_file)
        return all_links

def infobox_data(search, initial):
    page = wikipedia.page(search)
    page_content = page.content
    #Create URL to scrape
    url = page.url
    # url = 'https://en.wikipedia.org' + url
    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    table = soup.table

    #Narrow down to infobox
    if soup.find('table', class_='infobox vcard') is not None:
        table = soup.find('table', class_='infobox vcard')
    elif soup.find('table', class_='infobox biography vcard'):
        table = soup.find('table', class_='infobox biography vcard')
    table_rows = table.find_all('tr')

    counter = 1
    data = pd.DataFrame()

    #Get Title and Info
    for tr in table_rows:

        #Get Title
        th = tr.find('th')
        if th is not None:
            title = th.text.strip()
            title = title.replace('\n', ' - ')
        else:
            title = ''
        data.at[counter, 'title'] = title
        td = tr.find('td')

        #Get Info
        if td is not None:
            info = td.text.strip()
            info = info.replace('\n', ' - ')
        else:
            info = ''
        data.at[counter, 'info'] = info
        if title != '' and info != '':
            counter += 1

    #Get all links in the infocard
    links = table.find_all('a', href=True)
    linked = []
    for i in links:
        if links is not None:
            linked.append(i['href'])
    network = pd.DataFrame()
    network['links'] = linked

    #Write Title and Info to CSV & Write Network to CSV
    url = url.replace('https://en.wikipedia.org/wiki/','')
    if os.path.exists('C:/stat420/Baseball_graph/'+url) is False:
        os.makedirs('C:/stat420/Baseball_graph/'+url)
    file_name = 'C:/stat420/Baseball_graph/'+url+'/'+url+'.csv'
    file_name2 = 'C:/stat420/Baseball_graph/'+url+'/'+url+'_network.csv'
    data.to_csv(file_name)
    network.to_csv(file_name2)
    return linked, url

network_links, parent = infobox_data('/wiki/Nikola_Tesla', True)
network_infobox(network_links, parent, True)
# network_infobox(all_networks, parent, False)
