import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

import java.io.IOException;

/**
 * Created by sponge on 2016/11/29 0029.
 */
public class HBaseMRLoad {
    private static final String NAME = "HBaseMRLoad";

    static public class Uploader extends Mapper<LongWritable, Text, ImmutableBytesWritable, Put> {
        private long checkpoint = 100;
        private long count = 0;

        public void map(LongWritable key, Text line, Context context) {
            //each line is comma-delimited; row,family,qualifier,value
            String[] values = line.toString().split(",");
            if (values.length != 4) {
                return;
            }
            //extract each value
            byte[] rowkey = Bytes.toBytes(values[0]);
            byte[] family = Bytes.toBytes(values[1]);
            byte[] qualifier = Bytes.toBytes(values[2]);
            byte[] value = Bytes.toBytes(values[3]);

            Put put = new Put(rowkey);
            put.addColumn(family, qualifier, value);
            //uncomment below to disable WAL, This will improve performance but means you
            //will experience data loss in case of a RegionServer crash
            // put.setWriteToWAL(false);
            try {
                context.write(new ImmutableBytesWritable(rowkey), put);
            } catch (IOException e) {
                e.printStackTrace();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            //set the status every checkpoint line
            if (++count % checkpoint ==0 ) {
                context.setStatus("Emitting Put " + count);
            }
        }
    }

    /*
    Job configuration
     */

    public static Job configureJob(Configuration conf, String[] args ) throws IOException {
        Path inputPath = new Path(args[0]);
        String tableName = args[1];
        Job job = Job.getInstance(conf, NAME + "_" + tableName);

        job.setJarByClass(Uploader.class);
        FileInputFormat.setInputPaths(job, inputPath);

        job.setInputFormatClass(TextInputFormat.class);
        job.setMapperClass(Uploader.class);
        // No reducers.  Just write straight to table.  Call initTableReducerJob
        // because it sets up the TableOutputFormat.
        TableMapReduceUtil.initTableReducerJob(tableName, null, job);
        job.setNumReduceTasks(0);
        return job;
    }

    /**
     *Main entry point
     *
     * @param args The command line parameters
     * @throws Exception When running the job fails
     */

    public static void main(String[] args) throws Exception {
        Configuration conf = HBaseConfiguration.create();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if(otherArgs.length != 2) {
            System.err.println("Wrong number of arguments: " + otherArgs.length);
            System.err.println("Usage: " + NAME + " <input> <tablename>");
            System.exit(-1);
        }
        Job job = configureJob(conf, otherArgs);
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
