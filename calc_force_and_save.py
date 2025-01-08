import numpy as np
from tqdm.auto import tqdm
from optical_force import calculate_force_and_torque

def calc_and_save(dict_parameters: dict):
    for i in  dict_parameters:
        if dict_parameters[i] == None:
            print(f"Parameter {i} is missing")
            return None
    # Paramerters of the simulation
    radius = dict_parameters['radius']
    num_rays = dict_parameters['num_rays']
    w0 = dict_parameters['w0']
    P = dict_parameters['P']
    n_medium = dict_parameters['n_medium']
    n_particle = dict_parameters['n_particle']
    # Axis
    axis = dict_parameters['selected_view']
    # Min and max points of the simulation
    min_point = dict_parameters['min_point']
    max_point = dict_parameters['max_point']
    # Path to save the simulation
    save_path = dict_parameters['save_path']
    if save_path == "":
        pass
    else:
        save_path = save_path + "/"
    
    if max_point < min_point:
        print("Max point must be greater than Min point")
        return None
    
    # Create points to vary the sphere position
    points = np.arange(min_point, max_point+0.5, 0.5)
    # Create sphere_positions based on the chosen axis
    match axis:
        case 'X':
            sphere_positions = np.asarray([[x, 0, 0] for x in points])
        case 'Y':
            sphere_positions = np.asarray([[0, y, 0] for y in points])
        case 'Z':
            sphere_positions = np.asarray([[0, 0, z] for z in points])
        case _:
            print("Invalid axis to vary. Choose 'X', 'Y', or 'Z'.")
    
    # Initialize the results lists
    F_result = []
    Torque_result = []
    
    # Calculate the force and torque for each sphere position
    for position in tqdm(sphere_positions, position=0, leave=True):
        F, Torque, _ = calculate_force_and_torque(radius, num_rays, w0, P, n_medium, n_particle, position)
        F_result.append(np.insert(F, 0, position))
        Torque_result.append(np.insert(Torque, 0, position))

    # make Force and Torque as numpy arrays
    F_result = np.asarray(F_result)
    Torque_result = np.asarray(Torque_result)
    
    # Save the results
    np.savetxt(f"{save_path}F_{axis}.csv", F_result, delimiter=",")
    np.savetxt(f"{save_path}Torque_{axis}.csv", Torque_result, delimiter=",")
    print("Results saved successfully")