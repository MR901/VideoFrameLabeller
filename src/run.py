
## Configs
import pyglet
import os, time
# pyglet.lib.load_library('avbin')
# pyglet.have_avbin=True

## to solve this error
# errror: WAVEFormatException: AVbin is required to decode compressed media
# http://avbin.github.io/AVbin/Download.html

config_di = {
    'input_vid_path': '../data/input/sample_video.mp4',
    'saving_dir': '../data/output/',
    'save_every_nth_frame': 5,
}

## Internal Variable
input_path = config_di['input_vid_path']
frame_counter = 0
default_category = 'undefined'
category = default_category


## Check File Location
if os.path.exists(input_path) is False:
    raise Exception(f'File is not present at the location: {input_path}')

## Check Extension
vid_formats = ['mov', 'avi', 'mp4', 'mpg', 'mpeg', 'm4v', 'wmv', 'mkv']  # acceptable video suffixes
ext = input_path.split('.')[-1].lower()
if ext not in vid_formats:
    raise Exception(f'This file format "{ext}" is not supported.')

    
## Initializing 
# https://stackoverflow.com/questions/4986662/taking-a-screenshot-with-pyglet-fixd

source = pyglet.media.load(input_path)
fmt = source.video_format
window = pyglet.window.Window(width=fmt.width, height=fmt.height, fullscreen=False, resizable=True, caption='Video')
window.set_mouse_visible(False)
player = pyglet.media.Player()
player.queue(source)
time.sleep(5)
player.play()

'''
width, height, title = 500, 500, 'Player Window'
window= pyglet.window.Window(width, height, title)
# window= pyglet.window.Window()
player = pyglet.media.Player()
source = pyglet.media.StreamingSource()
MediaLoad = pyglet.media.load(input_path)
player.queue(MediaLoad)
player.play()
'''



def generate_frame_name(config, prefix=None, frame_counter=None, category=None):
    ''' 
    Input:
        config_dict: { 'input_vid_path': <>, 'saving_dir':<> }
        saving_dir: '../data/'
        prefix: 'vid_' # will contain the path in this
        frame_counter: 12
        category: 'SheetThrow'
        
    '''
    ## generate file name
    prefix = '' if prefix is None else str(prefix)
    frame_cnt = '' if frame_counter is None else '_fr'+format(frame_counter, '06d') 
    ts_val = '_ts'+ str(round(player.time,3))
    category = default_category if category is None else str(category).lower()
    saving_dir= config['saving_dir']
    vid_name = '.'.join(config['input_vid_path'].split('/')[-1].split('.')[:-1])
    
    if 'screenshot' in prefix.lower():
        saving_path = f'{saving_dir}{vid_name}/Screenshots/{prefix}{vid_name}{frame_cnt}{ts_val}_cls{category}.png'
    else:
        saving_path = f'{saving_dir}{vid_name}/{category}/{prefix}{vid_name}{frame_cnt}{ts_val}_cls{category}.png'
    
    ## creeating dir if it doeesn't exist
    if os.path.exists('/'.join(saving_path.split('/')[:-1])) is False:
        os.makedirs('/'.join(saving_path.split('/')[:-1]))
        
    return saving_path



# fps_display = pyglet.clock.ClockDisplay(
#     format='%(fps).1f',
#     color=(0.5, 0.5, 0.5, 1)
#     )

@window.event
def on_draw():
    '''  '''    
    ## getting variables
    global frame_counter, config_di, category
    frame_counter += 1
    
    if frame_counter%25==0:
        print(f'---| Current category: {category}\t Current Frame No.: {frame_counter}')
        
    ## skip if not nth multiple
    if frame_counter % config_di['save_every_nth_frame'] != 0: return 

    ## adding text on frame
    # label = pyglet.text.Label(f'{frame_counter} {category}',
    #                       font_name='Times New Roman',
    #                       font_size=36,
    #                       x=window.width//2, y=window.height//2,
    #                       anchor_x='center', anchor_y='center')
    # label.draw()
    # fps_display.draw()
    
    ## if continued then savee frame
    saving_path = generate_frame_name(
        config_di, 
        prefix=None, 
        frame_counter=frame_counter, 
        category=category
    )
    
    ## saving image
    pyglet.image.get_buffer_manager().get_color_buffer().save(saving_path)
    
    ## Clear the window 
    # window.clear() -- causes the video to pixelate
    if player.source and player.source.video_format:
        player.get_texture().blit(0,0,width=window.width, height=window.height)

@window.event
def on_key_press(symbol, modifier):
    ''' 
    Every nth frame will be saved 
    
    W : Pause and Add Label
    S : Just Pause the Video
    D : Resume with the same / Current Label
    A : Stop the Label and replace with default label
    
    Q : Take Screenshot of the current Frame
    '''
    global category, default_category
    
    if symbol==pyglet.window.key.W: 
        print('Video Paused and label will be added.')
        player.pause()
        category = input('Enter category name: ')
    elif symbol==pyglet.window.key.S: 
        print('Label under current stopped.')
        category = default_category
        player.pause()
    elif symbol==pyglet.window.key.D:
        print('Video Resumed.')
        player.play()
    elif symbol==pyglet.window.key.A:
        print('Video Paused.')
        player.pause()
    elif symbol==pyglet.window.key.ESCAPE: #[Esc]
        print('Exiting...')
        time.sleep(3)
        window.close()
        exit()
    
    elif symbol==pyglet.window.key.M:
        ## TAKE SCREENSHOT
        saving_name = generate_frame_name(config_di, prefix='Screenshot', frame_counter=None, category=None)
        pyglet.image.get_buffer_manager().get_color_buffer().save(saving_name)


print(''' 
    Every "{}" th frame  will be saved 
    
    W : Pause + Add Label
    S : Stop Category Label
    D : Resume Current Label
    A : Pause
    
    M : Take Screenshot of the current Frame
    '''.format(config_di['save_every_nth_frame']))
# pyglet.clock.schedule(update) # cause a timed event as fast as you can!
pyglet.app.run()



'''
import pyglet
from pyglet.gl import *
from threading import *

# REQUIRES: AVBin
#pyglet.options['audio'] = ('alsa', 'openal', 'silent')
key = pyglet.window.key

class main(pyglet.window.Window):
    def __init__ (self):
        super(main, self).__init__(800, 800, fullscreen = False)
        self.x, self.y = 0, 0

        self.player = pyglet.media.Player()
        self.player.queue(pyglet.media.load("video.mp4"))
        self.sprites = {'video' : None}

        self.alive = 1

    def on_draw(self):
        self.render()

    def on_close(self):
        self.alive = 0

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == 65307: # [ESC]
            self.alive = 0
        elif symbol == key.LCTRL:
            self.player.play()

    def render(self):
        self.clear()

        if self.player.playing:
            if self.sprites['video'] is None:
                texture = self.player.get_texture()
                if texture:
                    self.sprites['video'] = pyglet.sprite.Sprite(texture)
            else:
                self.sprites['video'].draw()

        self.flip()

    def run(self):
        while self.alive == 1:
            self.render()

            # -----------> This is key <----------
            # This is what replaces pyglet.app.run()
            # but is required for the GUI to not freeze
            #
            event = self.dispatch_events()

x = main()
x.run()
'''
