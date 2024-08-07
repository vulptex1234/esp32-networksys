import math
import ch_main

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
            parts = line.strip().split(',')
            id = int(parts[0].strip())
            battery = int(parts[1].strip())
            node = int(parts[2].strip())

            battery_norm = (battery - battery_min) / (battery_max - battery_min)
            node_norm = (node - node_min) / (node_max - node_min)

            normalized_data.append(f"{id},{battery_norm},{node_norm}\n")

        # Write the normalized data to a new CSV file
        with open('normalized_node_data.csv', 'w') as outfile:
            outfile.write('Node_ID,Battery_Normalized,Nodes_Normalized\n')
            outfile.writelines(normalized_data)

        print(f'battery: max={battery_max}, min={battery_min}')
        print(f'node: max={node_max}, min={node_min}')
        
    return normalized_data

# 実行
normalized_data = normalize()
print("Normalized data written to 'normalized_node_data.csv'")

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

def extract_from_csv():
    c_head = (100, 5)  # test use
    param_dict = {}

    with open('node_data.csv', 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            parts = line.strip().split(',')
            node_id = int(parts[0].strip())
            battery = int(parts[1].strip())
            node_number = int(parts[2].strip())

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