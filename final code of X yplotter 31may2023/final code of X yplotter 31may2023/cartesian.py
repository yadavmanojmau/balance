import time
from threading import Thread

import cv2
from flask import Flask, request
import asyncio

import os
from PIL import Image, ImageDraw, ImageFont
import webbrowser
import subprocess
from pywinauto.application import Application
import snap7
import struct
import re

import math

app = Flask(__name__)


@app.route('/send', methods=['post'])
def sendToPLC():
    print('method called')
    a = request.form.get('a')
    b = request.form.get('b')
    print(a + " " + b)
    return b


# @app.route('/fetch', methods=['get'])
# def fetchFromPLC():


#     # while i<10:
#     i=70
#         # time.sleep(2)
#     return {"i":str(i), "status":True}


@app.route('/generateGcode', methods=['post'])
def imageDraw():
    image_path = request.form.get('imagePath')

    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Sobel edge detection
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    edges = cv2.magnitude(sobelx, sobely)

    # Apply thresholding
    _, edges = cv2.threshold(edges, 94, 255, cv2.THRESH_BINARY)

    # Save the resulting image

    result_path = os.path.join(os.path.expanduser("~"), "Desktop", "result.jpg")
    cv2.imwrite(result_path, edges)

    # Open the image file
    desktop_path = os.path.expanduser("~\Desktop")
    file_path = os.path.join(desktop_path, r"result.jpg")
    image = Image.open(file_path)

    # Resize the image
    new_size = (200, 200)
    resized_image = image.resize(new_size)

    # Set the file path to save the resized image on the desktop
    # resized_file_path = os.path.join("C:\Users\Admin\Desktop\resized.jpg")

    resized_image.save('C:\\Users\\Admin\\Desktop\\resized.jpg')

    # cv2.imwrite(resized_file_path, resized_image)

    # Show the result
    # cv2.imshow('Edges', edges)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    inkscape_path = r"C:\Program Files\Inkscape\inkscape.exe"
    image_path = r'C:\Users\Admin\Desktop\resized.jpg'

    # Launch Inkscape and open the image filen b
    subprocess.Popen([inkscape_path, image_path])

    folder_path = r"C:\Users\Admin\Desktop\Gcodes"
    latest_modification_time = 0

    # Get a list of all files in the folder
    file_list = os.listdir(folder_path)

    # Loop through the list of files and check their modification times
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        modification_time = os.path.getmtime(file_path)
        if modification_time > latest_modification_time:
            latest_modification_time = modification_time
            latest_file_name = file_name

    # Read the contents of the latest file
    with open(os.path.join(folder_path, latest_file_name), "r") as file:
        Gcode = file.read()
        print(Gcode)

    # Set the path of the folder where you want to save the images
    folder_path = r"C:\Users\Admin\Desktop\size"

    # Check if the folder exists, and create it if it doesn't
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Load the image and save it to the folder
    image_path = r"C:\Users\Admin\Desktop\ImageToSave.png"
    image = Image.open(image_path)
    image.save(os.path.join(folder_path, "SavedImage.png"))

    # Launch Inkscape and open the image file
    subprocess.Popen([inkscape_path, image_path])
    return "OK"


start_address = 100  # starting address
length = 4  # double word

plc = snap7.client.Client()
plc.connect('192.168.0.1', 0, 1)  # IP address, rack, slot (from HW settings)


def readMemory(start_address, length):
    reading = plc.read_area(snap7.types.Areas.MK, 0, start_address, length)
    value = struct.unpack('>f', reading)  # big-endian
    return value


def writeMemory(start_address, length, value):
    plc.mb_write(start_address, length, bytearray(struct.pack('>f', value)))  # big-endian


