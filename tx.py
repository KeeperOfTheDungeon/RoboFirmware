from machine import Pin
from time import sleep
import rp2

# clear programs form pio for clean restart


# state machine programs

@rp2.asm_pio(out_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT, sideset_init=rp2.PIO.OUT_LOW)
def tx():
    
    wrap_target()   # start
    pull()
    # send message
    set(x, 8)         .side(1)
    label('single_frame')
    
    wait(1, pins, 25)
    out(pins, 1)
    
    jmp(x_dec, 'single_frame')
    
    wait(1, pins, 25)    .side(1)   
    wait(1, pins, 25)    .side(0)
    
    wrap()