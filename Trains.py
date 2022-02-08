from math import sqrt
import tkinter as tk
import random as rnd
from concurrent.futures import ThreadPoolExecutor, as_completed

time = 0

window_size = [1520,1000]

Visual = tk.Tk()
Visual.title("Trains")

Canvas = tk.Canvas(Visual, width=window_size[0], height=window_size[1])
Canvas.pack()

colours = ["Blue","Red","Green","Yellow","Cyan","Magenta"]

number_of_stations = 100
Stations = []
Station_Locatons = []

station_size = 5
line_width = 1

Connection_Radius = 300

def Generate_Stations():
    counter = 0
    while counter <= number_of_stations-1:
        point = [rnd.randint(station_size,window_size[0]),rnd.randint(station_size,window_size[1])]
        colour = rnd.randint(0,5)
        Stations.append(Canvas.create_oval(point[0]-station_size,point[1]-station_size,point[0]+station_size,point[1]+station_size,fill=colours[colour]))
        Label = Canvas.create_text(point, text=counter, font=("Purisa", station_size))
        Canvas.tag_raise(Label)
        Station_Locatons.append(point)
        #if counter >= 1:
            #tracks.append(Canvas.create_line(Station_Locatons[counter-1],Station_Locatons[counter]))
        counter += 1
    Generate_Tracks(Station_Locatons, counter)


Train_Count = 1000 #number_of_stations

Train_Objects = []
Avaliable_Targets = []
Train_Targets = []
Train_Location = []
train_size = 3


def Trains(Station_Locatons, Station_Count):
    

    def spawn_trains():
        count = 0
        while count <= Train_Count-1:
            station_NUMB = rnd.randint(0, Station_Count-1)
            station_target_NUMB = rnd.randint(0, Station_Count-1)
            colour = rnd.randint(0,5)
            point = Station_Locatons[station_NUMB]
            Train_Objects.append(Canvas.create_rectangle(point[0]-train_size,point[1]-train_size,point[0]+train_size,point[1]+train_size,fill=colours[colour]))
            Targets = []
            for Station in Station_Locatons:
                if (abs(point[0]-Station[0])+abs(point[1]-Station[1])) <= Connection_Radius:
                    Targets.append(Station)
            Avaliable_Targets.append(Targets)
            target = rnd.choice(Targets)
            Train_Targets.append(target)
            Train_Location.append(point)
            count += 1
        for train in Train_Objects:
            Canvas.tag_raise(train)

    def Train_Move():
        count = 0
        length = []
        for Trains in Train_Objects:
            length.append(sqrt((Train_Targets[count][0]-Canvas.coords(Trains)[0]+station_size)**2 + (Train_Targets[count][1]-Canvas.coords(Trains)[1]+station_size)**2))
        for Trains in Train_Objects:
            lengths = (sqrt((Train_Targets[count][0]-Canvas.coords(Trains)[0]+station_size)**2 + (Train_Targets[count][1]-Canvas.coords(Trains)[1]+station_size)**2))
            #target = [(Train_Targets[count][0]-Train_Location[count][0])/Lenght,(Train_Targets[count][1]-Train_Location[count][1])/Lenght]
            #print(target)
            #if Canvas.coords(Trains)[0]-Train_Targets[count][0] and Canvas.coords(Trains)[1] != Train_Targets[count][1]:
            #    Canvas.move(Trains, target[0],target[1])
            if Train_Targets[count][0] > Canvas.coords(Trains)[0]:
                Canvas.move(Trains, (Train_Targets[count][0] - Canvas.coords(Trains)[0])/lengths, 0)
            if Train_Targets[count][1] > Canvas.coords(Trains)[1]:
                Canvas.move(Trains, 0, (Train_Targets[count][1] - Canvas.coords(Trains)[1])/lengths)
            if Train_Targets[count][0] < Canvas.coords(Trains)[0]:
                Canvas.move(Trains, (Train_Targets[count][0] - Canvas.coords(Trains)[0])/lengths, 0)
            if Train_Targets[count][1] < Canvas.coords(Trains)[1]:
                Canvas.move(Trains, 0, (Train_Targets[count][1] - Canvas.coords(Trains)[1])/lengths)
            if abs((Train_Targets[count][0]) - (Canvas.coords(Trains)[0])) <= 1 and abs(Train_Targets[count][1]) - abs(Canvas.coords(Trains)[1]) <= 1:
                reschedual(Canvas.coords(Trains)[0], Canvas.coords(Trains)[1], count)
                #print("reschedual")
            count += 1
            #print(abs((Train_Targets[count-1][0]) - (Canvas.coords(Trains)[0])))
            #print(int(Train_Targets[count-1][1]) - int(Canvas.coords(Trains)[1]))
            #print(Train_Targets[1])
            #print(str(int(Canvas.coords(Train_Objects[1])[1])) + "," + str(int(Canvas.coords(Train_Objects[1])[0])))
            #print(Canvas.coords(Trains))
            #print(Train_Targets[count-1])
        
        #def train_handler():
            #processes = []
            #with ThreadPoolExecutor(12) as executor:
            #    count = 0
            #    for Trains in Train_Objects:
            #        processes.append(executor.submit(train_update, count))
            #train_update(count)
            #count = 0
            #for Trains in Train_Objects:
            #    train_update(count, Trains)
        #train_handler()
        Visual.after(1, Train_Move)

    def reschedual(Trainx, Trainy, count):
        Targets = []
        for Station in Station_Locatons:
            if (abs(Trainx-Station[0])+abs(Trainy-Station[1])) <= Connection_Radius:
                Targets.append(Station)
        Avaliable_Targets[count] = Targets
        target = rnd.choice(Targets)
        Train_Targets[count] = target

    spawn_trains()
    Train_Move()


def Generate_Tracks(Station_Locatons, Station_Count):
    tracks = []
    track_conections = []
    #tracks.append(Canvas.create_line(Station_Locatons, width=line_width, fill="red"))
    #tracks.append(Canvas.create_line(Station_Locatons[0], Station_Locatons[Station_Count-1], width=line_width))
    for Stations in Station_Locatons:
        conections = 0
        for Station in Station_Locatons:
            if (abs(Stations[0]-Station[0])+abs(Stations[1]-Station[1])) <= Connection_Radius:
                colour = rnd.randint(0,5)
                tracks.append(Canvas.create_line(Stations,Station,width=line_width,fill=colours[colour]))
                conections += 1            
        track_conections.append(conections)
    for track in tracks:
        Canvas.tag_lower(track)
    #print(track_conections)
    Trains(Station_Locatons, Station_Count)


Generate_Stations()


Visual.mainloop()