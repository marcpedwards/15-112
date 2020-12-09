Description:

FEPO.bet (For Educational Purposes Only) is the newest sports betting aide to hit the market. Most sports betting sites only offer places to make bets, but none offer insights and analysis of the teams that you want to bet on. With this betting aide, it will be possible for patrons to see the mainstays of sports betting (spread, total, ML) and get information and statistics to aid in their betting decisions such as Implicit Probability, Explicit Probability, and Edge %. There is also an added element of analysis that includes regression modeling to see if there are relationships between certain aspects of betting (historical edge% predicted by ML colored by WinLoss, relationship of current explicit probability and its relationship to the edge%, and more) and visuals that can lead patrons to conclusions based on results.

This is not a sports betting app, it is a platform that shows the spread, total, and ML odds and payouts with the additional statistical analysis. The games included in this platform will be from the National Football League. 

**DISCLAIMER**
Sports gambling is not legal in every state and/or territory and this project is for educational purposes only. You must be 21+ to gamble. If you or a loved has a gambling problem please call 1-800-GAMBLER

————————————————————————

How to Run:

This is a very simple app to run. First, ensure you have all the files from the .zip downloaded and in the same directory. Also be sure all required modules and libraries are adequately installed from within your computer’s terminal (all modules and packages are listed below). The .zip contains any outside data that is included and is imperative for a successful running. 

Once opened, run the tp3.py file. This will make several things happen. 2 eternal windows will open. One for the window of the app itself and one to an external browser, which will display the graphs. All graphs are clearly labeled and explain what is going on inside the browser. 

As for the app window, there are several commands listed on the window explaining several key presses. These key presses control the different parts of the analysis. You can press the keys to see the output of all the analyzed and manipulated data that includes the Implicit Probability, Explicit Probability, and Edge %. There are also key presses that includes the spread, total, and ML for all of the week’s upcoming games, and the results against the spread and other key stats. 

————————————————————————

Libraries and Modules:
To install, go to terminal and type ‘pip install nameOfLibrary’

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

————————————————————————

Shortcut commands:

None


