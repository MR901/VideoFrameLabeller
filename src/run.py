
## Configs
import pyglet
import os
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
window= pyglet.window.Window()
player = pyglet.media.Player()
source = pyglet.media.StreamingSource()
MediaLoad = pyglet.media.load(input_path)
player.queue(MediaLoad)
player.play()


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
    category = default_category if category is None else '_cls'+str(category)
    saving_dir= config['saving_dir']
    vid_name = '.'.join(config['input_vid_path'].split('/')[-1].split('.')[:-1])
    
    if 'screenshot' in prefix.lower():
        saving_path = f'{saving_dir}{vid_name}/Screenshots/{prefix}{frame_cnt}{ts_val}{category}.png'
    else:
        saving_path = f'{saving_dir}{vid_name}/{category}/{prefix}{frame_cnt}{ts_val}{category}.png'
    
    ## creeating dir if it doeesn't exist
    if os.path.exists('/'.join(saving_path.split('/')[:-1])) is False:
        os.makedirs('/'.join(saving_path.split('/')[:-1]))
        
    return saving_path



@window.event
def on_draw():
    ''' 
    '''
    window.clear()
    
    ## getting variables
    global frame_counter, config_di, category
    frame_counter += 1
    
    ## adding text on frame
    label = pyglet.text.Label(f'{frame_counter} {category}',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')
    label.draw()
    
    ## skip if not nth multiple
    if frame_counter % config_di['save_every_nth_frame'] != 0: return 
    
    ## if continued then savee frame
    saving_path = generate_frame_name(
        config_di, 
        prefix=None, 
        frame_counter=frame_counter, 
        category=category
    )
    
    ## saving image
    pyglet.image.get_buffer_manager().get_color_buffer().save(saving_path)
    
    if player.source and player.source.video_format:
        player.get_texture().blit(250,250)



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
        ## pause and label
        player.pause()
        category = input('Enter category name: ')
    elif symbol==pyglet.window.key.S: 
        ## pause and label
        player.pause()
    elif symbol==pyglet.window.key.D:
        ## resume
        player.play() 
    elif symbol==pyglet.window.key.A:
        ## stop
        category = default_category
    
    elif symbol==pyglet.window.key.Q:
        ## TAKE SCREENSHOT
        saving_name = generate_frame_name(config, prefix='Screenshot', frame_counter=None, category=None)
        pyglet.image.get_buffer_manager().get_color_buffer().save(saving_path)




print(    ''' 
    Every "{}" th frame  will be saved 
    
    W : Pause and Add Label
    S : Just Pause the Video
    D : Resume with the same / Current Label
    A : Stop the Label and replace with default label
    
    Q : Take Screenshot of the current Frame
    '''.format(config_di['save_every_nth_frame']))
# pyglet.clock.schedule(update) # cause a timed event as fast as you can!
pyglet.app.run()

