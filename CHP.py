'''
    Chrome History Parser
    By: sk3tchymoos3
        - extracts the downloads, visitedURLs, and keyword searches found in History file of Chrome
    Usage: python CHP.py -f <path to History File>
        - Tested in Windows and Linux
'''
import sqlite3 as lite
import csv, os, argparse, sys


parser = argparse.ArgumentParser(description="Chrome History Parser")
parser.add_argument("-f", required=True, dest="DB", help="Path to the History File", metavar="HISTORY_FILE")

#Let's ensure some stuff is in place first before we go further
try:
    args = parser.parse_args()
except:
    print "Please specify the path to the History file"
    sys.exit(1)

DB_path=args.DB

try:
    con = lite.connect(DB_path)
except:
    print "Incorrect path!"
    sys.exit(1)

cwd = os.getcwd()

#All good? Let's kick it (root down)

with con:
    cur = con.cursor()
    #First, we get all the downloads
    cur.execute("SELECT current_path,datetime(((start_time/1000000)-11644473600),'unixepoch'),referrer FROM downloads")
    rows = cur.fetchall()
    
    downloadsPath= cwd + "/downloads.csv"
    f = open(downloadsPath,'w')
    writer= csv.writer(f)
    writer.writerow(('Current Path','Downloading Time (local)','Referrer'))
    
    
    for row in rows:
        writer.writerow((row[0],row[1],row[2]))
    f.close()

    #Lets grab the URLs tool
    cur.execute("SELECT url,id,datetime(((last_visit_time/1000000)-11644473600),'unixepoch'),visit_count FROM urls")
    rows = cur.fetchall()

    visitedURLsPath= cwd + "/visitedURLs.csv"
    f = open(visitedURLsPath,'w')
    writer= csv.writer(f)
    writer.writerow(('URL','urlID','Last Visited Time (local)','Visit Count'))
    
    for row in rows:
        writer.writerow((row[0],row[1],row[2],row[3]))
    f.close()

    #Lets grab the search terms
    cur.execute("SELECT url_id,term FROM keyword_search_terms")
    rows = cur.fetchall()
    
    keywordSearchesPath= cwd + "/keywordSearches.csv"
    f = open(keywordSearchesPath,'w')
    writer= csv.writer(f)
    writer.writerow(('URL_ID','Search Term'))
    
    for row in rows:
        writer.writerow((row[0],row[1]))
    f.close()


