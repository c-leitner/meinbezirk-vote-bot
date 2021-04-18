import requests
import lxml
from bs4 import BeautifulSoup as BS
import time
import random
import timeit
from csv import reader
import sys
 
# number of votes being casted 
votes = 100

# number represents the vote option
voting_option =  "0"

# add the from id can be found in the source of page for Example "<div data-participation-event="1">"
form_id = "1"


URL = "https://www.meinbezirk.at/p/ajax/participationevent/interaction/"+form_id
URL1 = "https://www.meinbezirk.at/p/ajax/participationevent/form/participate/"+ form_id +"?finalSubmit=0"

print("Voting ", votes, " time(s)  @ ", URL)

c_voter = 0
x = 0
while c_voter < votes:
    # list of proxy servers to use for voting (nordvpn is used in file provided, credentials are mandatory)
    with open('socks5.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            if c_voter == votes:
                break
            s = requests.Session()
            try:
                print("Trying server: ",row[0],", Try Nr.: ",(x+1))
                x = x+1
                # add your credentials for proxies
                proxies = {'https': "socks5://username:password@"+row[0]+":1080"}
                r =s.get(url = URL,proxies=proxies,timeout=5)
            except Exception:
                print("trying next server\n")
                s.close()
                continue
            start = timeit.default_timer()
            print("PHPSESSID="+s.cookies.get('PHPSESSID'))
            #get text from inital respons
            respons = r.text
            soup = BS(respons,features="lxml")
            #find tag with participation id
            tag_id= "participation_participate_"+ form_id +"__token"
            tag = soup.find(id=tag_id)
            #Get participation id
            value = tag.attrs.get('value')

            payload = "participation_participate_"+form_id+"%5Binteraction_data%5D%5Bpoll_selection%5D="+voting_option+"&participation_participate_"+form_id+"%5B_token%5D="+value

            cookie = "PHPSESSID="+s.cookies.get('PHPSESSID')
            post1 = s.post(URL, data = payload, headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Cookie":cookie},proxies=proxies)
            post2 = s.post(URL1, data = payload, headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","TE": "Trailers","Cookie":cookie},proxies=proxies)
            #print(post2.text)
            if post2.text == "{}" and post2.status_code == 200 and post1.status_code == 200:
                c_voter = c_voter + 1
                print("Successfully voted " + str(c_voter) + " time(s)")

            #send get request after voting
            r1 =s.get(url = URL,proxies=proxies)
            #close connection
            s.close()

            #get finishing time
            stop = timeit.default_timer()

            #print overall time for voting
            print('Vote duration: ', round((stop - start),2), " seconds") 

            #generate rand nr to wait for next vote
            #next_vote = random.uniform(5, 10)
            next_vote = 0
            print('Next vote in: ', round(next_vote,2), " seconds", '\n')
            time.sleep(next_vote)