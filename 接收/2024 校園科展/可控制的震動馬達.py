import machine
import time

vibration_motor_pin = 1 
interrupt_pin = 15  # GP15引腳

motor_pin = machine.Pin(vibration_motor_pin, machine.Pin.OUT)
interrupt_pin_obj = machine.Pin(interrupt_pin, machine.Pin.IN, machine.Pin.PULL_UP)

running = True

def stop_program(pin):
    global running
    print("金鑰已插入，終止程式")
    running = False

# 設定中斷處理函式
interrupt_pin_obj.irq(trigger=machine.Pin.IRQ_FALLING, handler=stop_program)

def vibrate(duration_ms):
    global running
    # 將引腳設定為高電平，啟動震動
    motor_pin.value(1)
    
    while duration_ms > 0 and running:
        time.sleep_ms(100)
        duration_ms -= 100
    
    # 將引腳設定為低電平，停止震動
    motor_pin.value(0)

vibrate(100000)  # 震動10秒鐘
