import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.TreeMap;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

/** Count orders per item by streaming one HDFS file through a single client. */
public class ItemCount {
    public static void main(String[] args) throws Exception {
        Path path = new Path(args[0]);
        Map<String, Integer> counts = new TreeMap<>();
        long start = System.currentTimeMillis();
        try (FileSystem fs = FileSystem.get(new Configuration());
             FSDataInputStream in = fs.open(path);
             BufferedReader r = new BufferedReader(new InputStreamReader(in, StandardCharsets.UTF_8))) {
            r.readLine();                                         // skip the header
            String line;
            while ((line = r.readLine()) != null) {
                String item = line.split(",")[1];
                counts.merge(item, 1, Integer::sum);
            }
        }
        counts.forEach((item, n) -> System.out.printf("%-9s %,d%n", item, n));
        System.out.println("took " + (System.currentTimeMillis() - start) + " ms in one JVM");
    }
}
