pt = r"D:\Codes\AIProjects\T1\test1.txt"
d = r"D:\Codes\AIProjects\T1\test1p50.txt"
in_file = open(pt, "r")
out_file = open(d, "w")
txt = in_file.readlines()
for line in txt:
    tot = int(line.split(" ")[1])
    s = line[:-2]
    print(s[-1])
    if tot < 49:
        x = 49 - tot
        for p in range(x):
            s += ' 0' * 133
    out_file.write(s + '\n')
