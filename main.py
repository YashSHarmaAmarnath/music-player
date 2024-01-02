from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.ttk import Progressbar
from pygame import mixer
import os
from PIL import Image, ImageTk
import time
from mutagen.mp3 import MP3
mixer.init()

class Node:
    def __init__(self,data):
        self.pre = None
        self.path = data
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def insert_at_end(self,data):
        new_node = Node(data)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.pre = self.tail
            self.tail.next = new_node
            self.tail= new_node
        insert_in_list()

    def print_list(self):
        node = self.head
        while node is not None:
            print(node.path)
            node = node.next

def list_music_paths(folder_path):
    image_extensions = ['.mp3','.wav']  # Add more extensions if needed

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                music_list.insert_at_end(os.path.join(root, file))

def insert_in_list():
    if music_list.head is not None:
        listbox.delete(0, END)  # Clear existing content
        node = music_list.head
        while node is not None:
            item = os.path.basename(node.path)
            listbox.insert(END, item)
            node = node.next
        # music_list.print_list()  # For debugging]


def open_folder():
    global current
    folder_path = askdirectory()
    if folder_path:
        print("Selected folder:", folder_path)
        list_music_paths(folder_path)
        # music_list.print_list()
    if current is None:
        if music_list.head is not None:
            current = music_list.head
    current_music.config(text=os.path.basename(current.path) )

def openFile():
    global current
    file= askopenfilename(defaultextension=".mp3",
                          filetypes=[("audio file","*.mp3"),
                          ("audio file","*.wav")])
    if file=="":
        file=None
    else:
        f = open(file,"r")
        music_list.insert_at_end(f.name)
        f.close()
    if current is None:
        if music_list.head is not None:
            current = music_list.head
    current_music.config(text=os.path.basename(current.path) )

def delete():
    global current
    if current is not None:
        # if current.pre is None and current.next is None:
        #     current = None
        if current.next is None:
            current.pre.next = None
            current = current.pre
        elif current.pre is None:
            current.next.pre = None
            current = current.next

        else:
            current.pre.next = current.next
            current.next.pre = current.pre
            current = current.next
        insert_in_list()

def next_():
    global current

    if current.next is not None:
        current = current.next
        current_music.config(text=os.path.basename(current.path) )
        play_()

def previous_():
    global current

    if current.pre is not None:
        current = current.pre
        current_music.config(text=os.path.basename(current.path) )
        play_()

def play_():
    root.title(f'Music player - {current.path}')
    if not mixer.music.get_busy() and mixer.music.get_pos() != -1:
        mixer.music.unpause()
        return

    mixer.music.load(current.path)
    mixer.music.play()
    play_time()
    # update_music_length()

def play_time():
   
    current_time = mixer.music.get_pos()/1000
    current_time_format = time.strftime('%M:%S',time.gmtime(current_time))
    # status_bar.config(text=current_time_format)
    try:
        song_mut = MP3(current.path)
        song_len = song_mut.info.length
    except:
        song_len = mixer.Sound(current.path).get_length()
    current_song_time_format = time.strftime('%M:%S',time.gmtime(song_len))
    status_bar.config(text=f'{current_time_format}  |  {current_song_time_format}')

    if song_len>0:
        progressbar_['value'] = (current_time/song_len)*progressbar_['maximum']
    
    # print(current_time_format,' | ',current_song_time_format)
    # print(type(current_time_format), current_time_format)
    if current_time_format == current_song_time_format or current_time_format == '59:59' :
        print('changed')
        next_()

    
    status_bar.after(1000,play_time)


def stop_():
    mixer.music.pause()

def set_volume(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)

def next_10():
    global current,current_time
    if mixer.music.get_busy():
        current_time = mixer.music.get_pos() + 10000  # Add 10 seconds in milliseconds
        mixer.music.set_pos(current_time/1000)
        play_time()  # Update the status bar with the new time

def pre_10():
    global current
    if mixer.music.get_busy():
        current_pos = mixer.music.get_pos() / 1000  # Get current position in seconds
        new_pos = max(0, current_pos - 10)  # Calculate the new position in seconds, ensuring it doesn't go below 0
        mixer.music.set_pos(new_pos)  # Set the new position
        play_time()  # Update the status bar with the new time


