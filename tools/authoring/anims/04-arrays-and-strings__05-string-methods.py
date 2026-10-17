from mkanim import Anim
HEADING = "Watch it with an example: reading one line of a bank statement"
INTRO = "Banks export statements as CSV text. Watch <code>split</code>, <code>substring</code>, <code>contains</code> and <code>trim</code> turn one line into useful data."
A = Anim("Taking a CSV line apart", frames=6, h=226, label="string methods on a statement line")
A.box(6, 14, 348, 30, None, fill="board", stroke="board")
A.text(14, 34, "\"26-01-2025,UPI/ZOMATO/Food, -450.00 \"", cls="chalk", mono=True, size=10.5)
parts = [("[0]", "26-01-2025"), ("[1]", "UPI/ZOMATO/Food"), ("[2]", " -450.00 ")]
for i, (k, v) in enumerate(parts):
    y = 58 + i * 34
    A.text(12, y + 19, f"parts{k}", on="2-", mono=True, size=10, cls="ink2")
    A.box(76, y, 150, 28, f"\"{v}\"", on="2-", fill="soft-blue", stroke="blue", mono=True, size=10)
A.box(236, 58, 118, 28, "year = \"2025\"", on="3-", fill="soft-green", stroke="green", mono=True, size=10, bold=True)
A.box(236, 92, 118, 28, "isUpi = true", on="4-", fill="soft-green", stroke="green", mono=True, size=10, bold=True)
A.box(236, 126, 118, 28, "amt = -450.0", on="5-", fill="soft-green", stroke="green", mono=True, size=10, bold=True)
calls = {2: "line.split(\",\")  → 3 parts", 3: "parts[0].substring(6)  → from index 6", 4: "parts[1].contains(\"UPI\")",
         5: "Double.parseDouble(parts[2].trim())", 6: "Food spend: Rs 450 via UPI in 2025"}
for f, t in calls.items(): A.text(10, 186, t, on=str(f), mono=True, size=10, bold=True, cls="green" if f == 6 else "ink")
A.text(10, 186, "One String: date, description, amount", on="1", size=10.5)
A.text(10, 206, "each method returns a NEW value; line is unchanged", on="2-", size=9.5, cls="ink2")
A.caps([
 "<b>Raw text:</b> one line from a downloaded statement. Date, description and amount, separated by commas, with messy spaces.",
 "<b>split(\",\"):</b> cuts the String at every comma and returns a <code>String[]</code> with 3 parts.",
 "<b>substring(6):</b> characters from index 6 to the end of \"26-01-2025\" give the year \"2025\".",
 "<b>contains(\"UPI\"):</b> true, so this was a UPI payment. Expense apps tag transactions like this.",
 "<b>trim() then parse:</b> remove the spaces around \" -450.00 \", then convert the text to the number −450.0.",
 "<b>Done:</b> one line became clean data. Note that every method returned a new value; the original line String never changed.",
])
