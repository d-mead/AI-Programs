import sys
idx = int(sys.argv[1])-1
myRegexList = [
    r"/^.*[aeiou][b-df-hj-np-tv-z]{4}[aeiou].*/i",
    r'/".*?"/s',  # this string will need to contain double quotes
    r"/^def.*(\n  +.*)*/m",
    r"/^((01)+0?|(10)+1?)$/",
    r"/^(0|1*(00+|0*$))*$/",
    r"/^(1|0|22?2?(1|0|$))+$/",
    r"/^\d*(([2468]|^)[048]|[13579][26])$/",
    r"/^[26]*[13579]*$/",
    r"/^\?{9}(\?[xo.]{7}\?){6}\?{9}$/i",
    r"/(xxxx|(x.{8}){3}x|(x.{9}){3}.x|(x.{8}){3}x)/i"]
print(myRegexList[idx])