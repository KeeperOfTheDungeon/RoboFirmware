from machine import Pin
from time import sleep
from tx import tx
from rx import rx
import rp2

# clear programs form pio for clean restart
rp2.PIO(0).remove_program()
rp2.PIO(1).remove_program()
    
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def cl():
    
    wrap_target()   #start
    
    set(pins, 1)    [31]
    set(pins, 0)    [31]
    
    wrap()

sm_tx = rp2.StateMachine(0, tx, freq=2000, out_base=Pin(0), sideset_base=Pin(0))
sm_rx = rp2.StateMachine(1, rx, freq=2000, in_base=Pin(1))
sm_cl = rp2.StateMachine(2, cl, freq=2000, set_base=Pin('LED'))

sm_rx.irq(lambda x: print('Interrupt cleared'))

print('state machines starting')
sm_tx.active(1)
sm_rx.active(1)
sm_cl.active(1)

sm_tx.put(341) #0b101010101
sleep(3.0)
z = sm_rx.get()

sm_cl.active(0)
sm_rx.active(0)
sm_tx.active(0)

print(z)
