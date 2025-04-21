import tkinter as tk
pencere1=tk.Tk()

def degistir():
    yazi.config(text="yazi deyisti")
def faylyarat():
    fayl=open("test.txt","w")
    yazi.config(text="fayl yarandi")
def renk():
    yazi.config(fg="red", font="arial 20 bold")

yazi=tk.Label(pencere1, text="yazi deyisecek")
yazi.pack()


dugme=tk.Button(pencere1, text="bura bas", command=degistir)
dugme.pack()



dugme2=tk.Button(pencere1, text="cixis", command=pencere1.quit)
dugme2.pack()



dugme3=tk.Button(pencere1, text="fayl yarat", command=faylyarat)
dugme3.pack()

dugme4=tk.Button(pencere1, text="yazi rengini deyisdir", command=renk)
dugme4.pack()


pencere1.mainloop()