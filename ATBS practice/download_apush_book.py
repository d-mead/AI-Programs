import webbrowser
# import requests
# #webbrowser.open('http://inventwithpython.com/')
#
# res = requests.get('http://www.teachinginsanity.net/APUSH/Unit%2001/Henretta%20Chapter%202.pdf')
# print(type(res))
# res.raise_for_status()
# file = open('APUSH2.txt', 'wb')
# for chunk in res.iter_content(100000):
#     file.write(chunk)
# file.close()

import urllib2

def main():
    download_file("http://bcs.bedfordstmartins.com/webpub/Ektron/Henretta_Americas%20History_7e/ch_outline_html/Henretta%207%20OSG%20Ch%201%20Chapter%20Outline_Final.htm")

def download_file(download_url):
    response = urllib2.urlopen(download_url)
    file = open("chapter1.txt", 'w')
    file.write(response.read())
    file.close()
    print("Completed")

if __name__ == "__main__":
    main()