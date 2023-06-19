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
    mov(x,x)    .side(0)
    wait(1, pins, 2)
    
    
    wait(0, pins, 2)
    mov(x,x)    .side(1)
    wait(1, pins, 2)

    wrap()

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
    jmp(pin, 'exception')

    # normal execution
    in_(null, 23)
    push()

    jmp('end')

    # exception thrown to main thread
    label('exception')
    irq(block, rel(0))
    
    label('end')

    wrap()

Pin(1, Pin.IN, Pin.PULL_UP)

sm_tx = rp2.StateMachine(0, tx, freq=100000, out_base=Pin(0), sideset_base=Pin(0))
sm_rx = rp2.StateMachine(1, rx, freq=100000, in_base=Pin(1))

sm_rx.irq(lambda x: {print('error')})

print('starting state machines')

sm_tx.active(1)
sm_rx.active(1)

sm_tx.put(3)
sleep(5.0)
x=sm_rx.get()
print(x)

sm_tx.active(0)
sm_rx.active(0)

print('finish')
