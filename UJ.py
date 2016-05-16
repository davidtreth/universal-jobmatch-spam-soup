# -*- coding: utf-8 -*-
# David Trethewey
# 16-05-2016
# making Universal Jobmatch easier to read
# takes account of some changes in the HTML table from UJ -- May 2016

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

    there have been some changes to the format of Universal Jobmatch, as shown below.

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

    new format:
            <tr class="mobileTableBody">
               <td>
                    <div class="mobileTableTdContent">
                        <div class="mobileAltHeader">
                            <span id="MasterPage1_MainContent__ctlResultsFlatTrovix_rptResults__ctl1_msgDate2">Date</span>
                        </div>
                        <div class="mobileTd">
                            <a name="26643838"></a>
                            <span id="MasterPage1_MainContent__ctlResultsFlatTrovix_rptResults__ctl1_lblDate">09/05/2016</span>
                         </div>
                    </div>

                    <div class="mobileTableTdContent">
                        <div class="jobsSavedBy mobileAltHeader">
                            <span class="access"><span id="MasterPage1_MainContent__ctlResultsFlatTrovix_rptResults__ctl1_MONSMessage2">Jobs Saved by</span></span>
                        </div>
                        <div class="mobileTd">
                            
                            
                        </div>
                    </div>

                    <div class="mobileTableTdContent">
                        <div class="mobileAltHeader">
                            <span id="MasterPage1_MainContent__ctlResultsFlatTrovix_rptResults__ctl1_msgJobTitle2">Job title</span>
                        </div>
                        <div class="mobileTd">
                            <a id="MasterPage1_MainContent__ctlResultsFlatTrovix_rptResults__ctl1_lnkTitle" title="" href="http://jobsearch.direct.gov.uk/GetJob.ashx?JobID=26643838&amp;JobTitle=QA%20Software%20Tester&amp;AVSDM=2016-05-10T04%3a20%3a00-05%3a00">QA Software Tester</a>
                        </div>
                    </div>

                    <div class="mobileTableTdContent">
                        <div class="mobileAltHeader">
                            <span>Company</span>
                        </div>
                        <div class="mobileTd">
                            <span id="MasterPage1_MainContent__ctlResultsFlatTrovix_rptResults__ctl1_lblCompany">Headforwards Solutions Ltd</span>
                        </div>
                    </div>

                    <div class="mobileTableTdContent">
                        <div class="mobileAltHeader">
                            <span>Location</span>
                        </div>
                        <div class="mobileTd">
                            <span id="MasterPage1_MainContent__ctlResultsFlatTrovix_rptResults__ctl1_lblArea">SW-Redruth</span>
                            <span id="MasterPage1_MainContent__ctlResultsFlatTrovix_rptResults__ctl1_lblCity"></span>
                        </div>
                    </div>

               </td>
			</tr>
     """
    date = ""
    employer = ""
    location = ""
    joburl = ""
    jobtitle = ""
    for td in r.find_all('td'):
        #print(td)
        #print(td.contents)
        if (td.contents[0] != '\n' or len(td.contents) >1):
            linklist = td.find_all("a")
            # print("linklist={l}".format(l=linklist))
            if len(linklist)>0:
                # take account of change of format of universal jobmatch
                # the first <a> is empty, and the second contains the link
                i = linklist[1]
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
            #print("s={s}".format(s=spam))
            for i in spam:
                # these <span>s should be date
                # employer (or advertiser)
                # and location
                # use the 'id' tag in the span to check which one we are in
                # print(i)
                # take account of change of format of universal jobmatch
                # there are some <span>s without an id
                try:
                    if "lblDate" in i.get('id'):
                        date = i.string
                except:
                    date = ''
                try:
                    if "lblCompany" in i.get('id'):
                        employer = i.string
                except:
                    employer = ''
                try:
                    if "lblArea" in i.get('id'):
                        location = i.string
                except:
                    location = ''
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
    #print(tableheaders)
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

def readPage(page,q="*",t="*",loc="tr1",days=1,radiusM=20):
    if q=="*":
        kwordquery = ""
    else:
        kwordquery = "&q={q}".format(q=q)
    if t=="*":
        jtitlequery = ""
    else:
        jtitlequery = "&tjt={t}".format(t=t)
    urlUJ = "https://jobsearch.direct.gov.uk/JobSearch/PowerSearch.aspx?{jt}&tm={d}{kw}&where={w}&rad={rad}&sort=rv.dt.di&pp=25&rad_units=miles&pg={pg}".format(pg=str(page+1),w=str(loc),d=str(days),rad=str(radiusM),kw=kwordquery,jt=jtitlequery)    
    raw = urlopen(urlUJ).read()
    soup = BeautifulSoup(raw,"lxml")
    # print(raw)
    # print(soup.prettify())
    # print(soup.head)
    # print(soup.table.prettify())
    
    # pass nNewJobs up to getFromUJ to determine when to stop
    # after encountering page of duplicates
    if soup.table:
        # if there are no jobs, there isn't a <table>
        pagerowlist, nNewJobs = readTable(soup.table)
    else:
        pagerowlist, nNewJobs = [], -1
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
    # title row
    print("<tr class='titlerow'><th>Date</th><th>Job title</th><th>Advertiser</th><th>Location</th></tr>")

def printClosingRows(mode,nJobs):
    if mode == "html":        
        # number of jobs
        if nJobs > 0:
            print("<tr class='totalNjobs'><td></td><td>Total number of jobs found: {n}</td><td></td><td></td>".format(n=nJobs))
        # closing tagline
        print("<tr class='closingrow'><td></td><td>Created using <a href='https://bitbucket.org/davidtreth/universal-jobmatch-spam-soup'>Universal Jobmatch Spam Soup</a>.</td><td></td><td></td></tr>")
        printHTMLEnd()
    else:
        if nJobs > 0:
            print("\t\tTotal number of jobs found: {n}\t\t".format(n=nJobs))
        print("Created using Universal Jobmatch Spam Soup\thttps://bitbucket.org/davidtreth/universal-jobmatch-spam-soup")

def printHTMLEnd():
    """ print closing HTML boilerplate """
    print("</table>")
    print("</body>")
    print("</html>")

def getFromUJ(q="*",t="*",loc="tr1",days=1,npages=20,radiusM=20,mode="html"):
    """ This function queries Universal Jobmatch and prints it as a HTML table to standard output 

    Redirect the output to an HTML file as follows
    usage: python <optional arguments> UJ.py > file.html
    type "python --help UJ.py" for details of the optional arguments """

    # counter variable for total number of jobs found
    totalNjobs = 0

    if mode == "html":
        printHTMLIntro()
        # subtitle row
        print("<tr class='subt'><th>Last {d} days</th><th>Query: job title = '{t}', keyword = '{q}'</th><th></th><th>up to {r} miles from {l}</th></tr>".format(d=days,t=t,q=q,r=radiusM,l=loc))
    else:
        print("Date\tURL\tJob title\tAdvertiser\Location")
        print("Last {d} days\t\tQuery: job title = '{t}', keyword = '{q}'\t\tup to {r} miles from {l}".format(d=days,t=t,q=q,r=radiusM,l=loc))
    for page in range(npages):
        # print("Page {p}".format(p=page))
        pagerowlist, nNewJobs = readPage(page,q,t,loc,days,radiusM)
        if nNewJobs == -1:
            # if there are no jobs, print a message
            if mode == "html":
                print("<tr class='deadparrot'><td></td><td>No jobs! The economic recovery is an ex-parrot! It has ceased to be!</td><td></td><td></td></tr>")
            else:
                print("No jobs! The economic recovery is an ex-parrot! It has ceased to be!")
            break

        # add to counter variable to count total number
        totalNjobs += nNewJobs

        if nNewJobs == 0:
            # if they are only duplicates, stop
            break
        for job in pagerowlist:
            if mode == "text":
                job.printTableRow()
            else:
                job.printHTMLTableRow()            
    printClosingRows(mode,totalNjobs)

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
                        help="Specify skills/keyword search query (default is *).",
                        default="*")
    parser.add_argument("-t", "--jobtitle", type=str,
                        help="Specify job title search query (default is *).",
                        default = "*")
    parser.add_argument("-n", "--npages", type=int,
                        help="Specify number of pages (default is 20). It will stop anyway after a full page of duplicates.",
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
    getFromUJ(q=args.query,t=args.jobtitle,loc=args.postcode,days=args.days,npages=args.npages,radiusM=args.radius,mode=args.mode)
