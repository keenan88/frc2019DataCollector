from tkinter import *
from tkinter import Tk, messagebox
from PIL import Image, ImageTk
import csv
import os
import socket
import math


class mainWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master) #BIG FRAME
        self.welcomeWidgetPlacement()

    #WELCOME PAGE METHODS
    def welcomeWidgetPlacement(self):
        welcomeWidgets = []
        self.greetFr = Frame(self.master)
        self.greetFr.place(relx=0,rely=0,relwidth=1,relheight=1)
        self.greetFr.bind('<Configure>', lambda event, : self.resizeWelcomeWidgets(event, welcomeWidgets))


        self.clydeImage = Image.open("./images/clydeBackground.png")
        self.clydeImg_copy= self.clydeImage.copy()
        self.clydeCackground_image = ImageTk.PhotoImage(self.clydeImage)
        self.clydeBackground = Label(self.greetFr, image=self.clydeCackground_image)
        self.clydeBackground.pack(fill=BOTH, expand=YES)
        self.clydeBackground.bind('<Configure>', self.resizeClyde)

        self.greetingLbl = Label(self.greetFr, font=("Arial", 20), text="Team 4678\n Data Collector ",bg='black', fg="white")
        self.greetingLbl.place(relx=0.03,rely=0.05)
        welcomeWidgets.append(self.greetingLbl)

        self.IPEnt = Entry(self.greetFr, font=("Arial", 20), width = 12, bg='black', fg="white")
        self.IPEnt.insert(1, "Enter IP")
        self.IPEnt.place(relx=0.03,rely=0.3)
        welcomeWidgets.append(self.IPEnt)

        self.portEnt = Entry(self.greetFr, font=("Arial", 20), width = 12, bg='black', fg="white")
        self.portEnt.insert(1, "Enter Port")
        self.portEnt.place(relx=0.03,rely=0.45)
        welcomeWidgets.append(self.portEnt)

        self.enterBtn = Button(self.greetFr, text="Continue", font=("Arial", 22), width = 10, bg='black', fg="white", command=lambda:self.openMainWindow())
        self.enterBtn.place(relx=0.03,rely=0.6)
        welcomeWidgets.append(self.enterBtn)

    def resizeClyde(self,event):

        new_width = event.width
        new_height = event.height

        self.clydeImage = self.clydeImg_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.clydeImage)
        self.clydeBackground.configure(image =  self.background_image)

    def resizeWelcomeWidgets(self, event, widgets):
        for widget in widgets:
            widget.config(font=("Arial", math.floor(event.height/18)))

    def openMainWindow(self):
        self.IP = self.IPEnt.get()
        self.port = self.portEnt.get()


        try:
            s = socket.socket()
            s.connect((self.IP, int(self.port)))
            s.close()
            self.greetFr.place_forget()
            self.placeOriginalWidgets()
            messagebox.showinfo("Connected!", "Welcome to team 4678's 2019 data collector!\n You are connected to server "+self.IP+" on port "+self.port)

        except:
            messagebox.showinfo("No connection", "Coud not establish a connection.\nPlease check IP and port and try to connect.")

    #RESIZE FUNCTION FOR THE FIELD MAP
    def resizeFieldImg(self,event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)

    def resizeCommentBox(self, event, textbox):

        textbox.config(width=math.floor(event.width/9))
        textbox.config(height=math.floor(event.height/22))

    def resizeRevisePageWidgets(self, event, textboxes, labels):
        divisor = 60


        for textbox in textboxes:
            textbox.config(font=("Arial", math.floor(event.width/divisor)))

        for label in labels:
            label.config(font=("Arial", math.floor(event.width/divisor)))

    # 'set' functions change the values in the dictionary self.data
    def setTeamNum(self,teamNumLower):
        self.data['teamNum'] = teamNumLower


    def setMatchNum(self,matchNumLower):
        self.data['matchNum'] = matchNumLower


    def setClimbLevel(self, position):
        self.data['climbLevel'] = position

    def setGamePiecePlacement(self, location):
        if location[len(location)-6:len(location)] != "Cancel":
            self.data[location] = self.data[location] + 1

        self.placeInitialRocket()


    #WIDGET PLACERS AND UNPLACERS
    def placeOriginalWidgets(self):
        self.initialRocketButtons=[]
        self.rocketCargoButtons=[]
        self.rocketHatchButtons=[]
        self.cargoBayButtons=[]


        self.data={"teamNum":0,
                   "matchNum":0,
                   "climbLevel":0, #low(0), mid(1), or high(2)
                   "bayCargo":0, #integer count
                   "bayHatch":0, #integer count
                   "rocketCargoLow":0, #integer count
                   "rocketCargoMid":0, #integer count
                   "rocketCargoHigh":0, #integer count
                   "rocketHatchLow":0, #integer count
                   "rocketHatchMid":0, #integer count
                   "rocketHatchHigh":0,#integer count
                   "comments":"empty"
                   }

        self.fieldMapFr = Frame(self.master,bg="coral")
        self.fieldMapFr.place(relx=0,rely=0.05,relwidth=1,relheight=0.9)

        #ALL VARIABLES NEEDED FOR FIELD MAP RESIZING
        self.image = Image.open("./images/field.png")
        self.img_copy= self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self.fieldMapFr, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self.resizeFieldImg)

        #MENUBAR START
        self.myMenuBar = Menu(self)
        fileMenu = Menu(self.myMenuBar, tearoff=0)
        self.myMenuBar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Save game", command=lambda: self.revisePage()) #NEEDS NEW COMMAND #self.sendData()
        fileMenu.add_command(label="New game", command=self.master.quit) #NEEDS NEW COMMAND
        fileMenu.add_command(label="Close", command=self.quit)
        teamNums = [188, 2200, 2386, 2708, 2852, 2994, 3571, 4015, 4152, 4476, 4519, 4525, 4704, 4783, 4907, 4936, 4946, 4951, 5036, 5409, 5426, 5885, 6070, 610, 6110, 6135, 6514, 6859, 6864, 6866, 6867, 6975, 6987, 7267, 7564, 7614, 7690, 7710, 7712, 7735]
        teamMenu = Menu(self.myMenuBar, tearoff=0)
        self.myMenuBar.add_cascade(label="Team", menu=teamMenu)
        for x in teamNums:
            teamMenu.add_command(label=x, command=lambda z=x: self.setTeamNum(z))
        matchMenu = Menu(self.myMenuBar, tearoff=0)
        self.myMenuBar.add_cascade(label="Match", menu=matchMenu)
        for x in range(100):
            matchMenu.add_command(label=x, command=lambda z=x: self.setMatchNum(z))
        self.master.config(menu=self.myMenuBar)
        climbMenu = Menu(self.myMenuBar, tearoff=0)
        self.myMenuBar.add_cascade(label="Climb", menu = climbMenu)
        climbMenu.add_command(label="Low", command=lambda:self.setClimbLevel(0))
        climbMenu.add_command(label="Mid", command=lambda:self.setClimbLevel(1))
        climbMenu.add_command(label="High", command=lambda:self.setClimbLevel(2))

        #MENUBAR END

        #red and blue alliances cargo and hatch placement for cargo ship
        for x in range(2):
            myButton = Button(self.fieldMapFr, text="Cargo", command=lambda:self.setGamePiecePlacement("bayCargo"))
            myButton.place(relx=0.385+0.126*x, rely=0.46, relwidth=0.1, relheight=0.04)
            self.cargoBayButtons.append(myButton)
            myButton = Button(self.fieldMapFr, text="Hatch", command=lambda:self.setGamePiecePlacement("bayHatch"))
            myButton.place(relx=0.385+0.126*x, rely=0.5, relwidth=0.1, relheight=0.04)
            self.cargoBayButtons.append(myButton)

        #creating and placing rocket cargo and hatch buttons
        for x in range(2):
            for j in range(2):
                self.cargoBu = Button(self.fieldMapFr, text="Cargo", command=lambda:self.placeRocketHeightsCargo())
                self.cargoBu.place(relx=0.338+0.248*x, rely=0.05+0.8*j, relwidth=0.07, relheight=0.05)
                self.initialRocketButtons.append(self.cargoBu)

                self.hatchBu = Button(self.fieldMapFr, text="Hatch", command=lambda:self.placeRocketHeightsHatches())
                self.hatchBu.place(relx=0.338+0.248*x, rely=0.1+0.8*j, relwidth=0.07, relheight=0.05)
                self.initialRocketButtons.append(self.hatchBu)

        #creating but not placing rocket cargo buttons
        self.heights = ["Low","Mid","High", "Cancel"]
        for n in range(4):
            for x in range(len(self.heights)):
                self.myButton = Button(self.fieldMapFr, text=self.heights[x], command=lambda o="rocketCargo"+self.heights[x] :self.setGamePiecePlacement(o)) #rocketCargoMid
                self.rocketCargoButtons.append(self.myButton)

        #creating but not placing rocket hatch buttons
        for n in range(4):
            for x in range(len(self.heights)):
                self.myButton = Button(self.fieldMapFr, text=self.heights[x], command=lambda o="rocketHatch"+self.heights[x] :self.setGamePiecePlacement(o)) #rocketCargoMid
                self.rocketHatchButtons.append(self.myButton)

    def placeRocketHeightsCargo(self):
        for x in range(len(self.initialRocketButtons)):
            self.initialRocketButtons[x].place_forget()

        counter = 0
        for n in range(2):
            for f in range(2):
                for k in range(4):
                    self.rocketCargoButtons[counter].place(relx=0.338+0.25*f, rely=0.05+0.05*k+0.7*n, relwidth=0.07, relheight=0.05)
                    counter+=1

    def placeRocketHeightsHatches(self):
        heights = ["High","Mid","Low", "Cancel"]
        distances = ["Close", "Far"]
        for x in range(len(self.initialRocketButtons)):
            self.initialRocketButtons[x].place_forget()
        counter = 0

        for n in range(2):
            for k in range(2):
                for j in range(4):
                        self.rocketHatchButtons[counter].place(relx=0.338+0.25*k, rely=0.05+0.05*j+0.7*n, relwidth=0.07, relheight=0.05)
                        counter+=1

    def placeInitialRocket(self):
        self.unplaceRocketCargo()
        self.unplaceRocketHatches()

        counter = 0
        for x in range(2):
            for j in range(2):
                self.initialRocketButtons[counter].place(relx=0.338+0.248*x, rely=0.05+0.8*j, relwidth=0.07, relheight=0.05)
                counter+=1
                self.initialRocketButtons[counter].place(relx=0.338+0.248*x, rely=0.1+0.8*j, relwidth=0.07, relheight=0.05)
                counter+=1

    def unplaceAllWidgets(self):
        for x in range(len(self.initialRocketButtons)):
            self.initialRocketButtons[x].place_forget()

        for x in range(len(self.rocketCargoButtons)):
            self.rocketCargoButtons[x].place_forget()

        for x in range(len(self.rocketHatchButtons)):
            self.rocketHatchButtons[x].place_forget()

        for x in range(len(self.cargoBayButtons)):
            self.cargoBayButtons[x].place_forget()

    def unplaceRocketCargo(self):
        for x in range(len(self.rocketCargoButtons)):
           self.rocketCargoButtons[x].place_forget()

    def unplaceRocketHatches(self):
        for x in range(len(self.rocketHatchButtons)):
            self.rocketHatchButtons[x].place_forget()


    #END GAME FUNCTIONS, switches between pages
    def revisePage(self):
        self.unplaceAllWidgets()
        self.reviseFr = Frame(self.fieldMapFr, bg='grey75')
        self.reviseFr.place(relx=0.5,rely=0.5, anchor="c", relwidth=0.5, relheight=0.6)
        self.reviseFr.bind('<Configure>', lambda event, : self.resizeRevisePageWidgets(event, self.reviseTextBoxes, self.reviseLabels))

        keys = list(self.data.keys())
        self.reviseLabels = []
        self.reviseTextBoxes = []

        counter = 0
        vcmd = (self.register(self.validate))
        for y in range(3):
            for x in range(5):
                if counter >= (len(keys) - 1):
                    break
                myLabel = Label(self.reviseFr, text=keys[counter], font=("Arial", 10), bg="grey75")
                myLabel.place(relx=0.5+(x-2)*0.2, rely=0.4+0.33*(y-1), anchor="c")
                self.reviseLabels.append(myLabel)

                myTxt = Entry(self.reviseFr, validate='all', validatecommand=(vcmd, '%P'), width=10)
                myTxt.insert(1, self.data[keys[counter]])

                myTxt.place(relx=0.5+(x-2)*0.2, rely=0.52+0.33*(y-1), anchor="c")
                self.reviseTextBoxes.append(myTxt)
                counter +=1

        self.continueBu = Button(self.reviseFr, text="Continue", font=("Arial", 10), command=lambda:self.commentPage())
        self.continueBu.place(relx=0.8, rely=0.87, relwidth=0.18, relheight=0.1)

    def validate(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def commentPage(self):
        self.reviseFr.place_forget()
        self.continueBu.place_forget()

        self.commentFr = Frame(self.fieldMapFr, bg='grey75')
        self.commentFr.place(relx=0.5,rely=0.5, anchor="c", relwidth=0.5, relheight=0.6)

        self.commentFr.bind('<Configure>', lambda event, : self.resizeCommentBox(event, self.commentsTx))

        self.commentsTx = Text(self.commentFr, width=12, height=12)
        self.commentsTx.place(relx=0.5,rely=0.5,anchor="c")
        self.commentsTx.insert('1.0', "Comments")

        submitBu = Button(self.commentFr, text="Submit", command=lambda:self.submitData())
        submitBu.place(relx=0.88,rely=0.88,relwidth=0.1,relheight=0.1)


    #DATA WRITERS
    def submitData(self):
        self.data["comments"] = self.commentsTx.get('1.0', END)
        try:
            self.sendData()
            messagebox.showinfo("Thanks!", "Data saved to "+self.IP)
        except:
            messagebox.showinfo("Error!", "Could not send data back to server. Saved data locally to -> "+"localCSVData/"+str(self.data["teamNum"])+".csv")
            self.writeToJSONFile()

        self.commentFr.place_forget()
        self.placeOriginalWidgets()

    def writeToJSONFile(self):
        #csvrows = itertools.zip_longest(*[self.data[k] for k in keys], fillvalue='')
        fileName = "localCSVData/"+str(self.data["teamNum"])+".csv"
        file_exists = os.path.isfile(fileName)


        with open(fileName, 'a', newline='') as csvfile:
            w = csv.DictWriter(csvfile, self.data.keys())
            if not file_exists:
                w.writeheader()

            w.writerow(self.data)



    def sendData(self):
        s = socket.socket()
        s.connect((self.IP, int(self.port)))

        filename = "serverCSVData/"+str(self.data["teamNum"])+".csv"

        s.send(str.encode(filename)) #send the filename you want
        data = s.recv(4096) #recieving CSV file if it exists on server

        with open(filename, 'wb') as f:
            f.write(data)
        f.close()

        dataLi = []
        for key in list(self.data.keys()):
            dataLi.append(self.data[key])


        with open(filename, 'a', newline='') as n:
            wr = csv.writer(n)
            wr.writerow(dataLi)

        n.close()

        with open(filename, 'rb') as j:
            s.send(j.read(4096))
        j.close()


        s.close()



def main():
    root = Tk()
    app = mainWindow(root)
    root.minsize(width="960", height="480")
    root.title("Scouting App 2019")
    root.mainloop()


if __name__ == '__main__':
    main()


