import cv2, pixelsort, numpy, os, time, random
#import colorama
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from dotenv import load_dotenv, dotenv_values
start_time=time.time()
ver=1.2

#todo: colorama + name checker

#get variables from .env file
config = dotenv_values ("env.env")

input_txt_path = config['input_txt_path']
input_img_dataset = config['input_img_dataset']
output_path = config['output_path']
output_name= config['output_name']
video_height= int(config['video_height'])
video_width= int(config['video_width'])
overlay_color=(int(config['overlay_color_R']),int(config['overlay_color_G']),int(config['overlay_color_B']))
contrast_value= float(config['contrast_value'])
noise= int(config['noise'])
text_color = (int(config['text_color_R']), int(config['text_color_G']), int(config['text_color_B']))
text_size = int (config['text_size'])
text_left_align = int (config['text_left_align'])
text_top_align = int (config['text_top_align'])
text_font = config['text_font']
line_x=random.randint(int(config['line_x_rnd_min']), int(config['line_x_rnd_max']))
line_y=random.randint(int(config['line_y_rnd_min']), int(config['line_y_rnd_max']))
line_w=random.randint(int(config['line_w_rnd_min']),int(config['line_w_rnd_max']))
line_color=(int(config['line_color_R']),int(config['line_color_G']),int(config['line_color_B']))
lower_threshold= float(config['lower_threshold'])
l=int(config['l'])
add_noise=bool(config['add_noise'])
text=bool(config['text'])
lines=bool(config['lines'])
add_overlay=bool(config['add_overlay'])


ascii_art= ("""

    ██▀███   ▄▄▄       ███▄    █ ▓█████▄  ▒█████   ███▄ ▄███▓   
   ▓██ ▒ ██▒▒████▄     ██ ▀█   █ ▒██▀ ██▌▒██▒  ██▒▓██▒▀█▀ ██▒   
   ▓██ ░▄█ ▒▒██  ▀█▄  ▓██  ▀█ ██▒░██   █▌▒██░  ██▒▓██    ▓██░  
   ▒██▀▀█▄  ░██▄▄▄▄██ ▓██▒  ▐▌██▒░▓█▄   ▌▒██   ██░▒██    ▒██   
   ░██▓ ▒██▒ ▓█   ▓██▒▒██░   ▓██░░▒████▓ ░ ████▓▒░▒██▒   ░██▒   
   ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ▒░   ▒ ▒  ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒░   ░  ░   
     ░▒ ░ ▒░  ▒   ▒▒ ░░ ░░   ░ ▒░ ░ ▒  ▒   ░ ▒ ▒░ ░  ░      ░   
     ░░   ░   ░   ▒      ░   ░ ░  ░ ░  ░ ░ ░ ░ ▒  ░      ░     
      ░           ░  ░         ░    ░        ░ ░         ░     

       ▄████  ██▓     ██▓▄▄▄█████▓ ▄████▄   ██░ ██ ▓█████  ██▀███  
      ██▒ ▀█▒▓██▒    ▓██▒▓  ██▒ ▓▒▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▓██ ▒ ██▒
     ▒██░▄▄▄░▒██░    ▒██▒▒ ▓██░ ▒░▒▓█    ▄ ▒██▀▀██░▒███   ▓██ ░▄█ ▒
     ░▓█  ██▓▒██░    ░██░░ ▓██▓ ░ ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ▒██▀▀█▄  
    ░▒▓███▀▒░██████▒░██░  ▒██▒ ░ ▒ ▓███▀ ░░▓█▒░██▓░▒████▒░██▓ ▒██▒
     ░▒   ▒ ░ ▒░▓  ░░▓    ▒ ░░   ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒▓ ░▒▓░
      ░   ░ ░ ░ ▒  ░ ▒ ░    ░      ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░▒ ░ ▒░
      ░   ░   ░ ░    ▒ ░  ░      ░         ░  ░░ ░   ░     ░░   ░ 
          ░     ░  ░ ░           ░ ░       ░  ░  ░   ░  ░   ░     

   ┌─┐┌─┐┌┐┌┌─┐┬─┐┌─┐┌┬┐┌─┐  ┌─┐┬  ┬┌┬┐┌─┐┬ ┬┌─┐┌┬┐  ┬  ┬┬┌┬┐┌─┐┌─┐
   │ ┬├┤ │││├┤ ├┬┘├─┤ │ ├┤   │ ┬│  │ │ │  ├─┤├┤  ││  └┐┌┘│ ││├┤ │ │
   └─┘└─┘┘└┘└─┘┴└─┴ ┴ ┴ └─┘  └─┘┴─┘┴ ┴ └─┘┴ ┴└─┘─┴┘   └┘ ┴─┴┘└─┘└─┘
   ┌─┐┬─┐┌─┐┌┬┐  ┬─┐┌─┐┌┐┌┌┬┐┌─┐┌┬┐  ┌─┐┬┌─┐┌┬┐┬ ┬┬─┐┌─┐┌─┐  
   ├┤ ├┬┘│ ││││  ├┬┘├─┤│││ │││ ││││  ├─┘││   │ │ │├┬┘├┤ └─┐  
   └  ┴└─└─┘┴ ┴  ┴└─┴ ┴┘└┘─┴┘└─┘┴ ┴  ┴  ┴└─┘ ┴ └─┘┴└─└─┘└─┘  

""")

