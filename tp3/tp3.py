# tp3.py
# Marc Edwards
# mpedward

from cmu_112_graphics import * # graphics
from tkinter import * # interface
from bs4 import BeautifulSoup # scraping
import pandas as pd # beautiful dataframes
import xlrd # read excel files helper
import requests # also a scraping method
import lxml.html as lh # parsing
import plotly.express as px # visuals
import plotly
import math
import statistics as stat

# reading in excel data that shows results of previous games
#https://www.sportsbookreviewsonline.com/scoresoddsarchives/nfl/nfloddsarchives.htm

df19_20 = pd.read_excel(open("nfl odds 2019-20.xlsx", "rb"))
df19_20.insert(0, "Season", len(df19_20)*["2019-20"], True)
df18_19 = pd.read_excel(open("nfl odds 2018-19.xlsx", "rb"))
df18_19.insert(0, "Season", len(df18_19)*["2018-19"], True)
df17_18 = pd.read_excel(open("nfl odds 2017-18.xlsx", "rb"))
df17_18.insert(0, "Season", len(df17_18)*["2017-18"], True)
df16_17 = pd.read_excel(open("nfl odds 2016-17.xlsx", "rb"))
df16_17.insert(0, "Season", len(df16_17)*["2016-17"], True)

# combine the dfs of each season
combinedDf = pd.concat([df16_17, df17_18, df18_19, df19_20]) 

# changing index of all games 0:len(combinedDf - 1)
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reset_index.html
combinedDf.reset_index(drop = True, inplace = True)

# data and team name manipulation
# because some teams have relocated in last 5 years
# https://stackoverflow.com/questions/18548662/rename-elements-in-a-column-of-a-data-frame-using-pandas
combinedDf["Team"] = combinedDf["Team"].replace({"SanDiego": "Chargers",
                                                 "LosAngeles": "Rams", 
                                                 "LAChargers": "Chargers", 
                                                 "LARams": "Rams", 
                                                 "Oakland": "Raiders"})


##### higher order analysis, using statistics!

# probablitiy of winning
# https://www.sportsbookreviewsonline.com/sportsbettingarticles/sportsbettingarticle10.htm
# can you trust the moneyline?

# To determine the win percent necessary to breakeven at the offered 
# odds use the implied probability calculation.

breakeven = 100
impliedProbResult = []
for i in combinedDf["ML"]:
    # Favorite moneyline implied winning probability
    if i <= -100:
        impliedProbResult.append((i / (i - breakeven)))
    # underdog moneyline implied winning probability
    elif i >= 100:
        impliedProbResult.append((breakeven / (breakeven + i)))
    else:
        pass
combinedDf["ImpliedProbability"] = impliedProbResult

gameIndex = combinedDf["ImpliedProbability"]

# .loc method -> https://www.geeksforgeeks.org/python-pandas-dataframe-loc/
# calulate the decimal odds (1/ExplicitProbability[i]) and then 
# (1/ExplicitProbability[i] / 1/ExplicitProbability[i+1] - 1) * 100 = edge % 
for i in range(0, len(gameIndex), 2):
    combinedDf.loc[i, "ExplicitProbability"] = combinedDf.loc[i, "ImpliedProbability"] / (combinedDf.loc[i, "ImpliedProbability"] + combinedDf.loc[i+1, "ImpliedProbability"])
    combinedDf.loc[i+1, "ExplicitProbability"] = combinedDf.loc[i+1, "ImpliedProbability"] / (combinedDf.loc[i, "ImpliedProbability"] + combinedDf.loc[i+1, "ImpliedProbability"])
# Verified P = 1

# Edge, the higher your edge more you should consider betting
# https://professionalsportspicks.com/expected-value-perceived-edge-and-variance-in-sports-betting-4175/
for i in range(0, len(gameIndex)):
    combinedDf.loc[i, "Edge%"] = (combinedDf.loc[i, "ImpliedProbability"] - combinedDf.loc[i, "ExplicitProbability"]) * 100

