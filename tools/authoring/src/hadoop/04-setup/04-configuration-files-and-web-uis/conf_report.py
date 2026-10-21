# conf_report.py: which settings is the NameNode really using, and from which file?
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter

URL = "http://localhost:9870/conf"           # NameNode web UI
root = ET.fromstring(urllib.request.urlopen(URL).read())

props = {}
for p in root.iter("property"):
    props[p.findtext("name")] = (p.findtext("value"), p.findtext("source"))

print(f"{len(props)} properties loaded")
for source, n in Counter(src for _, src in props.values()).most_common():
    print(f"{n:>5}  {source}")

print()
for key in ["fs.defaultFS", "dfs.replication", "dfs.blocksize", "dfs.namenode.name.dir"]:
    value, source = props.get(key, ("(not set)", "-"))
    print(f"{key:24} = {value}   [{source}]")
