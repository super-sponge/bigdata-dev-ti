import java.sql.*;

/**
 * Created by sponge on 2016/11/30 0030.
 */
public class HiveJdbcApi {
    private static String driverName = "org.apache.hive.jdbc.HiveDriver";//jdbc驱动路径
    private static String url = "jdbc:hive2://10.183.5.11:11001/ods_ceshi";//hive库地址+库名
    private static String user = "ods_ceshi";//用户名
    private static String password = "ods_ceshi";//密码
    private static String sql = "";
    private static ResultSet res;

    public static void main(String[] args) {
       String sql = "select * from tmp_test1";
       executeQueryResult(sql);
    }

    private static Connection getConn() throws ClassNotFoundException,
            SQLException {
        Class.forName(driverName);
        Connection conn = DriverManager.getConnection(url, user, password);
        return conn;
    }

    private static void executeQueryResult(String sql) {
        Connection conn = null;
        Statement stmt = null;
        try {
            conn = getConn();
            stmt = conn.createStatement();
            System.out.println("运行:" + sql);
            res = stmt.executeQuery(sql);
            System.out.println("执行 " + sql +" 运行结果");
            while (res.next()) {
                System.out.println(res.getInt(1) + "\t" + res.getString(2));
            }

        } catch (ClassNotFoundException e) {
            e.printStackTrace();
            System.exit(1);
        } catch (SQLException e) {
            e.printStackTrace();
            System.exit(1);
        } finally {
            try {
                if (stmt != null) {
                    stmt.close();
                    stmt = null;
                }
                if (conn != null) {
                    conn.close();
                    conn = null;
                }
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}
