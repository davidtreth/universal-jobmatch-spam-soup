# -*- coding: utf-8 -*-
# David Trethewey
# 28-08-2015
# making Universal Jobmatch easier to read
from bs4 import BeautifulSoup
from urllib import urlopen
# Import the python Argument parser
import argparse
import copy

# urllist is to keep track of the job URLs to stop once duplicates are encountered
urllist = []

class Job:
    """
    structure to define attributes of a job advertised on UJ
    """
    def __init__(self, date, URL, title, employer, location):
        """Create a job!"""
        self.date = date
        self.URL = URL
        self.title = title
        self.employer = employer
        self.location = location

    def jobLink(self):
        """ Make the HTML for the link to the advert to go in the table
        such that clicking on the job title takes you to the job ad """
        self.jobLink = u'<a href="'+self.URL+u'">'+self.title+u'</a>'

    def textTableRow(self):
        """ create plain text tab separated table row"""
        trow = self.date + "\t" + self.URL+ "\t"+ self.title + "\t" + self.employer + "\t" + self.location
        self.textrow = trow.encode("utf-8")

    def printTableRow(self):
        """ print plain text version  of table row """
        self.textTableRow()
        print(self.textrow)

    def HTMLTableRow(self):
        """ create HTML version of table row """
        self.jobLink()
        trow = "<tr>" + "<td>"+self.date + "</td><td>" + self.jobLink + "</td><td>" + self.employer + "</td><td>" + self.location+"</td>"+"</tr>"        
        self.htmlrow = trow.encode("utf-8")

    def printHTMLTableRow(self):
        """ print HTML version of table row """
        self.HTMLTableRow()
        print(self.htmlrow)

    
def readRow(r):
    """ read a row and return it as a Job object

    note - a row will contain several <td> tags
    one will have an empty <a> tag and a <span> containing the date
    next will be empty
    then will get a <td> containing an <a> with url and job title
    then another <td> with a <span> containing the employer/advertiser
    then another <td> with 2 <span>s in containing location, though only one usually used

    Example:
    <tr>
    <td>
    <a name="18569396"></a>
    <span id="MasterPage1_MainContent__ctlResultsFlatTrovix_rptResults__ctl3_lblDate">28/08/2015</span>
    </td>
    <td></td>
    <td><a id="MasterPage1_MainContent__ctlResultsFlatTrovix_rptResults__ctl3_lnkTitle" title="" href="
    http://jobsearch.direct.gov.uk/GetJob.ashx?JobID=18569396&amp;JobTitle=Archive%20Services%20Manager">Archive Services Manager</a></td>
    <td><span id="MasterPage1_MainContent__ctlResultsFlatTrovix_rptResults__ctl3_lblCompany">Cornwall Council</span></td>
    <td><span id="MasterPage1_MainContent__ctlResultsFlatTrovix_rptResults__ctl3_lblArea">SW-Truro</span>
    <span id="MasterPage1_MainContent__ctlResultsFlatTrovix_rptResults__ctl3_lblCity"></span>
    </td>
    </tr>
     """
    date = ""
    employer = ""
    location = ""
    joburl = ""
    jobtitle = ""
    for td in r.find_all('td'):
        # print(td)
        # print(td.contents)
        if (td.contents[0] != '\n' or len(td.contents) >1):
            linklist = td.find_all("a")
            # print("linklist={l}".format(l=linklist))
            # there should be only one <a> in a <td>
            # which will either be empty or contain the job URL and title
            if len(linklist)>0:
                i = linklist[0]
                # i.string is the job title
                # get the URL by i.get('href')
                if i.string is not None:
                    joburl = i.get('href')
                    joburl = str(joburl).split("&")[0] # get rid of all the referrer stuff at end of URL we don't need
                    # print(joburl)
                    if joburl in urllist:
                        # if this is a duplicate of a URL seen already 
                        # print("repeat URL")
                        return None
                    else:
                        # print("new URL")
                        # add to the list to spot duplicates
                        urllist.append(joburl)
                        jobtitle = i.string
            # find the <span>s 
            spam = td.find_all("span")
            # print("s={s}".format(s=s))
            for i in spam:
                # these <span>s should be date
                # employer (or advertiser)
                # and location
                # use the 'id' tag in the span to check which one we are in
                if "Date" in i.get('id'):
                    date = i.string
                if "Company" in i.get('id'):
                    employer = i.string
                if "Area" in i.get('id'):
                    location = i.string
                # NB, the <span> with the "City" in the id is assumed to always be empty

        else:
            # if the <td> is empty
            # do nothing
            pass
    if joburl != "":
        """ if there is a URL for the advert, create a Job and return it """
        return Job(date,joburl,jobtitle,employer,location)
    else:
        return None