def GCODE(line, x1=0, h_done=0, x_done=0, y_done=0, A_done=0, Gcode=0):
    print("function has been called")
    Feed_Rate = 40
    gg = 0
    writeMemory(start_address + 25 * length, length, gg)
    prev_x = readMemory(start_address + 12 * length, length, )[0]
    prev_y = readMemory(start_address + 13 * length, length, )[0]
    current_velocity_y = 10
    current_velocity_x = 10
    inx = 0
    iny = 0
    G2_exe = 0
    if h_done == 1:
        prev_x = 0
        prev_y = 0
        writeMemory(start_address + 14 * length, length, prev_x)
        writeMemory(start_address + 15 * length, length, prev_y)
    while True:
        if line.startswith('Z03') or line.startswith('M03'):
            s_match = re.search('S(\d+)', line)
            if s_match:
                S = int(s_match.group(1))
            else:
                S = 0
            if S == 10:
                Sol_pos = 0
            writeMemory(start_address + 16 * length, length, Sol_pos)
            return 1
        elif line.startswith('Z05') or line.startswith('M05'):
            s_match = re.search('S(\d+)', line)
            if s_match:
                S = int(s_match.group(1))
            else:
                S = 0
            if S == 60:
                Sol_pos = 1
            writeMemory(start_address + 16 * length, length, Sol_pos)
            return 1
        elif line.startswith('G90'):
            return 1
        elif line.startswith('G21'):
            return 1
        elif line.startswith('G4 P'):
            return 1
        elif line.startswith('G1 F'):
            return 1
        elif line.startswith('G1'):
            x_match = re.search('X(\d+\.*\d+)', line)
            y_match = re.search('Y(\d+\.*\d+)', line)
            if x_match:
                x = float(x_match.group(1))
            else:
                x = 0.0

            if y_match:
                y = float(y_match.group(1))
            else:
                y = 0.0

            dx = x - prev_x
            dy = y - prev_y
            angle = math.atan2(dy, dx) * 180 / math.pi
            if angle < 0:
                angle = (angle + 360) % 360

            else:
                angle = angle
            print(f"Angle between ({prev_x}, {prev_y}) and ({x}, {y}): {angle:.2f} degrees")

            new_velocity_x = 0
            new_velocity_y = 0
            current_velocity_x = 10
            current_velocity_y = 10
            prev_x = x
            prev_y = y
            angle_1 = angle * 3.14 / 180
            new_velocity_x = current_velocity_x * math.cos(angle_1)
            new_velocity_y = current_velocity_y * math.sin(angle_1)
            new_velocity_x = abs(new_velocity_x)
            new_velocity_y = abs(new_velocity_y)
            if new_velocity_x <= 0.0001:
                new_velocity_x = 10
            if new_velocity_y <= 0.0001:
                new_velocity_y = 10
            print('X01:', x, 'Y01:', y, 'speed_x:', new_velocity_x, 'speed_y:', new_velocity_y, 'angle', angle)
            writeMemory(start_address + 1 * length, length, y)
            writeMemory(start_address + 3 * length, length, new_velocity_x)
            writeMemory(start_address + 4 * length, length, new_velocity_y)
            writeMemory(start_address + 5 * length, length, x)
            writeMemory(start_address + 14 * length, length, prev_x)
            writeMemory(start_address + 15 * length, length, prev_y)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)
            print("G1 exe")
            break
        elif line.startswith('G2'):
            i_match = re.search('I(-?\d+\.?\d*)', line)
            j_match = re.search('J(-?\d+\.?\d*)', line)
            x_match = re.search('X(-?\d+\.?\d*)', line)
            y_match = re.search('Y(-?\d+\.?\d*)', line)

            if i_match:
                i = float(i_match.group(1))
            else:
                i = 0

            if j_match:
                j = float(j_match.group(1))
            else:
                j = 0

            if x_match:
                x = float(x_match.group(1))
            else:
                x = 0

            if y_match:
                y = float(y_match.group(1))
            else:
                y = 0
            prev_x = readMemory(start_address + 12 * length, length, )[0]
            prev_y = readMemory(start_address + 13 * length, length, )[0]
            center_x = prev_x + i
            center_y = prev_y + j
            radius = math.sqrt(i ** 2 + j ** 2)
            start_angle = math.atan2(prev_y - center_y, prev_x - center_x)
            end_angle = math.atan2(y - center_y, x - center_x)
            if start_angle <= end_angle:
                start_angle += 2 * math.pi
            num_steps = int(abs((end_angle - start_angle) / (2 * math.pi) * 360 * radius) / Feed_Rate)
            try:
                delta_angle = (end_angle - start_angle) / num_steps
            except:
                return 1
                break
            for step in range(1, num_steps + 1):
                angle = start_angle + delta_angle * step
                arc_x = center_x + radius * math.cos(angle)
                arc_y = center_y + radius * math.sin(angle)
                angular_velocity = Feed_Rate / radius
                current_velocity_x = angular_velocity * radius * math.sin(angle)
                current_velocity_y = angular_velocity * radius * math.cos(angle)
                current_velocity_x = abs(current_velocity_x)
                current_velocity_y = abs(current_velocity_y)
                print(
                    f"Arc point ({arc_x:.2f}, {arc_y:.2f}, {current_velocity_x:.2f}, {current_velocity_y:.2f}, {angle:.2f})")
                writeMemory(start_address + 1 * length, length, arc_y)
                writeMemory(start_address + 3 * length, length, current_velocity_x)
                writeMemory(start_address + 4 * length, length, current_velocity_y)
                writeMemory(start_address + 5 * length, length, arc_x)
                prev_x = arc_x
                prev_y = arc_y
                writeMemory(start_address + 14 * length, length, prev_x)
                writeMemory(start_address + 15 * length, length, prev_y)
                gg = 1
                writeMemory(start_address + 25 * length, length, gg)
                gg = 0
                writeMemory(start_address + 25 * length, length, gg)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)
            gg = 0
            writeMemory(start_address + 25 * length, length, gg)
            return 1
            break

        elif line.startswith('G3'):

            i_match = re.search('I(-?\d+\.?\d*)', line)
            j_match = re.search('J(-?\d+\.?\d*)', line)
            x_match = re.search('X(-?\d+\.?\d*)', line)
            y_match = re.search('Y(-?\d+\.?\d*)', line)

            if i_match:
                i = float(i_match.group(1))
            else:
                i = 0

            if j_match:
                j = float(j_match.group(1))
            else:
                j = 0

            if x_match:
                x = float(x_match.group(1))
            else:
                x = 0

            if y_match:
                y = float(y_match.group(1))
            else:
                y = 0
            prev_x = readMemory(start_address + 12 * length, length, )[0]
            prev_y = readMemory(start_address + 13 * length, length, )[0]
            center_x = prev_x + i
            center_y = prev_y + j
            radius = math.sqrt(i ** 2 + j ** 2)
            start_angle = math.atan2(prev_y - center_y, prev_x - center_x)
            end_angle = math.atan2(y - center_y, x - center_x)
            if start_angle >= end_angle:
                end_angle += 2 * math.pi
            num_steps = int(abs((end_angle - start_angle) / (2 * math.pi) * 360 * radius) / Feed_Rate)
            try:
                delta_angle = (end_angle - start_angle) / num_steps
            except:
                return 1
                break
            for step in range(1, num_steps + 1):
                angle = start_angle + delta_angle * step
                arc_x = center_x + radius * math.cos(angle)
                arc_y = center_y + radius * math.sin(angle)
                angular_velocity = Feed_Rate / radius
                current_velocity_x = angular_velocity * radius * math.sin(angle)
                current_velocity_y = angular_velocity * radius * math.cos(angle)
                current_velocity_x = abs(current_velocity_x)
                current_velocity_y = abs(current_velocity_y)
                print(f"Arc point ({arc_x:.2f}, {arc_y:.2f}, {current_velocity_x:.2f}, {current_velocity_y:.2f})")
                writeMemory(start_address + 1 * length, length, arc_y)
                writeMemory(start_address + 3 * length, length, current_velocity_x)
                writeMemory(start_address + 4 * length, length, current_velocity_y)
                writeMemory(start_address + 5 * length, length, arc_x)
                prev_x = arc_x
                prev_y = arc_y
                writeMemory(start_address + 14 * length, length, prev_x)
                writeMemory(start_address + 15 * length, length, prev_y)
                gg = 1
                writeMemory(start_address + 25 * length, length, gg)
                gg = 0
                writeMemory(start_address + 25 * length, length, gg)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)
            gg = 0
            writeMemory(start_address + 25 * length, length, gg)
            return 1
            break
        else:
            return 1
    return "OK"


