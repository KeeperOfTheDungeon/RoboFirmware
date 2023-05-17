import rp2
from machine import Pin
from time import sleep

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def interr_send():
    wrap_target()
    irq(block, 0)
    #irq(0)
    set(pins, 0)
    
    wrap()
    
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def interr_rec():
    wrap_target()
    #wait(1, irq, 0)
    set(pins, 0)
    wrap()

sm_send = rp2.StateMachine(0, interr_send, freq=2000, set_base=Pin(0))

sm_rec = rp2.StateMachine(1, interr_rec, freq=2000, set_base=Pin('LED'))

sm_send.irq(lambda x: print('Interrupt cleared'))

sm_send.active(1)
sm_rec.active(1)
sleep(1.0)
sm_send.active(0)
sm_rec.active(0)