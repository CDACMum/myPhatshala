import java.io.*;

/** Makes System.out unbuffered so the tracer can attribute output to the exact line, then runs Main. */
public class JTraceBoot {
    public static void main(String[] args) throws Throwable {
        System.setOut(new PrintStream(new FileOutputStream(FileDescriptor.out), true, "UTF-8"));
        try {
            Class.forName("Main").getMethod("main", String[].class).invoke(null, (Object) new String[0]);
        } catch (java.lang.reflect.InvocationTargetException e) {
            Throwable c = e.getCause();
            System.err.println("Exception in thread \"main\" " + c);
            System.exit(1);
        }
    }
}