@app.route('/drawSquare', methods=['post'])
def square():
    # sqrt, x = 100, y = 50, side = 100
    x = int(request.form.get('x'))
    y = int(request.form.get('y'))
    side = int(request.form.get('side'))
    sqrt = int(request.form.get('sqrt'))
    pos1 = 0
    pos2 = 0
    pos3 = 0
    pos4 = 0
    pos5 = 0
    x1_done = 0
    y1_done = 0
    new_velocity_x = 10
    new_velocity_y = 10
    writeMemory(start_address + 3 * length, length, new_velocity_x)
    writeMemory(start_address + 4 * length, length, new_velocity_y)
    while True:

        gg = 0
        writeMemory(start_address + 25 * length, length, gg)
        if sqrt == 1:
            sqrt = 0
            Sol_pos = 0
            writeMemory(start_address + 16 * length, length, Sol_pos)
            writeMemory(start_address + 5 * length, length, x)
            writeMemory(start_address + 1 * length, length, y)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x_done = readMemory(start_address + 6 * length, length, )[0]

                if x_done == 0.0:
                    print('passing the value at stage 0')
                    pass

                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos1 = 1
                    print('Breaking from stage 0')

                    break

        if pos1 == 1:
            pos1 == 0
            Sol_pos = 1
            writeMemory(start_address + 16 * length, length, Sol_pos)
            time.sleep(0.5)
            x1 = x + side
            y1 = y
            print(x1)
            print(y1)
            writeMemory(start_address + 5 * length, length, x1)
            writeMemory(start_address + 1 * length, length, y1)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x1_done = readMemory(start_address + 30 * length, length, )[0]
                if x1_done == 0.0:
                    print('passing the value at stage 1')
                    pass
                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos2 = 1
                    print('Breaking from stage 1')

                    break

        if pos2 == 1:
            pos2 == 0
            print('Stage-II')
            x1 = x1
            y1 += side
            print(x1)
            print(y1)
            writeMemory(start_address + 5 * length, length, x1)
            writeMemory(start_address + 1 * length, length, y1)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                y1_done = readMemory(start_address + 31 * length, length, )[0]
                if y1_done == 0.0:
                    print('passing the value at stage 2')
                    pass
                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos3 = 1
                    print('Breaking from stage 2')

                    break

        if pos3 == 1:
            pos3 == 0
            print('Stage-III')
            x1 -= side
            print(x1)
            print(y1)
            writeMemory(start_address + 5 * length, length, x1)
            writeMemory(start_address + 1 * length, length, y1)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x1_done = readMemory(start_address + 30 * length, length, )[0]
                if x1_done == 0.0:
                    print('passing the value at stage 3')
                    pass
                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos4 = 1
                    print('Breaking from stage 3')

                    break

        if pos4 == 1:
            pos4 == 0
            print('Stage-IV')
            x1 = x
            y1 = y - 1.7
            print(x1)
            print(y1)
            writeMemory(start_address + 5 * length, length, x1)
            writeMemory(start_address + 1 * length, length, y1)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                y1_done = readMemory(start_address + 31 * length, length, )[0]
                if y1_done == 0.0:
                    print('passing the value at stage 4')
                    pass
                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos5 = 1
                    time.sleep(0.5)
                    Sol_pos = 0
                    writeMemory(start_address + 16 * length, length, Sol_pos)
                    print('Breaking from stage 4')

                    break

        if pos5 == 1:
            pos5 == 0
            print('Stage-V')
            y = 0
            x = 0

            writeMemory(start_address + 5 * length, length, x)
            writeMemory(start_address + 1 * length, length, y)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x_done = readMemory(start_address + 6 * length, length, )[0]
                if x_done == 0.0:
                    print('passing the value at stage 4')
                    pass
                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos6 = 1

                    print('Breaking from stage 5')
                    return pos6

                    break

        break
    return "OK"


