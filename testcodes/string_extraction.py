import re #extract numeric value from string
i= "i=2.7A"
s = re.search(r"\d+(\.\d+)?", i)
s1 = s.group(0)
print(s1)