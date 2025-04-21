import tkinter as tk
pencere=tk.Tk()


pencere.title("python tkinter")
etiket1=tk.Label(pencere,text="koduma xos geldin",fg="red",bg="yellow")
etiket1.pack()

etiket2=tk.Label(pencere,text="proqramlasdirmanin esaslari",fg="white",bg="black",font="times 22 italic" )
etiket2.pack()


etiket3=tk.Label(pencere, text="serxan talibzade",fg="cyan",font="times 18")
etiket3.pack()




pencere.mainloop()
