from telemetry_f1_2021.listener import TelemetryListener
from IPython import embed
import json
listener = TelemetryListener(port=20777, host='')

wheelData = {"speed" : 0, "gear" : 0, "delta" : 0, "lastLapTime" : 0, "tyre" : [], "brake" : [], "rpm" : 0 }

while True:
    packet = listener.get()
    packet = {k: packet.get_value(k) for k, _ in packet._fields_}
    # data.append(packet)
    carTelem = ""
    carTelem = packet.get('m_car_telemetry_data')
    if carTelem != None:
        # break
        wheelData["speed"] = carTelem[19]['m_speed']
        wheelData["gear"] = carTelem[19]['m_gear']
        wheelData["rpm"] = carTelem[19]['m_engine_rpm']
        wheelData["brake"] = carTelem[19]['m_brakes_temperature']
        wheelData["tyre"] = carTelem[19]['m_tyres_inner_temperature']
        print(wheelData)
        break
    
    # if packet.get('m_participants') != None:    
    #     break
           
embed()
        
       
       
        
    

# for i in range (12):
# packet = listener.get()

    # data.append(packet)
        



