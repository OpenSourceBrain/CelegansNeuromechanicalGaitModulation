import numpy as np
import time
import os

def generate_wcon(time_arr, x_arr, y_arr, original_file_name, wcon_file_name):

    assert(x_arr.shape == y_arr.shape)
    assert(time_arr.size == x_arr.shape[1])

    num_steps = time_arr.size
    num_positions_per_step = x_arr.shape[0]
    
    last_time_idx = num_steps - 1
    last_pos_idx = num_positions_per_step - 1

    info = "Loaded: %s points from %s, saving %i frames" % (num_steps, original_file_name, num_steps)
    wcon = open(wcon_file_name, 'w')

    wcon.write('''{
    "metadata":{
        "who":"CelegansNeuromechanicalGaitModulation",
        "timestamp":"%s",
        "protocol":"Generated by CelegansNeuromechanicalGaitModulation!"
    },
    "units":{ "t":"s",
                "x":"micrometers",
                "y":"micrometers"},
    "comment":"Saved from CelegansNeuromechanicalGaitModulation data.",
    "note":"%s",
    "data":[\n''' % (time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()), info))

    wcon.write('''            {"id":"wormTest",
                "t":[ ''')
    for i, t in enumerate(time_arr):
        wcon.write('%s' % (t))
        if i != last_time_idx:
            wcon.write(', ')
        else:
            wcon.write('],\n')

    wcon.write('''             "x":[ ''')
    for i, x_arr_at_time in enumerate(x_arr.T):
        wcon.write('[')
        for j, x in enumerate(x_arr_at_time):
            wcon.write('%s' % (float(x)))
            if j != last_pos_idx:
                wcon.write(', ')
        wcon.write(']')
        if i == last_time_idx:
            wcon.write(']')
        wcon.write(',\n')


    wcon.write('''             "y":[ ''')
    for i, y_arr_at_time in enumerate(y_arr.T):
        wcon.write('[')
        for j, y in enumerate(y_arr_at_time):
            wcon.write('%s' % (float(y)))
            if j != last_pos_idx:
                wcon.write(', ')
        wcon.write(']')

        if i != last_time_idx:
            wcon.write(',\n')
        else:
            wcon.write(']\n')

    wcon.write('\n}\n\n]\n\n}\n')

    wcon.close()

    print("Generated WCON file: %s"%wcon_file_name)

def validate(wcon_file):
    import json, jsonschema

    wcon_schema = "wcon_schema.json"

    if not os.path.isfile("wcon_schema.json"):
        print("Cannot validate file: %s!! WCON schema %s not found!!"%(wcon_file, wcon_schema))
        return

    # The WCON schema
    with open(wcon_schema, "r") as wcon_schema_file:
        schema = json.loads(wcon_schema_file.read())

    # Our example WCON file
    with open(wcon_file, 'r') as infile:
        serialized_data = infile.read()

    # Load the whole JSON file into a nested dict.
    w = json.loads(serialized_data)

    # Validate the raw file against the WCON schema
    jsonschema.validate(w, schema)

    print("File %s is valid WCON!!"%wcon_file)


if __name__ == "__main__":

    pos_file_name = "simdata.csv"
    data = np.genfromtxt(pos_file_name, delimiter=",").T
    ts = data[0]

    x_offset = 1
    y_offset = 2
    d_offset = 3

    x_slice = data[x_offset::3][:]
    y_slice = data[y_offset::3][:]

    wcon_file_name = "simdata.wcon"

    generate_wcon(ts, x_slice, y_slice, pos_file_name, wcon_file_name)
    validate(wcon_file_name) 
