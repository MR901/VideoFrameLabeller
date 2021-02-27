

import pyglet
import os


## Configs
parent_dir = ""  # change this as required on local system
vidPath = '' # change video you wanted to check
vid = vidPath.split(".")[0]
path_root = os.path.join(parent_dir,vid)
val_name = ''


## code Start
if os.path.isdir(path_root) == False:  
    os.mkdir(path_root)

path = ''
window= pyglet.window.Window()
player = pyglet.media.Player()
source = pyglet.media.StreamingSource()
MediaLoad = pyglet.media.load(vidPath)
player.queue(MediaLoad)
player.play()
i = 1
flag = False

@window.event
def on_draw():
    global i
    global flag
    window.clear()
    if flag == True:
        global i
        global path
        global vid
        global val_name
        print(path)
        time_check = (player.time)
        time_check = round(time_check,3)
        pyglet.image.get_buffer_manager().get_color_buffer().save(path+'/{}_{}_{}_{}.png'.format(vid,val_name,time_check,i))
        i = i+1
    else:
        i =1
        # print(i)
    if player.source and player.source.video_format:
        player.get_texture().blit(250,250)


@window.event
def on_key_press(symbol, modifier):
    def dcreenshot():
        print("aman")
  
    if symbol == pyglet.window.key.P: 
        player.pause()
        global val_name
        val = input("Enter folder name: ") # format should be something like throw_1 , throw_2
        val_name = val.split("_")[0] 
        directory = val
        global flag 
        global path
        global path_root
        flag = True
        path = os.path.join(path_root, directory) 
        os.mkdir(path)

    if symbol == pyglet.window.key.R:
        player.play() 

    if symbol == pyglet.window.key.S:
        # global flag 
        flag =False 


pyglet.app.run()
