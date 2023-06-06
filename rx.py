from machine import Pin
from time import sleep
import rp2

# clear programs form pio for clean restart

# state machine programs

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
    irq(block, 0)
    label('end')
    wrap()
