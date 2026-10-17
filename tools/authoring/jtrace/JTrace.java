import com.sun.jdi.*;
import com.sun.jdi.connect.*;
import com.sun.jdi.event.*;
import com.sun.jdi.request.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

/**
 * Runs a compiled program (class Main, compiled with -g) under JDI and prints, as JSON,
 * one snapshot per executed source line: line, stack frames with locals, reachable heap
 * objects, and stdout produced. Usage: java JTrace CLASSDIR STDIN_FILE > raw.json
 * Snapshot k describes the state AFTER line k ran (taken at the next line event).
 */
public class JTrace {
    static Map<Long, Integer> ids = new LinkedHashMap<>();
    static int nextId = 1;
    static StringBuilder json = new StringBuilder();

    public static void main(String[] a) throws Exception {
        String cp = a[0];
        byte[] stdin = a.length > 1 ? java.nio.file.Files.readAllBytes(new File(a[1]).toPath()) : new byte[0];
        LaunchingConnector lc = Bootstrap.virtualMachineManager().defaultConnector();
        Map<String, Connector.Argument> args = lc.defaultArguments();
        args.get("main").setValue("JTraceBoot");
        args.get("options").setValue("-cp " + cp + File.pathSeparator + System.getProperty("jtrace.boot"));
        VirtualMachine vm = lc.launch(args);
        Process p = vm.process();
        p.getOutputStream().write(stdin); p.getOutputStream().close();
        InputStream out = p.getInputStream(), err = p.getErrorStream();

        EventRequestManager erm = vm.eventRequestManager();
        ClassPrepareRequest cpr = erm.createClassPrepareRequest();
        cpr.addClassFilter("Main"); cpr.enable();
        MethodExitRequest mex = null;

        List<String> snaps = new ArrayList<>();
        int[] pendingLine = {-1};
        String pendingMeth = null;
        ByteArrayOutputStream outBuf = new ByteArrayOutputStream();
        String exitInfo = "";
        int exitLine = -1;
        vm.resume();
        boolean done = false;
        while (!done) {
            EventSet es = vm.eventQueue().remove();
            for (Event ev : es) {
                if (ev instanceof ClassPrepareEvent cpe) {
                    ReferenceType rt = cpe.referenceType();
                    Method m = rt.methodsByName("main").get(0);
                    BreakpointRequest bp = erm.createBreakpointRequest(m.location());
                    bp.enable();
                    mex = erm.createMethodExitRequest();
                    mex.addClassFilter(rt); mex.enable();
                } else if (ev instanceof BreakpointEvent be) {
                    ThreadReference t = be.thread();
                    StepRequest sr = erm.createStepRequest(t, StepRequest.STEP_LINE, StepRequest.STEP_INTO);
                    for (String x : new String[]{"java.*", "javax.*", "jdk.*", "sun.*", "com.sun.*", "JTraceBoot"}) sr.addClassExclusionFilter(x);
                    sr.enable();
                    pendingLine[0] = be.location().lineNumber();
                } else if (ev instanceof StepEvent se) {
                    if (se.location().lineNumber() < 0 || se.location().declaringType().name().contains("$$Lambda") || se.location().method().isBridge()) continue;   // skip javac's generic bridge methods
                    // state after pendingLine executed
                    String snap = snapshot(se.thread(), drain(out, outBuf));
                    snaps.add("{\"line\":" + pendingLine[0] + "," + snap + "}");
                    pendingLine[0] = se.location().lineNumber();
                } else if (ev instanceof MethodExitEvent mx) {
                    if (mx.method().name().equals("main") && mx.method().declaringType().name().equals("Main")) {
                        String snap = snapshot(mx.thread(), drain(out, outBuf));
                        snaps.add("{\"line\":" + pendingLine[0] + "," + snap + "}");
                        exitLine = mx.location().lineNumber();
                        pendingLine[0] = -2;
                    }
                } else if (ev instanceof VMDeathEvent || ev instanceof VMDisconnectEvent) {
                    done = true;
                }
            }
            if (!done) es.resume();
        }
        Thread.sleep(150);
        String rest = drain(out, outBuf);
        String errs = new String(err.readAllBytes(), StandardCharsets.UTF_8);
        if (pendingLine[0] > 0) { // crashed: record the line that threw
            snaps.add("{\"line\":" + pendingLine[0] + ",\"crash\":true,\"frames\":[],\"heap\":[],\"out\":" + q(rest) + "}");
            rest = "";
        }
        System.out.println("{\"exitLine\":" + exitLine + ",\"tail\":" + q(rest) + ",\"stderr\":" + q(errs) + ",\"steps\":[\n" + String.join(",\n", snaps) + "]}");
    }

