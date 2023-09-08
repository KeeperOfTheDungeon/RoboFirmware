from machine import Pin
from time import sleep
import rp2
from micropython import const

CLOCK_PIN = const(2)

# clear programs form pio for clean restart
rp2.PIO(0).remove_program()
rp2.PIO(1).remove_program()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW,
             in_shiftdir=rp2.PIO.SHIFT_RIGHT,
             fifo_join=rp2.PIO.JOIN_RX)
def rx():
    wrap_target()

    # wait for start bit
    label('ready')
    wait(0, pins, CLOCK_PIN)# warte auf 0 bei clock
    wait(1, pins, CLOCK_PIN)# warte auf 1 bei clock
    jmp(pin, 'ready') # wenn pin High dann kein Startbit
    
    set(pins, 1)
    
    # accept message
    set(x, 8)# setze counter auf 8 bits
    wait(0, pins, CLOCK_PIN)# warte auf 0 bei clock 
        
    label('loop')
        
    wait(1, pins, CLOCK_PIN)# warte auf 1 bei clock
    in_(pins, 1)# holle aktuelles bit
    wait(0, pins, CLOCK_PIN)# Warte auf 0 beiu clock
        
    jmp(x_dec, 'loop')# nächsten bit hollen (solange n > 0)

    # wait for end bit
    wait(1, pins,  CLOCK_PIN)# warte auf 1 bei Clock
    jmp(pin, 'end_bit')# springe zu ende 

    # exception as 10. LSB in word to main thread
    set(y, 1)
    in_(y, 23)
        
    jmp('end')# ende

    # normal execution
    label('end_bit')
    in_(null, 23)
        
    label('end')
    push(noblock)# push data to RX FIFO
    set(pins, 0)
    irq(rel(0))

    wrap()

Pin(1, Pin.IN, Pin.PULL_UP)

sm_rx = rp2.StateMachine(1, rx, freq=10000000, in_base=Pin(1), set_base=Pin(25), jmp_pin=Pin(1))
toke_buffer = array('h', [0 for i in range(TOKEN_BUFFER_SIZE)])
token_buffer_index = 0
token_buffer_read_index = 0
token = 0x000
isRead = False

def interrupt_callback(x):
    token = state_machine_rx.get()
    token_buffer[token_buffer_index] = token
    token_buffer_index = (token_buffer_index + 1) % TOKEN_BUFFER_SIZE
    isRead = True

sm_rx.irq(interrupt_callback)

print('starting state machines')

sm_rx.active(1)

while True:
    if isRead:
        
        isRead = False

sm_rx.active(0)

print('finish')