# adding win/loss column
for i in range(0, len(gameIndex), 2):
    if combinedDf.loc[i, "Final"] > combinedDf.loc[i+1, "Final"]:
        combinedDf.loc[i, "WinLoss"] = "W"
        combinedDf.loc[i+1, "WinLoss"] = "L"
    elif combinedDf.loc[i, "Final"] < combinedDf.loc[i+1, "Final"]:
        combinedDf.loc[i, "WinLoss"] = "L"
        combinedDf.loc[i+1, "WinLoss"] = "W"
    else:
        combinedDf.loc[i, "WinLoss"] = "T"
        combinedDf.loc[i+1, "WinLoss"] = "T"

#print(combinedDf)

## Same analysis as above but for the current odds
# odds, from https://www.teamrankings.com/nfl/odds/
# using excel and pandas method for obtaining this info
currentOddsDf = pd.read_excel(open("NFLodds.xlsx", "rb"))

breakeven = 100
oddsImpliedProbResult = []
for i in currentOddsDf["ML"]:
    # Favorite moneyline implied winning probability
    if i <= -100:
        oddsImpliedProbResult.append((i / (i - breakeven)))
    # underdog moneyline implied winning probability
    elif i >= 100:
        oddsImpliedProbResult.append((breakeven / (breakeven + i)))
    else:
        pass

currentOddsDf["ImpliedProbability"] = oddsImpliedProbResult
currentOddsIndex = currentOddsDf["ML"] # just length of columns

# .loc method -> https://www.geeksforgeeks.org/python-pandas-dataframe-loc/
# calulate the decimal odds (1/ExplicitProbability[i]) and then 
# (1/ExplicitProbability[i] / 1/ExplicitProbability[i+1] - 1) * 100 = edge % 
for i in range(0, len(currentOddsIndex), 2):
    currentOddsDf.loc[i, "ExplicitProbability"] = currentOddsDf.loc[i, "ImpliedProbability"] / (currentOddsDf.loc[i, "ImpliedProbability"] + currentOddsDf.loc[i+1, "ImpliedProbability"])
    currentOddsDf.loc[i+1, "ExplicitProbability"] = currentOddsDf.loc[i+1, "ImpliedProbability"] / (currentOddsDf.loc[i, "ImpliedProbability"] + currentOddsDf.loc[i+1, "ImpliedProbability"])
# Verified P = 1

# Edge, the higher your edge more you should consider betting
# https://professionalsportspicks.com/expected-value-perceived-edge-and-variance-in-sports-betting-4175/
for i in range(0, len(currentOddsIndex)):
    currentOddsDf.loc[i, "Edge%"] = (currentOddsDf.loc[i, "ImpliedProbability"] - currentOddsDf.loc[i, "ExplicitProbability"]) * 100

#print(currentOddsDf)


### cmu graphics stuff
### cmu_112_graphics compatable
### methods are from previous things we learned in class

def appStarted(app):
    app.waitingForFirstKeyPress = True
    app.gameOver = False
    pass

def linesAndOdds(app):
    print(currentOddsDf)

def historyResults(app):
    print(combinedDf)

def seasonATSresults(app):
    # Using pandas and bs4 for webscraping purposes
    # using requests and bs4 together
    # records against spread
    # method from
    # https://pythonprogramming.net/tables-xml-scraping-parsing-beautiful-soup-tutorial/

    urlATS = "https://www.teamrankings.com/nfl/trends/ats_trends/"
    # gets everything from html page
    rawUrlATS = requests.get(urlATS).text
    soupATS = BeautifulSoup(rawUrlATS, "lxml")
    atsTable = soupATS.find("table") 
    atsTableData = atsTable.find_all("tr")
    atsTableHeader = atsTable.find_all("thead")
    #ATS Record: The number of ATS covers, no-covers, and pushes
    #Cover %: The percentage of time the team covered, net of pushes
    #MOV: The average margin of victory (negative in losses)
    #ATS +/-: The average amount of points that the team covers the spread by
    # headers
    for thead in atsTableHeader:
        th = thead.find_all("th")
        headerRow = [h.text for h in th]
        #print(headerRow)

    # body data, no headers, creating dictionary
    for tr in atsTableData:
        td = tr.find_all("td")
        row = [i.text for i in td]
        if row == []: # removes empty list at top
            pass
        else:
            colTeam = row[0]
            colRecord = row[1]
            colCover = row[2]
            colMOV = row[3]
            colATS = row[4]
            # create dictionary to store the info
            dfATS = pd.DataFrame({"Team": [colTeam], "ATS Record": [colRecord], 
                            "Cover %": [colCover], "MOV": [colMOV],
                            "ATS +/-": [colATS]})
            print(dfATS)

