Universal Jobmatch Spam Soup
univeral-jobmatch-spam-soup
----------------------------
Written by David Trethewey
----------------------------

This is a command-line Python script to read the UK Department
of Work and Pensions <a href="https://jobsearch.direct.gov.uk">Universal Jobmatch</a> website, and convert
the information from a series of pages one has to click through,
to a single HTML table.

Specify the desired location, skills/keywords query, days before present,
and search distance as command line arguments.

usage: python <optional arguments> UJ.py > file.html  
type "python --help UJ.py" for details of the optional arguments

The UJ.css file contains a basic css style for the output HTML file

This program is licensed under the GNU General Public License.
Provided as is, with no warranty of any kind.