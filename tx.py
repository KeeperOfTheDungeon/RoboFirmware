from machine import Pin
from time import sleep
import rp2

# clear programs form pio for clean restart
rp2.PIO(0).remove_program()
rp2.PIO(1).remove_program()

@rp2.asm_pio(out_init=rp2.PIO.OUT_HIGH,
             out_shiftdir=rp2.PIO.SHIFT_RIGHT,
             sideset_init=rp2.PIO.OUT_HIGH)
def tx():
    wrap_target()

    #start bit
    pull()
    wait(0, pins, 2)
    set(x, 8)    .side(0)
    wait(1, pins, 2)

    # message
    label('loop')
    wait(0, pins, 2)
    out(pins, 1)
    wait(1, pins, 2)
    jmp(x_dec, 'loop')

    #end bit
    wait(0, pins, 2)
    mov(x,x)    .side(1)
    wait(1, pins, 2)
    
    
    wait(0, pins, 2)
    mov(x,x)    .side(1)
    wait(1, pins, 2)

    wrap()

sm_tx = rp2.StateMachine(0, tx, freq=1000000, out_base=Pin(0), sideset_base=Pin(0))

sm_tx.active(1)

while True:
    x = input('Enter Number to send:\n')
    sm_tx.put(int(x))


sm_tx.active(0)