@app.route('/drawImage', methods=['post'])
def drawImage():
    folder_path = r"C:\Users\Admin\Desktop\Gcodes"
    latest_modification_time = 0

    # Get a list of all files in the folder
    file_list = os.listdir(folder_path)

    # Loop through the list of files and check their modification times
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
    modification_time = os.path.getmtime(file_path)
    if modification_time > latest_modification_time:
        latest_modification_time = modification_time
    latest_file_name = file_name
    print("Latest file name", latest_file_name)

    # Read the contents of the latest file
    with open(os.path.join(folder_path, latest_file_name), "r") as file:
        Gcode = file.read()
    print(Gcode)

    prev_x = 0

    prev_y = 0
    writeMemory(start_address + 14 * length, length, prev_x)
    writeMemory(start_address + 15 * length, length, prev_y)
    current_velocity_y = 10

    current_velocity_x = 10

    g_stat = 0
    writeMemory(start_address + 28 * length, length, g_stat)
    latest_file_name = "C:\\Users\\Admin\\Desktop\\Gcodes\\" + latest_file_name
    print("Final file name", latest_file_name)
    with open(latest_file_name) as file:
        for line in file:
            print("line")
            while True:
                x = readMemory(start_address + 11 * length, length, )[0]
                x_done = readMemory(start_address + 6 * length, length, )[0]
                y_done = readMemory(start_address + 7 * length, length, )[0]
                h_done = readMemory(start_address + 10 * length, length, )[0]
                A_done = readMemory(start_address + 24 * length, length, )[0]

                g_stat_plc = readMemory(start_address + 29 * length, length, )[0]
                if x_done == 1.0 or h_done == 1.0 or g_stat_plc == 1.0:
                    print(h_done)
                    g_stat = 0
                    writeMemory(start_address + 28 * length, length, g_stat)

                    print(line)
                    if GCODE(line) == 1:
                        g_stat = 1
                        writeMemory(start_address + 28 * length, length, g_stat)
                    while True:
                        x = readMemory(start_address + 11 * length, length, )[0]
                        x_done = readMemory(start_address + 6 * length, length, )[0]
                        y_done = readMemory(start_address + 7 * length, length, )[0]
                        h_done = readMemory(start_address + 10 * length, length, )[0]
                        A_done = readMemory(start_address + 24 * length, length, )[0]
                        if x_done == 0 and h_done == 0:
                            break
                        else:
                            pass
                    break
                else:
                    pass
    return "OK"


