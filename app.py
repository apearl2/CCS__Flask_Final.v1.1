#Imports----------------------------------------------------------------------------------------------------------------
from flask import Flask, render_template, request

import requests
from bs4 import BeautifulSoup

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

#Global Variables-------------------------------------------------------------------------------------------------------
newrankList = []
finalList = []
finalListCollegesOnlyP = []
finalListCollegesOnlyC = []
reportfinalListP = []
reportfinalListC = []
customList = []

aImportance = 0
numPcalls = 0
numCcalls = 0

baseList = [25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
baseList2 = [25, 24.5, 24, 23.5, 23, 22.5, 22, 21.5, 21, 20.5, 20, 19.5, 19, 18.5, 18, 17.5, 17, 16.5, 16, 15.5, 15, 14.5, 14, 13.5, 13, 12.5, 12, 11.5, 11, 10.5, 10, 9.5, 9, 8.5, 8, 7.5, 7, 6.5, 6, 5.5, 5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1]

inputStr = ''

#Regular Functions------------------------------------------------------------------------------------------------------
#Creates final list with all schools and all points (no averages yet, must be used after every CF or P Call)
def listA(order, funkName):
    #Global Variables
    global finalList
    global newrankList
    global baseList
    global finalListCollegesOnlyP
    global finalListCollegesOnlyC
    global baseList2
    ###global finalConversionList

    #Reset baseList
    baseList = [25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    baseList2 = [25, 24.5, 24, 23.5, 23, 22.5, 22, 21.5, 21, 20.5, 20, 19.5, 19, 18.5, 18, 17.5, 17, 16.5, 16, 15.5, 15,
                 14.5, 14, 13.5, 13, 12.5, 12, 11.5, 11, 10.5, 10, 9.5, 9, 8.5, 8, 7.5, 7, 6.5, 6, 5.5, 5, 4.5, 4, 3.5,
                 3, 2.5, 2, 1.5, 1]

    lennrl = len(newrankList)
    if lennrl > 25:
        lennrl = 25
    i = 0
    i2 = 0
    i3 = 0
    g = 0
    alreadyExists = False

    #If Princeton Review is called
    if funkName == "P":
        #Multiples baseList by User-Selected Importance Value
        while g < len(baseList):
            baseList[g] *= aImportance
            g += 1
        #Determines if it is first attribute or not
        if order == 1:
            #First attribute process
            while i < lennrl:
                finalList.append(newrankList[i])
                finalList.append(baseList[i])
                finalListCollegesOnlyP.append(newrankList[i])

                i += 1
        else:
            #Second Attribute Process
            while i2 < lennrl:
                #Repeats for every element in newrankList
                alreadyExists = False
                i3 = 0

                while i3 < len(finalList):
                    #If college already exists in final list
                    if newrankList[i2] == finalList[i3]:
                        finalList.insert((i3 + 1), baseList[i2])
                        alreadyExists = True
                        #print(alreadyExists)
                        break

                    i3 += 1
                #print(alreadyExists)
                if alreadyExists == False:
                    finalList.append(newrankList[i2])
                    finalList.append(baseList[i2])

                    ###finalconversionlist.append
                    finalListCollegesOnlyP.append(newrankList[i2])
                else:
                    pass

                i2 += 1
    #If CollegeFactual Function is Called
    elif funkName == "C":
        #print(lennrl)
        #TODO

        # Multiples baseList by User-Selected Importance Value
        #print(type(aImportance))
        while g < len(baseList):
            #print(baseList[g])
            baseList[g] *= aImportance
            #print(baseList[g])
            baseList2[g] *= aImportance
            g += 1
        #print(baseList2)
        # Determines if it is first attribute or not
        if order == 1:
            # First attribute process
            while i < lennrl:
                finalList.append(newrankList[i])
                if lennrl < 50:
                    finalList.append(baseList[i])
                else:
                    finalList.append(baseList2[i])

                finalListCollegesOnlyC.append(newrankList[i])
                i += 1
        else:
            # Second Attribute Process
            while i2 < lennrl:
                # Repeats for every element in newrankList
                alreadyExists = False
                i3 = 0

                while i3 < len(finalList):
                    # If college already exists in final list
                    if newrankList[i2] == finalList[i3]:
                        if lennrl < 50:
                            finalList.insert((i3 + 1), baseList[i2])
                        else:
                            finalList.insert((i3 + 1), baseList2[i2])

                        alreadyExists = True
                        # print(alreadyExists)
                        break

                    i3 += 1
                # print(alreadyExists)
                if alreadyExists == False:
                    finalList.append(newrankList[i2])
                    if lennrl < 50:
                        finalList.append(baseList[i2])
                    else:
                        finalList.append(baseList2[i2])

                    finalListCollegesOnlyC.append(newrankList[i2])
                else:
                    pass

                i2 += 1

    #print(finalList)

#Average-creating function, (must run twice for C and P)
def averageA(funkName2):
    global finalList
    global numPcalls
    global numCcalls
    global finalListCollegesOnlyP
    global finalListCollegesOnlyC
    global reportfinalListP
    global reportfinalListC

    #To split string to isolate each college and their points
    i4 = 1
    i5 = 1
    totalPts = 0
    totalAvgPts = 0
    i6 = 0
    i7 = 1
    i8 = 0
    i9 = 1

    #print(finalListCollegesOnly)
    if funkName2 == "P":
        tfinalList = finalList
        tfnLLength = len(tfinalList)
        while i9 < tfnLLength:
            if i8 > (len(finalListCollegesOnlyP) - 1):
                break
            else:
                if type(finalList[i4]) == str:
                    #Adds all the numbers together between first string and second string
                    totalPts = 0
                    i7 = 1
                    #print(i4)

                    while i7 < i4:
                        totalPts += int(finalList[i7])
                        i7 += 1
                    #print(totalPts)
                    totalAvgPts = totalPts / numPcalls
                    totalAvgPts = round(totalAvgPts, 2)

                    #print(finalListCollegesOnlyP[i8])
                    reportfinalListP.append(finalListCollegesOnlyP[i8])
                    reportfinalListP.append(totalAvgPts)
                    #print(reportfinalList)



                    del finalList[0]
                    while type(finalList[0]) != str:
                        del finalList[0]

                    #print(finalList)


                    i8 += 1
                    i4 = 1
                else:
                    i4 += 1

                    pass

            i9 += 1
    elif funkName2 == "C":
        tfinalList = finalList
        tfnLLength = len(tfinalList)
        while i9 < tfnLLength:
            if type(finalList[i4]) == str:
                # Adds all the numbers together between first string and second string
                totalPts = 0
                i7 = 1
                # print(i4)

                while i7 < i4:
                    totalPts += int(finalList[i7])
                    i7 += 1
                # print(totalPts)
                totalAvgPts = totalPts / numCcalls
                totalAvgPts = round(totalAvgPts, 2)

                reportfinalListC.append(finalListCollegesOnlyC[i8])
                reportfinalListC.append(totalAvgPts)
                # print(reportfinalList)

                del finalList[0]
                while type(finalList[0]) != str:
                    del finalList[0]

                # print(finalList)

                i8 += 1
                i4 = 1
            else:
                i4 += 1

                pass

            i9 += 1

#Function to combines reportfinalListP and reportfinalListC
def joinA():
    global finalListCollegesOnlyC
    global finalListCollegesOnlyP
    global reportfinalListP
    global reportfinalListC

    # -------------------------------------------------------------------------------
    # First, Goes through all colleges in finalListCollegesOnlyC and divides them by 2 if they do not exist in P list
    i = 0
    while i < (len(reportfinalListC) - 1):
        now = reportfinalListC[i]

        try:
            trialI = finalListCollegesOnlyP.index(now)
        except ValueError:
            reportfinalListC[i + 1] /= 2

        i += 2

    #Loop through all colleges in final P list (e1)
    e1 = 0
    e2 = 0
    alreadyExists = False
    while e1 < len(reportfinalListP):
        alreadyExists = False
        #print("\n" + reportfinalListP[e1])
        #Loops through all colleges in final CF list (e2)
        e2 = 0
        while e2 < len(reportfinalListC):
            #print(reportfinalListC[e2])
            if reportfinalListP[e1] == reportfinalListC[e2]:
                #New point value for found college = existing value + value from P list    all over 2
                reportfinalListC[e2 + 1] = (reportfinalListC[e2 + 1] + reportfinalListP[e1 + 1])/2

                alreadyExists = True
                break

            e2 += 2

        if alreadyExists == False:
            reportfinalListC.append(reportfinalListP[e1])
            reportfinalListC.append((reportfinalListP[e1 + 1])/2)
        else:
            pass

        e1 += 2

#Function sorts reportfinalListC into order based on total points
def bestSort():
    global reportfinalListC
    global customList

    customList = []

    e3 = 1
    largest = reportfinalListC[1]

    #Main loop that finds top 10 of rfList
    i = 0
    rflC = (len(reportfinalListC) / 2)
    while i < rflC:
        #Resets
        largest = reportfinalListC[1]
        e3 = 1

        #Finds largest integer in list and then prints the corresponding school value
        while e3 < len(reportfinalListC):
            if reportfinalListC[e3] > largest:
                largest  = reportfinalListC[e3]

            e3 += 2

        realI = reportfinalListC.index(largest)

        topSchool = reportfinalListC[realI - 1]

        #Appends to final custom list
        ntopSchool = topSchool.replace("-", " ")
        customList.append(ntopSchool)
        #customList.append(reportfinalListC[realI])
        customList = [x.title() for x in customList]

        #Deletes elements from rfList
        del reportfinalListC[realI]
        del reportfinalListC[realI - 1]

        i += 1


#College Factual Function
def collegeFactual(pChoice, pImportance):
    global newrankList
    newrankList = []

    # Global Importance value
    global aImportance
    aImportance = int(pImportance)

    # Searches Google to find URL of Attribute Ranking Site
    query2 = "College Factual 2024/25 Best Colleges for " + pChoice

    for j in search(query2, tld="co.in", num=1, stop=1, pause=2):
        goodURL2 = j

    #print("Hello: " + goodURL2)
    # Gets HTML Data from URL
    r = requests.get(goodURL2)
    soup = BeautifulSoup(r.text, 'html.parser')
    j = soup.find_all('a', class_="rankListHeaderText")


    # Appends colleges to newrankList
    #TODO Emory University/Oxford College of Emory special case

    for element in j:
        if element.get_text() == 'oxford-college-of-emory-university':
            newrankList.append('emory-university')
        else:
            newrankList.append(element.get_text())

    #List Comprehension to convert all to lowercase
    newrankList = [x.lower() for x in newrankList]
    newrankList = [z.replace(' - ', ' ') for z in newrankList]
    newrankList = [y.replace(' ', '-') for y in newrankList]

    #print("\n CollegeFactual call done")
    #print(newrankList)

# Princeton Review Function
def princetonReview(pChoice, pImportance):
    global conversionList
    conversionList = []
    # Global Importance value
    global aImportance
    aImportance = int(pImportance)

    # Searches Google to find URL of Attribute Ranking Site

    # to search
    query = "The Princeton Review Best College " + pChoice

    for j in search(query, tld="co.in", num=1, stop=1, pause=2):
        goodURL = j

    # print("Hello: " + goodURL)
    # Gets HTML Data from URL
    r = requests.get(goodURL)
    soup = BeautifulSoup(r.text, 'html.parser')
    j = soup.find('main', class_="col-lg-8 col-md-12 col-sm-12").get_text(strip=True)
    # print(j)

    rank1 = j.find("#1")
    # print(rank1)
    # ------------------------------------------------------------------------------------------------------------#

    # Number for iterations v (testing purposes)
    if pChoice == "Internships Public" or pChoice == "Internships Private":
        testTimes = 20
    elif pChoice == "Public School value top 50" or pChoice == "Private School value top 50":
        testTimes = 25
    else:
        testTimes = 25
    # Loop to put top 25 in ordered list
    loop = 1
    rankList = []

    while loop < testTimes:
        # print(loop)
        loopS = str(loop)
        finder = '#' + loopS
        # print(finder)

        rank = j.find(finder)
        # print(rank)

        strnew = j.split(finder)
        # print(strnew)

        firstU = strnew[1]
        finalStr = ""
        i = 0
        x = 0

        while x < 4:
            while firstU[i] != ' ':
                finalStr = finalStr + firstU[i]
                i += 1

            # print(finalStr)
            i += 1
            x += 1

        # --------Editing the Final String
        upperList = []
        f = finalStr.find("Featured")
        if f == 0:
            finalStr = finalStr.replace("Featured", " ")
        for c in finalStr:
            if c.isupper() == True:
                upperList.append(c)
        # print(upperList)
        # print(finalStr)

        UnivExists = False
        CollegeOfExists = False

        if finalStr[0] == "U" and finalStr[10] == "o" or finalStr[11] == "o":
            UnivExists = True
        if finalStr[0] == "C" and finalStr[7] == "o":
            CollegeOfExists = True

        # print(finalStr)
        if UnivExists or CollegeOfExists:
            # Specific School Exception
            if finalStr == "UniversityofPuget":
                endCap = upperList[3]
            if finalStr == "UniversityofTexasat" or finalStr == "UniversityofIllinoisat":
                endCap = "a"
            else:
                if upperList[1] == upperList[2]:
                    endCap = upperList[3]
                else:
                    endCap = upperList[2]

            endCap_find = finalStr.find(endCap)
            newFinalStr = finalStr.split(finalStr[endCap_find])

            rankList.append(newFinalStr[0])
        else:
            if len(upperList) > 2:
                if upperList[0] == upperList[2]:
                    endCap = upperList[1]
                else:
                    endCap = upperList[2]
                endCap_find = finalStr.find(endCap)
                newFinalStr = finalStr.split(finalStr[endCap_find])
                rankList.append(newFinalStr[0])
            else:
                rankList.append("____ERROR____")

        # print(rankList)
        i = 0
        loop += 1

    # For loop to put error in missing colleges
    for num in range(testTimes - 1):
        if rankList[num] == ' ' or rankList[num] == '':
            rankList[num] = "____ERROR____"

    # printout of final ranking list (with errors included)
    # print(rankList)

    # Removes ____Error____'s from List
    i1 = 0
    global newrankList
    newrankList = []
    while i1 < (testTimes - 1):
        # print(i1)
        if rankList[i1] != "____ERROR____":
            newrankList.append(rankList[i1])
        i1 += 1

    # print("\nFinal Ranking: ")
    # print(newrankList)

    # print("\nPrincetonReview call done")
    # print(newrankList)

#P to CF variable conversions list:
def conversions():
    global finalListCollegesOnlyP

    finalPlist = [' UniversityofDenverDenver,', 'EmoryUniversity', 'LehighUniversity', 'FloridaState', 'VirginiaTech', 'WashingtonState', ' Auburn', ' WashingtonUniversityin', 'KansasState', 'RiceUniversity', 'TulaneUniversity', 'Hampden-Sydney', 'AngeloState', 'FranklinW.', 'ClaremontMc', 'UniversityofWisconsin-', 'CollegeoftheAtlantic', 'TheUniversityof', 'ThomasAquinas', 'Hamilton', 'Amherst', 'UniversityofCincinnatiCincinnati,', ' VanderbiltUniversity', ' GonzagaUniversity', 'ArizonaState', 'Syracuse', ' Clemson', 'BrighamYoung', 'TheOhio', 'MichiganState', 'UniversityofTex', 'ButlerUniversity', 'Wabash', 'UniversityofNotre', 'UniversityofDaytonDayton,', 'UniversityofTennessee-', 'UnitedStates', 'XavierUniversity(', ' UniversityofNebraska—', 'IowaState', ' BryantUniversity', 'UniversityofSan', 'BrynMawr', 'Lewis&', ' FloridaSouthern', 'MountHolyoke', ' SalveRegina', ' ReedCollege', ' RhodesCollege', 'RollinsCollege', ' HighPoint', 'TexasChristian', 'UniversityofPuget', 'UniversityofCalifornia—', 'PepperdineUniversity', ' LoyolaMarymount', 'AmericanUniversity', 'SimmonsUniversity', 'EmersonCollege', 'ColumbiaUniversity', 'CityUniversityof', 'EugeneLang', ' SuffolkUniversity', ' NortheasternUniversity', ' GeorgeWashington', 'TheCooper', 'UniversityofVermont', 'LoyolaUniversity', 'NewYork', ' DruryUniversity', 'JuniataCollege', "St.John's", 'DenisonUniversity', 'CaliforniaState', 'Wellesley', ' DrewUniversity', 'AgnesScott', 'St.Bonaventure', 'Bowdoin', 'Scripps', 'Pitzer', 'UniversityofKentucky', 'WheatonCollege(', 'Skidmore', ' ChristopherNewport', 'Elon', 'UniversityofMassachusetts-', 'CornellUniversity', 'BatesCollege', 'JamesMadison', ' MuhlenbergCollege', ' St.Olaf', ' Gettysburg', 'GeorgiaInstituteof', 'UniversityofVirginia', 'UniversityofMichigan—', 'NorthCarolina', 'UniversityofWashington', 'UniversityofGeorgia', 'UniversityofIllinois', ' StateUniversityof', 'MissouriUniversityof', 'William&', 'PurdueUniversity—', 'NewCollegeof', 'TexasA&', 'NewJersey', 'MassachusettsInstituteof', 'Princeton', 'Stanford', 'HarveyMudd', 'CaliforniaInstituteof', 'DartmouthCollege', 'Harvard', 'Williams', 'YaleUniversity', 'JohnsHopkins', 'CarnegieMellon', 'Universityof', 'BrownUniversity', 'Duke', 'ColgateUniversity', 'Pomona', 'MichiganTechnological', 'PennState', ' The', 'MiamiUniversity', 'OregonState', ' St.Lawrence', 'Rose-Hulman', 'WakeForest', 'Marquette', 'AustinCollege', ' HobartandWilliam', ' CollegeofWoosterWooster,', 'WorcesterPolytechnic']

    completePconversionList = ['university-of-denver', 'emory-university', 'lehigh-university', 'florida-state-university', 'virginia-tech', 'washington-state-university', 'auburn-university', 'washington-university-in-st-louis', 'kansas-state-university', 'rice-university', 'tulane-university-of-louisiana', 'hampden-sydney-college', 'angelo-state-university', 'franklin-university', 'claremont-mckenna-college', 'university-of-wisconsin-madison', 'college-of-the-atlantic', 'university-of-chicago', 'thomas-aquinas-college', 'hamilton-college', 'amherst-college', 'university-of-cincinnati-main-campus', 'vanderbilt-university', 'gonzaga-university', 'arizona-state-university', 'syracuse-university', 'clemson-university', 'brigham-young-university-provo', 'ohio-state-university-main-campus', 'michigan-state-university', 'the-university-of-texas-at-austin', 'butler-university', 'wabash-college', 'university-of-notre-dame', 'university-of-dayton', 'the-university-of-tennessee', 'united-states-naval-academy', 'xavier-university', 'university-of-nebraska-lincoln', 'iowa-state-university', 'bryant-university', 'university-of-san-francisco', 'bryn-mawr-college', 'lewis-and-clark-college', 'florida-southern-college', 'mount-holyoke-college', 'salve-regina-university', 'reed-college', 'rhodes-college', 'rollins-college', 'high-point-university', 'texas-christian-university', 'university-of-puget-sound', 'university-of-california-berkeley', 'pepperdine-university', 'loyola-marymount-university', 'american-university', 'simmons-college', 'emerson-college', 'columbia-university-in-the-city-of-new-york', 'city-university-of-seattle', 'suny-at-binghamton', 'suffolk-university', 'northeastern-university', 'george-washington-university', 'cooper-union-for-the-advancement-of-science-and-art', 'university-of-vermont', 'loyola-university-chicago', 'new-york-university', 'drury-university', 'juniata-college', 'st-johns-university-new-york', 'denison-university', 'california-state-university-los-angeles', 'wellesley-college', 'drew-university', 'agnes-scott-college', 'saint-bonaventure-university', 'bowdoin-college', 'scripps-college', 'pitzer-college', 'university-of-kentucky', 'wheaton-college-illinois', 'skidmore-college', 'christopher-newport-university', 'elon-university', 'university-of-massachusetts-amherst', 'cornell-university', 'bates-college', 'james-madison-university', 'muhlenberg-college', 'st-olaf-college', 'gettysburg-college', 'georgia-institute-of-technology-main-campus', 'university-of-virginia-main-campus', 'university-of-michigan-ann-arbor', 'university-of-north-carolina-at-chapel-hill', 'university-of-washington-seattle-campus', 'university-of-georgia', 'university-of-illinois-at-urbana-champaign', 'suny-at-binghamton', 'university-of-missouri-columbia', 'college-of-william-and-mary', 'purdue-university-main-campus', 'the-new-school', 'texas-a-and-m-university-college-station', 'the-college-of-new-jersey', 'massachusetts-institute-of-technology', 'princeton-university', 'stanford-university', 'harvey-mudd-college', 'california-institute-of-technology', 'dartmouth-college', 'harvard-university', 'williams-college', 'yale-university', 'johns-hopkins-university', 'carnegie-mellon-university', 'university-of-chicago', 'brown-university', 'duke-university', 'colgate-university', 'pomona-college', 'michigan-technological-university', 'pennsylvania-state-university-main-campus', 'suny-at-binghamton', 'miami-university-oxford', 'oregon-state-university', 'st-lawrence-university', 'rose-hulman-institute-of-technology', 'wake-forest-university', 'marquette-university', 'austin-college', 'hobart-william-smith-colleges', 'the-college-of-wooster', 'worcester-polytechnic-institute']

    #Loops through all of finalListCollegesOnlyP
    i = 0
    flcoplen = len(finalListCollegesOnlyP)
    while i < flcoplen:
        try:
            oneIndex = finalPlist.index(finalListCollegesOnlyP[i])

            finalListCollegesOnlyP.insert(i, completePconversionList[oneIndex])
            del finalListCollegesOnlyP[i + 1]
        except ValueError:
            pass

        i += 1



#Flask Section----------------------------------------------------------------------------------------------------------
app = Flask(__name__)

#Home Page-------------------------------------------------------------------------------
@app.route('/')
def home():
    return render_template('home.html')

#In Progress Page------------------------------------------------------------------------
@app.route('/calculate')
def next():
    # Gets all user inputs from URL and stores them in string
    global inputStr
    inputStr = ''

    inputStr = request.url
    print(inputStr)

    #11/16 - inputStr is no longer rendered to screen
    return render_template('in_progress.html')

#Algorithm for rankings------------------------------------------------------------------
@app.route('/results')
def results():
    print("Working")

    global customList
    global finalList
    global reportfinalListC
    global reportfinalListP
    global finalListCollegesOnlyP
    global finalListCollegesOnlyC
    global inputStr
    global numPcalls
    global numCcalls

    #Clears all lists
    reportfinalListP = []
    reportfinalListC = []
    finalList = []
    numPcalls = 0
    numCcalls = 0
    finalListCollegesOnlyP = []
    finalListCollegesOnlyC = []
    ultiStr = ''
    endStr = []
    first = ''
    second = ''
    third = ''
    fourth = ''
    fifth = ''
    sixth = ''
    seventh = ''
    eighth = ''
    ninth = ''
    tenth = ''
    eleventh = ''
    twelfth = ''
    thirteenth = ''
    fourteenth = ''
    fifteenth = ''
    sixteenth = ''
    seventeenth = ''
    eighteenth = ''
    nineteenth = ''
    twentieth = ''

    # Trims down inputStr
    try:
        endStr = inputStr.split("?", 1)
        ultiStr = endStr[1]
        print(ultiStr)
    except IndexError:
        ultiStr = inputStr

    # Determines which attributes to actually search for----

    # 3 CollegeFactual Attributes First---------------------
    # Intended major attribute
    #v  called Determines if CF function is actually called
    called = False
    imNameEq = ultiStr.find("=")
    imNameIeq = ultiStr.find("a")

    i1 = imNameEq + 1
    intendMajorName = ''
    try:
        while ultiStr[i1] != "&":
            intendMajorName = intendMajorName + ultiStr[i1]
            i1 += 1
    except IndexError:
        intendMajorName = ultiStr

        print(intendMajorName)

    intendMajorIM = ultiStr[imNameIeq + 3]
    print(intendMajorIM)

    if ultiStr[imNameEq + 1] == "&" or imNameIeq == -1 or ultiStr[imNameIeq + 3] == "0" or ultiStr[imNameIeq + 3] == "&":
        pass
    else:
        called = True
        numCcalls += 1

        collegeFactual(intendMajorName, intendMajorIM)
        listA(1, "C")

    #Deletes used part of string -- - - - - - - - - -
    if called == True:
        nextStr = ultiStr.split("&", 1)
        ultiStr = nextStr[1]

    print(ultiStr)
    # Undergrad School ranking
    called = False

    uSchoolNameEq = ultiStr.find("s")
    uSchoolIeq = ultiStr.find("b")

    i2 = uSchoolNameEq + 1
    uSchoolName = ''
    while ultiStr[i2] != "&":
        uSchoolName = uSchoolName + ultiStr[i2]
        i2 += 1
    print(uSchoolName)

    uSchoolIM = ultiStr[uSchoolIeq + 3]

    print(uSchoolIM)
    if ultiStr[uSchoolNameEq + 1] == "&" or uSchoolIeq == -1 or ultiStr[uSchoolIeq + 3] == "0" or ultiStr[uSchoolIeq + 3] == "&":
        pass
    else:
        called = True
        numCcalls += 1

        collegeFactual(uSchoolName, uSchoolIM)
        listA(2, "C")

    if called == True:
        nextStr = ultiStr.split("_", 1)
        ultiStr = nextStr[1]

    # Overall Prestige
    oPrestigeIeq = ultiStr.find("c")
    called = False

    if oPrestigeIeq == -1 or ultiStr[oPrestigeIeq + 3] == "0" or ultiStr[oPrestigeIeq + 3] == "&":
        pass
    else:
        called = True
        numCcalls += 1

        collegeFactual("Overall Prestige", oPrestigeIeq + 3)
        listA(3, "C")
        print(finalList)

    if called == True:
        nextStr = ultiStr.split("_", 1)
        ultiStr = nextStr[1]

    # averageA for CF calls
    print(finalListCollegesOnlyC)
    averageA("C")

    print(reportfinalListC)

    # 11 PrincetonReview attributes next--------------------------------------------------------------------------------
    print(ultiStr)

    # List of PrincetonReview attributes
    #First, Engineering special case
    engrIndex = ultiStr.find("E")
    if engrIndex != -1:
        nextStr = ultiStr.split("_", 1)
        ultiStr = nextStr[1]

    print(ultiStr)

    attributesList = ["Their Students Love these colleges", "Students love their school teams",
                      "Campus Beauty", "Cities", "Lots of race/class interaction", "Dorms", "Food",
                      "Public school value top 50", "Private school value top 50", "Internships Public",
                      "Internships Private"]
    pNameLoop = ["d", "e", "x", "f", "g", "h", "i", "j", "k", "l", "m"]
    preimportanceList = []
    importanceList = []

    for letter in pNameLoop:
        pnIndex = ultiStr.find(letter)
        preimportanceList.append(pnIndex)

    print(preimportanceList)

    for elem in preimportanceList:
        if elem == -1:
            rightIndex = "0"
        else:
            rightIndex = ultiStr[elem + 3]
        #print(rightIndex)
        if rightIndex == "&" or rightIndex == "0":
            importanceList.append(0)
        else:
            try:
                importanceList.append(int(rightIndex))
            except ValueError:
                importanceList.append(0)

    print(importanceList)

    #Now calls the P functions
    i2 = 0
    while i2 < 11:
        if importanceList[i2] == 0:
            pass
        else:
            numPcalls += 1

            princetonReview(attributesList[i2], importanceList[i2])
            listA(i2 + 1, "P")
            if finalList[1] < 25:
                del finalList[0]
                del finalList[1]

            print(finalList)
        i2 += 1

    #converions() and averageA() for P calls
    conversions()
    averageA("P")
    print(reportfinalListP)

    #Join P and CF list together
    joinA()
    print(reportfinalListC)

    #Deletes Southern New Hampshire University Case
    try:
        snhuT = 0
        snhuT = reportfinalListC.count("southern-new-hampshire-university")
        while snhuT != 0:
            snhuI = reportfinalListC.index("southern-new-hampshire-university")

            del reportfinalListC[snhuI]
            del reportfinalListC[snhuI]
            snhuI = 0
            snhuT -= 1

    except ValueError:
        pass

    print(reportfinalListC)
    #Gets top 10 schools   ... or top 20 schools
    bestSort()
    tenor20 = request.args.get("z", "twenty")
    print(tenor20)
    print(customList)

    #Other Way
    first = customList[0]
    second = customList[2]
    third = customList[4]
    fourth = customList[6]
    fifth = customList[8]
    sixth = customList[10]
    seventh = customList[12]
    eighth = customList[14]
    ninth = customList[16]
    tenth = customList[18]

    if tenor20 == "twenty":
        eleventh = customList[20]
        twelfth = customList[22]
        thirteenth = customList[24]
        fourteenth = customList[26]
        fifteenth = customList[28]
        sixteenth = customList[30]
        seventeenth = customList[32]
        eighteenth = customList[34]
        nineteenth = customList[36]
        twentieth = customList[38]

    if tenor20 == "twenty":
        return render_template('results.html', value1 = first, value2 = second, value3 = third, value4 = fourth, value5 = fifth, value6 = sixth, value7 = seventh, value8 = eighth, value9 = ninth, value10 = tenth, value11 =  "11. " + eleventh, value12 = "12. " + twelfth, value13 = "13. " + thirteenth, value14 = "14. " + fourteenth, value15 = "15. " + fifteenth, value16 = "16. " + sixteenth, value17 = "17. " + seventeenth, value18 = "18. " + eighteenth, value19 = "19. " + nineteenth, value20 = "20. " + twentieth)
    else:
        return render_template('results.html', value1=first, value2=second, value3=third, value4=fourth, value5=fifth, value6=sixth, value7=seventh, value8=eighth, value9=ninth, value10=tenth)

#Filters rankings based on acceptance rate... and ---------------------------------------
@app.route('/filter')
def aRateFilter():
    global customList

    minimum = int(request.args.get("filterI"))
    print(minimum)

    filterListCounter = 0
    i = 0
    filterList = []

    while filterListCounter < 10:
        while i < len(customList):
            if filterListCounter > 10:
                # Prints final filtered list
                print(filterList)
                #Changes List to String
                filterStr = str(filterList)
                f1 = filterStr.replace("'", "")
                f2 = f1.replace(",", "_____")
                f3 = f2.replace("[", "")
                f4 = f3.replace("]", "")
                #print(f4)

                return render_template('filter.html', valuei=f4)
            else:
                # Then search google for acceptance rate of each college on customList
                nowQuery = customList[i]

                # Searches Google to find URL of CF site and gets acceptance rate data
                query = "CollegeFactual " + nowQuery

                for j in search(query, tld="co.in", num=1, stop=1, pause=2):
                    goodURL2 = j

                print("Hello: " + goodURL2)
                # Gets HTML Data from URL
                r = requests.get(goodURL2)
                soup = BeautifulSoup(r.text, 'html.parser')
                f = soup.find('div', class_="grid quick-stats")
                g = str(f.get_text())

                aRateIndex = g.find("%")
                ultiRateInt = 0

                finalaRate = []
                finalaRate.append(g[aRateIndex - 1])
                if g[aRateIndex - 2] == "y":
                    ultiaRateInt = int(finalaRate[0])
                    pass
                else:
                    finalaRate.insert(0, (g[aRateIndex - 2]))
                    tempaRateInt = ''
                    tempaRateInt = finalaRate[0] + finalaRate[1]
                    ultiaRateInt = int(tempaRateInt)

                # print(g)
                # print(aRateIndex)
                # Returns integer of acceptance rate----------
                print(ultiaRateInt)

                # Now adds acceptance rates above value to filterList
                if ultiaRateInt > minimum:
                    filterList.append(nowQuery)
                    filterListCounter += 1
                    print(filterListCounter)
                else:
                    pass

                i += 1


#Runs Flask------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run()
