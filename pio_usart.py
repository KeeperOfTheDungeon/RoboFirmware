from machine import Pin
from time import sleep
import rp2

def tx_factory(clock_pin):
    @rp2.asm_pio(out_init=rp2.PIO.OUT_HIGH,
             out_shiftdir=rp2.PIO.SHIFT_RIGHT,
             sideset_init=rp2.PIO.OUT_HIGH)
    def tx():
        wrap_target()

        #start bit
        pull()
        wait(0, gpio, clock_pin)
        set(x, 8)    .side(0)
        wait(1, gpio, clock_pin)

        # message
        label('loop')
        wait(0, gpio, clock_pin)
        out(pins, 1)
        wait(1, gpio, clock_pin)
        jmp(x_dec, 'loop')

        #end bit
        wait(0, gpio, clock_pin)
        nop()    .side(1)
        wait(1, gpio, clock_pin)
        
        
        wait(0, gpio, clock_pin)
        nop()    .side(1)
        wait(1, gpio, clock_pin)

        wrap()
    return tx

def rx_factory(clock_pin):
    @rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_RIGHT,
                fifo_join=rp2.PIO.JOIN_RX)
    def rx():
        wrap_target()

        # wait for start bit
        label('ready')
        wait(0, gpio, clock_pin)
        wait(1, gpio, clock_pin)
        jmp(pin, 'ready')

        # accept message
        set(x, 8)
        wait(0, gpio, clock_pin) 
            
        label('loop')
            
        wait(1, gpio, clock_pin)
        in_(pins, 1)
        wait(0, gpio, clock_pin)
            
        jmp(x_dec, 'loop')

        # wait for end bit
        wait(1, gpio, clock_pin)
        jmp(pin, 'end_bit')

        # exception as 10. LSB in word to main thread
        set(y, 1)
        in_(y, 23)
            
        jmp('end')

        # normal execution
        label('end_bit')
        in_(null, 23)
            
        label('end')
        push()

        wrap()
    return rx

def main():
    # clear programs form pio for clean restart
    rp2.PIO(0).remove_program()
    rp2.PIO(1).remove_program()

    Pin(1, Pin.IN, Pin.PULL_UP)

    tx = tx_factory(2)
    rx = rx_factory(2)

    sm_tx = rp2.StateMachine(0, tx, freq=1000000, out_base=Pin(0), sideset_base=Pin(0))
    sm_rx = rp2.StateMachine(1, rx, freq=10000000, in_base=Pin(1), jmp_pin=Pin(1))

    sm_rx.irq(lambda x: {print('error')})

    print('starting state machines')

    sm_tx.active(1)
    sm_rx.active(1)

    while True:
        x = input('Enter Number to send:\n')
        sm_tx.put(int(x))
        y = sm_rx.get()
        print(y)

    sm_tx.active(0)
    sm_rx.active(0)

    print('finish')

if __name__ == '__main__':
    main()