@app.route('/drawRectangle', methods=['post'])
def rectangle():
    x = int(request.form.get('x'))
    y = int(request.form.get('y'))
    side = int(request.form.get('length'))
    side2 = int(request.form.get('breadth'))

    rect = 1

    pos1 = 0
    pos2 = 0
    pos3 = 0
    pos4 = 0
    pos5 = 0
    x1_done = 0
    y1_done = 0
    new_velocity_x = 10
    new_velocity_y = 10
    writeMemory(start_address + 3 * length, length, new_velocity_x)
    writeMemory(start_address + 4 * length, length, new_velocity_y)
    while True:

        gg = 0
        writeMemory(start_address + 25 * length, length, gg)
        if rect == 1:
            rect = 0
            Sol_pos = 0
            writeMemory(start_address + 16 * length, length, Sol_pos)
            writeMemory(start_address + 5 * length, length, x)
            writeMemory(start_address + 1 * length, length, y)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x_done = readMemory(start_address + 6 * length, length, )[0]

                if x_done == 0.0:
                    print('passing the value at stage 0')
                    pass

                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos1 = 1
                    print('Breaking from stage 0')

                    break

        if pos1 == 1:
            pos1 == 0
            Sol_pos = 1
            writeMemory(start_address + 16 * length, length, Sol_pos)
            time.sleep(0.5)
            x1 = x + side
            y1 = y
            print(x1)
            print(y1)
            writeMemory(start_address + 5 * length, length, x1)
            writeMemory(start_address + 1 * length, length, y1)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x1_done = readMemory(start_address + 30 * length, length, )[0]
                if x1_done == 0.0:
                    print('passing the value at stage 1')
                    pass
                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos2 = 1
                    print('Breaking from stage 1')

                    break

        if pos2 == 1:
            pos2 == 0
            print('Stage-II')
            y1 += side2
            print(x)
            print(y)
            writeMemory(start_address + 5 * length, length, x1)
            writeMemory(start_address + 1 * length, length, y1)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                y1_done = readMemory(start_address + 31 * length, length, )[0]
                if y1_done == 0.0:
                    print('passing the value at stage 2')
                    pass
                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos3 = 1
                    print('Breaking from stage 2')

                    break

        if pos3 == 1:
            pos3 == 0
            print('Stage-III')
            x1 -= side
            print(x)
            print(y)
            writeMemory(start_address + 5 * length, length, x1)
            writeMemory(start_address + 1 * length, length, y1)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x1_done = readMemory(start_address + 30 * length, length, )[0]
                if x1_done == 0.0:
                    print('passing the value at stage 3')
                    pass
                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos4 = 1
                    print('Breaking from stage 3')

                    break

        if pos4 == 1:
            pos4 == 0
            print('Stage-IV')
            x1 = x1
            y1 = y - 1.8
            print(x1)
            print(y1)
            writeMemory(start_address + 5 * length, length, x1)
            writeMemory(start_address + 1 * length, length, y1)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                y1_done = readMemory(start_address + 31 * length, length, )[0]
                if y1_done == 0.0:
                    print('passing the value at stage 4')
                    pass
                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos5 = 1
                    time.sleep(0.5)
                    Sol_pos = 0
                    writeMemory(start_address + 16 * length, length, Sol_pos)
                    print('Breaking from stage 4')

                    break

        if pos5 == 1:
            pos5 == 0
            print('Stage-V')
            y = 0
            x = 0

            writeMemory(start_address + 5 * length, length, x)
            writeMemory(start_address + 1 * length, length, y)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x_done = readMemory(start_address + 6 * length, length, )[0]
                if x_done == 0.0:
                    print('passing the value at stage 4')
                    pass
                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos6 = 1

                    print('Breaking from stage 5')
                    return pos6

                    break

        break
    return "OK"