class utils:
    def clear():
        """clear system console"""
        os.system('cls' if os.name=='nt' else 'clear')

    def interface(ascii_art, ver):
        """ print ascii art, version number, user instructions"""
        print(ascii_art)
        print("      made by e-garbage            licence GPLv3              version: "+f"{ver}"+"\n\n")
    
    def check_folder(folder):
        if not os.path.exists(folder):
            os.mkdir(folder)
        return folder 

    def read_input_text (path):
        with open(path) as f:
            lines = f.readlines()
        return lines
  
    def pick_random(path):
        files= os.listdir(path)
        rnd_file= random.choice(files)
        rnd_file= os.path.join(path + "/" + rnd_file)
        return rnd_file

    def name_generator():
        1+1
    
    def validation():
        valid = input("[?] Do you to continue Y/N ? ").lower()
        return valid
    def truncate (n, decimals=0):
        multiplier = 10**decimals
        return int (n * multiplier)/multiplier

class frame:
    def pixelsort_frame (image, lower_threshold, overlay, height, width, contrast, upper_threshold=0.8, angle=90, randomness=20, noise=6, add_noise=True, add_overlay=True):

        #pixelsort bg image
        img= pixelsort.pixelsort(image=image, randomness=randomness, lower_threshold=lower_threshold, upper_threshold= upper_threshold, angle= angle)
        size=(width, height)
        print("    -- Pixel sorting done")
        #resize (squeeze) bg image to desired fixe image size
        img= img.resize(size, Image.Resampling.LANCZOS)
        print("    -- Resizing done")
        #add rgb noise
        if add_noise==True:
            for i in range (round(img.size[0]*img.size[1]/noise)):
                img.putpixel(
                    (random.randint(0, img.size[0]-1), random.randint(0, img.size[1]-1)),
                    (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                )
            print("    -- Adding noise done")
        else:
            print("    -- Skipping noise")
        #blend bg image and overlay
        if add_overlay==True:
            frame_out= Image.blend(img, overlay, 0.65)
            print("    -- Blending overlay done")
        else:
            frame_out=img
            print("    -- Skipping overlay")
        #adjust contrast
        scale_value= contrast
        frame_out = ImageEnhance.Contrast(frame_out).enhance(scale_value)
        print("    -- Contrasting done")
        return frame_out

    def add_text (image, text, color1, color2, font, size, left_align, top_align):

        im= ImageDraw.Draw(image)
        text_font = ImageFont.truetype(font, size)
        a=1
        for i in text: 
            im.multiline_text((left_align+8,top_align+8+a), i, font=text_font, fill=(color1))
            im.multiline_text((left_align,top_align+a), i, font=text_font, fill=(color2))
            a= round(a+size*1.25)
        return image

    def add_lines(image, horiz_pos, vert_pos, color, width):

        im=ImageDraw.Draw(image)
        line_1_coord=[(horiz_pos, 0), (horiz_pos, 1920)]
        line_2_coord=[(0, vert_pos), (1080, vert_pos)]
        im.line(line_1_coord, fill=color, width=width)
        im.line(line_2_coord, fill=color, width=width)
        return image

    def save_frame(frame, output_folder, frame_number):

        frame_number=str(frame_number)
        frame_name= os.path.join (output_folder + "/" + frame_number + ".png")
        frame.save(frame_name, format="PNG")

class video:

    def save_video(video):
        video.release()
    

if __name__ == "__main__":

    utils.check_folder(output_path)
    temp_path = 'temp/'
    utils.check_folder(temp_path)
    utils.clear()
    utils.interface(ascii_art ,ver)
    print("[-] Choosing a random image in the following dataset: " + f"{input_img_dataset}")
    base_img = utils.pick_random(input_img_dataset)
    print ("[+] Base image is: "+f"{base_img}")
    print ("[+] The following parameters will be used: ")
    print ("    -- Video dimensions (WxH): "+f"{video_width}"+"x"+f"{video_height}")
    print ("    -- Add Noise: "+f"{add_noise}")
    print ("    -- Add Overlay Color: "+f"{add_overlay}")
    print ("    -- Lines: "+f"{lines}")
    print ("    -- Text: "+f"{text}")
    print ("    -- Saving video as "+f"{output_name}"+".mp4")
    print ("[!] You can change this parameters by editing the '.env' file ")
    valid = utils.validation()

    while valid not in ('n', 'no'):

        if valid in('y', 'yes'):
            im = Image.open (base_img)
            im= im.convert ("RGBA")
            overlay_size=(video_width,video_height)
            overlay= Image.new("RGBA", overlay_size, overlay_color)
            text=utils.read_input_text(input_txt_path)
            file_name=os.path.join(output_path+"/"+output_name+'.mp4')
            vid = cv2.VideoWriter(file_name, cv2.VideoWriter_fourcc(*'mp4v'),24.0, (video_width, video_height))
            frame_end=0
            frame_start=0
            for i in range (0, l):
                utils.clear()
                utils.interface(ascii_art ,ver)
                print ("[+] Base image is: "+f"{base_img}")
                frame_time=utils.truncate((frame_end - frame_start), 3)
                frame_start=time.time()
                print ("[-] Last frame generated in "+ f"{frame_time}"+" sec")
                print ("[+] Generating frame " + f"{i}"+"/"+f"{l}")
                fr = frame.pixelsort_frame(im, (numpy.sin(i/1000)+lower_threshold), overlay, video_height, video_width, contrast_value, randomness=20, angle=(90+i), noise=noise, add_noise=add_noise, add_overlay=add_overlay)
                if lines==True:
                    fr = frame.add_lines (fr, line_x, line_y, line_color, line_w)
                else:
                    fr=fr
                if text ==True:
                    fr = frame.add_text (fr,text, overlay_color, text_color, text_font, text_size, text_left_align, text_top_align )
                else:
                    fr=fr
                vid.write(cv2.cvtColor(numpy.array(fr), cv2.COLOR_RGB2BGR))
                frame_end=time.time()


            vid=video.save_video(vid)
            print("--- %s sec ---" % (time.time() - start_time))
            quit()

        else:
            print("[!] Invalid input")
        valid= utils.validation()
    print("[-] Quit without error, user interruption")
    quit()
