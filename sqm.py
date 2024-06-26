import numpy as np
from PIL import Image, ImageStat, ImageDraw, ImageFont
import os
from time import sleep
import math
from datetime import datetime
from utils import create_image_directories

width = 1024
height = 786
temp_img_path = "/home/sc36/sqm/temp_sqm_img.jpg"
log_file = "~/sqm/debug_sqm.csv"

command = "libcamera-still -n -o " + temp_img_path + " --gain 18 --ev 0 --awbgains 1.5,2 --immediate "
#command = "libcamera-still -n -o" + temp_img_path + " --gain 18 --ev 0 --awbgains 1.5,2 --roi 0.25,0.25,0.5,0.5 --width " + str(width) +" --height " + str(height) + " --immediate "

MOD0_SQRT = [101.11,97.07,95.07,91.36,89.56,85.86,83.85,80.41,78.69,75.12,73.43,70.9,68.19,67.93,67,65.12,64.11,61.93,60.94,53.77,53.47,54.15,54.38,52.69,54.84,52.3,55.21,59.04,56.42,51.59,58.2,56.84,51.38,50.53,50.02,48.94,48.41,47.37,46.93,45.36,44.58,43.77,43.08,41.71,40.87,39.21,38.34,36.57,35.66,33.8,32.86,31.22,30.38,28.59,27.73,25.86,25.22,23.72,23.03,21.57,20.79,19.16,18.32]
MOD0_SQM  = [0,0,0,0,0,0,0,0,5.98,6.08,6.13,6.22,6.24,6.29,6.31,6.39,6.42,6.49,6.52,6.52,6.52,6.53,6.54,6.54,6.55,6.55,6.56,6.57,6.58,6.58,6.59,6.59,6.6,6.63,6.64,6.66,6.68,6.7,6.72,6.77,6.79,6.81,6.81,6.83,6.85,6.9,6.94,7.02,7.06,7.14,7.18,7.26,7.29,7.36,7.39,7.46,7.5,7.57,7.61,7.69,7.73,7.83,7.87]
mymodel0 = np.poly1d(np.polyfit(MOD0_SQRT, MOD0_SQM, 5))

MOD005_SQRT = [20.25 , 25.15 , 27.63 , 30.92 , 37.76 , 41.31 , 45.79 , 54.86 , 59.27 , 65.06 , 76.08 , 81.38 , 88.37 , 101.62 , 107.97 , 116.01 , 130.41 , 137.08 , 145.34 , 159.53 , 165.55 , 173.04, 201.57,198.07,194.31,190.05,186.87,184.63,182.38,179.71,177.67,175.85,174.34,173.71,172.9,170.56,166.68,162.94,159.23,155.45,152,149.09,146.37,142.83,133.82,122.81,127.7,124.18,123.88,116.36,111.25,112.95,100.42,104.41,98.14,90.52,85.33,80.84,69.75,63.97,59.5,51.92,49.4,47.11,41.45,39.05,36.72,30.58,28.34,26.03,21.83,19.68,18.23]
MOD005_SQM = [12.19, 11.9, 11.77, 11.61, 11.33, 11.2, 11.05, 10.77, 10.65, 10.5, 10.24, 10.12, 9.98, 9.73, 9.63, 9.49, 9.26, 9.16, 9.04, 8.83, 8.74, 8.63, 7.83,7.87,7.94,7.99,8.06,8.08,8.12,8.15,8.16,8.18,8.19,8.2,8.21,8.24,8.3,8.42,8.45,8.52,8.59,8.63,8.64,8.72,8.97,9,9,9.04,9.08,9.15,9.2,9.21,9.29,9.32,9.35,9.46,9.54,9.67,10,10.2,10.32,10.54,10.6,10.63,10.72,10.85,10.92,11.15,11.28,11.35,11.57,11.68,11.79]
mymodel005 = np.poly1d(np.polyfit(MOD005_SQRT, MOD005_SQM,3))

