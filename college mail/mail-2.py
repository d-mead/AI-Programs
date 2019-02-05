#!/usr/bin/env python
#
# Very basic example of using Python 3 and IMAP to iterate over emails in a
# gmail folder/label.  This code is released into the public domain.
#
# This script is example code from this blog post:
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#
# This is an updated version of the original -- modified to work with Python 3.4.
#
import sys
import imaplib
import getpass
import email
import email.header
import datetime

import urllib
import urllib.request
import urllib3
import simplejson as json

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import csv
import numpy as np
import networkx as nx

import pickle

import xlsxwriter

DOMAIN = 'http://api.geonames.org/'
USERNAME = 'davidmead'  # enter your geonames username here

EMAIL_ACCOUNT = "dogsindoggles@gmail.com"  # ""davidmead1219@gmail.com"

# Use 'INBOX' to read inbox.  Note that whatever folder is specified,
# after successfully running this script all emails in that folder
# will be marked as read.
EMAIL_FOLDER = "Inbox"


def main():
    global colleges
    http = urllib3.PoolManager()

    M = imaplib.IMAP4_SSL('imap.gmail.com')

    # print(get_lng_lat_state("university of notre dame"))

    M = imaplib.IMAP4_SSL('mail.vamead.net')

    try:
        rv, data = M.login(EMAIL_ACCOUNT, getpass.getpass())
    except imaplib.IMAP4.error:
        print("LOGIN FAILED!!! ")
        sys.exit(1)

    print(rv, data)

    rv, mailboxes = M.list()
    if rv == 'OK':
        print("Mailboxes:")
        print(mailboxes)

    rv, data = M.select(EMAIL_FOLDER)
    if rv == 'OK':
        print("Processing mailbox...\n")
        process_mailbox(M)
        M.close()
    else:
        print("ERROR: Unable to open mailbox ", rv)

    colleges = ['connecticut college', 'babson college', 'college of charleston admissions', 'case western reserve university', 'college board', 'university of notre dame', 'university of portland', 'radford university', 'university of central florida']#'university of lynchburg', 'clemson university office of undergraduate admissions', 'hampshire college', 'clemson university office of undergraduate admissions', 'hampden-sydney college', "bard college at simon's rock", 'hampshire college', 'missouri university of science and technology', 'worcester polytechnic institute', 'university of maryland admissions', 'adelphi university', 'worcester polytechnic institute', 'university of tampa', 'university of tennessee', 'bridgewater college', 'creighton university', 'university of north carolina at pembroke']

    draw()

    # M.logout()


def fetchJson(method, params):
    uri = DOMAIN + '%s?%s&username=%s' % (method, urllib.parse.urlencode(params), USERNAME)
    resource = urllib.request.urlopen(uri).readlines()
    # resource = http.request('GET', uri).readlines()
    js = json.loads(resource[0])
    return js


def search(**kwargs):
    method = 'searchJSON'
    valid_kwargs = ('q', 'name', 'name_equals', 'name_startsWith', 'maxRows', 'startRow', 'country', 'countryBias', 'continentCode', 'adminCode1', 'adminCode2', 'adminCode3', 'featureClass', 'featureCode', 'lang', 'type', 'style', 'isNameRequired', 'tag', 'operator', 'charset',)
    params = {}
    for key in kwargs:
        if key in valid_kwargs:
            params[key] = kwargs[key]
    results = fetchJson(method, params)

    if('geonames' in results):
        return results['geonames']
    else:
        return None


def get_lng_lat_state(name):
    query = search(name=name)
    if len(query) > 0:
        info = query[0]
        return float(info.get("lng")), float(info.get("lat")), info.get('adminName1')
    return None


def process_mailbox(M):
    global colleges
    """
    Do something with emails messages in the folder.
    For the sake of this example, print some headers.
    """

    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    colleges = []

    start = 4300
    end = 11370

    count = 1

    badlist = ["college board", "mycollegeoptions"]

    for num in data[0].split()[start:end]:
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])

        # print(msg['Subject'])
        sender = msg['From']
        if sender:
            hdr = email.header.make_header(email.header.decode_header(sender))
            h = str(hdr).lower()
            if " " in h:
                if "<" in h:
                    h = h[:h.index("<")]
            h = h.replace("\"", "")
            h = h.rstrip()
            h = h.replace("the ", "")
            if "college" in h or "university" in h or "institute" in h:
                colleges.append(h)

        else:
            h = ""

        # if "@" not in h:
        #     print(h)
        print(msg['Date'])
        print("Reading Emails: %s/%s" % (count, end - start))
        count += 1

    print(colleges)


