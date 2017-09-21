with open('elastestgenin.txt') as f, open('elastestgenout.txt', 'w') as o:
    for line in f.readlines():
        o.write(line
        .replace('\n', '\\n')
        .replace('"', '\\"')
        )
