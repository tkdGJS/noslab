import csv
import sys


input_file = 'D_trace'
output_file = 'tracefile.csv'

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

