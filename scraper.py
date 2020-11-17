from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, SoupStrainer
from urllib.error import HTTPError
import datetime
from calendar import monthrange


postal_code = "L2M" + "%20" + "0A1"
baseurl = "https://www.almanac.com/weather/history/postalcode/"+ postal_code + "/"
warmest_day_temp = -1000
warmest_year=0
warmest_month=0
warmest_day=0
function = 0



def find_max_temp(year, month, day, page):
    only_tr_max = SoupStrainer("tr", "weatherhistory_results_datavalue temp_mx")
    soup = BeautifulSoup(page, parse_only=only_tr_max, features="lxml")
    dataSection = soup.find_all("tr", "weatherhistory_results_datavalue temp_mx")
    for section in dataSection:
        #print (section.find("th").text + " " + section.find("td").text)
        temp = float(section.find("span", "value").text)
        if (section.find("span", "units").text.find("F") == 1):
            temp = (temp-32)*5/9
        d = datetime.datetime.strptime(str(year) + '-' + str(month) + '-' + str(day), '%Y-%m-%d')
        print (d.strftime('%b %d, %Y') + ": " + str(temp))
        return temp

def find_warmest_day(year, month, day, page):
    temp = find_max_temp(year, month, day, page)
    global warmest_day_temp
    global warmest_day
    global warmest_month
    global warmest_year
    print(warmest_day_temp) 
    if (temp>warmest_day_temp):
        warmest_day_temp = temp
        warmest_day = day
        warmest_month = month
        warmest_year = year

def loopDays(year, month, startDay, endDay):
    for day in range(startDay, endDay):
        try:
            url = baseurl + str(year) + "-" + str(month) + "-" + str(day)
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            page = urlopen(req).read()
        except HTTPError:
            print ("You requested too many items in a short timeframe, please wait.")
        else:
            if (function==1):
                find_warmest_day(year, month, day, page)
            
                    
                        
                        
      

def loopMonths(year, startMonth, startDay, endMonth, endDay):
    for month in range(startMonth, endMonth+1):
        # if month == end month good
        if (month==endMonth):
            # if month == start month good
            if (month==startMonth):
                loopDays(year, month, startDay, endDay)
            # if not, then find number of days in month and loop to that
            else:
                loopDays(year, month, 1, endDay)
        # if not, then we need to find days in month and loop through that
        else:
            if (month==startMonth):
                loopDays(year, month, startDay, monthrange(year,month)[1])
            else:
                loopDays(year, month, 1, monthrange(year,month)[1])


def loopYears(startYear, startMonth, startDay, endYear, endMonth, endDay):


    tempStartMonth=startMonth
    tempStartDay=startDay
    tempEndMonth=endMonth
    tempEndDay=endDay

    for year in range(startYear, endYear+1):
        # if year == end year good
        if (year==endYear):
            # if year == start year good
            if (year==startYear):
                loopMonths(year, startMonth, startDay, endMonth, endDay)
            # if in the starting year, start at starting month
            else:
                loopMonths(year, 1, startDay, endMonth, endDay)
        # if not, then we need to go all 12 months
        else:
            if (year==startYear):
                loopMonths(year, startMonth, startDay, 12, endDay)
            else:
                loopMonths(year, 1, startDay, 12, endDay)



    

function = 1
loopYears(2020, 10, 28, 2020, 11, 16)
d = datetime.datetime.strptime(str(warmest_year) + '-' + str(warmest_month) + '-' + str(warmest_day), '%Y-%m-%d')
print("the warmest day was " + d.strftime('%b %d, %Y') + " with a temperature of " + str(warmest_day_temp) + "°C")

#dataSections = soup.findAll("tr","weatherhistory_results_datavalue")
#for section in dataSections:
    #print (section.find("th").text)
    #print (section.find("td").text)

