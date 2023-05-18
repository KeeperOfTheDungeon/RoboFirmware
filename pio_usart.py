from machine import Pin
from time import sleep
import rp2

@rp2.asm_pio(out_init=rp2.PIO.OUT_LOW)
def tx():
    
    pull()

    wrap_target()   # start
    wait(1, pins, 25)
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
    
@rp2.asm_pio()
def rx():
    wrap_target()   # start
    
    
    set(x, 8)
    label('single_frame')
    
    wait(1, pins, 25)
    in_(pins, 1)
    
    jmp(x_dec, 'single_frame')
    
    push
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
   

sm_tx = rp2.StateMachine(0, tx, freq=2000, out_base=Pin(0), out_shiftdir=rp2.PIO.SHIFT_RIGHT)
sm_rx = rp2.StateMachine(1, tx, freq=2000, in_base=Pin(1), in_shiftdir=rp2.PIO.SHIFT_RIGHT)
sm_cl = rp2.StateMachine(2, cl, freq=2000, set_base=Pin('LED'))

sm_tx.active(1)
sm_rx.active(1)
sm_cl.active(1)

sm_tx.put(5461) #0b1010101010101
sleep(3.0)
z = sm_rx.get()

sm_cl.active(0)
sm_rx.active(0)
sm_tx.active(0)

print(z)
