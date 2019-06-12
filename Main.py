import time
import turtle
import numpy as np
from tkinter.messagebox import *
from tkinter import *

WIN_SIZE = (1600 , 800)
BG_COLOR = '#000000'
FG_COLOR = '#ffffff'

WIDTH , HEIGHT =  (1500  , 475)
OFFSET_x , OFFSET_y = (75 , 75)

PENSIZE = 3
SPEED = 1


class MyTurtle(turtle.RawTurtle):

    def __init__(self , app , canvas):
        super().__init__(canvas)

        self.app = app

        self.getscreen().setworldcoordinates(-OFFSET_x, -OFFSET_y, WIDTH - OFFSET_x, HEIGHT - OFFSET_y)
        self.getscreen().getcanvas().create_line(0 , -HEIGHT , 0 , OFFSET_y , width= 3 , fill='#000000')
        self.getscreen().getcanvas().create_line(WIDTH , 0 ,  -OFFSET_x , 0 , width= 3 , fill='#000000')


    def PrepereTurtle(self , position , pen_size = PENSIZE , speed = SPEED , delay = 1):

        self.color('#008000')
        self.shape('circle')
        self.pensize(pen_size)
        self.speed(speed)
        self.penup()
        self.hideturtle()
        self.setpos(position)
        self.pendown()
        self.showturtle()

        time.sleep(delay)


    def Animate(self , Parameters):

        y0, vy0, ay, x0, vx0, ax = Parameters

        a = np.array([ax , ay])
        v = np.array([vx0 , vy0])
        r = np.array([x0 , y0])        

        self.PrepereTurtle((r[0] ,r[1]))

        t = 0

        while True :
            
            self.app.Log("%.3f(s) : (%.2f , %.2f)" % (t , self.xcor(), self.ycor()))  
        
            t1 = time.time()

            r += v
            v += a

            self.setpos(x = r[0] , y = r[1])

            if (r[1] - 50 < 0) : break

            t2 = time.time()
   
            t += t2 - t1


        time.sleep(0.3)
        self.color('#bb0000')

        self.app.Write('[+] Simulation has completed! ({0:.3f} Seconds)'.format(t) , color = '#22ff00')
        


class App() :


    root = Tk()
    root.title("Settings")
    root.geometry('{}x{}'.format(*WIN_SIZE))
    root.resizable(width = False , height = False)
    root.configure(bg = BG_COLOR)

    def __init__(self) :

        self.initGraph()
        self.root.mainloop()

    def Log(self , text) :

        self.log_box.config(state=NORMAL)
        self.log_box.insert("end" , text + "\n")
        self.log_box.see("end")
        self.log_box.config(state=DISABLED)

    def Write(self , text , color) :

        self.msg_box.config(stat = NORMAL , fg = color)
        self.msg_box.insert("end" , text + "\n")
        self.msg_box.see("end")
        self.msg_box.config(state=DISABLED)

    def clear(self):

        self.log_box.config(state=NORMAL)
        self.log_box.delete('1.0', END)
        self.log_box.update()
        self.log_box.config(state=DISABLED)

        self.msg_box.config(state=NORMAL)
        self.msg_box.delete('1.0', END)
        self.msg_box.update()
        self.msg_box.config(state=DISABLED)

        self.cvs.delete('all')

        

    def runTurtle(self) :

        try :

            my_turtle = MyTurtle(self , self.cvs)
            my_turtle.Animate( [float(var.get()) for var in self.Strings_vars] )

        except ValueError :

            showerror("Type Error" , "Invaild Number Value")

    def initGraph(self):

        Strings = ['y0' , 'vy0' , 'ay' , 'x0' , 'vx0' , 'ax']

        self.Strings_vars = [StringVar() for str in Strings]

        Labels = []
        Entrys = []

        for str in Strings :

            Labels.append(Label(self.root, text=('Set %s : ' % (str)), font='Unispace 10 bold' , bg = BG_COLOR , fg = FG_COLOR))
            Entrys.append(Entry(self.root, textvariable= self.Strings_vars[Strings.index(str)] , width = 15))

        i = 50
        for label , entry in zip(Labels[: 3] , Entrys[: 3]) :

            label.place(x = 50 , y = i)
            entry.place(x = 130 , y = i)
            i = i + 50

        i = 50
        for label , entry in zip(Labels[3 :] , Entrys[3 :]) :

            label.place(x = 250 , y = i)
            entry.place(x = 330 , y = i)
            i = i + 50


        self.cvs = Canvas(master = self.root , width = WIDTH , height = HEIGHT , bg = "white")
        self.cvs.place(x = 10 , y = i + 100)

        self.animate_button = Button(text = 'Animate !' ,  font = 'Unispace 15 bold' ,
                                     width = 12, bg = BG_COLOR  , fg = FG_COLOR , command = self.runTurtle)
        self.animate_button.place(x = 100 , y = i)

        self.reset_button = Button(text = 'Reset' ,  font = 'Unispace 15 bold' ,
                                     width = 12, bg = BG_COLOR  , fg = FG_COLOR , command = self.clear)
        self.reset_button.place(x = 275 , y = i)

        self.credit = Label(self.root , text = " Metiar High School's physics class" ,
                                 font= 'Unispace 8 bold' ,bg = BG_COLOR , fg = FG_COLOR)
        self.credit.place(x = 125 , y = i + 50)

        self.msg_box = Text(self.root, state=DISABLED, bg='#000000', fg= '#ffffff', height=15, width=50)
        self.msg_box.place(x=475, y=25)

        self.log_box = Text(self.root, state = DISABLED, bg = '#00008c', fg='#ffffff' , height=15, width=75)
        self.log_box.place(x = 910 , y = 25)



App()