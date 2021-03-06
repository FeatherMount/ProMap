import xml.etree.ElementTree as etree
from datetime import date 

# define isEmpty function to check if any object is empty
def isEmpty(obj):
    if (obj): return False
    else: return True

# find all the elements with the tag of tagname
# return a list of matching elements
def findInSubtree(element, tagname):
    result = []
    if (element.tag == tagname):
        result.extend([element])
    if (len(element) > 0):
        for child in element:
            result.extend(findInSubtree(child, tagname))
        return result
    return result



def parse(filename):
    """
    Takes the xml filename as input and returns a tuple 
    with pmcId, other author list, corresponding author, 
    and date of publication  
    """

    tree = etree.parse(filename)
    root = tree.getroot()
    # according to the structure of the xml article meta nested under 
    # front then article-meta
    articleMeta = root[0][1]
    # pubmed central article id
    pmcId = ''
    # the author list, the list of names excluding corresponding
    # athor
    otherAuthors = []
    # the name and email of the corresponding authors
    cAuthors = []
    # container for all the author groups
    authorGroups = []
    
    for child in articleMeta:
        # find the pmc id
        if ((child.tag == 'article-id') and not(isEmpty(child.attrib))):
            if (child.attrib['pub-id-type'] == 'pmc'):
                pmcId = child.text
        # find the author group
        elif (child.tag == 'contrib-group'):
            authorGroups.append(child)
        # this child may contain important corresponding information
        elif (child.tag == 'author-notes'):
            authorNotes = child
        # find the publication date
        elif (child.tag == 'history'):
            for theDate in child:
                if ('date-type' in theDate.attrib and theDate.attrib['date-type'] == 'accepted'):
                    #publiction date YEAR MONTH DAY
                    if (theDate.find('year') != None):
                        theYear = theDate.find('year').text
                    else:
                        theYear = 0	
                    if (theDate.find('month') != None):
                        theMonth = theDate.find('month').text
                    else:
                        theMonth = 6
                    if (theDate.find('day') != None):
                        theDay = theDate.find('day').text
                    else:
                        theDay = 1

                    publicationDate = (theYear, theMonth, theDay)
                    try:
                        dateCheck = date(int(theYear), int(theMonth), int(theDay))
                    except:
                        return((-1,))
        elif (child.tag == 'pub-date'):    
            if ('pub-type' in child.attrib and (child.attrib['pub-type'] == 'ppub' or child.attrib['pub-type'] == 'epub')):
                #for grandchild in child: print(grandchild.tag)
                
                if (child.find('year') != None):
                    theYear = child.find('year').text
                else:
                    theYear = 0
                
                if (child.find('month') != None):
                    theMonth = child.find('month').text
                else:
                    theMonth = 6
                
                if (child.find('day') != None):
                    theDay = child.find('day').text
                else:
                    theDay = 1					
                publicationDate = (theYear, theMonth, theDay)
                try:
                    dateCheck = date(int(theYear), int(theMonth), int(theDay))
                except:
                    return((-1,))
    case1 = False  # will be used for post-processing, corr author identified but no email
    for authorGroup in authorGroups:
        # parse author group information
        for child in authorGroup:
            if (child.tag == 'contrib' and child.attrib['contrib-type'] == 'author'):
                # the first child is the name tag
                try:
                    name = child[0].find('given-names').text + ' ' + child[0].find('surname').text
                except:
                    return((-1,))
                if ('corresp' in child.attrib): # and child.attrib['corresp'] == 'yes'):
                    # if it a corresponding author
                    # check to see if there is email field
                    if (len(child) > 2 and child[1].find('email') != None):
                        data = (name, child[1].find('email').text)
                        cAuthors.append(data)
                    #else post-process this case: case(1)
                    else:
                        data = (name, 'null')
                        cAuthors.append(data)
                        case1 = True
                else: 
                    # handle EMBO style xml 
                    xrefList = findInSubtree(child, 'xref')
                    if (len(xrefList) > 0):
                        for xref in xrefList:
                            if ('ref-type' in xref.attrib and xref.attrib['ref-type'] == 'corresp'):
                                # this is an corresponding author
                                data = (name, '')
                                cAuthors.append(data)
                                case1 = True
                        if (case1 == False):
                            otherAuthors.append(name)    
                    else:
                        # if not a corresponding author
                        otherAuthors.append(name)

    # not done yet, some corresponding author information are embedded in author-notes
    if (case1 and 'authorNotes' in locals()):
        i = 0
        # corresponding author identified but no email found
        for child in authorNotes:
            if (child.tag == 'corresp'):
                for grandchild in child:
                    if (grandchild.tag == 'email'):
                        if (i == len(cAuthors)): break	
                        cAuthors[i] = (cAuthors[i][0], grandchild.text)
                        i = i + 1
    elif ('authorNotes' in locals()):
        # the linking information is embedded entirely in the text
        text = etree.tostring(authorNotes).strip().decode('utf-8')
        emailElements = findInSubtree(authorNotes, 'email')
        for name in otherAuthors:
            j = 0
            if (text.find(name) != -1 and j < len(emailElements)):
                data = (name, emailElements[j].text)
                cAuthors.append(data)
                otherAuthors.remove(name)
                j = j + 1

    # sanity check here, reject anything that may corrupt the database
    if ('pmcId' in locals() and 'publicationDate' in locals()):
        try:
            print(pmcId, otherAuthors, cAuthors, publicationDate)
        except:
            return(pmcId, otherAuthors, cAuthors, publicationDate)
        return(pmcId, otherAuthors, cAuthors, publicationDate)
    else:
        return((-1,))

if __name__ == '__main__':
    parse('../resource/EMBO_J_2009_Oct_7_28(19)_3027-3039.nxml')
    parse('../resource/AAPS_J_2010_Oct_19_12(4)_716-728.nxml')
    parse('../resource/Acad_Emerg_Med_2008_Apr_15(4)_305-313.nxml')
    parse('../resource/ACS_Nano_2010_Dec_28_4(12)_7630-7636.nxml')
    parse('../resource/Cancer_Biol_Med_2012_Jun_9(2)_85-89.nxml')
    parse('../resource/EMBO_J_2009_Oct_7_28(19)_3027-3039.nxml')
    parse('../resource/Open_Biochem_J_2008_Apr_29_2_49-59.nxml')