    static String drain(InputStream in, ByteArrayOutputStream buf) throws IOException {
        byte[] b = new byte[8192]; StringBuilder s = new StringBuilder();
        while (in.available() > 0) { int n = in.read(b); if (n <= 0) break; s.append(new String(b, 0, n, StandardCharsets.UTF_8)); }
        return s.toString();
    }

    static String snapshot(ThreadReference t, String newOut) throws Exception {
        List<String> frames = new ArrayList<>();
        Set<Long> seenObj = new LinkedHashSet<>();
        List<ObjectReference> roots = new ArrayList<>();
        for (StackFrame f : t.frames()) {
            Location loc = f.location();
            String cls = loc.declaringType().name();
            if (cls.startsWith("java.") || cls.startsWith("jdk.") || cls.startsWith("sun.") || cls.equals("JTraceBoot") || cls.contains("$$Lambda")) continue;
            Method m = loc.method();
            if (m.isBridge()) continue;   // generic bridge (e.g. compareTo(Object)): not user code
            List<String> vars = new ArrayList<>();
            ObjectReference self = f.thisObject();
            if (self != null) { vars.add("[\"this\"," + q(val(self)) + "]"); roots.add(self); }
            try {
                for (LocalVariable lv : f.visibleVariables()) {
                    Value v = f.getValue(lv);
                    vars.add("[" + q(lv.name()) + "," + q(val(v)) + "]");
                    if (v instanceof ObjectReference o) roots.add(o);
                }
            } catch (AbsentInformationException e) { }
            frames.add("{\"cls\":" + q(cls) + ",\"m\":" + q(sig(m)) + ",\"line\":" + loc.lineNumber() + ",\"vars\":[" + String.join(",", vars) + "]}");
        }
        TreeMap<Integer, String> hm = new TreeMap<>();
        List<String> statics = new ArrayList<>();
        for (ReferenceType rt : t.virtualMachine().allClasses()) {
            String cn = rt.name();
            if (!rt.isPrepared() || !userClass(cn) || cn.contains("$$Lambda") || rt.classLoader() == null) continue;
            for (Field f : rt.fields()) {
                if (!f.isStatic() || f.isSynthetic() || f.isFinal()) continue;
                Value v = rt.getValue(f);
                if (v instanceof ObjectReference o) roots.add(o);
                statics.add(q(simple(cn) + "." + f.name() + " = " + val(v)));
            }
        }
        Collections.sort(statics);
        Deque<ObjectReference> dq = new ArrayDeque<>(roots);
        while (!dq.isEmpty()) {
            ObjectReference o = dq.poll();
            if (o == null || !seenObj.add(o.uniqueID())) continue;
            int k = id(o);
            hm.put(k, "{\"id\":" + k + ",\"d\":" + q(describe(o, dq)) + "}");
        }
        List<String> heap = new ArrayList<>(hm.values());
        return "\"frames\":[" + String.join(",", frames) + "],\"heap\":[" + String.join(",", heap) + "],\"statics\":[" + String.join(",", statics) + "],\"out\":" + q(newOut);
    }

    static String sig(Method m) {
        StringBuilder s = new StringBuilder();
        if (m.name().equals("<clinit>")) return simple(m.declaringType().name()) + " static initializer";
        String name = m.name().equals("<init>") ? simple(m.declaringType().name()) : m.name().startsWith("lambda$") ? "lambda body" : m.name();
        if (!m.declaringType().name().equals("Main")) name = m.name().equals("<init>") ? "new " + name : simple(m.declaringType().name()) + "." + name;
        s.append(name).append("(");
        try {
            List<LocalVariable> as = m.arguments();
            for (int i = 0; i < as.size(); i++) { if (i > 0) s.append(", "); s.append(simple(as.get(i).typeName())).append(" ").append(as.get(i).name()); }
        } catch (AbsentInformationException e) { s.append("…"); }
        return s.append(")").toString();
    }

