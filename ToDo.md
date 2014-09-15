This file outlines the road map in achieving the web application ProMap. 

Steps: 
1) Data collection
-- Collecting all (as many as possible) PMCIDs through Entrez EUtil. 
http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=cell&retstart=1&retmax=100000


-- Retrieve all pages based on PMCIDs collected. Parse the XML data.
-- Items to collect: Author sequence per ID; Author names; Emails if exist; Publication date; Cited by number; Zipcode of affiliation
   Retrieve XML page and in-memory parsing. Append tables in mysql database. 
   Difficulties: name is not unique; emails can not be the key. (ignore for now)

2) Data processing
3) Server-side front-end
