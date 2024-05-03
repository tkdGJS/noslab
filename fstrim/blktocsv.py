import csv
import sys

if __name__ == "__main__":
    if len(sys.argv) !=2:
        print("Usage: python3 blktocsv.py <file system>")
        sys.exit(1)

    fs = sys.argv[1]
    print("file system : ", fs)

input_file = fs + '-tracefile'
output_file = fs + '-tracefile.csv'

csv_headers = ['Device', 'Core', 'Index', 'Time', 'PID', 'Event', 'RWBS', 'Offset', 'Length', 'Process' ]

i = 0

with open(output_file, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(csv_headers)

with open(input_file, 'r') as txt_file:
    try:
        for line in txt_file:

    #        i = i+1
    #        print(i)

            parts = line.split()


            device, core, index, time, pid, event, rwbs = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]

                 
#    except IndentationError:
#        pass
            if len(parts)<10:

                offset = None
                length = None
                proc = parts[7]
                process = proc.replace('[', '').replace(']', '')

            else:
                offset = parts[7]
                length = parts[9]
                proc = parts[10]
                process = proc.replace('[', '').replace(']', '')

    #        print(parts)




            with open(output_file, 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([device, core, index, time, pid, event, rwbs, offset, length, process ])

    except IndexError:
        pass
print("CSV file create,,, file name :", output_file)

