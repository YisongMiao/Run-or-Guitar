from argparse import ArgumentParser
from pathlib import Path
import os
import matplotlib.pyplot as plt


def main():
    parser = ArgumentParser(description='Calculate player running record given the data directory.')
    parser.add_argument('-data', type=str, metavar='<name_of_datadirectory>', dest='dir_name', help='Directory containing the player data.')
    parser.add_argument('-show', type=int, metavar='<1 if want see the graph or not>', dest='isShow', help='Directory containing the player data.')
    A = parser.parse_args()
    cwd = os.getcwd()
    parent_path = Path(cwd).parent
    data_dir = os.path.join(str(parent_path), A.dir_name)
    print(data_dir)

    miles_dict = {}
    speed_dict = {}

    for dir_name in os.listdir(data_dir):
        miles_dict[dir_name] = []
        speed_dict[dir_name] = []
        for file_name in os.listdir(os.path.join(data_dir, dir_name)):
            if file_name.endswith('csv'):
                print(dir_name, file_name)
                file = open(os.path.join(os.path.join(data_dir, dir_name), file_name), 'r')
                mile_sum = 0
                running_time_sum = 0
                for line in file:
                    line = line.replace('\n', '')
                    line_split_result = line.split(',')
                    #print(line)
                    mile_sum += float(line_split_result[0])
                    running_time_sum += convert_to_hour(line_split_result[1])
                    #print('running', running_time_sum)
                    miles_dict[dir_name].append([line_split_result[2], mile_sum])
                    speed_dict[dir_name].append([line_split_result[2], mile_sum / running_time_sum])

    if(A.isShow == 1):
        drawing(miles_dict, 'km')
        drawing(speed_dict, 'speed')


def get_date_span(input_date):
    start_date = 18
    month = input_date.split('-')[0]
    date = input_date.split('-')[1]
    if(month == '12'):
        return (int(date) - start_date + 1)
    if(month == '1'):
        return (31 - start_date + 1 + int(date))


def convert_to_hour(input_time):
    split_result = input_time.split(':')
    if(len(split_result) == 3):
        return(float(split_result[0]) + float(split_result[1]) / 60.0 + float(split_result[2]) / 3600.0)
    if(len(split_result) == 2):
        return(float(split_result[0]) / 60.0 + float(split_result[1]) / 3600.0)


def drawing(input_dict, kind):
    for dir_name in input_dict:
        x_array = []
        y_array = []
        for entry in input_dict[dir_name]:
            x_array.append(get_date_span(entry[0]))
            y_array.append(entry[1])
        plt.plot(x_array, y_array, label=dir_name, linestyle='--', marker='o')
    plt.legend()
    plt.xlabel('Date')
    if(kind == 'km'):
        plt.title('Total KMs Ranking')
        plt.ylabel('Km')
    if(kind == 'speed'):
        plt.title('Total Speed Ranking')
        plt.ylabel('Km/h')
    plt.show()


if __name__ == '__main__': main()
