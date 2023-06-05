from machine import Pin
from time import sleep
import rp2

# clear programs form pio for clean restart

# state machine programs

@rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_RIGHT)
def rx():
    wrap_target()   # start

    wait(1, pins, 0)
    
    set(x, 8)
    label('recieve')
    wait(1, pins, 25)
    in_(pins, 1)
    jmp(x_dec, 'recieve')
    
    wait(1, pins, 25)
    jmp(pins, 'continue')
    
    irq(block, 0)
    jmp('end')
    
    label('continue')
    push()
    label('end')
    wrap()