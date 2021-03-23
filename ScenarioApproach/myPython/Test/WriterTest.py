path = '.\\Massachusetts_ODs.tntp'

f = open(path, "r")
lines = f.readlines()
origin = 0
f.close()

newLines = []

for line in lines:

    if len(line) > 7 and line[:6] == 'Origin':
        origin = line[6:-1]
    elif line == '\n':
        continue
    else:
        newLines.append(origin + '\t' + line)

f = open(path, "w")
f.writelines(newLines)
f.close()

pass
