import mechanize
br = mechanize.Browser()

LOGIN_URL = "https://gezer1.bgu.ac.il/teva/scomp.php"
ENTRANCE_URL = "https://gezer1.bgu.ac.il/meser/entrance.php"
CRS_URL = "https://gezer1.bgu.ac.il/teva/crslist.php"
loginPage = br.open(LOGIN_URL)
br.select_form(nr=0)
br["uname"]= "navatm"
br["passwd"]= "timP28gu"
br["id"] = "301227146"
iAgreePage = br.submit()
iAgreeHtml = iAgreePage.read()

br.select_form(nr=0)

# TODO check successful result
examsPage = br.submit()

req = br.request

# Pull the session information
headers = req.header_items()
data = req.data

del br
del req

# TODO store headers and data

# Build a new request
req = mechanize.Request(CRS_URL, " ")

for (header_name, header_value) in headers:
    req.add_header(header_name, header_value)
req.data = data

# Send the new request
res = mechanize.urlopen(req)

# Print the result
print res.read()
