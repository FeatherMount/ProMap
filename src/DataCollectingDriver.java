import au.com.bytecode.opencsv.CSVReader;
import java.io.FileReader;
import java.util.ArrayList;
public class DataCollectingDriver
{
    public static void main(String[] args) throws Exception
    {
        String journalListFile = "../resource/NIH_PA_journal_list_March_2014.csv";
        CSVReader reader = new CSVReader(new FileReader(journalListFile));
        String [] nextLine;
        ArrayList<String> journalNames = new ArrayList<String>();
        while ((nextLine = reader.readNext()) != null)
            journalNames.add(nextLine[0]);
        //XMLDownloader.downloadXML("Nature", 1, 10);
    }
}
