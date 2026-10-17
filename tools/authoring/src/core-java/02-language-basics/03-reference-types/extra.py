WORKED_INTRO = "A reference variable doesn't hold the object; it holds the way to reach it. These three programs show the consequences: two variables can share one object, Strings never change in place, and an empty reference is <code>null</code>. Watch the arrows from the stack to the heap."
EXAMPLES = [
dict(tag="E-commerce · cart", title="Two references, one shopping cart",
 problem="<p>A shopping app passes the same cart to the checkout screen. The checkout adds a gift wrap. Because both variables refer to the same object, the change is visible through both. Use a <code>StringBuilder</code> as a simple cart.</p>",
 inp="cart \"Shoes\"; checkout adds \", Gift wrap\"",
 approach=["Create one StringBuilder and point <code>cart</code> at it.",
           "<code>checkout = cart</code> copies the reference, not the object.",
           "Append through <code>checkout</code>, print through <code>cart</code>."],
 code='''public class Main {
    public static void main(String[] args) {
        StringBuilder cart = new StringBuilder("Shoes");
        StringBuilder checkout = cart;
        checkout.append(", Gift wrap");
        System.out.println("cart:     " + cart);
        System.out.println("checkout: " + checkout);
        System.out.println("same object? " + (cart == checkout));
    }
}
''', notes={3: "Object :: = One StringBuilder object (#n) on the heap; <code>cart</code> holds a reference to it.",
            4: "Copy the reference :: = <code>checkout</code> now refers to the same object. Still only one object.",
            5: "Change :: = The object itself changes; both variables see it.",
            8: "== :: For references, <code>==</code> checks whether they point to the same object: true."},
 tryit="Press <b>Run</b>. Then change line 4 to <code>new StringBuilder(cart)</code> (a copy) and compare the output."),
dict(tag="Messaging · text", title="Strings never change: each change makes a new String",
 problem="<p>A chat app builds a greeting: \"Hi\", then adds a name, then makes it upper case. Show that each step creates a new String object while the old one stays unchanged.</p>",
 inp="\"Hi\", name \"Asha\"",
 approach=["Keep the original in <code>first</code>.",
           "Build <code>greet</code> with <code>+</code> and <code>toUpperCase()</code>.",
           "Print the original to prove it didn't change."],
 code='''public class Main {
    public static void main(String[] args) {
        String first = "Hi";
        String greet = first + ", Asha";
        greet = greet.toUpperCase();
        System.out.println(greet);
        System.out.println("original still: " + first);
    }
}
''', notes={4: "New object :: = <code>+</code> builds a brand-new String \"Hi, Asha\"; \"Hi\" is untouched.",
            5: "Another new object :: = <code>toUpperCase()</code> returns a new String; <code>greet</code> now refers to it. The previous one is left for the garbage collector.",
            7: "Immutable :: <code>first</code> still says \"Hi\". Strings are immutable."},
 tryit="Press <b>Run</b>. Then call <code>first.toUpperCase();</code> without assigning it and print <code>first</code>: nothing changes."),
dict(tag="Hotel · rooms", title="Empty rooms are null",
 problem="<p>A small hotel has 4 rooms; a <code>String[]</code> holds the guest name for each. New arrays of references start full of <code>null</code>. Check in two guests and print rooms 1–3, then check whether room 2 is empty.</p>",
 inp="4 rooms; Asha in room 1 (index 0), Ravi in room 3 (index 2)",
 approach=["<code>new String[4]</code>: four references, all null.",
           "Assign two names.",
           "Print the slots, then test one with <code>== null</code>."],
 code='''public class Main {
    public static void main(String[] args) {
        String[] rooms = new String[4];
        rooms[0] = "Asha";
        rooms[2] = "Ravi";
        System.out.println("Room 1: " + rooms[0]);
        System.out.println("Room 2: " + rooms[1]);
        System.out.println("Room 3: " + rooms[2]);
        System.out.println("Room 2 empty? " + (rooms[1] == null));
    }
}
''', notes={3: "Array of references :: = The array object holds 4 slots, each <code>null</code>: no String objects exist yet.",
            4: "Check in :: = Slot 0 now refers to a String \"Asha\".",
            7: "null slot :: = Room 2's slot holds no reference, so println shows the word null.",
            9: "Check :: Test with <code>== null</code> before calling any method on a slot; calling a method on null throws NullPointerException."},
 tryit="Press <b>Run</b>. Then print <code>rooms[1].length()</code> and read the NullPointerException."),
]

