import xml.etree.ElementTree as etree

# define isEmpty function to check if any object is empty
def isEmpty(obj):
    if (obj): return False
    else: return True

def parse(filename):
    """
    Takes the xml filename as input and returns a tuple 
    with pmcId, authorlist, and corresponding author  
    """

    #filename = '../resource/AAPS_J_2010_Oct_19_12(4)_716-728.nxml'
    tree = etree.parse(filename)
    root = tree.getroot()
    # according to the structure of the xml article meta nested under 
    # front then article-meta
    articleMeta = root[0][1]
    # pubmed central article id
    pmcId = ''
    # the author list, the list of names
    authors = []
    # the name and email of one of the corresponding authors
    cAuthor = {'name': ' ', 'email': ' '}

    for child in articleMeta:
        # find the pmc id
        if ((child.tag == 'article-id') and not(isEmpty(child.attrib))):
            if (child.attrib['pub-id-type'] == 'pmc'):
                pmcId = child.text
        # find the author group
        elif (child.tag == 'contrib-group'):
            authorGroup = child
    
    # parse author group information
    for child in authorGroup:
        if (child.tag == 'contrib' and child.attrib['contrib-type'] == 'author'):
            # the first child is the name tag
            name = child[0].find('given-names').text + ' ' \
                    + child[0].find('surname').text
            authors.append(name)
            # if it is corresponding author log it
            if ('corresp' in child.attrib and child.attrib['corresp'] == 'yes'):
                cAuthor['name'] = name
                cAuthor['email'] = child[1].find('email').text
    return (pmcId, authors, cAuthor)

if __name__ == '__main__':
    parse('../resource/AAPS_J_2010_Oct_19_12(4)_716-728.nxml')
