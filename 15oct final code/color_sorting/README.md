
# Color Sorting Application with Robotic Arm

## Extablishing Connection
    
Connect PLC, PC and Robot on same Network via. Ethernet cable.

To check weather the connection is established:
    
    Open command Prompt
    Navigate to the color_sorting folder

    Run:
    python test.py

You will see "Done Connecting to PLC..." printed.

This means the connection is succesfully established
## Precautions

Set speed of the robot on moderate then after some trials increase it as our requirnment.
If any accident occurs with Robot press emergency STOP switch.

Check weather the Z axis of the Robot does not clash with the WebCam.


## Check for HSV Values (Optional)
In the color_sorting folder:

    Open Command Prompt
    navigate to color_sorting folder

    Run:
    python hsv_trackbar.py

Adjust the HSV values by moving the trackbars to adjust the values.

## Running the Main Code
Place the blocks in the work space. 

** Check if all the connectons are made correctly.

** Check for the Z axis of the robot, weather will it collide with the Webcam.

Put the Robot in the Auto Mode by rotating the Selector switch knob.

Start the process:

In the color_sorting folder 
    Open Command Prompt
    navigate to color_sorting folder

    Run:
    python main_file.py

Then Run the programme on the PLC/ Robot Side 
## Robot-->PLC Communication Testing

    1. In the GX WORKS software go on the communication test software icon and click on START.