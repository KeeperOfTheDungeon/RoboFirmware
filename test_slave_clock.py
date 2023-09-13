from machine import Pin
from time import sleep
import rp2

# clear programs form pio for clean restart
rp2.PIO(0).remove_program()
rp2.PIO(1).remove_program()

@rp2.asm_pio()
def listen():
    
    wrap_target()   #start
    
    wait(1, pins, 2)
    irq(0)
    
    wrap()
    
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def tick():
    
    wrap_target()
    
    set(pins, 1)    [31]
    set(pins, 0)    [31]
    
    wrap()

sm_ls = rp2.StateMachine(0, listen, freq=5000)
sm_cl = rp2.StateMachine(1, tick, freq=2000, set_base=Pin(2))

sm_ls.irq(lambda x: print('tick'))

print('state machines starting')
sm_ls.active(1)
#sm_cl.active(1)
sleep(3.0)
#sm_cl.active(0)
sm_ls.active(0)
print('finish')