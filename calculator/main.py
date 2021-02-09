import argparse
from datetime import datetime, timedelta
import csv
import os.path

def print_time(action: str):
    current_datetime = datetime.now()
    date_string = current_datetime.strftime("%Y/%m/%d")
    time_string = current_datetime.strftime("%H:%M:%S")
    print(date_string)
    print(time_string)
    with open('work_time.csv', mode='a') as work_time_file:
        work_time_writer = csv.writer(work_time_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        work_time_writer.writerow([date_string, time_string, action])
    

def calculate_delta_work_time(minutes_per_day: int):
    with open('work_time.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        start_row = [None] * 3
        end_row = [None] * 3
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]} {row[1]} {row[2]}')
                if row[2] == "start":
                    start_row = row
                elif row[2] == "end":
                    end_row = row
                
                if start_row[0] == end_row[0]:
                    start_time = datetime.strptime("{} {}".format(start_row[0], start_row[1]), '%Y/%m/%d %H:%M:%S')
                    end_time = datetime.strptime("{} {}".format(end_row[0], end_row[1]), '%Y/%m/%d %H:%M:%S')
                    time_worked = (end_time - start_time)
                    print("\tTime worked: {}".format(time_worked))
                    delta_working_time = time_worked - timedelta(minutes=minutes_per_day)
                    print("\tOver-/Underhours: {}".format(delta_working_time))

                line_count += 1


parser = argparse.ArgumentParser()
parser.add_argument("-s","--start", help="Log the current time as start of work", action="store_true")
parser.add_argument("-e","--end", help="Log the current time as end of work", action="store_true")
parser.add_argument("-c","--calculate", type=float, help="Calculate total work time (+/-) based on the value given here as work+break hours")

# create csv if it doesn't exist
if not os.path.isfile("work_time.csv"):
    with open('work_time.csv', mode='w') as work_time_file:
        work_time_writer = csv.writer(work_time_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        work_time_writer.writerow(['date', 'time', 'action'])

args = parser.parse_args()
if args.start:
    print_time("start")
elif args.end:
    print_time("end")
elif args.calculate:
    print("Calculating...")
    hours_in_minutes = args.calculate * 60
    print("Work time per day (minutes): {}".format(hours_in_minutes))
    calculate_delta_work_time(hours_in_minutes)
