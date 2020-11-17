from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, SoupStrainer
from urllib.error import HTTPError
import datetime
from calendar import monthrange


postal_code = "L2M" + "%20" + "0A1"
baseurl = "https://www.almanac.com/weather/history/postalcode/"+ postal_code + "/"

def find_warmest_day(startYear, startMonth, startDay, endYear, endMonth, endDay):
    warmest_day_temp = -1000
    warmest_year=0
    warmest_month=0
    warmest_day=0
    for year in range(startYear, endYear+1):
        # if year == end year good
        # if not, then we need to go all 12 months
        for month in range(startMonth, endMonth+1):
            # if month = end year good
            # if not, then we need to find days in month and loop through that
            for day in range(startDay, endDay+1):
                day+=1
                url = baseurl + str(year) + "-" + str(month) + "-" + str(day)
                req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
                try:
                    page = urlopen(req).read()
                except HTTPError:
                    print ("You requested too many items in a short timeframe, please wait.")
                    break
                else:
                    only_tr = SoupStrainer("tr", "weatherhistory_results_datavalue temp_mx")
                    soup = BeautifulSoup(page, parse_only=only_tr, features="lxml")
                    dataSection = soup.find_all("tr", "weatherhistory_results_datavalue temp_mx")
                    for section in dataSection:
                        print (section.find("th").text + " " + section.find("td").text)
                        temp = float(section.find("span", "value").text)
                        if (section.find("span", "units").text.find("F") == 1):
                            temp = (temp-32)*5/9
                        if (temp>warmest_day_temp):
                            warmest_day_temp = temp
                            warmest_day = day
                            warmest_month = month
                            warmest_year = year
                            print(temp)
    
    d = datetime.datetime.strptime(str(warmest_year) + '-' + str(warmest_month) + '-' + str(warmest_day), '%Y-%m-%d')
    print("the warmest day was " + d.strftime('%b %d, %Y'))


find_warmest_day(2020, 11, 1, 2020, 11, 15)

#dataSections = soup.findAll("tr","weatherhistory_results_datavalue")
#for section in dataSections:
    #print (section.find("th").text)
    #print (section.find("td").text)

