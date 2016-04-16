#pingo test

import pingo

board = pingo.detect.MyBoard()

yIn = board.pins[2]
yIn.mode = pingo.IN

yOut = board.pins[3]
yOut.mode = pingo.OUT

gIn = board.pins[4]
gIn.mode = pingo.IN

gOut = board.pins[5]
gOut.mode = pingo.OUT

wIn = board.pins[6]
wIn.mode = pingo.IN

wOut = board.pins[7]
wOut.mode = pingo.OUT

def read_stat():
    if yIn.state == 'HIGH':
        yOut.lo()
    else:
        yOut.high()

    if gIn.state == 'HIGH':
        gOut.lo()
    else:
        gOut.high()

    if wIn.state == 'HIGH':
        wOut.lo()
    else:
        wOut.high()
        
