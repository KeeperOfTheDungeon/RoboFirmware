from machine import Pin
from time import sleep
import rp2

# clear programs form pio for clean restart
rp2.PIO(0).remove_program()
rp2.PIO(1).remove_program()

@rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_RIGHT)
def rx():
    wrap_target()

    # wait for start bit
    label('ready')
    wait(0, pins, 2)
    wait(1, pins, 2)
    jmp(pin, 'ready')
    
    # accept message
    set(x, 8)
    wait(0, pins, 2)
    
    label('loop')
    
    wait(1, pins, 2)
    in_(pins, 1)
    wait(0, pins, 2)
    
    jmp(x_dec, 'loop')

    # wait for end bit
    wait(1, pins, 2)
    jmp(pin, 'end_bit')

    # exception thrown to main thread
    irq(block, rel(0))
    
    jmp('end')

    # normal execution
    label('end_bit')
    in_(null, 23)
    push()
    
    label('end')

    wrap()

Pin(1, Pin.IN, Pin.PULL_UP)
sm_rx = rp2.StateMachine(1, rx, freq=10000000, in_base=Pin(1), jmp_pin=Pin(1))

sm_rx.irq(lambda x: {print('error')})

sm_rx.active(1)

while True:
    x = sm_rx.get()
    print(x)
