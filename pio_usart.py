from machine import Pin
from time import sleep
import rp2

# clear programs form pio for clean restart
rp2.PIO(0).remove_program()
rp2.PIO(1).remove_program()

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

@rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_RIGHT)
def rx():
    wrap_target()   # start

    wait(1, pins, 0) # start bit
    
    set(x, 8)
    label('recieve')
    wait(1, pins, 2)
    in_(pins, 1)
    jmp(x_dec, 'recieve')
    
    wait(1, pins, 2)
    jmp(pins, 'continue') # end bit
    in_(null, 23)
    push()
    
    jmp('end')
    
    label('continue')
    irq(block, rel(0))
    label('end')
    wrap()

@rp2.asm_pio()
def cl():
    
    wrap_target()   #start
    
    #wait(1, pins, 2)
    #irq(0)
    set(pins, 1)    [31]
    set(pins, 0)    [31]
    
    wrap()

Pin(1, Pin.IN, Pin.PULL_UP)

sm_tx = rp2.StateMachine(0, tx, freq=5000, out_base=Pin(0), sideset_base=Pin(0))
sm_rx = rp2.StateMachine(1, rx, freq=5000, in_base=Pin(1))
sm_cl = rp2.StateMachine(2, cl, freq=5000, set_base=Pin(2))

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
