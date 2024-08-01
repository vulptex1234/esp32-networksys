import math
import ch_main

def sim_score(current_head, node, battery_weight=1.0, comm_weight=1.0, battery_penalty_factor=2, comm_penalty_factor=2):
    battery_current, comm_nodes_current = current_head
    battery_node, comm_nodes_node = node

    #calculate diff battery
    if battery_node < battery_current:
        battery_diff = (battery_current - battery_node) * battery_penalty_factor
    else:
        battery_diff = battery_current - battery_node

    #calculate diff communicatable nodes
    if comm_nodes_node < comm_nodes_current:
        comm_nodes_diff = (comm_nodes_current - comm_nodes_node) * comm_penalty_factor
    else:
        comm_nodes_diff = comm_nodes_current - comm_nodes_node

    #euclidian distance
    weighted_distance = math.sqrt((battery_diff * battery_weight)**2 + (comm_nodes_diff * comm_weight)**2)
    return weighted_distance

def extract_from_csv():
    c_head = (100, 5) #test use

    with open('node_data.csv', 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            parts = line.strip().split(',')
            node_id = int(parts[0].strip())
            battery = int(parts[1].strip())
            node_number = int(parts[2].strip())

            print(node_id,battery,node_number)
            node = (battery,node_number)

            param = sim_score(c_head,node)
            ch_main.param_dict[node_id] = param

    print(ch_main.param_dict)