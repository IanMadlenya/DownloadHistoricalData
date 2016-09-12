#
# Copyright (c) 2016 Yatpang Cheung. All rights reserved.
#

# imports
import urllib
import requests

#local paths to store data, change to local setting and create the folders
exchangeDataBase = '/Users/.../exchangeData/'
equitiesDataBase = '/Users/.../equitiesData/'

# NASDAQ link, can adjust additional parameters here
downloadLinkA = 'http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&marketcap='
downloadLinkB = '&country=United%20States&render=download'

# Yahoo Finance historical data
yahooFinance = 'http://ichart.finance.yahoo.com/table.csv?s='

# download the file at a particular url and saves it to filename
def downloadFile(url, filename):
    urllib.urlretrieve(url, filename)

# retrieves the data for some categories of stock universe
# getHistorical = True if you want to retrieve historical data as well
def getData(allCat, getHistorical):

    #csv file of all tickers and all columns
    allFile = open(exchangeDataBase+'All.csv', 'w')

    #text file of tickers with market cap and sector
    tickerFile = open(exchangeDataBase+'Tickers.txt', 'w')

    tracker = 0

    for cat in allCat:
        downloadFile(downloadLinkA+cat+downloadLinkB, exchangeDataBase+cat+'.csv')

        with open(exchangeDataBase+cat+'.csv') as f:
            content = f.read()

            for line in content.split('\n')[1:]:
                if line != '':
                    lineTemp = line[1:]
                    lineTemp = lineTemp[:-2]
                    col = lineTemp.split('","')

                    # clean up data and exclude ETFs and funds
                    if(col[7] != 'n/a' and col[8] != 'n/a' and float(col[2]) > 0.0 and float(col[3])> 0.0):
                        allFile.write(line+'\n')
                        marketcap = float(col[3])
                        tickerFile.write(col[0]+' '+col[3]+' '+col[7]+'\n')

                        # downloads historical data if true
                        if(getHistorical):
                            downloadFile(yahooFinance+col[0], equitiesDataBase+col[0]+'.csv')
                            tracker = tracker + 1
                            print "Count: "+str(tracker)+"."+" Ticker Downloaded: "+col[0]+'\n'

    allFile.close()
    tickerFile.close()

if __name__ == '__main__':

    # by market cap
    # comment out what is not needed 
    allCat = []
    allCat.append('Mega-cap')
    allCat.append('Large-cap')
    allCat.append('Mid-cap')
    allCat.append('Small-cap')
    allCat.append('Micro-cap')
    allCat.append('Nano-cap')

    # True to retrieve historical data as well for each ticker
    getData(allCat, True)

