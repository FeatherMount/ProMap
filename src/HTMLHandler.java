/*
 * This class is modified from the example class in Apache website. 
 * ====================================================================
 *
 * This software consists of voluntary contributions made by many
 * individuals on behalf of the Apache Software Foundation.  For more
 * information on the Apache Software Foundation, please see
 * <http://www.apache.org/>.
 *
 */
import java.io.IOException;
import java.io.PrintWriter;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.apache.commons.logging.LogFactory;
import org.apache.commons.logging.impl.*;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.message.BasicNameValuePair;
import java.util.LinkedList;
import java.util.ArrayList;
import java.util.List;
import org.apache.http.NameValuePair;
import java.io.File;
import java.lang.Thread;

public class HTMLHandler 
{
    private File idListFile;

    public HTMLHandler(String idListFilename) throws Exception
    {
        idListFile = new File(idListFilename);
    }

    private static final void downloadHTML(String pmcId) throws Exception 
    {
        // sample uri
        // http://www.ncbi.nlm.nih.gov/pmc/articles/PMC256976/
        CloseableHttpClient httpclient = HttpClients.createDefault();
        try 
        {
            String uri = "http://www.ncbi.nlm.nih.gov/pmc/articles/PMC" + pmcId  + "/";
            HttpGet httpget = new HttpGet(uri);

            System.out.println("Executing request " + httpget.getRequestLine());
            
            // Create a custom response handler
            ResponseHandler<String> responseHandler = new ResponseHandler<String>() 
            {

                @Override
                public String handleResponse(
                        final HttpResponse response) throws ClientProtocolException, IOException 
                {
                    int status = response.getStatusLine().getStatusCode();
                    if (status >= 200 && status < 300) 
                    {
                        HttpEntity entity = response.getEntity();
                        return entity != null ? EntityUtils.toString(entity) : null;
                    } else 
                    {
                        throw new ClientProtocolException("Unexpected response status: " + status);
                    }
                }

            };
            String responseBody = httpclient.execute(httpget, responseHandler);
            // continue writing here for HTML parsing
            //
            // interesting keyword = citation_authors
            //
            // continue here
        } 
        finally 
        {
            httpclient.close();
        }
    }

    public final void parseAllHTML () throws Exception
    {
        FileInputStream fis = new FileInputStream(idListFile);
        BufferedReader br = new BufferedReader(new InputStreamReader(fis));
        String pmcId = null;
        while ((pmcId = br.readLine()) != null)
        {
            downloadHTML(pmcId);
            try {
                Thread.sleep(400);
            } catch (InterruptedException ie){
                Thread.currentThread().interrupt();
                return;
            }
        }
    }
}