MOD01_SQRT = [ 54.42,21.31,23.17,80.43,21.49,37.36,19.73,24.27,55.33,100.9,64.31,59.39,39.8,90.39,78.18,46.41,98.49,58.33,28.95,132.08,49.47,110.25,85.21,69.59,27.02,119.55,32.44,19.3,21.22,44.61,39.91,29.52,48.67,26.42,82.06,64.7,58.69,69.77,89.45,95.71, 20.15 , 22.3 , 25.04 , 31.05 , 34.22 , 38.26 , 46.56 , 50.65 , 56.02 , 66.75 , 71.86 , 78.37 , 91.36 , 97.68 , 106.16 , 123.25 , 131.56]
MOD01_SQM  = [13.42,14.84,14.77,12.78,14.88,14.13,15.05,14.78,13.52,12.41,13.31,13.49,14.16,12.71,13.01,13.99,12.59,13.63,14.74,12.07,13.96,12.45,13,13.41,14.93,12.34,14.69,15.39,15.28,14.22,14.39,14.84,14.09,15.01,13.16,13.61,13.78,13.47,13.01,12.88 , 15.52, 15.4, 15.23, 14.93, 14.77, 14.63, 14.32, 14.18, 14.0, 13.69, 13.55, 13.38, 13.08, 12.95, 12.77, 12.47, 12.35]
mymodel01 = np.poly1d(np.polyfit(MOD01_SQRT, MOD01_SQM, 5))

