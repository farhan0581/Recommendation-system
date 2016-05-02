""".."""
# sudo apt-get -y install python-setuptools python-dev python-pip
# pip install beautifulsoup4

import urllib
import json
from bs4 import BeautifulSoup as Bs
import re
import pprint

# parsing the content of last.fm html to get the name of song and artist
def parse_html(soup):
    """.."""
    result = []
    s = soup.findAll("section", attrs={"id": "top-tracks-section"})[0].findAll('tbody')[0].findAll("tr")
    for tr in s:
        try:
            # t = tr.findAll('a', attrs={"class": "link-block-target"})[0].get('title')
            # result.append(t.replace(u'\u2014', " "))
            singer = tr.find('span',{'class':'chartlist-artists'}).getText()
            album = tr.find('a',{'class':'link-block-target'}).getText()
            singer = singer.encode("ascii","ignore").strip()
            album = album.encode("ascii","ignore").strip()
            album_number = tr.find('td',{'class':'chartlist-index'}).getText().strip()
            result.append([singer,album,album_number])
        except:
            pass
    return result

# to get track name list from last.fm
def get_track_name():
    """."""
    result = []
    url = "http://www.last.fm/tag/happy/tracks?page={0}"
    # change the value in xrange to get more pages for eg 1-2 or 1-10 accordingly
    # first test with small value
    for i in xrange(1, 2):
        temp_url = url.format(str(i))
        try:
            r = urllib.urlopen(temp_url)
            html = r.read()
            soup = Bs(html)
            result = result + parse_html(soup)
            # print parse_html(soup)
        except:
            pass
    return result

# to download and get the track
def check_for_track(lis,artist,song,album_number):
    flag = 0
    for i in range(len(lis)):
        if (artist.lower() == lis[i]['artist'].lower() and
            song.lower() == lis[i]['trackName'].lower()):
            print lis[0]['artist'].lower()
            print lis[i]['trackName'].lower()
            download_url = lis[i]['previewUrl']
            print download_url
            filename = str(album_number) + '__' + str(artist) + '_' + str(song) + '.mp3'
            urllib.urlretrieve(download_url,filename=filename)
            flag = 1
            break
    if flag == 0:
        print ('cannot download for ' + str(album_number) + '__' +
         str(artist) + '_' + str(song)  + ' might be some issue...')

        
    # print artist,song


# to search the shazam and get the json data from its api
def main():
    """.."""
    count = 0
    track_list = get_track_name()
    print track_list
    url = "http://www.shazam.com/fragment/search/{0}?size=large"
    for track in track_list:
        count = count + 1
        try:
            r = urllib.urlopen(url.format(urllib.quote(track[1] + '-' + track[0])))
            data = json.loads(r.read())
            # pprint.pprint(data)
            
            # print (data['tracksresult']['tracks'][0].get('previewUrl'))
            check_for_track(data['tracksresult']['tracks'],track[0],track[1],track[2])
            # urllib.urlretrieve((data['tracksresult']['tracks'][0].get('previewUrl')),
                        # filename=filename)
        except Exception as e:
            print(e)
        break


if __name__ == '__main__':
    main()