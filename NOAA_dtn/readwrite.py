import time

count=0

while True:
    if count>10:
        with open('file.txt', 'r') as fin:
            data = fin.read().splitlines(True)
            fin.close()
        with open('file.txt', 'w') as fout:
            fout.writelines(data[1:])
            fout.write(str(count)+"\n")
            fout.close()
    else:
        with open('file.txt', 'a') as fout:
            fout.write(str(count)+"\n")
            fout.close()
    count=count+1
    time.sleep(1)
