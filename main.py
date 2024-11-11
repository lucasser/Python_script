import serial
import threading
import time

import serial.tools.list_ports

#multiple serial ports to work together
class SerialGroup():
    esp = []
    active = False

    def __init__(self):
        print ('Search ports...')
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "USB" in p.device_path:
                print(p.device, flush=True)
                e = serial.Serial(port=p.device,  baudrate=115200, timeout=.1)
                t = threading.Thread(target=self.monitor, args=([e,len(self.esp)]))
                self.esp.append({"esp":e, "thread":t, "data":[]})
                t.daemon = True
                t.start()
        print(self.esp)

    #send to all
    def broadcast(self, data):
        for e in self.esp:
            e["esp"].write(bytes(data, 'utf-8'))
            print(data)

    #launch on sepparate thread to monitor serial connection
    def monitor(self, espNode, index):
        print("started monitor")
        text = ""
        while True:
            try:
                if (espNode.inWaiting() > 0):
                    text += espNode.readline().decode("utf=8")
                elif (text != ""):
                    print("\n"+espNode.port + ": " + text)
                    text = ""
            except IOError:
                print(espNode.port + " disconnected")
                del self.esp[index]
                break



#main code

ms = SerialGroup()

print("ready")

commands = ("a1 x150", "a1 z200", "a1 x0", "a1 z0", "a1 x100 z200")

for c in commands:
    ms.broadcast(c)
    time.sleep(0.25)

while True:
    num = input("Enter input: ")
    ms.broadcast(num)