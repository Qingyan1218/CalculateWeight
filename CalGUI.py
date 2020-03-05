from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno,showinfo
from calculate import splitexpr,getparam

class mybasicframe():
    def __init__(self,title='basic title',ico=None):
        """to initialize the GUI"""
        self.basicwin = Tk()
        self.basicwin.title(title)
        if ico:
            self.basicwin.iconbitmap(ico)
        self.makewidgets()
        self.paramdict = {}
        self.currentrow=1
        self.basicwin.mainloop()

    def makewidgets(self):
        """to make widgets"""
        self.intext=Text(self.basicwin, width=80, height=30) #30的意思是30个平均字符的宽度，height设置为两行
        self.intext.config(font=('华文宋体 常规', 12, 'normal'))
        self.outtext = Text(self.basicwin, width=80, height=30)
        self.outtext.config(font=('华文宋体 常规', 12, 'normal'))
        self.intext.grid(row=1,column=0)
        self.outtext.grid(row=1,column=1)
        btnrow=Frame(self.basicwin)
        btnrow.grid(row=2,columnspan=2)
        btnlist=[['show new result','self.shownew',45],['clear and show result','self.showall',45],
                 ['clear all','self.clearall',45],['show help','self.showhelp',45]]
        for i in range(len(btnlist)):
            btn = Button(btnrow, text=btnlist[i][0], width=btnlist[i][2], command=eval(btnlist[i][1]))
            btn.grid(row=0, column=i)

    def clearall(self):
        """to clear the windows"""
        if askyesno('Verify','Do you really want to clear all?'):
            self.outtext.delete('1.0','end')
            self.intext.delete('1.0', 'end')
            self.paramdict={}
        else:
            pass

    def show(self,i):
        """the function is to show the result ,argument i is the current row"""
        while True:
            beginaddr = "%d.0" % i
            endaddr = "%d.end" % i
            word = self.intext.get(beginaddr, endaddr)
            if word:
                result=splitexpr(word,self.paramdict)
                try:
                    partresult=getparam(result)
                    if partresult:
                        for item in partresult:
                            self.paramdict[item[0]]=item[1]
                except:
                    showinfo('warnings','something is wrong')
                self.outtext.insert(INSERT,(result+'\n'))
                i=i+1
            else:
                break
        self.currentrow=i
        #self.outtext.tag_add('tag2','1.0','end')
        #self.outtext.tag_config('tag2',font=('华文宋体 常规', 12, 'normal'))


    def showall(self):
        """At first, the interface needs to be cleared, then to show the new result"""
        self.outtext.delete('1.0','end')
        self.show(1)
        #self.intext.tag_add('tag1','1.0','end')
        #self.intext.tag_config('tag1',font=('华文宋体 常规', 12, 'normal'))

    def shownew(self):
        """to show the new result of the expression added"""
        self.show(self.currentrow)

    def showhelp(self):
        """show help document"""
        self.outtext.delete('1.0','end')
        self.outtext.insert(INSERT,"there is no help document now")

try:
    iconfile='.\\weight.ico'
except:
    iconfile=None
basicwin=mybasicframe('Calculate Expression',iconfile)