    static String show(String t) { return t.replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t"); }

    static boolean userClass(String cn) {
        return !(cn.startsWith("java.") || cn.startsWith("javax.") || cn.startsWith("jdk.") || cn.startsWith("sun.") || cn.startsWith("com.sun.") || cn.startsWith("JTrace") || cn.endsWith("[]"));
    }

    static boolean isA(ReferenceType rt, String cls) {
        if (!(rt instanceof ClassType ct)) return false;
        for (ClassType c = ct; c != null; c = c.superclass()) if (c.name().equals(cls)) return true;
        return false;
    }

    static Value fv(ObjectReference o, String name) {
        for (ReferenceType r = o.referenceType(); r != null; r = (r instanceof ClassType ct) ? ct.superclass() : null) {
            Field f = r.fieldByName(name);
            if (f != null) return o.getValue(f);
        }
        return null;
    }

    static int ival(ObjectReference o, String name) { Value v = fv(o, name); return v instanceof IntegerValue iv ? iv.value() : -1; }

    static void inorder(ObjectReference e, List<String> out, Deque<ObjectReference> dq, boolean withVal) {
        if (e == null || out.size() > 40) return;
        inorder((ObjectReference) fv(e, "left"), out, dq, withVal);
        out.add(inner(fv(e, "key"), dq) + (withVal ? "=" + inner(fv(e, "value"), dq) : ""));
        inorder((ObjectReference) fv(e, "right"), out, dq, withVal);
    }

    static String mapText(ObjectReference m, Deque<ObjectReference> dq, boolean keysOnly) {
        String n = m.referenceType().name();
        int size = ival(m, "size");
        List<String> el = new ArrayList<>();
        if (n.equals("java.util.TreeMap")) {
            inorder((ObjectReference) fv(m, "root"), el, dq, !keysOnly);
            return "size " + size + (keysOnly ? " [" : " {") + String.join(", ", el) + (keysOnly ? "]" : "}") + " (sorted)";
        }
        if (n.equals("java.util.LinkedHashMap")) {
            for (ObjectReference e = (ObjectReference) fv(m, "head"); e != null && el.size() < 40; e = (ObjectReference) fv(e, "after"))
                el.add(inner(fv(e, "key"), dq) + (keysOnly ? "" : "=" + inner(fv(e, "value"), dq)));
            return "size " + size + (keysOnly ? " [" : " {") + String.join(", ", el) + (keysOnly ? "]" : "}") + " (insertion order)";
        }
        ArrayReference table = (ArrayReference) fv(m, "table");
        if (table == null) return "size " + size + " (no bucket table yet)";
        List<String> buckets = new ArrayList<>();
        for (int i = 0; i < table.length(); i++) {
            ObjectReference e = (ObjectReference) table.getValue(i);
            if (e == null) continue;
            List<String> chain = new ArrayList<>();
            for (; e != null && chain.size() < 10; e = (ObjectReference) fv(e, "next"))
                chain.add(inner(fv(e, "key"), dq) + (keysOnly ? "" : "=" + inner(fv(e, "value"), dq)));
            buckets.add("[" + i + "] " + String.join(" → ", chain));
        }
        return "size " + size + ", " + table.length() + " buckets: " + String.join(" | ", buckets);
    }

    static String simple(String n) { int i = n.lastIndexOf('.'); n = i >= 0 ? n.substring(i + 1) : n; return n.replace('$', '.'); }

    static int id(ObjectReference o) { return ids.computeIfAbsent(o.uniqueID(), k -> nextId++); }

    static boolean isArgsArray(ObjectReference o) {
        return o instanceof ArrayReference ar && ar.length() == 0 && ar.referenceType().name().equals("java.lang.String[]");
    }

    static String val(Value v) {
        if (v == null) return "null";
        if (v instanceof CharValue c) return "'" + c.value() + "'";
        if (v instanceof PrimitiveValue) return v.toString();
        ObjectReference o = (ObjectReference) v;
        if (isArgsArray(o)) return "→ String[0]";
        if (o instanceof StringReference s) return "→ #" + id(o) + " \"" + show(s.value()) + "\"";
        String box = boxed(o);
        if (box != null) return "→ #" + id(o) + " " + box;
        String tn = o.referenceType().name().contains("$$Lambda") ? "lambda" : simple(o.referenceType().name());
        if (o instanceof ArrayReference ar) tn = tn.replaceFirst("\\[\\]", "[" + ar.length() + "]");
        return "→ #" + id(o) + " " + tn;
    }

    static String boxed(ObjectReference o) {
        String n = o.referenceType().name();
        if (n.equals("java.lang.Integer") || n.equals("java.lang.Long") || n.equals("java.lang.Double") || n.equals("java.lang.Boolean") || n.equals("java.lang.Character")) {
            Field f = o.referenceType().fieldByName("value");
            return simple(n) + " " + val(o.getValue(f));
        }
        return null;
    }

    static String inner(Value v, Deque<ObjectReference> dq) {
        if (v instanceof ObjectReference bo && !(v instanceof StringReference)) { String b = boxed(bo); if (b != null) return b.substring(b.indexOf(' ') + 1); }
        if (v instanceof ObjectReference o && !(v instanceof StringReference)) { dq.add(o); return "→#" + id(o); }
        if (v instanceof StringReference s) { dq.add(s); return "\"" + show(s.value()) + "\""; }
        return val(v);
    }

    static String sbText(ObjectReference o) {
        ReferenceType rt = o.referenceType();
        Field fv = rt.fieldByName("value"), fc = rt.fieldByName("count"), fco = rt.fieldByName("coder");
        ArrayReference arr = (ArrayReference) o.getValue(fv);
        int count = ((IntegerValue) o.getValue(fc)).value();
        int coder = ((ByteValue) o.getValue(fco)).value();
        List<Value> vals = arr.getValues();
        StringBuilder s = new StringBuilder();
        if (coder == 0) for (int i = 0; i < count; i++) s.append((char) (((ByteValue) vals.get(i)).value() & 0xff));
        else for (int i = 0; i < count; i++) { int lo = ((ByteValue) vals.get(2 * i)).value() & 0xff, hi = ((ByteValue) vals.get(2 * i + 1)).value() & 0xff; s.append((char) (lo | hi << 8)); }
        int cap = coder == 0 ? arr.length() : arr.length() / 2;
        return "\"" + show(s.toString()) + "\" (length " + count + ", capacity " + cap + ")";
    }

    static String describe(ObjectReference o, Deque<ObjectReference> dq) {
        String tn = simple(o.referenceType().name());
        if (isArgsArray(o)) return "String[0] (args, empty)";
        if (o instanceof StringReference s) return "String \"" + show(s.value()) + "\"";
        String box = boxed(o);
        if (box != null) return box;
        if (o instanceof ArrayReference ar) {
            List<String> el = new ArrayList<>();
            List<Value> vs = ar.getValues();
            for (int i = 0; i < vs.size() && i < 14; i++) el.add(inner(vs.get(i), dq));
            if (vs.size() > 14) el.add("…");
            return tn.replaceFirst("\\[\\]", "[" + ar.length() + "]") + " {" + String.join(", ", el) + "}";
        }
        String full = o.referenceType().name();
        if (full.equals("java.lang.StringBuilder") || full.equals("java.lang.StringBuffer")) return tn + " " + sbText(o);
        if (full.equals("java.util.ArrayList")) {
            int size = ((IntegerValue) o.getValue(o.referenceType().fieldByName("size"))).value();
            ArrayReference ed = (ArrayReference) o.getValue(o.referenceType().fieldByName("elementData"));
            List<String> el = new ArrayList<>();
            for (int i = 0; i < size; i++) el.add(inner(ed.getValue(i), dq));
            return "ArrayList size " + size + ", capacity " + ed.length() + " [" + String.join(", ", el) + "]";
        }
        if (full.equals("java.util.ImmutableCollections$ListN") || full.equals("java.util.ImmutableCollections$List12")) {
            List<String> el = new ArrayList<>();
            if (full.endsWith("ListN")) { ArrayReference es = (ArrayReference) fv(o, "elements"); for (int i = 0; i < es.length() && i < 40; i++) el.add(inner(es.getValue(i), dq)); }
            else { el.add(inner(fv(o, "e0"), dq)); Value e1 = fv(o, "e1"); if (e1 != null && !(e1 instanceof ObjectReference r1 && r1.referenceType().name().equals("java.lang.Object"))) el.add(inner(e1, dq)); }
            return "immutable List (List.of) size " + el.size() + " [" + String.join(", ", el) + "]";
        }
        if (full.equals("java.util.ArrayDeque")) {
            ArrayReference es = (ArrayReference) fv(o, "elements");
            int head = ival(o, "head"), tail = ival(o, "tail"), n = es.length();
            List<String> el = new ArrayList<>();
            for (int i = head; i != tail && el.size() < 40; i = (i + 1) % n) el.add(inner(es.getValue(i), dq));
            return "ArrayDeque size " + el.size() + " [" + String.join(", ", el) + "] (front → back)";
        }
        if (full.equals("java.util.PriorityQueue")) {
            ArrayReference q = (ArrayReference) fv(o, "queue");
            int size = ival(o, "size");
            List<String> el = new ArrayList<>();
            for (int i = 0; i < size && i < 40; i++) el.add(inner(q.getValue(i), dq));
            return "PriorityQueue size " + size + " heap array [" + String.join(", ", el) + "] (smallest first)";
        }
        if (o instanceof ThreadReference th) {
            String st = switch (th.status()) { case ThreadReference.THREAD_STATUS_RUNNING -> "RUNNABLE"; case ThreadReference.THREAD_STATUS_SLEEPING -> "TIMED_WAITING (sleeping)";
                case ThreadReference.THREAD_STATUS_MONITOR -> "BLOCKED"; case ThreadReference.THREAD_STATUS_WAIT -> "WAITING"; case ThreadReference.THREAD_STATUS_NOT_STARTED -> "NEW";
                case ThreadReference.THREAD_STATUS_ZOMBIE -> "TERMINATED"; default -> th.isCollected() ? "TERMINATED" : "NEW"; };
            return "Thread \"" + th.name() + "\" (" + st + ")";
        }
        if (full.contains("$$Lambda")) {
            String itf = (o.referenceType() instanceof ClassType ct && !ct.interfaces().isEmpty()) ? simple(ct.interfaces().get(0).name()) : "?";
            return "lambda object (a " + itf + ")";
        }
        if (isA(o.referenceType(), "java.lang.Throwable")) {
            Value msg = fv(o, "detailMessage");
            return tn + (msg instanceof StringReference sr ? ": " + show(sr.value()) : "");
        }
        if (full.equals("java.util.HashMap") || full.equals("java.util.LinkedHashMap") || full.equals("java.util.TreeMap")) return tn + " " + mapText(o, dq, false);
        if (full.equals("java.util.HashSet") || full.equals("java.util.LinkedHashSet")) return tn + " " + mapText((ObjectReference) fv(o, "map"), dq, true);
        if (full.equals("java.util.TreeSet")) return tn + " " + mapText((ObjectReference) fv(o, "m"), dq, true);
        if (full.equals("java.util.LinkedList")) {
            List<String> el = new ArrayList<>();
            for (ObjectReference nd = (ObjectReference) fv(o, "first"); nd != null && el.size() < 30; nd = (ObjectReference) fv(nd, "next")) el.add(inner(fv(nd, "item"), dq));
            return "LinkedList size " + ival(o, "size") + " [" + String.join(" ⇄ ", el) + "]";
        }
        if (full.equals("java.util.Optional")) { Value v = fv(o, "value"); return v == null ? "Optional.empty" : "Optional[" + inner(v, dq) + "]"; }
        if (full.startsWith("java.util.concurrent.atomic.Atomic") && fv(o, "value") instanceof PrimitiveValue pv) return tn + " " + pv;
        if (full.endsWith("$Itr") || full.endsWith("$ListItr")) return tn + " {cursor=" + ival(o, "cursor") + ", lastRet=" + ival(o, "lastRet") + "}";
        if (full.startsWith("java.") || full.startsWith("jdk.") || full.startsWith("sun.")) return tn;
        List<String> fs = new ArrayList<>();
        for (Field f : o.referenceType().allFields()) {
            // show the hidden links javac adds to inner/local/anonymous classes: this$0 (outer object), val$x (captured local)
            if (f.isStatic() || (f.isSynthetic() && !f.name().startsWith("this$") && !f.name().startsWith("val$"))) continue;
            fs.add(f.name() + "=" + inner(o.getValue(f), dq));
        }
        return tn + " {" + String.join(", ", fs) + "}";
    }

    static String q(String s) {
        StringBuilder b = new StringBuilder("\"");
        for (char c : s.toCharArray()) {
            switch (c) {
                case '"' -> b.append("\\\""); case '\\' -> b.append("\\\\"); case '\n' -> b.append("\\n");
                case '\r' -> {} case '\t' -> b.append("\\t");
                default -> { if (c < 32) b.append(String.format("\\u%04x", (int) c)); else b.append(c); }
            }
        }
        return b.append('"').toString();
    }
}
