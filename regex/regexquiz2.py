import sys

idx = int(sys.argv[1]) - 1
myRegexList = [
    r"/\w+(?=\W+said)/",
    r"/.*\b(\w+)\b.*\b\1\b.*/is",
    r"/^c*(?=b*(a[bc]*){4}$)(?=a*(b[ac]*){3}$).*/",
    r"/.*(?=[b-df-gj-np-tv-z]{3})(.)(?!\1)(.)(?!(\1|\2)).*/",
    r"/^(x|y)(?!(.)\2)[abcd]{2}\1$/"]
print(myRegexList[idx])