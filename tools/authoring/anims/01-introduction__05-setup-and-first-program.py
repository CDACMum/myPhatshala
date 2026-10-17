from mkanim import Anim
HEADING = "Watch it with an example: two commands in the terminal"
INTRO = "Riya's folder and terminal, side by side. See which file each command needs and what it creates."
A = Anim("javac Hello.java, then java Hello", frames=6, h=226)
A.box(6, 14, 130, 150, None, fill="card", stroke="line")
A.text(16, 32, "📁 D:\\java", size=10.5, bold=True)
A.text(16, 56, "Hello.java", mono=True, size=10.5, on="1-")
A.text(16, 76, "Hello.class", mono=True, size=10.5, cls="acc", bold=True, on="2-")
A.box(146, 14, 208, 150, None, fill="board", stroke="board")
A.text(156, 36, "&gt; javac Hello.java", mono=True, cls="kw", size=10, on="2-")
A.text(156, 56, "(no message = success)", mono=True, cls="str", size=9.5, on="2-")
A.text(156, 80, "&gt; java Hello", mono=True, cls="kw", size=10, on="3-")
A.text(156, 100, "Hello, Riya!", mono=True, cls="chalk", size=10, on="5-6")
A.text(156, 124, "&gt; java hello", mono=True, cls="kw", size=10, on="6")
A.text(156, 142, "Error: Could not find or", mono=True, cls="kw", size=9, on="6")
A.text(156, 156, "load main class hello", mono=True, cls="kw", size=9, on="6")
A.box(6, 176, 348, 36, None, fill="soft-green", stroke="green", on="3-5")
A.text(180, 192, "JVM starts → loads Hello.class", anchor="middle", size=10, on="3")
A.text(180, 192, "finds  public static void main(String[] args)", anchor="middle", size=10, mono=True, on="4")
A.text(180, 192, "runs main → println", anchor="middle", size=10, on="5")
A.text(180, 205, "", size=1)
A.caps([
 "<b>Start:</b> the folder has only the source file <code>Hello.java</code>.",
 "<b>Compile:</b> <code>javac Hello.java</code> checks the code and writes <code>Hello.class</code>. If javac prints nothing, it worked.",
 "<b>Run:</b> <code>java Hello</code> starts a JVM. Note: the class name, <b>without</b> <code>.class</code>.",
 "<b>Entry point:</b> the JVM looks inside the class for exactly <code>public static void main(String[] args)</code>.",
 "<b>Output:</b> main runs and the text appears in the terminal.",
 "<b>Common mistake:</b> Java is case-sensitive. <code>java hello</code> fails because the class is named <code>Hello</code>.",
])