music_list = DoublyLinkedList()
current = None
ten_plus = False
ten_minus = False


if __name__ == '__main__':
    
    root = Tk()
    root.geometry("600x380")
    root.minsize(600,380)
    root.maxsize(600,380)
    root.title('Music player')
    
    

    MenuBar = Menu(root)
   
    #file menue
    FileMenu = Menu(MenuBar,tearoff=0)
    #open
    FileMenu.add_command(label="Open",command=openFile)
    FileMenu.add_command(label="Open folder",command=open_folder)
    
    FileMenu.add_separator()
    #exit 1

    FileMenu.add_command(label="Exit",command=root.quit)
    MenuBar.add_cascade(label="File",menu=FileMenu)
    root.config(menu=MenuBar) 

    left_frame = Frame(root, bg="#1e1f20")
    left_frame.pack(side="left", fill="both", expand=True)
    
    right_frame = Frame(root)
    right_frame.pack(side="right", fill="both", expand=True)

    bottom_frame = Frame(root, bg="#ffffff")
    bottom_frame.place(x=0, y=325, width=600, height=35)

    listbox = Listbox(left_frame, selectmode=SINGLE, bg="#1e1f20", fg='white', width=5)
    scrollbar = Scrollbar(left_frame, orient="vertical", command=listbox.yview)
    listbox.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    listbox.pack(side="left", fill="both", expand=True)
    # items = ["Item 1", "Item 2", "Item 3", ...]  # Replace with your list of items
    # for item in items:
    #     listbox.insert("end", item)



    Next = Button(root, text="⏭️", height=1, width=2, bg="black", fg="white", command=next_)
    Next.place(x=320, y=330)
    play = Button(root, text="▶️", height=1, width=2, bg="black", fg="white", command=play_)
    play.place(x=290,y=330)
    stop = Button(root, text="⏸️", height=1, width=2, bg="black", fg="white", command=stop_)
    stop.place(x=260,y=330)
    prev = Button(root,text="⏮️",height=1,width=2,bg="black",fg="white",command=previous_)
    prev.place(x=230,y=330)
    delete = Button(root, text="💀", height=1,bg="black",fg="white", width=2,  border=0,command=delete)
    delete.place(x=570,y=330)
    next_10_plus = Button(root, text="+10", height=1, width=2, bg="black", fg="white", command=next_10)
    next_10_plus.place(x=390, y=330)
    pre_10_minus = Button(root, text="-10", height=1, width=2, bg="black", fg="white", command=pre_10)
    pre_10_minus.place(x=360, y=330)
    
    volume_controll = Scale(root, from_=0, to=100, orient=HORIZONTAL,length=100, command=set_volume)
    volume_controll.set(50)  # Set default volume to 50volume_controll = Scale(root, orient=HORIZONTAL, length=200)
    # volume_controll.place(x=360, y=320)
    volume_controll.place(x=460, y=320)
    
    progressbar_ = Progressbar(root, orient=HORIZONTAL, length=210, mode="determinate")
    progressbar_.place(x=10, y=330)


    current_music = Label(root,text='----',bg="#23272e",width=60,fg='#ffed32',font = ('Arial', 12, 'bold'))
    current_music.place(x=10, y=300)

    status_bar = Label(root,text='--:--  |  --:--',bd=1,relief=GROOVE,anchor=E)
    # status_bar.pack(fill=X,side=BOTTOM,ipady=2)
    status_bar.place(x=0, y=360,width=600)
    img_label = Label(right_frame,image=None,height=330,width=600)
    img = Image.open('46df9d7e-e795-4080-9b8f-2734e9bb76f0.png')
    width, height = img.size
    new_height = 320
    new_width = int( new_height*  width/height)
    img = ImageTk.PhotoImage(img.resize((new_width, new_height), Image.LANCZOS))

    img_label.config(image=img)
    img_label.image = img
    img_label.place(x=-170,y=0)

    root.mainloop()
'''
[]jump to time
'''