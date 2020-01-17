pt = r"D:\Codes\AIProjects\T1\test1.txt"
# d = r"D:\Codes\AIProjects\T1\test1p50.txt"
in_file = open(pt, "r")
# out_file = open(d, "w")
txt = in_file.readlines()
cnt = set()
for line in txt:
    name = line.split(" ")[0]
    cnt.add(name)
print(len(cnt))
