import math
import ch_main
import random

def normalize():
    with open('node_data.csv', 'r') as file:
        lines = file.readlines()
        battery_max = 0
        battery_min = 1000000
        node_max = 0
        node_min = 100000
        normalized_data = []

        # Find min and max values for battery and nodes
        for line in lines[1:]:
            parts = line.strip().split(',')
            battery = int(parts[1].strip())
            node = int(parts[2].strip())
            if battery >= battery_max:
                battery_max = battery
            if battery <= battery_min:
                battery_min = battery
            if node >= node_max:
                node_max = node
            if node <= node_min:
                node_min = node

        # Normalize the data
        for line in lines[1:]:
            print(f'current parts:{line}')
            parts = line.strip().split(',')
            id = int(parts[0].strip())
            battery = int(parts[1].strip())
            node = int(parts[2].strip())

            # Avoid division by zero for battery normalization
            if battery_max == battery_min:
                battery_norm = 0.0  # or any appropriate value
            else:
                battery_norm = (battery - battery_min) / (battery_max - battery_min)

            # Avoid division by zero for node normalization
            if node_max == node_min:
                node_norm = 0.0  # or any appropriate value
            else:
                node_norm = (node - node_min) / (node_max - node_min)

            normalized_data.append(f"{id},{battery_norm},{node_norm}\n")
            print(f"appended:{id},{battery_norm},{node_norm}\n")

        # Write the normalized data to a new CSV file
        with open('normalized_node_data.csv', 'w') as outfile:
            outfile.write('Node_ID,Battery_Normalized,Nodes_Normalized\n')
            for lines in normalized_data:
                outfile.write(lines)

        print(f'battery: max={battery_max}, min={battery_min}')
        print(f'node: max={node_max}, min={node_min}')
        
    return normalized_data

def sim_score(current_head, node, battery_weight=1.0, comm_weight=1.0, battery_penalty_factor=2, comm_penalty_factor=2):
    battery_current, comm_nodes_current = current_head
    battery_node, comm_nodes_node = node

    # calculate diff battery
    if battery_node < battery_current:
        battery_diff = (battery_current - battery_node) * battery_penalty_factor
    else:
        battery_diff = battery_current - battery_node

    # calculate diff communicatable nodes
    if comm_nodes_node < comm_nodes_current:
        comm_nodes_diff = (comm_nodes_current - comm_nodes_node) * comm_penalty_factor
    else:
        comm_nodes_diff = comm_nodes_current - comm_nodes_node

    # euclidian distance
    weighted_distance = math.sqrt((battery_diff * battery_weight)**2 + (comm_nodes_diff * comm_weight)**2)
    return weighted_distance

def extract_from_csv_norm():
    # 実行
    # normalized_data = normalize()
    normalize()
    print("Normalized data written to 'normalized_node_data.csv'")
    param_dict = {}
    c_head = (1.0,1.0)
    with open('normalized_node_data.csv','r') as file:
        lines = file.readlines()
        for line in lines[1:]: #正規化の時は2:, 通常の値の時は1
            parts = line.strip().split(',')
            node_id = int(parts[0].strip())
            battery = float(parts[1].strip())
            node_number = float(parts[2].strip())
            if node_id == 0:
                c_head = (battery, node_number)
            else:
                print(node_id, battery, node_number)
                node = (battery, node_number)
                param = sim_score(c_head, node)
                param_dict[node_id] = param

    print('param_dict in extract_from_csv:', param_dict)  # 追加: param_dictの内容を確認
    return param_dict

def head_selection(param_dict):
    print('param_dict:', param_dict)
    if not param_dict:
        raise ValueError("param_dict is empty")
    cluster_head = min(param_dict, key=param_dict.get)
    return cluster_head

def leach(param_dict):
    cluster_head = random.choice(list(param_dict.items()))
    return cluster_head