MOD5_SQRT=[14.89,13.97,12.86,15.78,10.96,17.35,11.7,18.34,18.14,12.65,8.18,48.1,61.18,50.51,52.76,85.78,87.94,54.11,58.43,84.13,53.72,82.37,56.31,58.99,56.89,75.1,59.56,79.73,62.31,71.36,72.41,65.75,69.41,5.07,5.14,4.99,4.92,4.93,64.63,46.48,45.08,45.58,4.97,6.53,4.86,4.86,5,67.44,47.36,4.92,4.99,5.07,6.06,5.1,76.29,49.32,90.42,72.1, 223.7,221.87,221.7,219.73,215.43,209.43,186.77,171.57,158.09,132.75,123.28,116.91,103.85,97.49,91.97,87.91,81.09,76.41,72.79,63.72,66.48,58.63,54.8,48.12,47.2,104.26,87.91,84.47,85.38,67.38,66.48,70.01,55.76,53.94,48.12,45.45,39.87,36.9,34.46,31.36,26.62,26.11,24.52,22.31,19.38,20.11,18.08,22.93,15.46,14.62,14.75,17.76,12.74,12.17,11.98,10.61,13.78,17.84,10.46,9.37,9.5,9.36,15.71,9,10.76,8.64,8.21,8.71,8.73,8.28,8.26,8.13,8.48,13.11,8.13,8.63,8.59,8.21,7.87,8.19,13.56,8.04,13.17,7.87,7.87,8.14,7.7,12.83,7.8,7.71,8.22,12.51,7.18,7.14,12.24,7.01,11.86,6.55,6.21,11.75,6.83,6.9,7.36,6.68,7.27,7.06,6.72,11.39,7.44,6.86,11.54,6.55,6.86,6.43,7.11,11.17,11.17,11.16,7.12,6.69,6.88,6.75,10.75,6.94,10.7,5.89,6.47,6.11,6.54,10.46,10.56,6.55,6.79,6.24,6.71,6.4,7.1,10.05,10.24,7.31,5.85,6.23,10.06,6.63,6.1,6.42,6.68,6.31,6.54,6.2,6.31,6.68,6.37,9.75,6.25,9.63,6.53,6.49,6.18,6.41,6.14,6.49,6.9,6.67,6.59,5.8,9.47,6.37,6.9,6.18,6.15,9.23,6.48,6.64,6.25,6.38,6.27,5.48,6.37,9.07,5.98,5.87,5.77,8.86,6.47,6.61,5.89,6.32,6.27,6.2,5.77,8.47,6.12,6.09,6.15,5.45,6.37,6.29,6.01,6.02,8.01,5.92,6.26,6.29,5.81,5.52,6.12,6.06,6.16,6.28,6.42,6.06,5.71,5.92,5.8,6,5.31,7.82,6.12,6.71,5.95,5.46,5.48,6.41,5.9,5.44,5.79,5.75,7.64,5.56,5.39,5.44,6.13,6.34,5.91,5.85,7.43,5.94,5.72,5.75,5.39,5.23,5.28,5.76,5.62,5.51,5.67,5.28,5.43,5.24,5.26,6.95,5.34,5.58,5.6,6.11,5.28,5.35,5.53,5.82,5.46,5.18,6.72,5.71,5.51,5.35,5.44,5.16,5.63,6.73,5.55,5.39,5.56,5.57,4.78,6.52,5.37,5.15,4.81,6.23,4.73,6.17,4.81,5.62,4.56,5.78,5.65,4.32,4.74,4.82,4.42,5.41,4.22,4.58,4.35,4.64,5.14,4.18,4.58,5.24,4.32,4.37,4.5,4.49,4.36,4.1,4.19,4.42,4.39,4.35,4.32,5.33,4.27,4.32,4.69,4.04,4.22,3.95,4.32,4.33,4.28,4.34,4.36,3.95,4.3,4,4.34,4.36,4.33,4.25,4.24,4.28,3.85,4.28,4.3,4.29,4.23,3.84,3.85,4.27,4.2,4.17,4.16,4.2, 7.22,6.98,6.97,6.85,6.79,6.92,6.25,6.91,7.22,7.08,6.32,6.33,6.93,5.54,92.1,24.04,7.14,6.81,6.83,6.84,6.03,6.74,6.42,6.8,7.91,7.41,7.35,6.88,180.66,7.05,6.99,6.77,7.2,7.14,6.73,46,6.88,6.39,10.48,15.98,8.05,6.71,5.72,6.8,6.54,11.28,13,16.93,22.43,7.2,7.19,6.84,6.66,6.85,6.14,7.48,8.04,7.89,7.8,7.76,7.55,12.43,17.13,129.77,8.29,7.4,7.19,6.6,6.96,43.2,6.71,6.76,7.59,6.02,6.89,6.88,7.08,7.99,15.24,9.31,184.85,6.59,6.63,7.29,7.72,8.81,8.49,8.18,8.41,7.28,6.7,13.76,14.08,21.79,7.7,6.93,6.89,6.92,6.44,6.43,6.01,28.87,6.65,7.06,8.44,8.04,7.97,8.85,8.76,8.23,8.01,7.79,7.36,9.76,8.3,188.37,7.24,8.5,8.51,8.33,8.36,8.37,6.95,7.51,7.49,7.43,7.47,8.1,8.12,8.22,8.4,8.14,7.89,8.3,8.69,8.43,8.36,8.21,8.15,127.66,10.14,8.87,6.81,7.29,7.36,7.15,8.94,8.08,8.67,8.69,8.66,8.46,97.55,104.61,28.16,7.62,8.37,8.5,8.09,8.36,8.35,8.34,8.89,8.54,8.13,18.55,11.22,38.45,7.6,6.69,6.24,7.54,8.63,8.77,8.5,8.44,8.47,8.4,8.28,8.74,8.02,8.18,141.1,19.59,10.92,7.53,7.31,7.55,8.2,8.92,8.44,8.71,8.5,8.41,17.34,13.91,12.48,5.93,36.98,177.91,27.45,7.65,7.26,8.32,7.91,8.81,8.82,8.87,8.68,8.31,8.13,8.33,7.97,8.5,7.93,16.86,14.81,11.89,6.8,7.33,7.44,8.73,8.81,8.29,8.29,8.23,7.94,8.08,8.9,8.48,8,15.35,5.94,6.92,8.27,144.59,13.33,183.48,7.18,7.97,8.37,8.69,8.46,8.48,8.48,8.85,8.18,7.98,107.58,26.03,8.18,8.74,167.87,173.18,8.1,8.19,133.75,6.04,6.11,156.38,161.44,7.67,8.59,24.55,8.78,6.33,137.31,153.94,163.18,9.23,33.66,184.43,23.23,22.19,21.17,6.23,6.45,6.49,8.18,173.24,6.96,9.93,7.09,118.15,179.68,19.19,159.42,7.37,31.24,18.34,18.14,12.65,8.18,7.31,17.35,11.7,26.94,15.78,10.96,7.92,26.06,12.86,14.89,13.97,8.21,124.65,9.88,166.61,8.63,8.84,22.53,23.97,132.83,10.15,136.43,11.01,20.06,11.35,19.5,154.87,18.09,13.6,15.35,17.06,14.83,12.46]
MOD5_SQM=[19.61,19.69,19.8,19.55,19.98,19.43,19.92,19.36,19.38,19.86,20.28,18.42,17.89,18.33,18.24,17.29,17.26,18.2,18.04,17.35,18.24,17.4,18.15,18.05,18.13,17.58,18.04,17.48,17.96,17.7,17.68,17.86,17.76,21.49,21.48,21.49,21.5,21.5,17.72,18.44,18.52,18.5,21.52,21.36,21.53,21.53,21.51,17.66,18.43,21.53,21.52,21.52,21.43,21.52,17.44,18.35,17.19,17.56, 14.13,14.31,14.44,14.71,14.9,15.08,15.36,15.55,15.68,16,16.13,16.28,16.5,16.62,16.74,16.97,16.97,17.08,17.19,17.44,17.46,17.61,17.76,17.98,18,16.52,16.97,17.01,17.14,17.43,17.46,17.51,17.75,17.77,17.98,18.09,18.37,18.42,18.47,18.78,18.85,18.91,19.02,19.13,19.24,19.3,19.3,19.4,19.56,19.57,19.58,19.71,19.77,19.85,19.87,19.96,19.99,19.99,20.02,20.06,20.1,20.13,20.17,20.23,20.26,20.26,20.27,20.27,20.28,20.29,20.29,20.31,20.32,20.36,20.36,20.38,20.38,20.38,20.39,20.39,20.4,20.42,20.45,20.45,20.45,20.45,20.47,20.48,20.48,20.49,20.5,20.51,20.52,20.52,20.54,20.54,20.56,20.56,20.56,20.57,20.57,20.57,20.57,20.58,20.58,20.58,20.58,20.59,20.6,20.6,20.61,20.62,20.62,20.62,20.62,20.63,20.64,20.65,20.65,20.65,20.66,20.66,20.67,20.67,20.68,20.68,20.69,20.69,20.69,20.7,20.7,20.7,20.7,20.7,20.71,20.71,20.72,20.72,20.72,20.72,20.72,20.74,20.74,20.74,20.74,20.74,20.74,20.74,20.75,20.75,20.75,20.75,20.75,20.76,20.76,20.77,20.77,20.77,20.78,20.78,20.78,20.78,20.78,20.78,20.78,20.78,20.79,20.79,20.79,20.79,20.79,20.8,20.8,20.8,20.8,20.8,20.81,20.81,20.81,20.82,20.82,20.82,20.82,20.83,20.83,20.83,20.83,20.84,20.84,20.85,20.86,20.86,20.86,20.86,20.86,20.86,20.86,20.86,20.86,20.86,20.87,20.87,20.87,20.87,20.88,20.88,20.88,20.88,20.88,20.88,20.88,20.88,20.88,20.88,20.88,20.89,20.89,20.89,20.89,20.89,20.89,20.9,20.9,20.9,20.9,20.9,20.91,20.92,20.92,20.93,20.93,20.93,20.93,20.93,20.93,20.93,20.94,20.94,20.94,20.94,20.96,20.96,20.96,20.96,20.96,20.96,20.97,20.97,20.97,20.97,20.97,20.97,20.97,20.97,20.97,20.97,20.97,20.98,20.98,20.98,20.99,20.99,20.99,20.99,20.99,21,21,21.01,21.02,21.02,21.02,21.02,21.03,21.03,21.04,21.04,21.04,21.05,21.07,21.08,21.09,21.1,21.12,21.12,21.14,21.14,21.18,21.19,21.2,21.2,21.2,21.22,21.23,21.24,21.25,21.26,21.26,21.27,21.29,21.29,21.3,21.31,21.32,21.33,21.34,21.34,21.35,21.36,21.36,21.38,21.39,21.4,21.4,21.4,21.4,21.41,21.42,21.46,21.47,21.48,21.48,21.49,21.49,21.5,21.51,21.51,21.51,21.52,21.52,21.53,21.53,21.53,21.54,21.54,21.54,21.54,21.55,21.55,21.55,21.55,21.56,21.58,21.58,21.58, 20.65,20.68,20.68,20.69,20.69,20.68,20.73,20.67,20.64,20.66,20.73,20.73,20.67,20.8,16.73,19.31,20.65,20.68,20.68,20.68,20.75,20.67,20.7,20.66,20.55,20.6,20.61,20.65,15.69,20.65,20.66,20.68,20.64,20.64,20.68,18.04,20.64,20.69,20.3,19.8,20.55,20.67,20.76,20.65,20.68,20.22,20.06,19.72,19.4,20.63,20.63,20.66,20.68,20.64,20.71,20.57,20.52,20.53,20.54,20.55,20.57,20.11,19.69,16.32,20.52,20.6,20.62,20.67,20.64,18.16,20.65,20.65,20.58,20.72,20.62,20.62,20.6,20.51,19.85,20.42,15.53,20.65,20.65,20.58,20.54,20.43,20.47,20.5,20.47,20.58,20.64,19.98,19.95,19.43,20.56,20.63,20.63,20.63,20.68,20.68,20.72,18.78,20.64,20.6,20.46,20.5,20.51,20.42,20.43,20.48,20.5,20.52,20.57,20.37,20.5,15.44,20.58,20.45,20.45,20.47,20.47,20.47,20.6,20.54,20.54,20.55,20.55,20.48,20.48,20.47,20.45,20.48,20.5,20.46,20.43,20.45,20.46,20.47,20.48,16.12,20.33,20.44,20.6,20.55,20.55,20.57,20.39,20.48,20.42,20.42,20.42,20.44,16.59,16.5,18.81,20.52,20.45,20.43,20.47,20.45,20.45,20.45,20.4,20.43,20.47,19.63,20.22,18.36,20.51,20.6,20.65,20.52,20.41,20.4,20.42,20.43,20.43,20.43,20.45,20.4,20.47,20.46,16.18,19.55,20.24,20.51,20.53,20.51,20.44,20.37,20.42,20.39,20.42,20.42,19.71,19.98,20.1,20.67,18.42,15.63,18.84,20.5,20.54,20.43,20.47,20.38,20.38,20.38,20.4,20.43,20.45,20.43,20.47,20.41,20.47,19.74,19.91,20.15,20.57,20.52,20.51,20.38,20.38,20.43,20.42,20.43,20.46,20.45,20.37,20.41,20.45,19.85,20.66,20.55,20.42,16.12,20.01,15.49,20.52,20.45,20.41,20.38,20.4,20.4,20.4,20.36,20.43,20.45,16.43,18.91,20.42,20.36,15.82,15.67,20.41,20.4,16.02,20.62,20.62,15.87,15.81,20.45,20.36,18.98,20.32,20.57,15.97,15.97,15.86,20.26,18.53,15.43,19.06,19.13,19.21,20.55,20.52,20.52,20.34,15.6,20.47,20.16,20.44,16.22,15.5,19.32,15.74,20.4,18.6,19.36,19.38,19.86,20.28,20.37,19.43,19.92,18.83,19.55,19.98,20.29,18.88,19.8,19.61,19.69,20.25,16.08,20.09,15.63,20.19,20.17,19.05,18.95,15.96,20.01,15.92,19.93,19.21,19.89,19.24,15.72,19.33,19.68,19.53,19.4,19.57,19.75]
mymodel5 = np.poly1d(np.polyfit(MOD5_SQRT, MOD5_SQM,6))


