from machine import Pin
from time import sleep
import rp2

COMMAND_TOKEN = b'#'
MESSAGE_START_TOKEN = b'*'
STREAM_START_TOKEN = b'$'

EXCEPTION_START_TOKEN = b'^'
ALLERT_START_TOKEN = b'!'

OK_START_TOKEN = b'O'
FAIL_START_TOKEN = b'N'
END_TOKEN = b';'

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

@rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_RIGHT)
def rx():
    wrap_target()

    # wait for start bit
    label('ready')
    wait(0, pins, 2)
    wait(1, pins, 2)
    jmp(pin, 'ready')
    
    # prüfen ob vorher 1 und jetzt 0

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

def pio_setup() :
    rp2.PIO(0).remove_program()
    rp2.PIO(1).remove_program()

    Pin(1, Pin.IN, Pin.PULL_UP)

    sm_tx = rp2.StateMachine(0, tx, freq=1000000, out_base=Pin(0), sideset_base=Pin(0))
    sm_rx = rp2.StateMachine(1, rx, freq=10000000, in_base=Pin(1), jmp_pin=Pin(1))

    sm_rx.irq(lambda x: {print('error')})

    sm_tx.active(1)
    sm_rx.active(1)

    return (sm_tx, sm_rx)


"""
output:
    1. take cmd input
    2. tokenize
    3. buffer
    4. send to pio
"""
    

def pack(message: str) -> bytes:
    frame = bytearray(COMMAND_TOKEN)
    frame += message.encode('ascii')
    frame += END_TOKEN

    return frame

def transmit(frame: bytes) -> None:
    for token in frame:
        sm_tx.put(token)



"""
    input:
        1. check pio for input
        2. read and buffer
        3. tokenize
        4. build string
        5. cmd output
"""

def unpack(frame: bytearray) -> str:
    return frame.decode('ascii')[1:len(frame) - 1]

def listen() -> bytearray:
    frame = b''

    while sm_rx.rx_fifo() > 0:
        token = sm_rx.get().to_bytes(1, 'big')
        frame += token
    
    return frame
        

# main function
if __name__ == '__main__':
    (sm_tx, sm_rx) = pio_setup()
    message_send = input()
    transmit(pack(message_send))
    
    sleep(3.0)

    message_recieve = unpack(listen())
    print(message_recieve)
    sm_tx.active(0)
    sm_rx.active(0)
    
