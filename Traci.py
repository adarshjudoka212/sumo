import traci
import time
import traci.constants as tc
import pytz

import datetime
from random import randrange
import pandas as pd


def flatten_list(_2d_list):
    flat_list = []
    for element in _2d_list:
        if type(element) is list:
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list


sumoCmd = ["sumo-gui", "-c","map.sumocfg"]
traci.start(sumoCmd)




packVehicleData = []
packTLSData = []
packBigData = []

while traci.simulation.getMinExpectedNumber() > 0:
       
        traci.simulationStep();

        vehicles=traci.vehicle.getIDList();
        trafficlights=traci.trafficlight.getIDList();

           
        for i in range(0,len(vehicles)):
        	


                vehid = vehicles[i][3:]
                x_coord, y_coord = traci.vehicle.getPosition(vehicles[i])
                #coord = [x, y]
                lon, lat = traci.simulation.convertGeo(x_coord, y_coord)
                gpscoord = [lon, lat]
                spd = round(traci.vehicle.getSpeed(vehicles[i])*3.6,2)
                
                roadid= traci.vehicle.getRoadID(vehicles[i])
                
                lane = traci.vehicle.getLaneID(vehicles[i])
                displacement = round(traci.vehicle.getDistance(vehicles[i]),2)
                turnAngle = round(traci.vehicle.getAngle(vehicles[i]),2)
                nextTLS = traci.vehicle.getNextTLS(vehicles[i])
                
                waitingtime=traci.vehicle.getWaitingTime(vehicles[i])
                stop=traci.vehicle.isStopped(vehicles[i])
                laneindex=traci.vehicle.getLaneIndex(vehicles[i]) 
               
                noofvehicle=traci.lane.getLastStepVehicleNumber(lane)
                arrivaldelay=traci.vehicle.getStopArrivalDelay(vehicles[i])
                route=traci.vehicle.getRoute(vehicles[i])
               
                traveltime=traci.lane.getTraveltime(lane)
                bestlane=traci.vehicle.getBestLanes(vehicles[i]) 
                pendingvehicle=len(traci.lane.getPendingVehicles(lane))
                dest=route[len(route)-1]

                #Packing of all the data for export to CSV/XLSX
                vehList = [ vehid, x_coord,y_coord, lon,lat, spd, traveltime,roadid ,dest ,waitingtime,laneindex  ,displacement ]

                idd = traci.vehicle.getLaneID(vehicles[i])

                 
                packBigDataLine = flatten_list([vehList])

                packBigData.append(packBigDataLine)

 
                   
traci.close()

#Generate Excel file
columnnames = [ 'vehid','x_coord', 'y_coord','lon','lat', 'spd' , 'traveltime', 'roadid','destination', 'waitingtime',   'laneindex'  ,'displacement']
dataset = pd.DataFrame(packBigData, index=None, columns=columnnames)
dataset.to_excel("output.xlsx", index=False)
time.sleep(5)