from machine import Pin
from time import sleep
import rp2

# clear programs form pio for clean restart


# state machine programs

@rp2.asm_pio(out_init=rp2.PIO.OUT_HIGH, out_shiftdir=rp2.PIO.SHIFT_RIGHT, sideset_init=rp2.PIO.OUT_HIGH)
def tx():
    
    wrap_target()   # start
    pull()
    # send message
    set(x, 8)         .side(0)
    label('single_frame')
    
    wait(1, pins, 2)
    out(pins, 1)
    
    jmp(x_dec, 'single_frame')
    
    wait(1, pins, 2)    .side(0)   
    wait(1, pins, 2)    .side(1)
    
    wrap()
