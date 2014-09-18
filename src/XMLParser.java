import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
public class XMLParser
{
    private ArrayList<String> idList;
    private String filename;
    private Document dom;

    public XMLParser(String filename)
    {
        this.filename = filename;
        idList = new ArrayList<String>();
    }

    public int getTotalRecordCount()
    {
        parseXmlFile();
        // get the root element
        Element docEle = dom.getDocumentElement();

        // get value of the root with tag <Count>
        NodeList nl = docEle.getElementsByTagName("Count");
        if (nl != null && nl.getLength() > 0)
        {
            Element ele = (Element) nl.item(0);
            return Integer.parseInt(ele.getFirstChild().getNodeValue());
        }
        else
        {
            return -1;
        }
    }

    private void parseXmlFile()
    {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        try
        {
            DocumentBuilder db = dbf.newDocumentBuilder();
            dom = db.parse(filename);
        }
        catch (ParserConfigurationException pce)
        {
            pce.printStackTrace();
        }
        catch (SAXException se)
        {
            se.printStackTrace();
        }
        catch (IOException ioe)
        {
            ioe.printStackTrace();
        }
    }

    public ArrayList<String> getIdList()
    {
        parseXmlFile();
        // get the root element
        Element docEle = dom.getDocumentElement();
        // get the nodelist of <IdList>
        NodeList nlIdList = docEle.getElementsByTagName("IdList");
        if (nlIdList != null && nlIdList.getLength() > 0)
        {
            Element eleIdList = (Element) nlIdList.item(0);
            // get the nodelist of <Id>
            NodeList nlId = eleIdList.getElementsByTagName("Id");
            if (nlId != null && nlId.getLength() > 0)
            {
                for (int i = 0; i < nlId.getLength(); i++)
                {
                    // get the id element
                    Element eleId = (Element) nlId.item(i);
                    // get the value of the id element
                    String id = eleId.getFirstChild().getNodeValue();
                    idList.add(id);
                }
            }
        }
        return idList;
    }
}