def get_sqm_image(obstacles, grid_x_count, grid_y_count):
    model = select_model()
    generate_sqm_image(model, obstacles, grid_x_count, grid_y_count)

def generate_sqm_image(model, obstacles, grid_x_count, grid_y_count):
    image = Image.open(temp_img_path)
    mask = np.zeros((image.size[1], image.size[0], 3), dtype=np.uint8)

    #obstacles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 34, 35, 36, 37, 38, 39, 56, 57, 58, 59, 76, 77, 78, 79, 96, 97, 98, 99, 116, 136, 156, 176, 177, 157, 137, 117, 118, 138, 158, 178, 119, 139, 159, 179, 195, 196, 197, 198, 199, 194, 214, 215, 216, 217, 218, 219, 234, 235, 236, 237, 239, 238, 213, 233, 232, 212, 211, 231, 230, 229, 209, 208, 228, 227, 207, 187, 188, 168, 167, 166, 186, 206, 226, 185, 205, 225, 224, 223, 222, 221, 220, 200, 201, 202, 203, 204, 184, 165, 164, 163, 183, 182, 162, 161, 181, 180, 160, 144, 143, 142, 141, 140, 120, 121, 122, 123, 124, 104, 103, 102, 101, 100, 80, 81, 83, 84, 82, 64, 44, 45, 46, 26, 25, 24, 23, 43, 63, 62, 42, 22, 21, 41, 61, 60, 40, 20]

    draw = ImageDraw.Draw(image)
    sqm_values = np.zeros([grid_y_count, grid_x_count])
    min, max = 100, 0 # Set min to 100 since max value passible is 22
    x_gap = image.size[0]//grid_x_count
    y_gap = image.size[1]//grid_y_count

    if image is not None:
        for x in range(grid_x_count):
            for y in range(grid_y_count):
                if y*grid_x_count+x not in obstacles:
                    box = (x*x_gap, y*y_gap, (x+1)*x_gap-1, (y+1)*y_gap-1)
                    sqrt_rms = calculateRMS(image, box)
                    sqm_values[y, x] = round(getPSQM(sqrt_rms, model), 2)

                    if sqm_values[y, x] > max:
                        max = sqm_values[y, x]
                    if sqm_values[y, x] < min:
                        min = sqm_values[y, x]

                draw.text((x*x_gap, y_gap*(1/3 + y)), str(sqm_values[y, x]), font=ImageFont.truetype("static/Roboto-Bold.ttf", 50), fill=(255, 255, 255))

        interval = max - min
        for x in range(grid_x_count):
            for y in range(grid_y_count):
                if y*grid_x_count+x not in obstacles:
                    val = int(255*(1-(sqm_values[y, x]-min)/interval))
                    mask[y*y_gap:(y+1)*y_gap-1, x*x_gap:(x+1)*x_gap-1] = [0, 0.5*val, val]

        mask_image = Image.fromarray(mask)
        blended_image = Image.blend(image, mask_image, alpha=0.4)
        save_image(blended_image)
      
    else:
        print("Image was not found")


