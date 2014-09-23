import java.io.PrintWriter;
import java.io.File;
import java.util.ArrayList;
import java.io.IOException;
public class PMCIdRetriever
{
    public static void main(String[] args) throws Exception
    {
        File PMCIdList = new File("../resource/PMCIdList.dat");
        PrintWriter pw = new PrintWriter (PMCIdList);
        try
        {
            File folder = new File("../resource/xml/");
            for (File fileEntry : folder.listFiles())
            {
                XMLParser xp = new XMLParser(fileEntry.getCanonicalPath());
                ArrayList<String> idList = xp.getIdList();
                for (String id : idList)
                    pw.println(id);
            }
        }
        catch (IOException ioe)
        {
           ioe.printStackTrace();
        }
        
        finally
        {
            pw.close();
        }
    }
}
