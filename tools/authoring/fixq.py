import re,ast,sys
p=sys.argv[1]; s=open(p).read()
s=re.sub(r"(?<=[A-Za-z]{2})'(?=[A-Za-z])","’",s)
s=re.sub(r"(?<=[A-Za-z]{2})\\'(?=[A-Za-z])","’",s)
ast.parse(s); open(p,'w').write(s); print('quotes ok')
