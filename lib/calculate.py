from argparse import ArgumentParser
from pathlib import Path
import os
import matplotlib.pyplot as plt


def main():
    parser = ArgumentParser(description='Calculate player running record given the data directory.')
    parser.add_argument('-data', type=str, metavar='<name_of_datadirectory>', dest='dir_name', help='Directory containing the player data.')
    parser.add_argument('-show', type=int, metavar='<show graph or not>', dest='isShow', help='1 if want see the graph.')
    parser.add_argument('-output', type=str, metavar='<name_of_output>', dest='output', help='Output file')
    A = parser.parse_args()
    cwd = os.getcwd()
    parent_path = Path(cwd).parent
    data_dir = os.path.join(str(parent_path), A.dir_name)

    miles_dict = {}
    speed_dict = {}

    for dir_name in os.listdir(data_dir):
        miles_dict[dir_name] = []
        speed_dict[dir_name] = []
        for file_name in os.listdir(os.path.join(data_dir, dir_name)):
            if file_name.endswith('csv'):
                file = open(os.path.join(os.path.join(data_dir, dir_name), file_name), 'r')
                mile_sum = 0
                running_time_sum = 0
                for line in file:
                    line = line.replace('\n', '')
                    line_split_result = line.split(',')
                    mile_sum += float(line_split_result[0])
                    running_time_sum += convert_to_hour(line_split_result[1])
                    #print('running', mile_sum, running_time_sum)
                    miles_dict[dir_name].append([line_split_result[2], mile_sum])
                    speed_dict[dir_name].append([line_split_result[2], mile_sum / running_time_sum])

    #print(miles_dict)
    if(A.isShow == 1):
        drawing(miles_dict, 'km')
        drawing(speed_dict, 'speed')

    result_dict = calculate_reward(700, miles_dict, speed_dict)

    writefile = open(os.path.join(str(parent_path), A.output), 'w')
    writefile.write('player,Basic Reward(RMB),Total Km,Km Ranking,Km Portion,Km Reward(RMB),Average Speed,Speed Ranking,Speed Portion,Speed Reward(RMB), Total Reward(RMB)\n')
    entry_names = ['basic_reward', 'total_Km', 'Km_Ranking', 'Km_Ranking_Portion', 'Km_Reward', 'avg_speed', 'Speed_Ranking', 'Speed_Ranking_Portion', 'Speed_Reward', 'Total_Reward']
    for player in result_dict:
        writefile.write(player)
        writefile.write(',')
        for index, entry in enumerate(entry_names):
            writefile.write(str(result_dict[player][entry]))
            if index != len(entry_names) - 1:
                writefile.write(',')
        writefile.write('\n')
    print('Result Writen to', os.path.join(str(parent_path), A.output))


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


def reward_distribution(index, player_count):
    return((2.0 * player_count - index) / (player_count * (player_count * 1.5 - 0.5)))


def calculate_reward(total_reward, input_mile_dict, input_speed_dict):
    result_dict = {}
    mile_inverted_dict = {}
    mile_list = []
    speed_inverted_dict = {}
    speed_list = []
    for player in input_mile_dict:
        result_dict[player] = {}
        result_dict[player]['basic_reward'] = total_reward * 0.33 / 5.0

        result_dict[player]['total_Km'] = input_mile_dict[player][len(input_mile_dict[player]) - 1][1]
        mile_inverted_dict[input_mile_dict[player][len(input_mile_dict[player]) - 1][1]] = player
        mile_list.append(input_mile_dict[player][len(input_mile_dict[player]) - 1][1])

        result_dict[player]['avg_speed'] = input_speed_dict[player][len(input_speed_dict[player]) - 1][1]
        speed_inverted_dict[input_speed_dict[player][len(input_speed_dict[player]) - 1][1]] = player
        speed_list.append(input_speed_dict[player][len(input_speed_dict[player]) - 1][1])

    mile_list = sorted(mile_list, reverse=True)
    speed_list = sorted(speed_list, reverse=True)

    for index, item in enumerate(mile_list):
        result_dict[mile_inverted_dict[item]]['Km_Ranking'] = index + 1
        result_dict[mile_inverted_dict[item]]['Km_Ranking_Portion'] = reward_distribution(index + 1, 5)
        result_dict[mile_inverted_dict[item]]['Km_Reward'] = total_reward * 0.34 * result_dict[mile_inverted_dict[item]]['Km_Ranking_Portion']

    for index, item in enumerate(speed_list):
        result_dict[speed_inverted_dict[item]]['Speed_Ranking'] = index + 1
        result_dict[speed_inverted_dict[item]]['Speed_Ranking_Portion'] = reward_distribution(index + 1, 5)
        result_dict[speed_inverted_dict[item]]['Speed_Reward'] = total_reward * 0.33 * result_dict[speed_inverted_dict[item]]['Speed_Ranking_Portion']

    for player in result_dict:
        result_dict[player]['Total_Reward'] = result_dict[player]['basic_reward'] + result_dict[player]['Km_Reward'] + result_dict[player]['Speed_Reward']

    return result_dict


if __name__ == '__main__': main()
