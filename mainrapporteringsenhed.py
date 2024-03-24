
import network,espnow,math,esp32,time,dht
from machine import Pin,deepsleep
from hcsr04 import HCSR04            
from adc_sub import ADC_substitute

dashboard_mac_address = b'\xB0\xA7\x32\xDE\x67\xF0' 

sensor_hcsr04_id = "Ultrasound"               
pin_us_trigger = 26                  
pin_us_echo = 25               
sensitivity = 50


sensor_KY026_id = "Flamme"                  
pin_sensor_KY026 = 16                

sensor_DHT11_id = "DHT11 Klimasensor"                   
pin_dht11 = 4                        

pin_battery = 34              


pushbutton = Pin(32,Pin.IN,Pin.PULL_UP) 


red_led = Pin(21, Pin.OUT)

esp32.wake_on_ext0(pin = pushbutton,
    level = esp32.WAKEUP_ALL_LOW)
on_off = 0

sta = network.WLAN(network.STA_IF)    
sta.active(True)                      

en = espnow.ESPNow()                 
en.active(True)                       

sensor = HCSR04(pin_us_trigger, pin_us_echo, 10000) 
sensor_KY026 = Pin(pin_sensor_KY026, Pin.IN)
sensor_DHT11 = dht.DHT11(Pin(pin_dht11))

battery = ADC_substitute(pin_battery) 
ip1 = 1.4                             
ip2 = 2.4                            
bp1 = 0                               
bp2 = 100                              
alpha = (bp2 - bp1) / (ip2 - ip1)      
beta = bp1 - alpha * ip1               

prev_sensor_value_KY026 = -999       
prev_sensor_value_HCSR504 = -999               
prev_bat_pct = -1                    
prev_sensor_DHT11_temp = -999         
prev_sensor_DHT11_hum = -999          

time_last_toggle = 0
time_last_toggleMovement = 0

def get_battery_percentage():
    ip = battery.read_voltage()        
    
    bp = alpha * ip + beta             
    bp = int(bp)                     
    
    if bp < 0:                         
        bp = 0
    elif bp > 100:
        bp = 100
    
    return bp   

def time_now():
    now = time.localtime()
    current_time = (" {}-{}-{}-{}H-{}M-{}S".format(now[0], now[1], now[2],now[3],now[4],now[5]))
    return current_time


def initialization():
    print(time_now())
    print(sensor_hcsr04_id)
    print(sensor_DHT11_id)
    print(sensor_KY026_id)
    print("Starting up and ready!")
    
get_battery_percentage()
bat_pct = get_battery_percentage()
sensor_DHT11.measure()
sensor_DHT11_temp = sensor_DHT11.temperature()
sensor_DHT11_hum = sensor_DHT11.humidity()

en.add_peer(dashboard_mac_address)     # Must add_peer() before send()


initialization()

while True:
    button_state = pushbutton.value()

    if button_state == 0:  
        on_off = not on_off 
        time.sleep(0.5) 
        print("Going to sleep!")
        deepsleep() 
    if time.ticks_diff(time.ticks_ms(), time_last_toggle) > 3600000: 
        get_battery_percentage()
        bat_pct = get_battery_percentage()
        time_last_toggle = time.ticks_ms()
        sensor_DHT11.measure()
        sensor_DHT11_temp = sensor_DHT11.temperature()
        sensor_DHT11_hum = sensor_DHT11.humidity()
    
    sensor_value_HCSR504 = sensor.distance_cm()
    sensor_value_KY026 = sensor_KY026.value()

    if math.fabs(sensor_value_HCSR504 - prev_sensor_value_HCSR504) > sensitivity: 
        red_led.on() 
        movement = 1
    else:
        movement = 0
        red_led.off()
    
    if bat_pct != prev_bat_pct or sensor_value_KY026 != prev_sensor_value_KY026 or movement != prev_movement:
        data_string = str(time_now()) + '#' + str(bat_pct) + '#' + str(movement) + '#' + str(sensor_value_KY026) + '#' + str(sensor_DHT11_temp) + '#' + str(sensor_DHT11_hum) + '#' + '1' + '#' + '\n'  # The data to send. CHANGE IT!
        print("Sending: " + data_string)
        try:

            red_led.off()
            en.send(dashboard_mac_address, data_string, False)
        except ValueError as e:
            print("Error sending the message: " + str(e))
            
        prev_bat_pct = bat_pct
        prev_sensor_value_HCSR504 = sensor_value_HCSR504
        prev_sensor_value_KY026 = sensor_value_KY026
        prev_movement = movement
    
    time.sleep_ms(20)                 