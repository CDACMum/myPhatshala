import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.BlockLocation;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

public class HdfsBasics {
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();          // reads core-site.xml, hdfs-site.xml
        try (FileSystem fs = FileSystem.get(conf)) {
            System.out.println("Connected to: " + fs.getUri());

            Path dir = new Path("/user/hadoop/api_demo");
            fs.mkdirs(dir);

            // write a small file
            Path file = new Path(dir, "orders.csv");
            try (FSDataOutputStream out = fs.create(file, true)) {   // true = overwrite
                out.write("order_id,item,amount\n".getBytes(StandardCharsets.UTF_8));
                out.write("3001,samosa,18\n3002,chai,15\n".getBytes(StandardCharsets.UTF_8));
            }

            // read it back
            try (FSDataInputStream in = fs.open(file);
                 BufferedReader r = new BufferedReader(new InputStreamReader(in, StandardCharsets.UTF_8))) {
                String line;
                while ((line = r.readLine()) != null) {
                    System.out.println("  read: " + line);
                }
            }

            // metadata, as the NameNode stores it
            FileStatus st = fs.getFileStatus(file);
            System.out.printf("%s  %d bytes  replication %d  block size %d MB  owner %s%n",
                    st.getPath().getName(), st.getLen(), st.getReplication(),
                    st.getBlockSize() / (1024 * 1024), st.getOwner());

            // where are the blocks of a big file?
            Path big = new Path("/user/hadoop/data/orders_x30.csv");
            FileStatus bs = fs.getFileStatus(big);
            for (BlockLocation b : fs.getFileBlockLocations(bs, 0, bs.getLen())) {
                System.out.printf("  block at offset %,d length %,d on %s%n",
                        b.getOffset(), b.getLength(), String.join(", ", b.getHosts()));
            }

            // list, rename, delete
            for (FileStatus s : fs.listStatus(dir)) {
                System.out.println("  ls: " + s.getPath());
            }
            Path renamed = new Path(dir, "orders_old.csv");
            System.out.println("rename: " + fs.rename(file, renamed));
            System.out.println("exists after rename: " + fs.exists(file));
            System.out.println("delete: " + fs.delete(dir, true));             // true = recursive
        }
    }
}
