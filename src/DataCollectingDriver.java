public class DataCollectingDriver
{
    public static void main(String[] args) throws Exception
    {
        //String journalListFile = "../resource/NIH_PA_journal_list_March_2014.csv";
        //CSVParser.parseCsvFile(journalListFile);
        XMLDownloader.downloadXML("Nature", 1, 10);
    }
}
