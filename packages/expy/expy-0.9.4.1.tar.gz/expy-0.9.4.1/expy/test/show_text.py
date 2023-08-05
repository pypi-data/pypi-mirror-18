# coding:utf-8
##### package test #####
import sys
sys.path.append('../../')
################

from expy import *  # Import the needed functions
start()  # Initiate the experiment environment

'''General usage'''
# Draw text on the canvas
drawText('Hello world!')
show(3000)  # Display current canvas
''''''

# Draw text on the canvas, with given font(size)
drawText('Hello world!', fontname='normalFont')
show(3000)  # Display current canvas

# Draw text on the canvas, with center's position
drawText('Hello! world!', x=-0.5, y=0.0)
show(3000)  # Display current canvas

# Draw text on the canvas, with left center's position
drawText('Hello! world!', x=-0.5, y=0.0, benchmark='left_center')
show(3000)  # Display current canvas

drawText('Hello\nworld\n!')  # Draw multi-line text on the canvas
show(3000)  # Display current canvas

# Display text on a new slide, it's functionally equals to clear+drawText+show,
textSlide('Hello\nworld\nagain!')
