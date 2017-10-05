import csv
import itertools 
network_monitor_list = []
diskio_monitor_list = []
cup_monitor_list = []
mem_monitor_list = []


with open('monitor') as f:

    reader1, reader2 = itertools.tee(csv.reader(f, delimiter=","))
    
    for row in reader2:
   #     print(row[0])
        columns=len(next(reader1))
        print(columns)

    for row in csv.DictReader(f, ['network', 'diskio', 'cpu', 'mem']):
        if(len(row) != 4):
            print("not 4")
            continue
        print(len(row))
        network_monitor_list.append(row['network'].strip())
        diskio_monitor_list.append(row['diskio'].strip())
        cup_monitor_list.append(row['cpu'].strip())
        mem_monitor_list.append(row['mem'].strip())

