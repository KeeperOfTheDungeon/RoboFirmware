from machine import Pin
from time import sleep
import rp2

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def tx():
    label("synchronisation")
    
    irq(0)
    wait(0, irq, 0)
    
    wrap_target()   #start
    
    set(pins, 1)    [31]
    nop()           [31]
    nop()           [31]
    nop()           [31]
    set(pins, 0)    [31]
    nop()           [31]
    nop()           [31]
    nop()           [31]
    
    wrap()
    
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def rx():
    label("synchronisation")
    
    #irq(block, 4)
    #wait(0, irq, 4)
    
    wrap_target()
    
    set(pins, 1)    [31]
    nop()           [31]
    nop()           [31]
    nop()           [31]
    set(pins, 0)    [31]
    nop()           [31]
    nop()           [31]
    nop()           [31]
    
    wrap()
   
   
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def cl():
    label("synchronisation")
    
    irq(clear, 0)
    
    wrap_target()   #start
    
    set(pins, 1)    [31]
    nop()           [31]
    nop()           [31]
    set(pins, 0)    [31]
    nop()           [31]
    nop()           [31]
    
    wrap()
   

sm_tx = rp2.StateMachine(0, tx, freq=2000, set_base=Pin(0))
sm_rx = rp2.StateMachine(1, tx, freq=2000, set_base=Pin(1))
sm_cl = rp2.StateMachine(2, tx, freq=2000, set_base=Pin("LED"))

sm_tx.active(1)
sm_rx.active(1)
sm_cl.active(1)
#sleep(3.0)
#sm_tx.active(0)
#sm_rx.active(0)
#sm_cl.active(0)
