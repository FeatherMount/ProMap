import java.sql.*;
public class DatabaseManager
{
    private String url;
    private String username;
    private String password;

    public DatabaseManager(String url, String username, String password)
    {
        this.url = url;
        this.username = username;
        this.password = password;
    }

    public void addToTable(String tableName, String pmcId, String authorList, String citedBy, String publicationDate)
    {
        Connection conn = null;
        Statement stment = null;
        try{
            // instantiate a connection
            conn = DriverManager.getConnection(url, username, password);
            // make a statement
            stment = conn.createStatement();
            // execute a query
            StringBuilder sb = new StringBuilder();
            sb.append("insert into " + tableName + " ");
            sb.append("(PmcId, AuthorList, CitedBy, PublicationDate)");
            sb.append("values (" + pmcId +", " + authorList + ", " + citedBy + ", " + publicationDate + ")");
            String sql = new String(sb);
            stment.executeUpdate(sql);
        }catch (SQLException e){
            e.printStackTrace();
        }finally{
            try{
                if (stment != null) 
                    stment.close();
            }catch (SQLException se){}
            try{
                if (conn != null)
                    conn.close();
            }catch (SQLException se){}
        }
    }
}
