import com.google.common.base.Charsets;
import com.stumbleupon.async.Callback;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.zookeeper.ZKConfig;
import org.hbase.async.GetRequest;
import org.hbase.async.HBaseClient;
import org.hbase.async.KeyValue;
import org.hbase.async.PutRequest;

import java.util.ArrayList;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Created by sponge on 2016/12/27 0027.
 */
public class HBaseAsyncAPI {
    public static final String DEFAULT_ZK_DIR="/hbase";

    private HBaseClient hBaseClient;
    private String tableName;
    private String colFamily;
    private String zkQuorum;

    public HBaseAsyncAPI(String tableName, String colFamily, String zkQuorum) {
        this.tableName = tableName;
        this.colFamily = colFamily;
        this.zkQuorum = zkQuorum;
    }

    public void init() throws Exception {
        if (zkQuorum == null || zkQuorum.isEmpty()) {
            Configuration conf = HBaseConfiguration.create();
            zkQuorum = ZKConfig.getZKQuorumServersString(conf);
        }

        hBaseClient = new HBaseClient(zkQuorum, DEFAULT_ZK_DIR, Executors.newCachedThreadPool());

        final CountDownLatch latch = new CountDownLatch(1);
        final AtomicBoolean fail = new AtomicBoolean(false);

        hBaseClient.ensureTableFamilyExists(tableName, colFamily).addCallbacks(
                new Callback<Object, Object>() {
                    @Override
                    public Object call(Object arg) throws Exception {
                        latch.countDown();
                        return null;
                    }
                },
                new Callback<Object, Object>() {
                    @Override
                    public Object call(Object arg) throws Exception {
                        fail.set(true);
                        latch.countDown();
                        return null;
                    }
                }
        );

        try {
            latch.wait();
        } catch (InterruptedException e) {
            throw new Exception("Interrupted", e);
        }

        if (fail.get()) {
            throw new Exception("Table or Column Family doesn't exist");
        }
    }

    public void putData(byte[] rowKey, String data) throws Exception{
        PutRequest putRequest = new PutRequest(
                tableName.getBytes(Charsets.UTF_8),
                rowKey,
                colFamily.getBytes(Charsets.UTF_8),
                "payload".getBytes(Charsets.UTF_8),
                data.getBytes(Charsets.UTF_8)
        );

        final CountDownLatch latch = new CountDownLatch(1);
        final AtomicBoolean fail = new AtomicBoolean(false);
        hBaseClient.put(putRequest).addCallbacks(
                new Callback<Object, Object>() {
                    @Override
                    public Object call(Object arg) {
                        latch.countDown();
                        return null;
                    }
                },
                new Callback<Object, Object>() {
                    @Override
                    public Object call(Object arg) {
                        fail.set(true);
                        latch.countDown();
                        return null;
                    }
                }
        );
        try {
            latch.wait();
        } catch (InterruptedException e) {
            throw new Exception("Interrupted", e);
        }

        if (fail.get()) {
            throw new Exception("put request failed");
        }
    }

    public byte[] getData(byte[] rowKey) throws Exception {
        GetRequest getRequest = new GetRequest(tableName, rowKey);
        ArrayList<KeyValue> kvs = hBaseClient.get(getRequest).join();
        return kvs.get(0).value();
    }
    public static void main(String[] args) throws Exception {
        byte[] rowKey = UUID.randomUUID().toString().getBytes(Charsets.UTF_8);
        HBaseAsyncAPI asyncHBaseQuickStart = new HBaseAsyncAPI("ODS:sync_test", "data", null);
        asyncHBaseQuickStart.init();
        asyncHBaseQuickStart.putData(rowKey, "Sample Data #1");
        System.out.println(new String(asyncHBaseQuickStart.getData(rowKey)));
    }
}
