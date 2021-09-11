import serial
import os
import sys
import time
import pyboard

if __name__=="__main__":

    ser = serial.Serial()
    ser.baudrate = 115200

    try:
        com_port = input("\n請輸入 ESP32 連接的序列埠: ")
        print("\n\n測試序列埠...\n")
        ser.port = com_port
        ser.open()
        ser.close()
        print("序列埠測試成功...")
        while True:
            print("\n\n==================== 燒錄韌體 ====================\n\n")
            os.system("python.exe Scripts\\esptool.py --chip esp32 --port "+com_port+" erase_flash")
            os.system("python.exe Scripts\\esptool.py --chip esp32 --port "+com_port+" --baud 460800 write_flash -z 0x1000 esp32-20210902-v1.17.bin")

            print("\n\n==================== 測試韌體 ====================\n\n")
            pyb = pyboard.Pyboard(com_port)
            time.sleep(2)
            pyb.enter_raw_repl()
            ret=str(pyb.exec('help()'), 'utf-8')
            pyb.exit_raw_repl()
            pyb.close()
            
            if "Welcome to MicroPython on the ESP32!" in ret:
                print("-------------------- 韌體燒錄成功！ --------------------\n\n")
            else:
                print("----- 韌體燒錄失敗！ 韌體燒錄失敗！ 韌體燒錄失敗！ -----\n\n")

            break
            text = input("請換下一片 ESP32 控制板, 然後按 Enter 鍵燒錄")
    except Exception as e:
        print(e.message)
    finally:
        ser.close()