def lineChanges(app):
    # Using pandas and bs4 for webscraping purposes
    # using requests and bs4 together
    # odds tables changes
    # method from
    # https://pythonprogramming.net/tables-xml-scraping-parsing-beautiful-soup-tutorial/
    # https://www.pluralsight.com/guides/extracting-data-html-beautifulsoup

    urlOdds = "https://www.teamrankings.com/nfl/odds/"
    rawUrlOdds = requests.get(urlOdds).text
    soupOdds = BeautifulSoup(rawUrlOdds, "lxml")
    oddsTable = soupOdds.find("table") 
    oddsTableData = oddsTable.find_all("tr")
    oddsTableHeader = oddsTable.find_all("thead")
    oddsTableBody = oddsTable.find_all("tbody")

    for thead in oddsTableHeader:
        th = thead.find_all("th")
        headerRowChanges = [h.text for h in th]
        print(headerRowChanges)
    # biggest line moves, found at bottom of page
    # will be good for analysis
    for tr in oddsTableData:
        td = tr.find_all("td")
        rowOddsChanges = [i.text for i in td]
        print(rowOddsChanges)

def analysisRegression(app):
    # how does ML equate to edge% ?
    # Simple Linear regression
    # https://towardsdatascience.com/linear-regression-from-scratch-cd0dee067f72

    Y = combinedDf["Edge%"].values
    X1 = combinedDf["ML"].values
    print("The relationship between the ML and Edge%")

    # mean of the independent and dependent parameters
    x1Mean = stat.mean(X1)
    yMean = stat.mean(Y)
    n = len(Y)

    # finding coefficients of our independent and dependent parameters
    numerator = 0
    denominator = 0
    for i in range(n):
        numerator += (Y[i] - yMean) * (X1[i] - x1Mean)
        denominator += (X1[i] - x1Mean) ** 2 # SE
        
    b1 = numerator / denominator
    b0 = yMean - (b1 * x1Mean)
    #printing the coefficient
    print("b0:", b0, "b1:", b1)
    # cover = b0 + b1*wins

    # Mean Squared Error
    # Finding r-sqaured, goodness of model
    mse = 0
    for i in range(n):
        yPred=  b0 + b1* X1[i] # + so on for more terms
        mse += (Y[i] - yPred) ** 2
        
    mse = math.sqrt(mse/n)
    print("Mean Sqaure Error:", mse)

    # Sum of squares total and Sum square of residuals
    sst = 0
    ssr = 0
    for i in range(n) :
        yPred = b0 + b1 * X1[i] # + so on for more terms
        sst += (Y[i] - yMean) ** 2
        ssr += (Y[i] - yPred) ** 2
        
    rSquared  = 1 - (ssr/sst)
    print("rSquared:", rSquared) # = 0.7085493335881201, pretty solid

    print("-----------------------") # divider for veiwing pleasure 
    ##### Another one
    Yb = combinedDf["Edge%"].values
    X1b = combinedDf["ExplicitProbability"].values
    print("The relationship between the Explicit Probability and Edge%")

    # mean of the independent and dependent parameters
    x1bMean = stat.mean(X1b)
    ybMean = stat.mean(Yb)
    nb = len(Yb)

    # finding coefficients of our independent and dependent parameters
    numerator2 = 0
    denominator2 = 0
    for i in range(n):
        numerator2 += (Yb[i] - ybMean) * (X1b[i] - x1bMean)
        denominator2 += (X1b[i] - x1bMean) ** 2 # SE
        
    b1b = numerator2 / denominator2
    b0b = yMean - (b1b * x1bMean)
    #printing the coefficient
    print("b0:", b0b, "b1:", b1b)
    # edge% = b0 + b1*ML

    # Mean Squared Error
    # Finding r-sqaured, goodness of model
    mse2 = 0
    for i in range(nb):
        ybPred=  b0b + b1b* X1b[i] # + so on for more terms
        mse2 += (Yb[i] - ybPred) ** 2
        
    mse2 = math.sqrt(mse2/nb)
    print("Mean Square Error:",mse2)

    # Sum of squares total and Sum square of residuals
    sst2 = 0
    ssr2 = 0
    for i in range(nb) :
        ybPred = b0b + b1b * X1b[i] # + so on for more terms
        sst2 += (Yb[i] - ybMean) ** 2
        ssr2 += (Yb[i] - ybPred) ** 2
        
    rSquared2  = 1 - (ssr2/sst2)
    print("rSquared:", rSquared2) # = 0.7085493335881201, pretty solid

    ### visuals
    # https://plotly.com/python/bar-charts/
    # https://plotly.com/python/text-and-annotations/

    # historical edge% predicted by ML colored by WinLoss
    edgePlot = px.scatter(combinedDf, x = "ML", y = "Edge%", color = "WinLoss",
                title = "Relationship between Edge'%' and ML, colored by WinLoss")
    edgePlot.show()

    #  display current edge %
    figEdge = px.bar(currentOddsDf, x = "Team", y = "Edge%", text = "Edge%", 
                title = "Current Edge'%' for Teams this Week --- Higher the Better Chance for Success")
    figEdge.show()

    # history of explicit probablity refelcting the edge%, colored by WinLoss
    figExProb = px.scatter(combinedDf, x = "ExplicitProbability", y = "Edge%", color = "WinLoss", 
                title = "History of the Relationship between Explicit Probability and Edge %, colored by WinLoss")
    figExProb.show()

    # current of explicit probablity refelcting the edge%,
    figExProbCurrent = px.scatter(currentOddsDf, x = "ExplicitProbability", y = "Edge%",
                title = "Does a Higher Edge'%' Show a Higher Expected Win Probablity for this Week's Games? --- According to Vegas, Yes")
    figExProbCurrent.show()


