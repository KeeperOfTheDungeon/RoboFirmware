from machine import Pin
from time import sleep
import rp2
from _thread import allocate_lock
from micropython import const

# clear programs form pio for clean restart
rp2.PIO(0).remove_program()
rp2.PIO(1).remove_program()

CLOCK_PIN = const(2)

myLock = allocate_lock()

@rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_RIGHT)
def rx():
    wrap_target()

    # wait for start bit
    label('ready')
    wait(0, pins, CLOCK_PIN)# warte auf 0 bei clock
    wait(1, pins, CLOCK_PIN)# warte auf 1 bei clock
    jmp(pin, 'ready') # wenn pin High dann kein Startbit

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
    
    jmp('end')    # ende

    # normal execution
    label('end_bit')
    in_(null, 23)
    
    label('end')
    push()    # push data to RX FIFO
    irq(rel(0))

    wrap()


Pin(1, Pin.IN, Pin.PULL_UP)
sm_rx = rp2.StateMachine(1, rx, freq=10000000, in_base=Pin(1), jmp_pin=Pin(1))

def callback(x):
    myLock.acquire()
    while sm_rx.rx_fifo() > 0:
        x = sm_rx.get()
        print(x)
    #sleep(.25)
    myLock.release()

sm_rx.irq(callback)

sm_rx.active(1)

while True:
    print('alive')
    sleep(10)

