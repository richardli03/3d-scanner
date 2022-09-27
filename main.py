"""
Runs the main pipeline of our 3D visualizer system
"""

import math
import serial
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Define a few constants to streamline workflow
USING_SENSOR = False  # So there aren't errors if we just want to simulate data
IR_SENSOR_PORT = "/dev/ttyACM1" # the port that the arduino is plugged into
BAUD_RATE = 9600

DISPLAY = True  # Show the plot with the visualization of the data
CALCULATE = True  # Calculate the actual distance associated with the sensor readings
LOGGING = True  # Save the data to some file for future visualization


def visualize(path):
    """
    To simplify repeating the visualization of the data without needing to run with the
    arduino every time, we saved the data from a previous arduino run into some .csv,
    and now we can simply visualize that instead with this code.

    Args:
        path (str): the path to the csv file containing the IR sensor data.

    Returns:
        Nothing, but visualizes the plot
    """
    display = pd.read_csv(f"{path}.csv")
    display = display.iloc[:, 1:]
    display = display.to_numpy()
    
    # normalize colors to map them.
    normalized_colors = display[2]/np.linalg.norm(display[2])

    fig = plt.figure()
    # to prevent stretching
    plt.axis("equal")

    # negate x values because we scanned right -> left
    plt.scatter(x=-display[0], y=display[1], cmap="Greys", c=normalized_colors)
    plt.savefig('K_panning.png', dpi='figure')
    fig.tight_layout()
    plt.show()

def calculate(path):
    """
    Calculate real distances given the sensor readings

    Args:
      PATH (str): The path to the datafile containing our IR data.

    Returns:
      True once completed

    """
    new_distances = []
    database = pd.read_csv(f"{path}.csv")
    database = database.iloc[:, 1:]
    database = database.to_numpy()
    for distance in database[2]:
        distance = calculate_real_distance(distance)
        new_distances.append(distance) 
    database[2] = new_distances    
    pd.DataFrame(database).to_csv(f"{path}_calculations.csv")
    return True

def calculate_real_distance(ir_reading):
    """
    Given some reading from the IR sensor, plug it into the calibration
    curve to translate that to a real distance.

    Args:
        ir_reading (int): the raw number that the ir sensor spits out.
    """
    # We want to account for this case because ln(0) returns an error
    if ir_reading == 0:
        return 0.0
    distance = (math.log(ir_reading/780))/-0.0253
    return distance

def main():
    """
    Run the main pipeline of the sensor visualization.
    """
    if USING_SENSOR:
        serial_port = serial.Serial(IR_SENSOR_PORT, BAUD_RATE, timeout=1)

    # Corresponding with degrees. Set based upon arduino settings
    tilt_range = 1
    pan_range = 45

    # X for pan degree, Y for tilt degree, S for raw sensor reading
    display = pd.DataFrame(index=["X", "Y", "S"],
                           columns=range(0, ((tilt_range-1)*pan_range)))

    # Initialize steppers that will iterate through dataframe
    tilt_step = 0
    pan_step = 0
    step = 0

    # Wait for the arduino to say you're starting before starting
    starting = False
    while starting is False:
        data = serial_port.readline().decode()
        if len(data) > 0:
            if data == "starting\r\n":
                starting = True

    # Main workflow: step through pan and tilt and record sensor reading
    while pan_step < pan_range and starting:
        data = serial_port.readline().decode()
        if len(data) > 0:
            print(data)
            if "tilt" in data:
                tilt_step += 1
                # Print out tilt angle
                print(data)
                continue

            if "pan" in data:
                pan_step += 1
                tilt_step = 0
                # Print out pan angle
                print(data)
                continue

            # Log to database
            display.at["X", step] = int(pan_step)
            display.at["Y", step] = int(tilt_step)
            display.at["S", step] = int(data)

        step += 1

    # Define a filename to log to
    path = "display_panning"

    if LOGGING:
        display.to_csv(f"{path}.csv")

    if DISPLAY:
        visualize(path)

    if CALCULATE:
        calculate(path)


if __name__ == "__main__":
    main()
    