import bluetooth
import time

# 設定你想要連接的藍牙裝置的地址
addr = "00:00:00:00:00:00"  # 請將此處替換為你的藍牙裝置的MAC地址

# 建立一個藍牙socket
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# 連接到藍牙裝置
sock.connect((addr, 1))

try:
    while True:
        # 發送訊號
        sock.send("這是一個訊號\n")
        # 等待一秒
        time.sleep(1)
except KeyboardInterrupt:
    # 如果使用者按下Ctrl+C，則關閉socket並結束程式
    sock.close()
