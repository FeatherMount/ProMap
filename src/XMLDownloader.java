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
import java.util.List;
import org.apache.http.NameValuePair;

public class XMLDownloader 
{
    public static final void downloadXML(String journalName, int restart, int retmax) throws Exception 
    {
        journalName = journalName.replace(' ', '+');
        CloseableHttpClient httpclient = HttpClients.createDefault();
        try 
        {
            NameValuePair dbQuery = new BasicNameValuePair("db", "pmc");
            NameValuePair termQuery = new BasicNameValuePair("term", journalName);
            NameValuePair restartQuery = new BasicNameValuePair("restart", Integer.toString(restart));
            NameValuePair retmaxQuery = new BasicNameValuePair("retmax", Integer.toString(retmax));
            List<NameValuePair> queryList = new LinkedList<NameValuePair>();
            queryList.add(dbQuery);
            queryList.add(termQuery);
            queryList.add(restartQuery);
            queryList.add(retmaxQuery);
            
            URIBuilder uriBuilder = new URIBuilder()
                .setScheme("http")
                .setHost("eutils.ncbi.nlm.nih.gov")
                .setPath("/entrez/eutils/esearch.fcgi")
                .setParameters(queryList);
            String uri = uriBuilder.toString();
            System.out.println(uri);
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
            System.out.println("----------------------------------------");
            System.out.println(responseBody);
        } 
        finally 
        {
            httpclient.close();
        }
    }

}