@app.route('/drawTriangle', methods=['post'])
def tri():
    x = int(request.form.get('x'))
    y = int(request.form.get('y'))
    side = int(request.form.get('side'))
    tri = 1
    pos1 = 0
    pos2 = 0
    pos3 = 0
    pos4 = 0
    pos5 = 0
    x1_done = 0
    y1_done = 0
    new_velocity_x = 10
    new_velocity_y = 10
    writeMemory(start_address + 3 * length, length, new_velocity_x)
    writeMemory(start_address + 4 * length, length, new_velocity_y)
    while True:

        gg = 0
        writeMemory(start_address + 25 * length, length, gg)
        if tri == 1:
            tri = 0
            Sol_pos = 0
            print(f'x:{x}')
            print(f'y:{y}')
            writeMemory(start_address + 16 * length, length, Sol_pos)
            writeMemory(start_address + 5 * length, length, x)
            writeMemory(start_address + 1 * length, length, y)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x_done = readMemory(start_address + 6 * length, length, )[0]

                if x_done == 0.0:
                    print('passing the value at stage 0')
                    pass

                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos1 = 1
                    print('Breaking from stage 0')

                    break
        if pos1 == 1:
            pos1 = 0
            Sol_pos = 1
            writeMemory(start_address + 16 * length, length, Sol_pos)
            time.sleep(0.5)
            x1 = x + side
            y1 = y
            print(f'x:{x1}')
            print(f'y:{y1}')
            writeMemory(start_address + 5 * length, length, x1)
            writeMemory(start_address + 1 * length, length, y1)

            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x1_done = readMemory(start_address + 30 * length, length, )[0]

                if x1_done == 0.0:
                    print('passing the value at stage 1')
                    pass

                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos2 = 1
                    print('Breaking from stage 1')

                    break

        if pos2 == 1:
            pos2 = 0

            x1 -= (0.5 * side)
            y1 = y1 + math.sqrt(side ** 2 - (0.5 * side) ** 2)
            print(f'x:{x}')
            print(f'y:{y}')
            writeMemory(start_address + 5 * length, length, x1)
            writeMemory(start_address + 1 * length, length, y1)
            angle = 60
            angle_1 = angle * 3.14 / 180
            new_velocity_x = new_velocity_x * math.cos(angle_1)
            new_velocity_y = new_velocity_y * math.sin(angle_1)
            writeMemory(start_address + 3 * length, length, new_velocity_x)
            writeMemory(start_address + 4 * length, length, new_velocity_y)

            new_velocity_x = abs(new_velocity_x)
            new_velocity_y = abs(new_velocity_y)
            time.sleep(1)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                y1_done = readMemory(start_address + 31 * length, length, )[0]

                if y1_done == 0.0:
                    print('passing the value at stage 2')
                    pass

                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos3 = 1
                    print('Breaking from stage 2')

                    break
        if pos3 == 1:
            pos3 = 0

            x1 = x
            y1 = y
            print(f'x:{x1}')
            print(f'y:{y1}')
            writeMemory(start_address + 5 * length, length, x1)
            writeMemory(start_address + 1 * length, length, y1)

            time.sleep(1)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                y1_done = readMemory(start_address + 31 * length, length, )[0]

                if y1_done == 0.0:
                    print('passing the value at stage 2')
                    pass

                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos4 = 1
                    time.sleep(0.5)
                    Sol_pos = 0
                    writeMemory(start_address + 16 * length, length, Sol_pos)
                    print('Breaking from stage 2')

                    break

        if pos4 == 1:
            pos4 = 0

            x = 0
            y = 0
            print(f'x:{x}')
            print(f'y:{y}')
            writeMemory(start_address + 5 * length, length, x)
            writeMemory(start_address + 1 * length, length, y)

            new_velocity_x = 10
            new_velocity_y = 10
            writeMemory(start_address + 3 * length, length, new_velocity_x)
            writeMemory(start_address + 4 * length, length, new_velocity_y)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                y1_done = readMemory(start_address + 31 * length, length, )[0]

                if y1_done == 0.0:
                    print('passing the value at stage 2')
                    pass

                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos5 = 1

                    print('Breaking from stage 2')

                    break
        else:
            print('Printing Else')

        break
    return "OK"