def readTable(jobtable):
    """ read the table, do the headers separately, then the rest """
    tablerowlist = []
    tableheaders = jobtable.find_all('th')
    # print(tableheaders)
    thlist = [] 
    for h in tableheaders:
        content = h.span.string
        # print(content)
        thlist.append(content)
    tablerows = jobtable.find_all('tr')
    joblist = [readRow(r) for r in tablerows]
    # filter out None Job s
    joblist = [j for j in joblist if j]
    
    nNewJobs = len(joblist)
    """ if there are no new jobs then we've exhausted them
    and reached a page full of duplicates
    of ones that appeared in earlier pages """
    return joblist,nNewJobs

def readPage(page,q="*",loc="tr1",days=1,radiusM=20):
    if q=="*":
        urlUJ = "https://jobsearch.direct.gov.uk/JobSearch/PowerSearch.aspx?pp=25&pg={pg}&where={w}&sort=rv.dt.di&rad={rad}&rad_units=miles&re=134&tm={d}".format(pg=str(page+1),w=str(loc),d=str(days),rad=str(radiusM))    
    else:
        urlUJ = "https://jobsearch.direct.gov.uk/JobSearch/PowerSearch.aspx?pp=25&pg={pg}&q={q}&where={w}&sort=rv.dt.di&rad={rad}&rad_units=miles&re=134&tm={d}".format(pg=str(page+1),w=str(loc),d=str(days),rad=str(radiusM),q=str(q))    
    raw = urlopen(urlUJ).read()
    soup = BeautifulSoup(raw)
    # print(raw)
    # print(soup.prettify())
    # print(soup.head)
    # print(soup.table.prettify())
    
    # pass nNewJobs up to getFromUJ to determine when to stop
    # after encountering page of duplicates
    pagerowlist, nNewJobs = readTable(soup.table)
    return pagerowlist, nNewJobs
    

def printHTMLIntro():
    """ print opening HTML boilerplate """
    print("<!DOCTYPE html>")
    print("<html>")
    print("<head>")
    print("<meta charset='UTF-8'>")
    print("<title>UJ</title>")
    print("<link href='UJ.css' rel='stylesheet' type='text/css' media='all'>")
    print("</head>")
    print("<body>")
    print("<table>")
    print("<tr><th>Date</th><th>Job title</th><th>Advertiser</th><th>Location</th></tr>")

def printHTMLEnd():
    """ print closing HTML boilerplate """
    print("</table>")
    print("</body>")
    print("</html>")

    
def getFromUJ(q="*",loc="tr1",days=1,npages=20,radiusM=20,mode="html"):
    """ This function queries Universal Jobmatch and prints it as a HTML table to standard output 

    Redirect the output to an HTML file as follows
    usage: python <optional arguments> UJ.py > file.html
    type "python --help UJ.py" for details of the optional arguments """

    if mode == "html":
        printHTMLIntro()
    
    for page in range(npages):
        #print("Page {p}".format(p=page))
        pagerowlist, nNewJobs = readPage(page,q,loc,days,radiusM)
        if nNewJobs == 0:
            # if they are only duplicates, stop
            break
        for job in pagerowlist:
            if mode == "text":
                job.printTableRow()
            else:
                job.printHTMLTableRow()            
    if mode == "html":
        printHTMLEnd()
    
if __name__ == '__main__':
    """ Create the command line options with ArgumentParser. """
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--postcode", type=str,
                        help="Specify the central search postcode (default is TR1).", 
                        default="TR1")
    parser.add_argument("-r", "--radius", type=int,
                        help="Specify search radius in miles (default is 20).",
                        default=20)
    parser.add_argument("-q", "--query", type=str,
                        help="Specify search query keyword (default is *).",
                        default="*")
    parser.add_argument("-n", "--npages", type=int,
                        help="Specify number of pages (default is 20).",
                        default=20)
    parser.add_argument("-d", "--days", type=int,
                        help="Specify number of days to search back (default is 1 - i.e. posted today or yesterday).",
                        default=1)
    parser.add_argument("-m", "--mode", type=str,
                        help="Specify mode - text seperated by tab or HTML (default is HTML).",
                        default="html")
    # Call the parser to parse the arguments.
    args = parser.parse_args()
    args.postcode = args.postcode.replace(" ","%20")
    getFromUJ(q=args.query,loc=args.postcode,days=args.days,npages=args.npages,radiusM=args.radius,mode=args.mode)