# event key and mouse pressed for interaction
def keyPressed(app, event):
    if (app.waitingForFirstKeyPress):
        app.waitingForFirstKeyPress = False
        
    elif (event.key == "r"):
        historyResults(app)

    elif (event.key == "c"):
        lineChanges(app)

    elif (event.key == "g"):
        seasonATSresults(app)

    elif (event.key == "o"):
        linesAndOdds(app)

    elif (event.key == "a"):
        analysisRegression(app)

    elif app.gameOver == True:
        if event.key == "q":
            # draw new board using method in appStarted()
            drawMainScreen(app, canvas)  

# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

def drawCell(app, canvas, row, col):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, x1, y0, y1)


# splash page for instructions how to use
def drawSplashPage(app, canvas):
    canvas.create_text(app.width//2, app.height//2, 
    text="WELCOME TO FEPO.bet!",
    font="Arial 32 bold")

    canvas.create_text(app.width//2, app.height//2+40, 
    text="Press any key to continue",
    font="Arial 20 bold")


def drawMainScreen(app, canvas):
    canvas.create_text(app.width//2, app.height//2, 
    text="FEPO.bet", 
    font="Arial 16 bold")
    
    canvas.create_text(app.width//2, app.height//2 + 15, 
    text="Press O to get latest odds, lines, spreads and totals", 
    font="Arial 16 bold")
    
    canvas.create_text(app.width//2, app.height//2 + 30, 
    text="Press G to get game summaries and team performances", 
    font="Arial 16 bold")

    canvas.create_text(app.width//2, app.height//2 + 45, 
    text="Press R to get game results and betting stats from previous seasons", 
    font="Arial 16 bold")

    canvas.create_text(app.width//2, app.height//2 + 60,
    text = "Press C to see the biggest changes in the line, spread, and total this week",
    font = "Arial 16 bold")

    canvas.create_text(app.width//2, app.height//2 + 75,
    text = "Press A for some dope analysis for your next winner",
    font = "Arial 16 bold")
    
    #canvas.create_text(app.width//2, app.height//2 + 90,
    #text = "Press Q to quit and return to the homepage (this page)",
    #font = "Arial 16 bold")

# need to figure out how to draw and print the actual stuff into the window

def redrawAll(app, canvas):
    if (app.waitingForFirstKeyPress):
        drawSplashPage(app, canvas)
    elif app.waitingForFirstKeyPress == False:
        drawMainScreen(app, canvas)
    else:
        pass

runApp(width=600, height=400)

## WooHoo! ##