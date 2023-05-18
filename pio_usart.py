from machine import Pin
from time import sleep
import rp2

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_init=rp2.PIO.OUT_LOW)
def tx():
    
    pull()

    wrap_target()   #start
    
    wait(1, pins, 0)
    out(pins, 1)
    nop()           [7]
    nop()           [7]
    nop()           [7]
    nop()           [7]
    nop()           [7]
    nop()           [7]
    nop()           [7]
    nop()           [7]
    
    wrap()
    
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def cl():
    
    wrap_target()   #start
    
    set(pins, 1)    [31]
    nop()           [31]
    nop()           [31]
    set(pins, 0)    [31]
    nop()           [31]
    nop()           [31]
    
    wrap()
   

sm_tx = rp2.StateMachine(0, tx, freq=2000, in_base=Pin(0), out_base=Pin('LED'), out_shiftdir=rp2.PIO.SHIFT_RIGHT)
sm_cl = rp2.StateMachine(1, cl, freq=2000, set_base=Pin(0))

sm_tx.active(1)
sm_cl.active(1)
sm_tx.put(5461) #0b1010101010101
sleep(3.0)
sm_tx.active(0)
sm_cl.active(0)
print('Bye')
