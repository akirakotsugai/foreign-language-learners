from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from iso3166 import countries
import operator
import matplotlib.pyplot as plt
import numpy as np

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False



print("Loading...\n")

counter = 0;
flag = True
flag2 = True
url = "https://www.interpals.net/app/online?order=modified&age1=13&age2=110&dir=desc&offset="
users = []
scrappedcountries = []
ages = []
onlyages = []

while(flag):

    req = Request(url+str(counter), headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req)
    bsObj = BeautifulSoup(html,"lxml")
    online = int(bsObj.find("div",{"class":"boxText"}).findChildren()[1].getText())

    userdetails = bsObj.findAll("div",{"class":"olUserDetails"})

    for info in userdetails:
        person_and_country = info.findAll("span",{"class":"nobreak"})
        person = person_and_country[0].getText().split(" ")

        if len(person) == 2:
            if RepresentsInt(person[1]):
                age = int(person[1])

        country = person_and_country[1].findChildren()[0]['href'][-2::]

        contain = False
        for pais in scrappedcountries:
            if country in pais:
                contain = True
                pais[1].append(age)
                break

        if contain == False:
            c = [country,[]]
            c[1].append(age)
            scrappedcountries.append(c)

        ages.append([age,country])
        onlyages.append(age)


    
    if flag2 == False:
        flag = False
    if counter + 60 >= online:
        counter = counter + (online-counter)-1
        flag2 = False
    else:
        counter += 60


for country in scrappedcountries:
    country[1].sort()
    country.append(len(country[1]))

scrappedcountries = sorted(scrappedcountries, key = operator.itemgetter(2), reverse = True)
ages = sorted(ages, key = operator.itemgetter(0), reverse = True)

topcountriestoplot = []
topaccessestoplot = []
bottomcountriestoplot = []
bottomaccessestoplot = []


topagestoplot = []
topcountriesbyagetoplot = []
bottomagestoplot = []
bottomcountriesbyagetoplot = []

index = 0
while index < 30:
    topcountriestoplot.append(scrappedcountries[index][0])
    topaccessestoplot.append(scrappedcountries[index][2])
    if index < 15:
        topagestoplot.append(ages[index][0])
        topcountriesbyagetoplot.append(ages[index][1])
    index += 1

index = -30
while index < 0:
    bottomcountriestoplot.append(scrappedcountries[index][0])
    bottomaccessestoplot.append(scrappedcountries[index][2])
    if index < -15:
        bottomagestoplot.append(ages[index][0])
        bottomcountriesbyagetoplot.append(ages[index][1])
    index += 1

topagestoplot.append(0)
topcountriesbyagetoplot.append("...")

agestoplot = topagestoplot+bottomagestoplot
countriesbyagetoplot = topcountriesbyagetoplot+bottomcountriesbyagetoplot




rodar = True
while rodar:
    print("Which graphic would you like to take a look at?")
    print("1 - Countries that have the most online users")
    print("2 - Countries that have the fewest online users")
    print("3 - Oldest and youngest online users")
    print("4 - Online users' ages")
    option = int(input(""))
    if option == 1:
        y_pos = np.arange(len(topaccessestoplot))
        guide = ""
        for country in topcountriestoplot:
            guide += country + " - " + countries.get(country).name+"\n"

        plt.bar(y_pos, topaccessestoplot, align = 'center')
        plt.xticks(y_pos, topcountriestoplot)
        plt.figtext(.6, .2, guide)
        plt.ylabel('number of online people')   
        plt.show()

    elif option == 2:
        comparisoncountriestoplot = []
        comparisonaccessestoplot = []
        fewesttotal = 0
        guide = "30 countries with the fewest online users:\n"
        for access in bottomaccessestoplot:
            fewesttotal += access
        for country in bottomcountriestoplot:
            guide += countries.get(country).name+"\n"
            
        comparisoncountriestoplot.append(scrappedcountries[0][0])
        comparisoncountriestoplot.append("other countries")
        comparisoncountriestoplot.append("30 countries with the fewest online users")

        comparisonaccessestoplot.append(len(scrappedcountries[0][1]))
        comparisonaccessestoplot.append(len(onlyages)-fewesttotal-len(scrappedcountries[0][1]))
        comparisonaccessestoplot.append(fewesttotal)
        plt.axis("equal")
        plt.pie(comparisonaccessestoplot, labels = comparisoncountriestoplot)
        plt.figtext(.1, .3, guide)
        plt.title("Countries that have the fewest online users")
        plt.show()   
        
    elif option == 3:
        y_pos = np.arange(len(agestoplot))
        guide = ""
        norepetition = []
        for country in countriesbyagetoplot:
            if country not in norepetition:
                norepetition.append(country)

        for country in norepetition:
            if country != "...":
                guide += country + " - " + countries.get(country).name+"\n"
        plt.bar(y_pos, agestoplot, align = 'center')
        plt.xticks(y_pos, countriesbyagetoplot)
        plt.figtext(.6, .4, guide)
        plt.ylabel('''online users' ages''')
        plt.title('Contrast between the oldest and youngest 15 online users')
        plt.show()

    elif option == 4:
        bins = [0,10,20,30,40,50,60,70,80,90,100,110]
        plt.hist(onlyages, bins, histtype='bar')
        plt.ylabel("""Online users' quantities""")
        plt.xlabel("Online users' ages in tens")
        plt.title("How many people are aged in determined group of ten")
        plt.show()
    
    
