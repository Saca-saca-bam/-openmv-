

import sensor, image, time
from pyb import UART
import json
red_threshold = (0, 97, 7, 61, -4, 47)
#red_threshold =(4, 97, 11, 61, 1, 47)
sendvalue=0
sensor.reset()
sensor.set_pixformat(sensor.RGB565) # 灰度更快(160x120 max on OpenMV-M7)
sensor.set_framesize(sensor.QVGA)  #320*240
sensor.skip_frames(time = 200)

clock = time.clock()
uart = UART(3, 9600)
def find_max(blobs):

    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob

def get_cornor():
    global r
    for r in img.find_rects((0,0,250,250),threshold = 25000):
     img.draw_rectangle(r.rect(), color = (255, 0, 0))
     for p in r.corners(): img.draw_circle(p[0], p[1], 1, color = (0, 255, 0))
def send():
    global sendvalue
    p=r.corners()
    output_str = "////////////%d,%d,%d,%d,%d,%d,%d,%d"% (int(p[0][0]),int(p[0][1]),\
                                                         int(p[1][0]),int(p[1][1]),\
                                                         int(p[2][0]),int(p[2][1]),\
                                                         int(p[3][0]),int(p[3][1]))
    uart.write(output_str+'\n')
    sendvalue=0

while(True):
    clock.tick()
    img = sensor.snapshot()
    get_cornor()
    if uart.any():
       sendvalue=int(uart.readline().decode().strip())
    if sendvalue:
        send()
    blobs0 = img.find_blobs([red_threshold])

    if blobs0 :
        max_blob = find_max(blobs0)
        cx = max_blob.cx()-img.width()/2
        cy = max_blob.cy()-img.height()/2
        img.draw_cross(max_blob.cx(), max_blob.cy()) # cx, cy
        print("cx:",cx)
        print("cy:",cy)
        z="/%d,%d" % (max_blob.cx(),max_blob.cy())
        uart.write(z+'\r\n')