def process_colleges(colleges):

    workbook = xlsxwriter.Workbook(str(datetime.datetime.now()) + '.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "college")
    worksheet.write(0, 1, "lat")
    worksheet.write(0, 2, "long")
    worksheet.write(0, 3, "state")

    coord_list = []

    print("Making Coordinates")

    for i, college in enumerate(colleges):
        coord = get_lng_lat_state(college)
        if coord:
            long, lat, state = coord
            coord_list.append((long, lat))
            worksheet.write(i+1, 0, college)
            worksheet.write(i+1, 1, lat)
            worksheet.write(i+1, 2, long)
            worksheet.write(i+1, 3, state)
        print("Creating Coordinates: %s/%s" % (i+1, len(colleges)))

    workbook.close()

    return coord_list


def draw():
    global colleges

    nodes = process_colleges(colleges)

    print("Setting Up Map")

    plt.figure(figsize=(7, 7))
    # set up orthographic map projection with
    # perspective of satellite looking down at 50N, 100W.
    # use low resolution coastlines.

    # map = Basemap(projection='merc', llcrnrlon = -133, llcrnrlat= 14, urcrnrlon=-57, urcrnrlat= 62, resolution='l')
    # map = Basemap(projection='stere', llcrnrlon=-133, llcrnrlat=14, urcrnrlon=-57, urcrnrlat=62, lon_0 = 96, lat_0 = -38, resolution='l')
    map = Basemap(projection='lcc', resolution='l', width=5E6, height=5E6, lat_0=38, lon_0=-96)
    # map = Basemap(projection='ortho', lat_0=45, lon_0=-100, resolution='l')

    node_color = "limegreen"  # "#F8FF9C"

    map.drawcoastlines(linewidth=0.25, color="black")
    map.drawcountries(linewidth=0.25, color="black")
    map.drawstates(linewidth=0.15, color="black")
    # map.fillcontinents(color='#08001d', lake_color='#010211')
    # map.fillcontinents(color='lightgrey', lake_color='lightblue')
    # map.drawmapboundary(fill_color="lightblue") ##85C1E9

    map.bluemarble()

    # map.shadedrelief()

    # position in decimal lat/lon

    ids = list()
    lats = list()
    lons = list()

    count = 0

    a = plt.subplot(111)

    print("Adding Nodes")

    for lon, lat in nodes:
        lats.append(lat)
        lons.append(lon)
        count += 1
        print("Processing Nodes: %s/%s" % (count, len(nodes)))

    # lats = [37.96, 42.82]
    # lons = [-121.29, -73.95]
    # convert lat and lon to map projection
    mx, my = map(lons, lats)

    # The NetworkX part
    # put map projection coordinates in pos dictionary
    G = nx.DiGraph(dircted=False)

    print(G.nodes)


    count = 0

    # nx.draw_networkx(G, pos, with_labels=False, node_size=.25, node_color='#F8FF9C', alpha=.1, edge_color='lime',
    #                  arrowsize=0.01, edgelist={})
    # nx.draw_networkx(G, pos, with_labels=False, node_size=.001, node_color='#F8FF9C', alpha=.9, edge_color='lime',
    #                  arrowsize=0.01, width=.4)

    plt.title('railroads')
    # plt.draw()
    # plt.pause(.1)

    mx, my = map(lons, lats)

    pos = {}

    count = 0
    for node in nodes:
        G.add_node(node)
        pos[node] = (mx[count], my[count])
        count += 1
        print("Adding Nodes: %s/%s" % (count, len(nodes)))

    print("Displaying")

    nx.draw_networkx_nodes(G, pos, with_labels=False, node_size=.5, node_color=node_color, alpha=.85)

    print("Saving to File")

    with open("college_coords.pkl", "wb") as outfile:
        pickle.dump(G, outfile)

    plt.show()


def draw_file():



    for lon, lat in nodes:
        lats.append(lat)
        lons.append(lon)
        count += 1
        print("Processing Nodes: %s/%s" % (count, len(nodes)))

    mx, my = map(lons, lats)

    G = nx.DiGraph(dircted=False)

    print(G.nodes)

    mx, my = map(lons, lats)

    pos = {}

    count = 0
    for node in nodes:
        G.add_node(node)
        pos[node] = (mx[count], my[count])
        count += 1
        print("Adding Nodes: %s/%s" % (count, len(nodes)))

    print("Displaying")

    nx.draw_networkx_nodes(G, pos, with_labels=False, node_size=.5, node_color=node_color, alpha=.85)

    print("Saving to File")

    with open("college_coords.pkl", "wb") as outfile:
        pickle.dump(G, outfile)

    plt.show()


if __name__ == "__main__":
    # main func!
    main()