def select_model():
    box = (width//4, height//4, 3*width//4, 3*height//4)
    secs = 0.0001
    p = take_picture(secs)
    print(p)
    rms = calculateRMS(Image.open(p), box)
    print("RMS0 = " + str(round(rms,2)))
    if rms < 14:
        os.remove(p)
        secs = 0.005
        p = take_picture(secs)
        rms = calculateRMS(Image.open(p), box)
        print("RMS005 = " + str(round(rms,2)))
        if rms <  18:
            os.remove(p)
            secs = 0.1
            p = take_picture(secs)
            rms = calculateRMS(Image.open(p), box)
            print("RMS01 = " + str(round(rms,2)))
            if rms < 18:
                os.remove(p)
                secs = 5
                model = "mod5"
                p = take_picture(secs)
                rms = calculateRMS(Image.open(p), box)
                print("RMS5 = " + str(round(rms,2)))
                model = "mod5"
            elif rms >=18 and rms <= 230:
                model = "mod01"
        else:
            model  = "mod005"
    elif rms >= 18 and rms <=87:
        model = "mod0"
    else:
        model = "--"

    return model

def take_picture(secs):
    ex = str(secs * 1000000)
    custom_command = command + " --shutter " + ex
    print(command)
    os.system(custom_command)

    print(f"Taking {temp_img_path}")
    exists = False
    while exists:
        sleep(0.5)
        if os.path.exists(temp_img_path):
            print("True")
            exists = True
    
    return temp_img_path

def getPSQM(rms, model):
    if model =="mod0":
       psqm  = mymodel0(rms)
    elif model =="mod005":
       psqm  = mymodel005(rms)
    elif model =="mod01":
       psqm  = mymodel01(rms)
    elif model =="mod5":
       psqm  = mymodel5(rms)
    else:
       psqm = 0
    return psqm

def calculateRMS(image, box):
    print("Calculating SQRT RMS...")
    r,g,b = ImageStat.Stat(image.crop(box)).rms
    sqrt_rms = math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))
    return sqrt_rms

def logInfo(secs, rms, model, psqm):
    print("logging debug info...")

    date_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    with open(log_file, 'a') as f:
        a  = str(date_time) + " ;"
        a += " Secs; "+ str(secs) + " ;"
        a += " Model: " + model + " ; "
        a += " RMS ; "+ str(round(rms,2)) + " ;"
        a +="  PSQM; "+ str(round(psqm,2)) + "\n"
        print(a)
        f.write(a)
        f.close()
    return

def save_image(image):
    dir = create_image_directories()
    image_name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
    image.save(os.path.join(os.getcwd(), "static/images/current_sqm_image.jpg"))
    image.save(os.path.join(dir, image_name))