PRACTICE_INTRO = "Work with references: Strings, arrays and objects, null, and the difference between == and equals. Every output is fixed. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="String methods", stmt="<p>For \"Bengaluru\", print its length, first character and upper-case form.</p>", inp="Bengaluru",
 code='''public class Main {
    public static void main(String[] args) {
        String city = "Bengaluru";
        System.out.println(city.length() + " " + city.charAt(0) + " " + city.toUpperCase());
    }
}''', explain="<p><b>How it works:</b> reference types have methods; primitives don't.</p>"),
dict(level="easy", title="Default value of a reference", stmt="<p>Create a <code>String[]</code> of size 2 and print its first element.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        String[] names = new String[2];
        System.out.println(names[0]);
    }
}''', explain="<p><b>How it works:</b> reference slots start as <code>null</code>; println prints the word null.</p>"),
dict(level="easy", title="Array length", stmt="<p>Create an int array {5, 10, 15, 20} and print its length and last element.</p>", inp="{5, 10, 15, 20}",
 code='''public class Main {
    public static void main(String[] args) {
        int[] a = {5, 10, 15, 20};
        System.out.println(a.length + " " + a[a.length - 1]);
    }
}''', explain="<p><b>How it works:</b> the last index is always length − 1.</p>"),
dict(level="medium", title="== vs equals", stmt="<p>Compare two Strings \"pune\" built differently with == and equals.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        String a = "pune";
        String b = new String("pune");
        System.out.println((a == b) + " " + a.equals(b));
    }
}''', explain="<p><b>How it works:</b> == compares references (different objects); equals compares the text. Always use equals for Strings.</p>"),
dict(level="medium", title="Shared array", stmt="<p>Make <code>b</code> refer to the same array as <code>a</code>, change b[0] to 99, and print a[0].</p>", inp="a = {1, 2, 3}",
 code='''public class Main {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        int[] b = a;
        b[0] = 99;
        System.out.println(a[0]);
    }
}''', explain="<p><b>How it works:</b> arrays are objects; assigning copies the reference, so a and b are the same array.</p>"),
dict(level="business", title="Customer name check", stmt="<p>A form field may be null if the user skipped it. Print whether a name was given, before and after the user fills it in.</p>", inp="null, then \"Meena\"",
 code='''public class Main {
    public static void main(String[] args) {
        String name = null;
        System.out.println("Name given? " + (name != null));
        name = "Meena";
        System.out.println("Name given? " + (name != null) + ", name: " + name);
    }
}''', explain="<p><b>How it works:</b> checking for null before using a reference prevents NullPointerException.</p>"),
dict(level="business", title="Coupon code comparison", stmt="<p>A user types \"save50\". The valid code is \"SAVE50\". Compare ignoring case.</p>", inp="save50",
 code='''public class Main {
    public static void main(String[] args) {
        String typed = "save50";
        System.out.println("Valid: " + typed.equalsIgnoreCase("SAVE50"));
    }
}''', explain="<p><b>How it works:</b> <code>equalsIgnoreCase</code> compares text without caring about capitals.</p>"),
dict(level="business", title="Order list as an array", stmt="<p>Store 3 order ids in a String array and print them with their positions.</p>", inp="ORD-11, ORD-12, ORD-13",
 code='''public class Main {
    public static void main(String[] args) {
        String[] orders = {"ORD-11", "ORD-12", "ORD-13"};
        System.out.println("1. " + orders[0]);
        System.out.println("2. " + orders[1]);
        System.out.println("3. " + orders[2]);
    }
}''', explain="<p><b>How it works:</b> the array holds three references, each pointing to a String on the heap. (Loops will make this shorter in Module 3.)</p>"),
]
