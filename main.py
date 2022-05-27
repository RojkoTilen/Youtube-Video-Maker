from os import walk
from color_matcher import ColorMatcher
from color_matcher.io_handler import load_img_file, save_img_file, FILE_EXTS
from color_matcher.normalizer import Normalizer
from PIL import Image
import os
import time
from moviepy.editor import *
import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
from vlog_channel import setter as Vlog_Setter
from vlog_channel import upload_video as Vlog_Upload



def get_immediate_subdirectories_wpath(a_dir):
    c = [f.path for f in os.scandir(a_dir) if f.is_dir()]
    return c


def get_channel_paths(a_dir):
    c = [f.path for f in os.scandir(a_dir) if f.is_dir()]
    b = []
    for i in range(0, len(c)):
        if "assets" in c[i]:
            b.append(c[i])
    return b


def get_list_of_file_names(dir_with_path):
    f = []
    file_dict = {}
    file_dict["dir"] = dir_with_path + "\\"
    for (dirpath, dirnames, filenames) in walk(dir_with_path):
        f.extend(filenames)
        break
    for name in f:
        if "text" in name:
            file_name = dir_with_path + "\\" + name
            file_dict["text"] = file_name
        elif "ref" in name:
            file_name = dir_with_path + "\\" + name
            file_dict["reference"] = file_name
        elif ".jpg" in name:
            file_name = dir_with_path + "\\" + name
            file_dict["background"] = file_name
        elif ".mp3" in name:
            file_name = dir_with_path + "\\" + name
            file_dict["music"] = file_name
    return file_dict


def make_thumbnail(file_dir_dict):
    #colour correct
    img_ref = load_img_file(file_dir_dict["reference"])
    img_src = load_img_file(file_dir_dict["background"])
    obj = ColorMatcher(src=img_src, ref=img_ref, method='mkl')
    img_res = obj.main()
    img_res = Normalizer(img_res).uint8_norm()
    output_filename = file_dir_dict['dir'] + 'thumbnail_graded.png'
    save_img_file(img_res, output_filename)
    #make thumbnail
    basewidth = 1920
    img = Image.open(output_filename)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    output_resized = file_dir_dict['dir'] + 'thumbnail_sized.jpg'
    img.save(output_resized)
    background = Image.open(output_resized)
    text_overlay_path = file_dir_dict['dir'] + "text.png"
    foreground = Image.open(text_overlay_path)
    background.paste(foreground, (0, 0), foreground)
    thumbnail_path = file_dir_dict['dir'] + "thumbnail.jpg"
    background.save(thumbnail_path)


def make_youtube_n_desc_tags(full_file_name):

    upload_date_time = datetime.datetime(2022, 2, 14, 17, 0, 0).isoformat() + '.000Z'

    splt_char = "\\"
    temp = full_file_name.split(splt_char)
    res = splt_char.join(temp[6:])

    splt_char = "."
    temp = res.split(splt_char)
    youtube_name = splt_char.join(temp[:1])
    youtube_name_for_tags = youtube_name.replace("(", "")
    youtube_name_for_tags = youtube_name_for_tags.replace(")", "")

    split_tags = youtube_name_for_tags.lower().split()
    print(split_tags)

    tags_1 = [youtube_name_for_tags.lower()]
    tags_2 = ["vlog no copyright music",
              "no copyright",
              "vlog",
              "vlog no copyright",
              "no copyright vlog",
              "music vlog no copyright",
              "no copyright vlog music",
              "no copyright music vlog",
              "vlogging music",
              "vlogging",
              "vlogger",
              "vlogger music",
              "free music",
              "music free",
              "music vlog",
              "vlog music",
              "background music",
              "music background"]

    tags = split_tags+tags_1+tags_2
    print(tags)


    youtube_description = """
Best vlog no copyright music that is non copyrighted so you can use it in your youtube videos.

Get it here:


#NoCopyrightMusic #VlogMusic #VlogNoCopyrightMusic
    """

    request_body = {
        'snippet': {
            'categoryI': 10,
            'title': youtube_name,
            'description': youtube_description,
            'tags': tags
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': upload_date_time,
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': True
    }

    return request_body


def make_video(file_dir_dict):

    print("make video")
    audio = AudioFileClip(file_dir_dict["music"])
    thumbnail_path = file_dir_dict['dir'] + "thumbnail.jpg"
    clip = ImageClip(thumbnail_path).set_duration(audio.duration)
    clip = clip.set_audio(audio)
    render_path = file_dir_dict["dir"] + "render.mp4"
    clip.write_videofile(render_path, fps=30)


if __name__ == "__main__":

    channel_paths = get_channel_paths("C:\\Ony Music Bots\\youtubebot\\sub_music_channels")
    print(channel_paths)

    dir_with_path = get_immediate_subdirectories_wpath("C:\\Ony Music Bots\\youtubebot\\sub_music_channels\\vlog_channel_assets")
    print(dir_with_path)

    Vlog_Setter("C:\\Ony Music Bots\\youtubebot\\sub_music_channels\\vlog_channel_assets\\aritmo_cred.json")

    i = 1
    for director in dir_with_path:
        file_dir_dict = get_list_of_file_names(director)
        print(file_dir_dict)
        date = datetime.date.today() + datetime.timedelta(days=i)
        formated_date = date.isoformat() + 'T17:00:00.000Z'
        print(formated_date)

        make_thumbnail(file_dir_dict)

        make_video(file_dir_dict)

        youtube_request_body = make_youtube_n_desc_tags(file_dir_dict["background"])
        print(youtube_request_body)
        Vlog_Upload(youtube_request_body, file_dir_dict["dir"])
        i = i+1