@app.route('/drawCircleStar', methods=['post'])
def drawCircleOrStar():
    command = request.form.get('command')

    if command == "circle":
        latest_file_name = "C:\\Users\\Admin\\Desktop\\preloaded\\circle.txt"
    else:
        latest_file_name = "C:\\Users\\Admin\\Desktop\\preloaded\\star.txt"
    print("Final file name", latest_file_name)
    folder_path = r'C:\Users\Admin\Desktop\preloaded'

    prev_x = 0

    prev_y = 0
    writeMemory(start_address + 14 * length, length, prev_x)
    writeMemory(start_address + 15 * length, length, prev_y)
    current_velocity_y = 10

    current_velocity_x = 10

    g_stat = 0
    writeMemory(start_address + 28 * length, length, g_stat)

    with open(latest_file_name) as file:
        for line in file:
            print("line")
            while True:
                x = readMemory(start_address + 11 * length, length, )[0]
                x_done = readMemory(start_address + 6 * length, length, )[0]
                y_done = readMemory(start_address + 7 * length, length, )[0]
                h_done = readMemory(start_address + 10 * length, length, )[0]
                A_done = readMemory(start_address + 2 * length, length, )[0]

                g_stat_plc = readMemory(start_address + 29 * length, length, )[0]
                if x_done == 1.0 or h_done == 1.0 or g_stat_plc == 1.0 or A_done == 1.0:
                    print(h_done)
                    g_stat = 0
                    writeMemory(start_address + 28 * length, length, g_stat)

                    print(line)
                    if GCODE(line) == 1:
                        g_stat = 1
                        writeMemory(start_address + 28 * length, length, g_stat)
                    while True:
                        x = readMemory(start_address + 11 * length, length, )[0]
                        x_done = readMemory(start_address + 6 * length, length, )[0]
                        y_done = readMemory(start_address + 7 * length, length, )[0]
                        h_done = readMemory(start_address + 10 * length, length, )[0]
                        if x_done == 0 and h_done == 0:
                            break
                        else:
                            pass
                    break
                else:
                    pass

    return "OK"


@app.route('/pulseToLine', methods=['post'])
def pulses_to_line():
    puls = 1
    x = 50
    y = 50
    pulses = int(request.form.get('pulses'))
    in_min = 1000
    in_max = 200000
    out_min = 1
    out_max = 200
    # ans = (pulses - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    pos1 = 0
    pos2 = 0
    pos3 = 0
    x1_done = 0
    y1_done = 0
    new_velocity_x = 10
    new_velocity_y = 10
    writeMemory(start_address + 3 * length, length, new_velocity_x)
    writeMemory(start_address + 4 * length, length, new_velocity_y)
    while True:

        gg = 0
        writeMemory(start_address + 25 * length, length, gg)
        if puls == 1:
            puls = 0
            Sol_pos = 0
            writeMemory(start_address + 16 * length, length, Sol_pos)
            writeMemory(start_address + 5 * length, length, x)
            writeMemory(start_address + 1 * length, length, y)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x_done = readMemory(start_address + 6 * length, length, )[0]

                if x_done == 0.0:
                    pass

                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos1 = 1

                    break

        if pos1 == 1:
            pos1 == 0
            Sol_pos = 1
            writeMemory(start_address + 16 * length, length, Sol_pos)
            x += pulses / 1000
            writeMemory(start_address + 5 * length, length, x)
            writeMemory(start_address + 1 * length, length, y)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x1_done = readMemory(start_address + 30 * length, length, )[0]
                if x1_done == 0.0:
                    p, mm = encoder()
                    print(f'pulses = {p}, distance traveled ={mm}mm')
                    pass
                else:
                    Sol_pos = 0
                    writeMemory(start_address + 16 * length, length, Sol_pos)
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos2 = 1
                    time.sleep(5)

                    break

        if pos2 == 1:
            pos2 == 0

            y = 0
            x = 0
            Sol_pos = 0
            writeMemory(start_address + 16 * length, length, Sol_pos)
            writeMemory(start_address + 5 * length, length, x)
            writeMemory(start_address + 1 * length, length, y)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x_done = readMemory(start_address + 6 * length, length, )[0]
                if x_done == 0.0:
                    pass
                else:

                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos3 = 1
                    return pos3

                    break

        break
    return "OK"


