import xml.etree.ElementTree as etree

# define isEmpty function to check if any object is empty
def isEmpty(obj):
    if (obj): return False
    else: return True

def parse(filename):
    """
    Takes the xml filename as input and returns a tuple 
    with pmcId, other author list, corresponding author, 
    and date of publication  
    """

    #filename = '../resource/AAPS_J_2010_Oct_19_12(4)_716-728.nxml'
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
    
    for child in articleMeta:
        # find the pmc id
        if ((child.tag == 'article-id') and not(isEmpty(child.attrib))):
            if (child.attrib['pub-id-type'] == 'pmc'):
                pmcId = child.text
        # find the author group
        elif (child.tag == 'contrib-group'):
            authorGroup = child
        # find the publication date
        elif (child.tag == "history"):
            for date in child:
                if (date.attrib['date-type'] == 'accepted'):
                    #publiction date YEAR MONTH DAY
                    publicationDate = (date.find('year').text, \
                            date.find('month').text, date.find('day').text)
    
    # parse author group information
    for child in authorGroup:
        if (child.tag == 'contrib' and child.attrib['contrib-type'] == 'author'):
            # the first child is the name tag
            name = child[0].find('given-names').text + ' ' \
                    + child[0].find('surname').text
            if ('corresp' in child.attrib and child.attrib['corresp'] == 'yes'):
                # if it a corresponding author
                data = (name, child[1].find('email').text)
                cAuthors.append(data)
            else:
                # if not a corresponding author
                otherAuthors.append(name)
    print(pmcId, otherAuthors, cAuthors, publicationDate)
    return(pmcId, otherAuthors, cAuthors, publicationDate)

if __name__ == '__main__':
    parse('../resource/AAPS_J_2010_Oct_19_12(4)_716-728.nxml')
