import machine
import time
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral

# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()

# Create an instance of the BLESimplePeripheral class with the BLE object
sp = BLESimplePeripheral(ble)

vibration_motor_pin = 1
motor_pin = machine.Pin(vibration_motor_pin, machine.Pin.OUT)
running = True

def vibrate(duration_ms):
    global running
    # 將引腳設定為高電平，啟動震動
    motor_pin.value(1)
    
    while duration_ms > 0 and running:
        time.sleep_ms(100)
        duration_ms -= 100
    
    # 將引腳設定為低電平，停止震動
    motor_pin.value(0)

# Define a callback function to handle received data
def on_rx(data):
    print("Data received: ", data)  # Print the received data
    if data == b'vibrate_motor\r\n':  # Check if the received data is "vibrate_motor"
        vibrate(10000)  # Vibrate for 10 seconds

# Start an infinite loop
while True:
    if sp.is_connected():  # Check if a BLE connection is established
        sp.on_write(on_rx)  # Set the callback function for data reception
    
    # Scan for devices
    advs = ble.gap_scan(2000)  # Scan for 2 seconds
    
    # Check if there are valid scan results
    if advs is not None:
        for adv in advs:
            # Check if the advertisement contains the ESP32 service UUID
            if bytes([0x6C, 0x92]) in adv['adv_data']:
                # Extract the transmitted data
                esp32_data = adv['adv_data'][adv['adv_data'].index(bytes([0x6C, 0x92])) + 2 : ]
                # Check if the received password matches the expected password
                if esp32_data == b'MySecretPassword':
                    # If the passwords match, start vibrating the motor
                    vibrate(5000)  # Vibrate for 5 seconds
