from machine import Pin
from time import sleep
import rp2

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def tx():
    label("synchronisation")
    
    #irq(0)
    #wait(0, irq, 0)
    
    wrap_target()   #start
    
    # pull from queue
    pull()
    
    set(pins, 1)    [30]# start bit
    nop()    [31]
    nop()    [31]
    
    set(x, 8)
    label("send_frame")
    
    #TODO: add clock interrupt
    out(pins, 1)    [30]
    nop()    [31]
    nop()    [31]
    
    jmp(x_dec, "send_frame")
 
    set(pins, 1)    [31] # end bit
    nop()    [31]
    nop()    [31]
    set(pins, 0)    [31]
    
    # shift out one bit at a time for 9 bits
    
    wrap()
    
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def rx():
    label("synchronisation")
    
    #irq(block, 4)
    #wait(0, irq, 4)
    
    wrap_target()
    
    wait(1, pin, 0)    [30]# start bit
    
    set(x, 8)
    label("recieve_frame")
    
    #TODO: add clock interrupt
    in_(pins, 1)    [30]
    
    jmp(x_dec, "recieve_frame")
    
    wait(1, pin, 0)     [30]
    
    push()
    
    wrap()
   
   
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def cl():
    label("synchronisation")
    
    #irq(clear, 0)
    
    wrap_target()   #start
    
    set(pins, 1)    [31]
    nop()           [31]
    nop()           [31]
    set(pins, 0)    [31]
    nop()           [31]
    nop()           [31]
    
    wrap()
   

sm_tx = rp2.StateMachine(0, tx, freq=2000, set_base=Pin(0))
#sm_rx = rp2.StateMachine(1, tx, freq=2000, set_base=Pin(1))
#sm_cl = rp2.StateMachine(2, tx, freq=2000, set_base=Pin("LED"))

sm_tx.active(1)

sm_tx.put(341) # 0b101010101
#sm_rx.active(1)
#sm_cl.active(1)
sleep(3.0)
sm_tx.active(0)
#sm_rx.active(0)
#sm_cl.active(0)