@app.route('/lineToPulse', methods=['post'])
def line_to_pulses():
    line = 1
    x = 50
    y = 50
    MM = int(request.form.get('mm'))
    in_min = 0
    in_max = 200000
    out_min = 1
    out_max = 200
    ans = (MM - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    pos1 = 0
    pos2 = 0
    pos3 = 0
    x1_done = 0
    y1_done = 0
    new_velocity_x = 10
    new_velocity_y = 10
    writeMemory(start_address + 3 * length, length, new_velocity_x)
    writeMemory(start_address + 4 * length, length, new_velocity_y)
    while True:

        gg = 0
        writeMemory(start_address + 25 * length, length, gg)
        if line == 1:
            line = 0
            Sol_pos = 0
            writeMemory(start_address + 16 * length, length, Sol_pos)
            writeMemory(start_address + 5 * length, length, x)
            writeMemory(start_address + 1 * length, length, y)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x_done = readMemory(start_address + 6 * length, length, )[0]

                if x_done == 0.0:
                    pass

                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos1 = 1

                    break

        if pos1 == 1:
            pos1 == 0
            Sol_pos = 1
            writeMemory(start_address + 16 * length, length, Sol_pos)
            x += MM
            writeMemory(start_address + 5 * length, length, x)
            writeMemory(start_address + 1 * length, length, y)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x1_done = readMemory(start_address + 30 * length, length, )[0]
                if x1_done == 0.0:
                    p, mm = encoder()
                    print(f'the pulses ={p},mm value = {mm}')

                    pass
                else:
                    Sol_pos = 0
                    writeMemory(start_address + 16 * length, length, Sol_pos)
                    time.sleep(5)
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos2 = 1

                    break

        if pos2 == 1:
            pos2 == 0

            y = 0
            x = 0
            Sol_pos = 0
            writeMemory(start_address + 16 * length, length, Sol_pos)
            writeMemory(start_address + 5 * length, length, x)
            writeMemory(start_address + 1 * length, length, y)
            gg = 1
            writeMemory(start_address + 25 * length, length, gg)

            while True:
                x_done = readMemory(start_address + 6 * length, length, )[0]
                if x_done == 0.0:
                    pass
                else:
                    gg = 0
                    writeMemory(start_address + 25 * length, length, gg)
                    pos3 = 1
                    return pos3

                    break

        break
    return "OK"


@app.route('/drawWord', methods=['post'])
def drawWord():
    text = request.form.get('text')
    # Set image size and font properties
    img_width = 190
    img_height = 190
    bg_color = (255, 255, 255)  # white background color
    text_color = (0, 0, 0)  # black text color
    font_size = 50
    font = ImageFont.truetype("arial.ttf", font_size)

    # Create image object
    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    # Calculate text position
    text_width, text_height = draw.textsize(text, font=font)
    x_pos = (img_width - text_width) / 2
    y_pos = (img_height - text_height) / 2

    # Draw text on image
    draw.text((x_pos, y_pos), text, fill=text_color, font=font)

    # Save image to the desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    image_path = os.path.join(desktop_path, "text_image.png")
    img.save(image_path)
    img = cv2.imread(r"text_image.png")

    # Open the image file
    desktop_path = os.path.expanduser("~\Desktop")
    file_path = os.path.join(desktop_path, r'text_image.png')
    image = Image.open(file_path)

    # Resize the image
    new_size = (200, 200)
    resized_image = image.resize(new_size)

    # Set the file path to save the resized image on the desktop
    # resized_file_path = os.path.join("C:\Users\Admin\Desktop\resized.jpg")

    resized_image.save('C:\\Users\\Admin\\Desktop\\resized.jpg')
    inkscape_path = r"C:\Program Files\Inkscape\inkscape.exe"
    image_path = r'C:\Users\Admin\Desktop\resized.jpg'

    # Launch Inkscape and open the image filen b
    subprocess.Popen([inkscape_path, image_path])
    folder_path = r"C:\Users\Admin\Desktop\Gcodes"
    latest_modification_time = 0
    return "Ok"


def encoder():
    X_enc = readMemory(start_address + 32 * length, length, )[0]
    Y_enc = readMemory(start_address + 33 * length, length, )[0]
    pulse_x = (X_enc * 1000 * 200 / 40960) - 30000
    mm_x = pulse_x / 1000
    return pulse_x, mm_x


@app.route('/pulse', methods=['get'])
def getPulse():
    pulse, mm = encoder()
    return {"pulse": str(pulse)}


@app.route('/mm', methods=['get'])
def getMM():
    pulse, mm = encoder()
    return {"mm": str(mm)}


@app.route('/homing', methods=['post'])
def homing():
    home = 1
    writeMemory(start_address + 38 * length, length, home)
    home = 0
    writeMemory(start_address + 38 * length, length, home)
    Sol_pos = 0
    writeMemory(start_address + 16 * length, length, Sol_pos)
    return "OK"


if __name__ == '__main__':
    app.run(debug=True)
