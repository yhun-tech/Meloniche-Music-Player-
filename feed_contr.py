import customtkinter
import customtkinter as ctk
import pygame
from tkinter import filedialog as fd
from PIL import Image

from config import *

import mutagen
from mutagen.mp3 import MP3
import os
import time
import mutagen









sidebar_width = 200
content_frame_width = 700
aside_width = 400
btns = 20,20





def default_aside_right(self):

    # Initialize pygame mixer
    pygame.mixer.init()

    self.is_playing = False
    self.current_music_file = None
    self.music_length = 0
    self.slider_dragging = False
    self.just_seeked = False
    self.current_position = 0
    self.seek_playback_offset = 0



    for widget in self.aside_right.winfo_children():
        widget.destroy()


    # Frames
    self.asr_top_nav = ctk.CTkFrame(self.aside_right, width=aside_width, height=50, fg_color=backup_ppl_2)
    self.asr_username = ctk.CTkLabel(self.asr_top_nav,text="John Doe",text_color=w_f5,font=(fn_PM,13))
    self.asr_userprofile_image = ctk.CTkImage(light_image=Image.open("Images/User Profile.png"),
                                              dark_image=Image.open("Images/User Profile.png"),
                                              size=(35,35))
    self.asr_userprofile_holder = ctk.CTkLabel(self.asr_top_nav, text=" ",image=self.asr_userprofile_image,
                                     font=(fn_PM, 12))


    self.asr_image_track_div = ctk.CTkFrame(self.aside_right, width=aside_width, height=250, fg_color=backup_ppl_2)

    self.asr_track_image = ctk.CTkImage(light_image=Image.open("Images/MELONICHE PLAYER LOGO.png"),
                                        dark_image=Image.open("Images/MELONICHE PLAYER LOGO.png"),
                                        size=(250, 200))


    self.asr_aside_image_holder = ctk.CTkButton(self.asr_image_track_div,image=self.asr_track_image,
                                                text="",width=460,height=200,
                                                fg_color=backup_ppl_2,hover_color=backup_ppl_2)

    self.music_title_lbl_frame = ctk.CTkFrame(self.asr_image_track_div,fg_color=backup_ppl_2,height=50,width=360)
    self.music_title_lbl = ctk.CTkLabel(self.music_title_lbl_frame,text="",font=(fn_PM,12))

    self.asr_music_player_div = ctk.CTkFrame(self.aside_right, width=aside_width, height=100, fg_color=tlr_dark)
    self.asr_music_control_div = ctk.CTkFrame(self.asr_music_player_div, fg_color=tlr_dark, width=375, height=100)

    self.asr_music_progress_div = ctk.CTkFrame(self.asr_music_control_div, fg_color=tlr_dark, width=375, height=50)

    self.asr_music_button_div = ctk.CTkFrame(self.asr_music_control_div, fg_color=tlr_dark, width=375, height=50)


    # Load images
    self.prev_image = ctk.CTkImage(light_image=Image.open("Images/skip-back-fill.png"),
                                   dark_image=Image.open("Images/skip-back-fill.png"), size=btns)
    self.play_image = ctk.CTkImage(light_image=Image.open("Images/play-large-fill.png"),
                                   dark_image=Image.open("Images/play-large-fill.png"), size=btns)
    self.pause_image = ctk.CTkImage(light_image=Image.open("Images/pause-large-fill .png"),
                                   dark_image=Image.open("Images/pause-large-fill .png"), size=btns)
    self.next_image = ctk.CTkImage(light_image=Image.open("Images/skip-forward-fill.png"),
                                   dark_image=Image.open("Images/skip-forward-fill.png"), size=btns)




    # FUNCTIONS =========== =========== =========== =========== ===========
    def set_volume(value):
        volume = float(value) / 100
        volume_val = int(self.my_volume.get() * 1)
        pygame.mixer.music.set_volume(volume)
        self.volume_lbl.configure(text=volume_val)


    # SLIDER ============ =============== ============== ================== ===================
    self.progress_slider = ctk.CTkSlider(
        self.asr_music_progress_div,
        to=100,
        command=lambda value: on_slider_change(self, value),
        fg_color=tlr_purple_1,
        state="disable"
    )


    self.progress_label = ctk.CTkLabel(self.asr_music_progress_div, text="--:-- / --:--", font=(fn_PM, 12))

    self.progress_slider.bind("<Button-1>", on_slider_press)
    self.progress_slider.bind("<ButtonRelease-1>", lambda event: on_slider_release(self, event))

    # Start the periodic slider update
    update_slider(self)

    # BUTTONS
    self.prev_btn = ctk.CTkButton(self.asr_music_button_div, text="", image=self.prev_image, width=20,
                                  fg_color=tlr_dark, hover_color=tlr_purple_4)
    self.play_pause_btn = ctk.CTkButton(self.asr_music_button_div, text="", image=self.play_image, width=20,
                                        fg_color=tlr_dark, hover_color=tlr_purple_4,
                                        command=lambda:play_pause_music(self))
    self.next_btn = ctk.CTkButton(self.asr_music_button_div, text="", image=self.next_image, width=20,
                                  fg_color=tlr_dark, hover_color=tlr_purple_4)

    self.asr_music_vol_div = ctk.CTkFrame(self.asr_music_player_div, fg_color=tlr_dark, height=100)
    self.my_volume = ctk.CTkSlider(self.asr_music_vol_div, from_=0, to=100, orientation="vertical", height=80,
                                   command=set_volume)
    self.my_volume.set(70)
    self.volume_lbl = ctk.CTkLabel(self.asr_music_vol_div, text="", font=(fn_PM, 12))

    self.asr_suggest_div = ctk.CTkFrame(self.aside_right, width=aside_width, fg_color=tlr_dark,height=300)
    self.asr_suggest_list_title_frame = ctk.CTkFrame(self.asr_suggest_div,height=40,fg_color=tlr_dark)
    self.asr_suggest_div_title = ctk.CTkLabel(self.asr_suggest_list_title_frame,text="SUGGESTIONS",
                                              text_color=w_f5,font=(fn_PM,17))
    self.asr_suggest_list_sframe = ctk.CTkScrollableFrame(self.asr_suggest_div,fg_color=backup_ppl_2,
                                                          scrollbar_button_color=backup_ppl_2,
                                                          scrollbar_button_hover_color=tlr_purple_1)


    # SUGGESTIONs MUSIC  === === === === === === === === === === === === === === === === === ===  === ===

    # DOUBLE TAKE
    self.disas_list_wrapper = ctk.CTkFrame(self.asr_suggest_list_sframe, height=50, width=655,
                                            corner_radius=20, fg_color=backup_ppl_2)

    self.disas_list_image = ctk.CTkImage(light_image=Image.open("Albums/Selfish Machine.png"),
                                          dark_image=Image.open("Albums/Selfish Machine.png"),
                                          size=(50, 50))
    self.disas_list_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Selfish Machine.png"),
                                          dark_image=Image.open("Albums/Selfish Machine.png"),
                                          size=(220, 200))

    self.disas_list_holder = ctk.CTkButton(self.disas_list_wrapper, text=f"3:26",
                                            command=lambda: play_music(self,
                                                                       "Musics/Pierce The Veil _Disasterology.mp3",
                                                                       "Pierce The Veil - Disasterology",
                                                                       self.disas_list_image_pl),
                                            text_color="grey",
                                            font=(fn_PR, 12),
                                            fg_color=backup_ppl_2, hover_color=backup_ppl_1,
                                            corner_radius=20, width=655, height=50)
    self.disas_image_holder = ctk.CTkButton(self.disas_list_holder, text="",
                                            command=lambda: play_music(self,
                                                                       "Musics/Pierce The Veil _Disasterology.mp3",
                                                                       "Pierce The Veil - Disasterology",
                                                                       self.disas_list_image_pl),
                                             image=self.disas_list_image,
                                             width=50,
                                            fg_color=backup_ppl_2, hover_color=backup_ppl_1)
    self.disas_list_info_frame = ctk.CTkButton(self.disas_list_holder, text="",
                                               command=lambda: play_music(self,
                                                                          "Musics/Pierce The Veil _Disasterology.mp3",
                                                                          "Pierce The Veil - Disasterology",
                                                                          self.disas_list_image_pl),
                                                width=150, height=50,fg_color=backup_ppl_2, hover_color=backup_ppl_1)
    self.disas_list_author = ctk.CTkLabel(self.disas_list_info_frame, text="Pierce The Veil",
                                           text_color=w_f5, font=(fn_PM, 15))
    self.disas_list_title = ctk.CTkLabel(self.disas_list_info_frame, text="Disasterology",
                                          text_color="grey",
                                          font=(fn_PR, 12))



    self.disas_list_wrapper.pack_propagate(False)
    self.disas_list_holder.pack_propagate(False)
    self.disas_list_info_frame.pack_propagate(False)
    self.disas_list_wrapper.grid(padx=10, pady=10)
    self.disas_list_holder.pack(fill="both", expand=True)
    self.disas_image_holder.pack(anchor="w", side=ctk.LEFT)
    self.disas_list_info_frame.pack(anchor="w", side=ctk.LEFT)
    self.disas_list_author.pack(anchor="w")
    self.disas_list_title.pack(anchor="w")




    # GOOD FOR U
    self.gforu_list_wrapper = ctk.CTkFrame(self.asr_suggest_list_sframe, height=50, width=655,
                                            corner_radius=20, fg_color=backup_ppl_2)

    self.gforu_list_image = ctk.CTkImage(light_image=Image.open("Albums/Olivia Rodrigo.png"),
                                          dark_image=Image.open("Albums/Olivia Rodrigo.png"),
                                          size=(50, 50))
    self.gforu_list_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Olivia Rodrigo.png"),
                                             dark_image=Image.open("Albums/Olivia Rodrigo.png"),
                                             size=(220, 200))

    self.gforu_list_holder = ctk.CTkButton(self.gforu_list_wrapper, text=f"3:18",
                                            command=lambda: play_music(self,
                                                                       "Musics/Olivia Rodrigo - good 4 u.mp3",
                                                                       "Olivia Rodrigo - good 4 u",
                                                                       self.gforu_list_image_pl),
                                            text_color="grey",
                                            font=(fn_PR, 12),
                                            fg_color=backup_ppl_2, hover_color=backup_ppl_1,
                                            corner_radius=20, width=655, height=50)
    self.gforu_image_holder = ctk.CTkButton(self.gforu_list_holder, text="",
                                            command=lambda: play_music(self,
                                                                       "Musics/Olivia Rodrigo - good 4 u.mp3",
                                                                       "Olivia Rodrigo - good 4 u",
                                                                       self.gforu_list_image_pl),
                                             image=self.gforu_list_image ,
                                             width=50,
                                             fg_color=backup_ppl_2, hover_color=backup_ppl_1)
    self.gforu_list_info_frame = ctk.CTkButton(self.gforu_list_holder, text="",
                                               command=lambda: play_music(self,
                                                                          "Musics/Olivia Rodrigo - good 4 u.mp3",
                                                                          "Olivia Rodrigo - good 4 u",
                                                                          self.gforu_list_image_pl),
                                                width=150, height=50, hover_color=backup_ppl_1, fg_color=backup_ppl_2,
                                               )
    self.gforu_list_author = ctk.CTkLabel(self.gforu_list_info_frame, text="Olivia Rodrigo",
                                           text_color=w_f5, font=(fn_PM, 15))
    self.gforu_list_title = ctk.CTkLabel(self.gforu_list_info_frame, text="good 4 u",
                                          text_color="grey",
                                          font=(fn_PR, 12))

    self.gforu_list_wrapper.pack_propagate(False)
    self.gforu_list_holder.pack_propagate(False)
    self.gforu_list_info_frame.pack_propagate(False)
    self.gforu_list_wrapper.grid(padx=10, pady=10)
    self.gforu_list_holder.pack(fill="both", expand=True)
    self.gforu_image_holder.pack(anchor="w", side=ctk.LEFT)
    self.gforu_list_info_frame.pack(anchor="w", side=ctk.LEFT)
    self.gforu_list_author.pack(anchor="w")
    self.gforu_list_title.pack(anchor="w")


    # DOUBLE TAKE
    self.dbtake_list_wrapper = ctk.CTkFrame(self.asr_suggest_list_sframe, height=50, width=655,
                                            corner_radius=20, fg_color=backup_ppl_2)

    self.dbtake_list_image = ctk.CTkImage(light_image=Image.open("Albums/Double Take.png"),
                                          dark_image=Image.open("Albums/Double Take.png"),
                                          size=(50, 50))
    self.dbtake_list_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Double Take.png"),
                                             dark_image=Image.open("Albums/Double Take.png"),
                                             size=(220, 200))

    self.dbtake_list_holder = ctk.CTkButton(self.dbtake_list_wrapper, text=f"2:49",
                                            command=lambda: play_music(self,
                                                                       "Musics/Dhruv - double take.mp3",
                                                                       "Dhruv - Double Take",
                                                                       self.dbtake_list_image_pl),
                                            text_color="grey",
                                            font=(fn_PR, 12),
                                            fg_color=backup_ppl_2, hover_color=backup_ppl_1,
                                            corner_radius=20, width=655, height=50)
    self.dbtake_image_holder = ctk.CTkButton(self.dbtake_list_holder, text="",
                                             command=lambda: play_music(self,
                                                                        "Musics/Dhruv - double take.mp3",
                                                                        "Dhruv - Double Take",
                                                                        self.dbtake_list_image_pl),
                                             image=self.dbtake_list_image,
                                             width=50,
                                             fg_color=backup_ppl_2,hover_color=backup_ppl_1)
    self.dbtake_list_info_frame = ctk.CTkButton(self.dbtake_list_holder, text="",
                                                command=lambda: play_music(self,
                                                                           "Musics/Dhruv - double take.mp3",
                                                                           "Dhruv - Double Take",
                                                                           self.dbtake_list_image_pl),
                                                width=150, height=50, hover_color=backup_ppl_1, fg_color=backup_ppl_2)
    self.dbtake_list_author = ctk.CTkLabel(self.dbtake_list_info_frame, text="Dhruv",
                                           text_color=w_f5, font=(fn_PM, 15))
    self.dbtake_list_title = ctk.CTkLabel(self.dbtake_list_info_frame, text="Double Take",
                                          text_color="grey",
                                          font=(fn_PR, 12))

    self.dbtake_list_wrapper.pack_propagate(False)
    self.dbtake_list_holder.pack_propagate(False)
    self.dbtake_list_info_frame.pack_propagate(False)
    self.dbtake_list_wrapper.grid(padx=10, pady=10)
    self.dbtake_list_holder.pack(fill="both", expand=True)
    self.dbtake_image_holder.pack(anchor="w", side=ctk.LEFT)
    self.dbtake_list_info_frame.pack(anchor="w", side=ctk.LEFT)
    self.dbtake_list_author.pack(anchor="w")
    self.dbtake_list_title.pack(anchor="w")

    # END OF SUGGESTION MUSIC === === === === === === === === === === === === === === === === === ===








    # Packing
    self.asr_top_nav.pack_propagate(False)
    self.asr_top_nav.pack(padx=0, pady=(10, 10), fill="x")
    self.asr_userprofile_holder.pack(padx=(10,80),anchor="e",side=ctk.RIGHT)
    self.asr_username.pack(anchor="e",side=ctk.RIGHT)



    # IMAGE TRACK FRAME
    self.asr_image_track_div.pack(padx=0, pady=(10, 10), fill="x")
    self.asr_aside_image_holder.pack(pady=(10,5),padx=(0,50),fill="both", expand=True)
    self.music_title_lbl_frame.pack_propagate(False)
    self.music_title_lbl_frame.pack(fill="both",expand=True,padx=20,pady=10)
    self.music_title_lbl.pack(pady=(5,10),padx=(0,70))




    # CONTROLS AND PROGRESS FRAME
    self.asr_music_player_div.grid_propagate(False)
    self.asr_music_player_div.pack(padx=0, pady=(0, 10), fill="x")

    self.asr_music_control_div.grid_propagate(False)
    self.asr_music_control_div.grid(row=0, column=1)

    self.asr_music_progress_div.pack_propagate(False)
    self.asr_music_button_div.grid_propagate(False)

    self.asr_music_progress_div.pack(fill="x", expand=True)
    self.asr_music_button_div.pack(fill="x", expand=True)

    self.progress_slider.pack(fill="x", padx=10, pady=5)
    self.progress_slider.set(0)
    self.progress_label.pack()

    self.prev_btn.grid(row=0, column=1, pady=10, padx=(123, 5))
    self.play_pause_btn.grid(row=0, column=2, pady=10, padx=5)
    self.next_btn.grid(row=0, column=3, pady=10, padx=5)

    self.asr_music_vol_div.grid_propagate(False)
    self.asr_music_vol_div.grid(row=0, column=2)
    self.my_volume.grid(row=0, column=1, padx=30)
    self.volume_lbl.grid(row=2, column=1)




    # SONG LIST FRAME
    self.asr_suggest_div.pack_propagate(False)
    self.asr_suggest_list_title_frame.pack_propagate(False)
    self.asr_suggest_div.pack(fill="both", expand=True)

    self.asr_suggest_list_title_frame.pack(fill="x")
    self.asr_suggest_div_title.pack(anchor="w",pady=10)

    self.asr_suggest_list_sframe.pack(padx=(0,65),fill="both",expand=True)



slider_dragging = False
music_playing = False
music_length = 0


# Called when slider is pressed
def on_slider_press(event):
    global slider_dragging
    slider_dragging = True

# Called when slider is released
def on_slider_release(self, event):
    global slider_dragging
    slider_dragging = False
    update_music_position(self)

# Called when slider is moved
def on_slider_change(self, value):
    global slider_dragging
    global minutes,seconds

    # Always update the label text
    minutes = int(float(value) // 60)
    seconds = int(float(value) % 60)
    self.progress_label.configure(
        text=f"{minutes:02d}:{seconds:02d} / {time.strftime('%M:%S', time.gmtime(self.music_length))}"
    )


    # Optional: preview seek while dragging
    if slider_dragging:
        update_music_position(self)


def update_music_position(self):
    new_position = self.progress_slider.get()
    music_position = (new_position / 100) * self.music_length


    try:
        # If dragged to the end, just restart from beginning
        if music_position >= self.music_length - 0.5:
            music_position = 0

        pygame.mixer.music.play(start=music_position)
        self.seek_position = music_position
        self.last_update_time = time.time()

    except Exception as e:
        print("Seeking failed:", e)


# Periodically called to update slider thumb with actual music position

def update_slider(self):

    global slider_dragging
    if music_playing and not slider_dragging:
        try:
            current_time = pygame.mixer.music.get_pos() / 1000  # in seconds
            slider_value = (current_time / self.music_length) * 100
            self.progress_slider.set(slider_value)


            minutes = int(current_time // 60)
            seconds = int(current_time % 60)
            self.progress_label.configure(
                text=f"{minutes:02d}:{seconds:02d} / {time.strftime('%M:%S', time.gmtime(self.music_length))}"
            )
        except:
            pass


    # Call again after 500ms
    self.progress_slider.after(500, lambda: update_slider(self))






def play_pause_music(self):
    if self.is_playing:
        pygame.mixer.music.pause()
        self.is_playing = False
        self.play_pause_btn.configure(image=self.play_image)
    else:
        pygame.mixer.music.unpause()
        self.is_playing = True
        self.play_pause_btn.configure(image=self.pause_image)

        if self.is_playing == True and self.current_music_file == None:
            self.music_title_lbl.configure(text="Select A Music")



def update_progress(self):

    global slider_dragging
    if self.is_playing and not slider_dragging:
        try:
            elapsed = time.time() - self.last_update_time
            current_pos = self.seek_position + elapsed

            current_pos = min(current_pos, self.music_length)

            slider_val = (current_pos / self.music_length) * 100
            self.progress_slider.set(slider_val)

            current_time = time.strftime('%M:%S', time.gmtime(current_pos))
            total_time = time.strftime('%M:%S', time.gmtime(self.music_length))
            self.progress_label.configure(text=f"{current_time} / {total_time}")


        except Exception as e:
            print(f"Progress update error: {e}")

    self.aside_right.after(500, lambda: update_progress(self))



def play_music(self, filepath, title,image):

    try:
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        self.current_music_file = filepath
        self.is_playing = True
        self.play_pause_btn.configure(image=self.pause_image)


        self.music_title_lbl.configure(text=title)
        self.asr_aside_image_holder.configure(image=image,text=" ")
        self.asr_aside_image_holder.pack(fill="both",expand=True)

        # Use mutagen to get music length
        audio = MP3(filepath)
        self.music_length = audio.info.length

        self.progress_slider.configure(to=self.music_length,
                                       state="normal",
                                       fg_color=tlr_purple_4)

        # Initialize time tracking values
        self.last_update_time = time.time()
        self.seek_position = 0

        update_progress(self)


    except Exception as e:
        print("Error loading music:", e)



# SIDEBAR
def show_plays(self):

    for widget in self.button_frame.winfo_children():
        widget.destroy()

    # SIDEBAR BUTTONS HIGHLIGHT EFFECTS
    self.feed_btn = customtkinter.CTkButton(self.button_frame, text="Feed",
                                            command=lambda: show_plays(self),
                                            font=(fn_PM, 12),
                                            hover_color=tlr_purple_4,
                                            fg_color=tlr_purple_3)
    self.trends_btn = customtkinter.CTkButton(self.button_frame, text="Trends",
                                              command=lambda: show_trends(self),
                                              font=(fn_PM, 12),
                                              hover_color=tlr_purple_4,
                                              fg_color=tlr_dark)
    self.library_btn = customtkinter.CTkButton(self.button_frame, text="Library",
                                               command=lambda: show_library(self),
                                               font=(fn_PM, 12),
                                               hover_color=tlr_purple_4,
                                               fg_color=tlr_dark)



    self.feed_btn.pack(pady=10, padx=10, fill="x")
    self.trends_btn.pack(pady=10, padx=10, fill="x")
    self.library_btn.pack(pady=10, padx=10, fill="x")



    # TOP NAV
    for widget in self.cf_top_nav.winfo_children():
        widget.destroy()

    self.top_n_searchbar = customtkinter.CTkEntry(self.cf_top_nav,
                                                  width=350,
                                                  height=30,
                                                  fg_color=backup_ppl_2,
                                                  border_color=backup_ppl_1,
                                                  font=(fn_PR, 12),
                                                  placeholder_text="Search Anything......")

    self.top_n_searchbar.grid(row=0, column=1, pady=(9, 8), padx=10)



    for widget in self.main_music_feed_wrapper.winfo_children():
        widget.destroy()


    # HERO TRACK WRAPPER
    self.hero_track_wrapper = customtkinter.CTkFrame(self.main_music_feed_wrapper,
                                                     width=content_frame_width, height=300,
                                                     fg_color=tlr_dark)
    self.hero_track_cat_div = customtkinter.CTkFrame(self.main_music_feed_wrapper,
                                                     width=content_frame_width, height=25,
                                                     fg_color=tlr_dark)
    self.hero_track_cat_lbl = customtkinter.CTkLabel(self.hero_track_cat_div, text="MOST PLAYED SONGS",
                                                     font=(fn_PM, 16))

    # IMAGE FRAME
    self.hero_track_image_frame = customtkinter.CTkFrame(self.hero_track_wrapper,
                                                         width=402, height=300,
                                                         fg_color=tlr_dark)

    self.hero_track_image = customtkinter.CTkImage(light_image=Image.open("Albums/Requem H Track A.png"),
                                                   dark_image=Image.open("Albums/Requem H Track A.png"),
                                                   size=(352, 310))

    self.hero_track_img_lbl = customtkinter.CTkLabel(self.hero_track_image_frame, text="",
                                                     image=self.hero_track_image)

    # IMAGE DETAILS
    self.hero_track_image_details = customtkinter.CTkFrame(self.hero_track_wrapper,
                                                           width=400, height=300,
                                                           fg_color=tlr_dark, corner_radius=20)

    self.hero_track_name = customtkinter.CTkFrame(self.hero_track_image_details,
                                                  width=340, height=150,
                                                  fg_color=tlr_dark,
                                                  corner_radius=20)

    self.htn_category_div = customtkinter.CTkFrame(self.hero_track_name,
                                                   height=150,
                                                   corner_radius=10,
                                                   fg_color=backup_ppl_2,
                                                   width=100)
    self.ht_title_cat_div = customtkinter.CTkFrame(self.htn_category_div,
                                                   width=100, height=50, fg_color=backup_ppl_2)
    self.ht_title_lbl = customtkinter.CTkLabel(self.ht_title_cat_div, text="Title",
                                               text_color=moonphased, font=(fn_PR, 11))

    self.ht_author_cat_div = customtkinter.CTkFrame(self.htn_category_div,
                                                    width=100, height=50, fg_color=backup_ppl_2)
    self.ht_author_lbl = customtkinter.CTkLabel(self.ht_author_cat_div, text="Author",
                                                text_color=moonphased, font=(fn_PR, 11))

    self.ht_album_cat_div = customtkinter.CTkFrame(self.htn_category_div, fg_color=backup_ppl_2,
                                                   width=100, height=50)
    self.ht_album_lbl = customtkinter.CTkLabel(self.ht_album_cat_div, text="Album",
                                               text_color=moonphased, font=(fn_PR, 11))

    self.ht_data_div = customtkinter.CTkFrame(self.hero_track_name, corner_radius=10,
                                              width=240, height=150, fg_color=backup_ppl_2)
    self.ht_title_div = customtkinter.CTkFrame(self.ht_data_div, fg_color=backup_ppl_2,
                                               width=200, height=50)
    self.ht_song_title_lbl = customtkinter.CTkLabel(self.ht_title_div, text="Soft Spot",
                                                    font=(fn_PM, 13), text_color=w_pure_white)

    self.ht_author_div = customtkinter.CTkFrame(self.ht_data_div,
                                                width=200, height=50, fg_color=backup_ppl_2)
    self.ht_song_author_lbl = customtkinter.CTkLabel(self.ht_author_div, text="Keshi",
                                                     font=(fn_PM, 13), text_color=w_pure_white)

    self.ht_album_div = customtkinter.CTkFrame(self.ht_data_div, fg_color=backup_ppl_2,
                                               width=200, height=50)
    self.ht_song_album_lbl = customtkinter.CTkLabel(self.ht_album_div, text="Requiem",
                                                    font=(fn_PM, 13), text_color=w_pure_white)

    self.hero_times_played = customtkinter.CTkFrame(self.hero_track_image_details,
                                                    width=340, height=150,
                                                    fg_color=backup_ppl_2,
                                                    corner_radius=10)

    self.htp_lbl_a = customtkinter.CTkFrame(self.hero_times_played,
                                            width=340, height=40,
                                            corner_radius=10, fg_color=backup_ppl_2)
    self.htp_lbl_a_text = customtkinter.CTkLabel(self.htp_lbl_a, text="You played It", font=(fn_PR, 12),
                                                 text_color=w_main_white)

    self.htp_played_count = customtkinter.CTkFrame(self.hero_times_played,
                                                   width=340, height=60,
                                                   corner_radius=10, fg_color=backup_ppl_2)
    self.htp_played_count_text = customtkinter.CTkLabel(self.htp_played_count,
                                                        text="678",
                                                        font=("Cropar", 30), text_color=w_pure_white)

    self.htp_lbl_b = customtkinter.CTkFrame(self.hero_times_played,
                                            width=340, height=40,
                                            corner_radius=10, fg_color=backup_ppl_2)
    self.htp_lbl_b_text = customtkinter.CTkLabel(self.htp_lbl_b, text="times", font=(fn_PR, 12),
                                                 text_color=w_main_white)

    self.recom_music_feed_wrapper = customtkinter.CTkScrollableFrame(self.main_music_feed_wrapper,
                                                                     corner_radius=10,
                                                                     width=content_frame_width,
                                                                     fg_color=backup_ppl_2)











    # IGNORANCE
    self.ignorance_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                                    width=150, height=200,
                                                    fg_color=backup_ppl_2)

    self.ignorance_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Brand New Eyes.png"),
                                                  dark_image=Image.open("Albums/Brand New Eyes.png"),
                                                  size=(220, 200))

    self.ignorance_image = customtkinter.CTkImage(light_image=Image.open("Albums/Brand New Eyes.png"),
                                                  dark_image=Image.open("Albums/Brand New Eyes.png"),
                                                  size=(145, 143))

    self.ignorance_holder = customtkinter.CTkButton(self.ignorance_wrapper,
                                                    command=lambda:play_music(self,
                                                                              "Musics/Paramore - Ignorance.mp3",
                                                                              "Paramore - Ignorance",
                                                                              self.ignorance_image_pl),
                                                    text="",
                                                    image=self.ignorance_image,
                                                    fg_color=backup_ppl_2,
                                                    hover_color=tlr_purple_4,
                                                    height=150)

    self.ignorance_artist = customtkinter.CTkLabel(self.ignorance_wrapper, text="Paramore", font=(fn_PM, 15),
                                                   text_color=w_pure_white)
    self.ignorance_title = customtkinter.CTkLabel(self.ignorance_wrapper, text="Ignorance", font=(fn_PR, 12),
                                                  text_color="gray")

    self.ignorance_wrapper.pack_propagate(False)
    self.ignorance_wrapper.grid(row=0, column=1, pady=(4, 2), padx=5)
    self.ignorance_holder.pack()
    self.ignorance_artist.pack(padx=(5, 63), pady=(3, 5))
    self.ignorance_title.pack(padx=(2, 75))



    # AWAKE WRAPPER
    self.awake_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                                width=150, height=200,
                                                fg_color=backup_ppl_2)

    self.awake_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Awake.png"),
                                                     dark_image=Image.open("Albums/Awake.png"),
                                                     size=(220, 200))

    self.awake_image = customtkinter.CTkImage(light_image=Image.open("Albums/Awake.png"),
                                              dark_image=Image.open("Albums/Awake.png"),
                                              size=(150, 150))

    self.awake_holder = customtkinter.CTkButton(self.awake_wrapper,
                                                command=lambda: play_music(self,"Musics/Awake_(Remastered)(256k).mp3",
                                                                           "Secondhand Serenade - Awake",
                                                                            self.awake_image_pl),
                                                text="",
                                                image=self.awake_image,
                                                fg_color=backup_ppl_2,
                                                hover_color=tlr_purple_4,
                                                height=150)


    self.awake_artist = customtkinter.CTkLabel(self.awake_wrapper, text="Seconhand", font=(fn_PM, 15),
                                               text_color=w_pure_white)
    self.awake_title = customtkinter.CTkLabel(self.awake_wrapper, text="Awake", font=(fn_PR, 12),
                                              text_color="gray")

    self.awake_wrapper.pack_propagate(False)
    self.awake_wrapper.grid(row=0, column=2, pady=10, padx=5)
    self.awake_holder.pack()
    self.awake_artist.pack(padx=(0, 50))
    self.awake_title.pack(padx=(2, 100))




    # I SWEAR I NEVER LEAVE AGAIN
    self.like_i_need_u_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                                        width=150, height=200,
                                                        fg_color=backup_ppl_2)

    self.like_i_need_u_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Reaper.png"),
                                                 dark_image=Image.open("Albums/Reaper.png"),
                                                 size=(220, 200))

    self.like_i_need_u_image = customtkinter.CTkImage(light_image=Image.open("Albums/Reaper.png"),
                                                      dark_image=Image.open("Albums/Reaper.png"),
                                                      size=(140, 140))

    self.like_i_need_u_holder = customtkinter.CTkButton(self.like_i_need_u_wrapper,
                                                        command=lambda:
                                                        play_music(self,"Musics/keshi - like I need u (0).mp3",
                                                        "Keshi - Like I Need U",self.like_i_need_u_image_pl),
                                                        text="",
                                                        image=self.like_i_need_u_image,
                                                        fg_color=backup_ppl_2,
                                                        hover_color=tlr_purple_4,
                                                        height=150)

    self.like_i_need_u_artist = customtkinter.CTkLabel(self.like_i_need_u_wrapper, text="Keshi", font=(fn_PM, 15),
                                                       text_color=w_pure_white)
    self.like_i_need_u_title = customtkinter.CTkLabel(self.like_i_need_u_wrapper, text="Like I Need U",
                                                      font=(fn_PR, 12),
                                                      text_color="gray")

    self.like_i_need_u_wrapper.pack_propagate(False)
    self.like_i_need_u_wrapper.grid(row=0, column=3, pady=10, padx=5)
    self.like_i_need_u_holder.pack(pady=(3, 0))
    self.like_i_need_u_artist.pack(padx=(2, 95))
    self.like_i_need_u_title.pack(padx=(2, 65))



    # KISSING SCARS
    self.kissing_scars_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                                        width=150, height=200,
                                                        fg_color=backup_ppl_2)

    self.kissing_scars_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Selfish Machine.png"),
                                                         dark_image=Image.open("Albums/Selfish Machine.png"),
                                                         size=(220, 200))

    self.kissing_scars_image = customtkinter.CTkImage(light_image=Image.open("Albums/Selfish Machine.png"),
                                                      dark_image=Image.open("Albums/Selfish Machine.png"),
                                                      size=(140, 143))

    self.kissing_scars_holder = customtkinter.CTkButton(self.kissing_scars_wrapper, text="",
                                                        command=lambda:
                                                        play_music(self, "Musics/Kissing in Cars (Bonus Track) [EFsWKsMJBtE].mp3",
                                                                   "Pierce The Veil - Kissing Scars",
                                                                    self.kissing_scars_image_pl),

                                                        image=self.kissing_scars_image,
                                                        fg_color=backup_ppl_2,
                                                        hover_color=tlr_purple_4,
                                                        height=150)

    self.kissing_scars_artist = customtkinter.CTkLabel(self.kissing_scars_wrapper, text="Pierce The Veil",
                                                       font=(fn_PM, 15),
                                                       text_color=w_pure_white)
    self.kissing_scars_title = customtkinter.CTkLabel(self.kissing_scars_wrapper, text="Kissing in Scars",
                                                      font=(fn_PR, 12),
                                                      text_color="gray")

    self.kissing_scars_wrapper.pack_propagate(False)
    self.kissing_scars_wrapper.grid(row=0, column=4, pady=10, padx=5)
    self.kissing_scars_holder.pack(pady=2)
    self.kissing_scars_artist.pack(padx=(2, 30))
    self.kissing_scars_title.pack(padx=(2, 45))



    # A TWIST IN MY STORY
    self.a_twist_in_my_story_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                                              width=150, height=200,
                                                              fg_color=backup_ppl_2)

    self.a_twist_in_my_story_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/A Twist in my Story.png"),
                                                         dark_image=Image.open("Albums/A Twist in my Story.png"),
                                                         size=(220, 200))

    self.a_twist_in_my_story_image = customtkinter.CTkImage(light_image=Image.open("Albums/A Twist in my Story.png"),
                                                            dark_image=Image.open("Albums/A Twist in my Story.png"),
                                                            size=(150, 150))

    self.a_twist_in_my_story_holder = customtkinter.CTkButton(self.a_twist_in_my_story_wrapper, text="",
                                                              command=lambda:
                                                              play_music(self, "Musics/Secondhand Serenade - Goodbye.mp3",
                                                              "Secondhand Serenade - Goodbye",
                                                              self.a_twist_in_my_story_image_pl),

                                                              image=self.a_twist_in_my_story_image,
                                                              fg_color=backup_ppl_2,
                                                              hover_color=tlr_purple_4,
                                                              height=150)

    self.a_twist_in_my_story_artist = customtkinter.CTkLabel(self.a_twist_in_my_story_wrapper, text="Secondhand",
                                                             font=(fn_PM, 15),
                                                             text_color=w_pure_white)

    self.a_twist_in_my_story_title = customtkinter.CTkLabel(self.a_twist_in_my_story_wrapper, text="Goodbye",
                                                            font=(fn_PR, 12),
                                                            text_color="gray")

    self.a_twist_in_my_story_wrapper.pack_propagate(False)
    self.a_twist_in_my_story_wrapper.grid(row=1, column=1, pady=10, padx=5)
    self.a_twist_in_my_story_holder.pack()
    self.a_twist_in_my_story_artist.pack(padx=(2, 40))
    self.a_twist_in_my_story_title.pack(padx=(2, 80))





    # KESHI BLUE =========== ================
    self.blue_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                               width=150, height=200,
                                               fg_color=backup_ppl_2)

    self.blue_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Bandaids.png"),
                                                               dark_image=Image.open("Albums/Bandaids.png"),
                                                               size=(220, 200))

    self.blue_image = customtkinter.CTkImage(light_image=Image.open("Albums/Bandaids.png"),
                                             dark_image=Image.open("Albums/Bandaids.png"),
                                             size=(140, 150))

    self.blue_holder = customtkinter.CTkButton(self.blue_wrapper, text="",
                                               command=lambda:
                                               play_music(self, "Musics/keshi - blue.mp3",
                                               "Keshi - Blue",
                                               self.blue_image_pl),
                                               image=self.blue_image,
                                               fg_color=backup_ppl_2,
                                               hover_color=tlr_purple_4,
                                               height=150)

    self.blue_artist = customtkinter.CTkLabel(self.blue_wrapper, text="Keshi",
                                              font=(fn_PM, 15),
                                              text_color=w_pure_white)

    self.blue_title = customtkinter.CTkLabel(self.blue_wrapper, text="Blue",
                                             font=(fn_PR, 12),
                                             text_color="gray")

    self.blue_wrapper.pack_propagate(False)
    self.blue_wrapper.grid(row=1, column=2, pady=10, padx=5)
    self.blue_holder.pack()
    self.blue_artist.pack(padx=(0, 100))
    self.blue_title.pack(padx=(2, 115))



    # ON YOUR SIDE WRAPPER ==================== ================== ===================
    self.oys_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                              width=155, height=200,
                                              fg_color=backup_ppl_2)

    self.oys_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/On Your Side.png"),
                                                dark_image=Image.open("Albums/On Your Side.png"),
                                                size=(220, 200))

    self.oys_image = customtkinter.CTkImage(light_image=Image.open("Albums/On Your Side.png"),
                                            dark_image=Image.open("Albums/On Your Side.png"),
                                            size=(155, 150))

    self.oys_holder = customtkinter.CTkButton(self.oys_wrapper, text="",
                                              command=lambda:
                                              play_music(self, "Musics/A Rocket To The Moon - On Your Side.mp3",
                                              "A Rocket To The Moon - On Your Side",
                                              self.oys_image_pl),

                                              image=self.oys_image,
                                              fg_color=backup_ppl_2,
                                              hover_color=tlr_purple_4,
                                              height=150)

    self.oys_artist = customtkinter.CTkLabel(self.oys_wrapper, text="A Rocket To The",
                                             font=(fn_PM, 15),
                                             text_color=w_pure_white)

    self.oys_title = customtkinter.CTkLabel(self.oys_wrapper, text="On Your Side",
                                            font=(fn_PR, 12),
                                            text_color="gray")

    self.oys_wrapper.pack_propagate(False)
    self.oys_wrapper.grid(row=1, column=3, pady=10, padx=5)
    self.oys_holder.pack()
    self.oys_artist.pack(padx=(0, 3))
    self.oys_title.pack(padx=(2, 45))




    # LIMBO
    self.gabriel_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                                  width=155, height=200,
                                                  fg_color=backup_ppl_2)

    self.gabriel_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Gabriel.png"),
                                               dark_image=Image.open("Albums/Gabriel.png"),
                                               size=(220, 200))

    self.gabriel_image = customtkinter.CTkImage(light_image=Image.open("Albums/Gabriel.png"),
                                                dark_image=Image.open("Albums/Gabriel.png"),
                                                size=(155, 157))

    self.gabriel_holder = customtkinter.CTkButton(self.gabriel_wrapper, text="",
                                                  command=lambda:
                                                  play_music(self, "Musics/keshi - LIMBO.mp3",
                                                  "Keshi - Limbo",
                                                  self.gabriel_image_pl),

                                                  image=self.gabriel_image,
                                                  fg_color=backup_ppl_2,
                                                  hover_color=tlr_purple_4,
                                                  height=100)

    self.gabriel_artist = customtkinter.CTkLabel(self.gabriel_wrapper, text="Keshi",
                                                 font=(fn_PM, 15),
                                                 text_color=w_pure_white)

    self.gabriel_title = customtkinter.CTkLabel(self.gabriel_wrapper, text="Limbo",
                                                font=(fn_PR, 12),
                                                text_color="gray")

    self.gabriel_wrapper.pack_propagate(False)
    self.gabriel_wrapper.grid(row=1, column=4, pady=(0, 7), padx=5)
    self.gabriel_holder.pack_propagate(False)
    self.gabriel_holder.pack()
    self.gabriel_artist.pack(padx=(2, 103))
    self.gabriel_title.pack(padx=(2, 103))




    # MISERABLE AT BEST ==================== ================== ===================
    self.mab_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                              width=155, height=200,
                                              fg_color=backup_ppl_2)

    self.map_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Lesson For Romantics.png"),
                                                   dark_image=Image.open("Albums/Lesson For Romantics.png"),
                                                   size=(220, 200))


    self.mab_image = customtkinter.CTkImage(light_image=Image.open("Albums/Lesson For Romantics.png"),
                                            dark_image=Image.open("Albums/Lesson For Romantics.png"),
                                            size=(155, 157))

    self.mab_holder = customtkinter.CTkButton(self.mab_wrapper, text="",
                                              command=lambda:
                                              play_music(self, "Musics/Mayday Parade - Miserable At Best.mp3",
                                              "Mayday Parade - Miserable At Best",
                                              self.map_image_pl),


                                              image=self.mab_image,
                                              fg_color=backup_ppl_2,
                                              hover_color=tlr_purple_4,
                                              height=100)

    self.mab_artist = customtkinter.CTkLabel(self.mab_wrapper, text="Mayday Parade",
                                             font=(fn_PM, 15),
                                             text_color=w_pure_white)

    self.mab_title = customtkinter.CTkLabel(self.mab_wrapper, text="Miserable At Best",
                                            font=(fn_PR, 12),
                                            text_color="gray")

    self.mab_wrapper.pack_propagate(False)
    self.mab_wrapper.grid(row=2, column=1, pady=(0, 7), padx=5)
    self.mab_holder.pack_propagate(False)
    self.mab_holder.pack()
    self.mab_artist.pack(padx=(0, 5))
    self.mab_title.pack(padx=(0, 25))




    # IF YOU CAN'T HANG ==================== ================== ===================
    self.iych_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                               width=155, height=200,
                                               fg_color=backup_ppl_2)

    self.iych_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Lets Cheer To This.png"),
                                               dark_image=Image.open("Albums/Lets Cheer To This.png"),
                                               size=(220, 200))

    self.iych_image = customtkinter.CTkImage(light_image=Image.open("Albums/Lets Cheer To This.png"),
                                             dark_image=Image.open("Albums/Lets Cheer To This.png"),
                                             size=(155, 157))

    self.iych_holder = customtkinter.CTkButton(self.iych_wrapper, text="",
                                               command=lambda:
                                               play_music(self, "Musics/Sleeping With Sirens - If You Can't Hang.mp3",
                                               "Sleeping With Sirens - If You Can't Hang",
                                               self.iych_image_pl),

                                               image=self.iych_image,
                                               fg_color=backup_ppl_2,
                                               hover_color=tlr_purple_4,
                                               height=100)

    self.iych_artist = customtkinter.CTkLabel(self.iych_wrapper, text="Sleeping With Sirens",
                                              font=(fn_PM, 15),
                                              text_color=w_pure_white)

    self.iych_title = customtkinter.CTkLabel(self.iych_wrapper, text="If You Can't Hang",
                                             font=(fn_PR, 12),
                                             text_color="gray")

    self.iych_wrapper.pack_propagate(False)
    self.iych_wrapper.grid(row=2, column=2, pady=(0, 7), padx=5)
    self.iych_holder.pack_propagate(False)
    self.iych_holder.pack()
    self.iych_artist.pack()
    self.iych_title.pack(padx=(0, 20))



    # Say Keshi ================ =========== ================== ====================
    self.say_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                              width=155, height=200,
                                              fg_color=backup_ppl_2)

    self.say_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Requiem.png"),
                                                dark_image=Image.open("Albums/Requiem.png"),
                                                size=(220, 200))
    self.say_image = customtkinter.CTkImage(light_image=Image.open("Albums/Requiem.png"),
                                            dark_image=Image.open("Albums/Requiem.png"),
                                            size=(155, 157))

    self.say_holder = customtkinter.CTkButton(self.say_wrapper, text="",
                                              command=lambda:
                                              play_music(self, "Musics/keshi - Say.mp3",
                                                         "Keshi - Say",
                                                         self.say_image_pl),
                                              image=self.say_image,
                                              fg_color=backup_ppl_2,
                                              hover_color=tlr_purple_4,
                                              height=100)

    self.say_artist = customtkinter.CTkLabel(self.say_wrapper, text="Keshi",
                                             font=(fn_PM, 15),
                                             text_color=w_pure_white)

    self.say_title = customtkinter.CTkLabel(self.say_wrapper, text="Say",
                                            font=(fn_PR, 12),
                                            text_color="gray")

    self.say_wrapper.pack_propagate(False)
    self.say_wrapper.grid(row=2, column=3, pady=(0, 7), padx=5)
    self.say_holder.pack_propagate(False)
    self.say_holder.pack()
    self.say_artist.pack(padx=(0, 80))
    self.say_title.pack(padx=(0, 100))


    # With Eears to See And Eyes To Hear ============= === =========== ================== ====================
    self.wetsaeth_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                                   width=155, height=200,
                                                   fg_color=backup_ppl_2)



    self.wetsaeth_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/With Ears To See And Eyes To Hear.png"),
                                               dark_image=Image.open("Albums/With Ears To See And Eyes To Hear.png"),
                                               size=(220, 200))
    self.wetsaeth_image = customtkinter.CTkImage(
        light_image=Image.open("Albums/With Eears To See And Eyes To Hear.png"),
        dark_image=Image.open("Albums/With Eears To See And Eyes To Hear.png"),
        size=(155, 157))

    self.wetsaeth_holder = customtkinter.CTkButton(self.wetsaeth_wrapper, text="",
                                                   command=lambda:
                                                   play_music(self, "Musics/Sleeping With Sirens - If I'm James Dean, You're Audrey Hepburn.mp3",
                                                              "Sleeping With Sirens - If Im James Dean You're Audrey Hepburn",
                                                              self.wetsaeth_image_pl),

                                                   image=self.wetsaeth_image,
                                                   fg_color=backup_ppl_2,
                                                   hover_color=tlr_purple_4,
                                                   height=100)

    self.wetsaeth_artist = customtkinter.CTkLabel(  self.wetsaeth_wrapper, text="Sleeping With Sirens",
                                                  font=(fn_PM, 15),
                                                  text_color=w_pure_white)

    self.wetsaeth_title = customtkinter.CTkLabel(self.wetsaeth_wrapper, text="If Im James Dean",
                                                 font=(fn_PR, 12),
                                                 text_color="gray")

    self.wetsaeth_wrapper.pack_propagate(False)
    self.wetsaeth_wrapper.grid(row=2, column=4, pady=(0, 7), padx=5)
    self.wetsaeth_holder.pack_propagate(False)
    self.wetsaeth_holder.pack()
    self.wetsaeth_artist.pack(padx=(0))
    self.wetsaeth_title.pack(padx=(0, 35))



    self.hero_track_cat_div.grid_propagate(False)
    self.hero_track_cat_div.pack(fill="x", pady=5)
    self.hero_track_cat_lbl.grid(row=0, column=1,padx=(8,0))

    self.hero_track_wrapper.pack_propagate(False)
    self.hero_track_wrapper.pack(fill="x")

    self.hero_track_image_frame.grid(row=1, column=0)
    self.hero_track_img_lbl.grid(row=0, column=1)

    self.hero_track_image_details.grid(row=1, column=1, padx=(10, 10))
    self.hero_track_image_details.grid_propagate(False)

    self.hero_track_image_details.grid_columnconfigure(0, weight=1)
    self.hero_track_image_details.grid_columnconfigure(1, weight=1)

    self.hero_track_name.grid_propagate(False)
    self.hero_track_name.pack(pady=(0, 5))

    self.htn_category_div.grid_propagate(False)
    self.htn_category_div.grid(row=0, column=1)
    self.ht_title_cat_div.pack_propagate(False)
    self.ht_title_cat_div.grid(row=0, column=1, padx=(20, 0))
    self.ht_title_lbl.pack(padx=(10, 0), pady=8)

    self.ht_author_cat_div.pack_propagate(False)
    self.ht_author_cat_div.grid(row=1, column=1, padx=(20, 0))
    self.ht_author_lbl.pack(padx=(10, 0), pady=8)

    self.ht_album_cat_div.pack_propagate(False)
    self.ht_album_cat_div.grid(row=2, column=1, padx=(20, 0))
    self.ht_album_lbl.pack(padx=(10, 0), pady=8)

    self.ht_data_div.grid_propagate(False)
    self.ht_data_div.grid(row=0, column=2)

    self.ht_title_div.grid_propagate(False)
    self.ht_title_div.grid(row=0, column=2)
    self.ht_song_title_lbl.grid(row=0, column=1, padx=(80, 0), pady=8)

    self.ht_author_div.grid_propagate(False)
    self.ht_author_div.grid(row=1, column=2)
    self.ht_song_author_lbl.grid(row=0, column=1, padx=(80, 0), pady=8)

    self.ht_album_div.grid_propagate(False)
    self.ht_album_div.grid(row=2, column=2)
    self.ht_song_album_lbl.grid(row=0, column=1, padx=(80, 0), pady=8)

    self.hero_times_played.pack_propagate(False)
    self.hero_times_played.pack(pady=(5, 0))

    self.htp_lbl_a.grid_propagate(False)
    self.htp_lbl_a.pack(pady=(20, 0))
    self.htp_lbl_a_text.grid(row=0, column=1, padx=(80, 0))

    self.htp_played_count.pack()
    self.htp_played_count_text.pack(pady=(0, 10))

    self.htp_lbl_b.grid_propagate(False)
    self.htp_lbl_b.pack(pady=(5, 8))
    self.htp_lbl_b_text.pack(padx=(100, 20))

    self.recom_music_feed_wrapper.pack(padx=0, pady=10, fill="both", expand=True)



def heart_unheart_artist(self):

    self.heart_line_image = ctk.CTkImage(light_image=Image.open("Images/heart-line.png"),
                                    dark_image=Image.open("Images/heart-line.png"),
                                    size=(20, 20))
    self.heart_fill_image = ctk.CTkImage(light_image=Image.open("Images/heart-fill.png"),
                                      dark_image=Image.open("Images/heart-fill.png"),
                                      size=(20, 20))

    if  self.heart_artist:
        self.heart_artist = False
        self.artist_heart_button.configure(image=self.heart_line_image)
        print("UNHEART ARTIST")
    else:
        print("HEART ARTIST")
        self.heart_artist = True
        self.artist_heart_button.configure(image=self.heart_fill_image)


def follow_unfollow_artist(self):

    if self.follow_artist:
       self.follow_artist = False
       self.artist_follow_button.configure(text="Follow",font=(fn_PM,12))
    else:
       self.follow_artist = True
       self.artist_follow_button.configure(text="Unfollow", font=(fn_PM, 12))



def show_trends(self):

        self.heart_artist = False
        self.follow_artist = False

        for widget in self.button_frame.winfo_children():
            widget.destroy()

        # SIDEBAR BUTTONS
        self.feed_btn = customtkinter.CTkButton(self.button_frame, text="Feed",
                                                command=lambda: show_plays(self),
                                                font=(fn_PM, 12),
                                                hover_color=tlr_purple_4,
                                                fg_color=tlr_dark)

        self.trends_btn = customtkinter.CTkButton(self.button_frame, text="Trends",
                                                  command=lambda: show_trends(self),
                                                  font=(fn_PM, 12),
                                                  hover_color=tlr_purple_4,
                                                  fg_color=tlr_purple_3)

        self.library_btn = customtkinter.CTkButton(self.button_frame, text="Library",
                                                   command=lambda: show_library(self),
                                                   font=(fn_PM, 12),
                                                   hover_color=tlr_purple_4,
                                                   fg_color=tlr_dark)



        self.feed_btn.pack(pady=10, padx=10, fill="x")
        self.trends_btn.pack(pady=10, padx=10, fill="x")
        self.library_btn.pack(pady=10, padx=10, fill="x")




        # TOP NAV === === === === === === === === === === === === === === === === === === === === ===

        for widget in self.cf_top_nav.winfo_children():
            widget.destroy()

        self.top_n_searchbar = customtkinter.CTkEntry(self.cf_top_nav,
                                                      width=350,
                                                      height=30,
                                                      fg_color=backup_ppl_2,
                                                      border_color=backup_ppl_1,
                                                      font=(fn_PR, 12),
                                                      placeholder_text="Search Anything......")

        self.top_n_searchbar.grid(row=0, column=1, pady=(9, 8), padx=10)



        # MAION MUSIC FEED ==== ==== ==== ==== ==== ===== ===== ===== ===== ====== ====== ===== ======
        for widget in self.main_music_feed_wrapper.winfo_children():
            widget.destroy()




        self.trends_hero_content_wrapper = ctk.CTkFrame(self.main_music_feed_wrapper,
                                                      width=content_frame_width,height=350,fg_color=tlr_dark)

        self.trends_cat_frame = ctk.CTkFrame(self.trends_hero_content_wrapper,
                                                      width=content_frame_width,
                                                      height=30,fg_color=tlr_dark)
        self.trends_cat_lbl = ctk.CTkLabel(self.trends_cat_frame,text="TRENDS",font=(fn_PM,16),fg_color=tlr_dark)

        tthf_width = content_frame_width / 2
        self.trends_track_hero_wrapper = ctk.CTkFrame(self.trends_hero_content_wrapper,fg_color=tlr_dark)


        self.birds_of_feather = ctk.CTkImage(light_image=Image.open("Albums/Birds of Feather A.png"),
                                             dark_image=Image.open("Albums/Birds of Feather A.png"),
                                             size=(352, 310))
        self.trend_track_holder = ctk.CTkLabel(self.trends_track_hero_wrapper,text="",image=self.birds_of_feather,
                                                width=tthf_width - 2,height=305,
                                                fg_color=tlr_dark)
        self.trends_track_infos = ctk.CTkFrame(self.trends_track_hero_wrapper,
                                               width=tthf_width - 2,height=305,
                                               fg_color=tlr_dark)

        info_a_lr_width = tthf_width / 2
        self.trend_info_a = ctk.CTkFrame(self.trends_track_infos,height=145,fg_color=tlr_dark)

        self.artist_profile = ctk.CTkImage(light_image=Image.open("Albums/Biliie Elish A.png"),
                                           dark_image=Image.open("Albums/Biliie Elish A.png"),
                                           size=(100,92))

        self.heart_image = ctk.CTkImage(light_image=Image.open("Images/heart-line.png"),
                                        dark_image=Image.open("Images/heart-line.png"),
                                        size=(20,20))

        self.trend_info_a_left = ctk.CTkFrame(self.trend_info_a,width=120,fg_color=tlr_dark)
        self.artist_profile_holder = ctk.CTkLabel(self.trend_info_a_left,text="",image=self.artist_profile,
                                                   fg_color=tlr_dark,height=100,width=100)

        self.artist_heart_button = ctk.CTkButton(self.trend_info_a_left, command=lambda:heart_unheart_artist(self),
                                                 text="",image=self.heart_image,
                                                 fg_color=tlr_dark,hover_color=tlr_purple_4,
                                                 width=5, height=30)

        self.trend_info_a_right = ctk.CTkFrame(self.trend_info_a, width=200,fg_color=tlr_dark)
        self.artist_follow_button = ctk.CTkButton(self.trend_info_a_right,command=lambda:follow_unfollow_artist(self),
                                                  text="Follow",font=(fn_PM,12),
                                                  fg_color=tlr_purple_3,hover_color=tlr_purple_4)
        self.trend_artist_name = ctk.CTkLabel(self.trend_info_a_right, text="Billie Eilish", text_color=w_f5,
                                              font=(fn_PM, 20))
        self.artist_listener_numbers = ctk.CTkLabel(self.trend_info_a_right,text="153,012 Monthly Listener",
                                                    font=(fn_PM,12),text_color="gray")


        self.trend_info_b = ctk.CTkFrame(self.trends_track_infos,height=160,fg_color=tlr_dark)
        self.trend_artist_song_b = ctk.CTkLabel(self.trend_info_b,text="Birds of Feader",text_color=w_f5,font=(fn_PM,25))
        self.trend_artist_name_b = ctk.CTkLabel(self.trend_info_b,text="by Billie Eilish",text_color="grey",font=(fn_PR,12))





        self.trends_recom_music_feed_wrapper = customtkinter.CTkScrollableFrame(self.main_music_feed_wrapper,
                                                                               width=content_frame_width,

                                                                               fg_color=backup_ppl_2,height=450)


        # MUSCIS ===== =====  =====  ===== =====  =====  ===== =====  =====  ===== =====  =====  ===== =====  =====

        # BLUE
        self.yung_kai_image = ctk.CTkImage(light_image=Image.open("Albums/Yung Kai.png"),
                                           dark_image=Image.open("Albums/Yung Kai.png"),
                                           size=(150,150))

        self.yung_kai_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Yung Kai.png"),
                                                         dark_image=Image.open("Albums/Yung Kai.png"),
                                                         size=(220, 200))

        self.yung_kai_blue_wrapper = ctk.CTkFrame(self.trends_recom_music_feed_wrapper,width=150, height=200,
                                                fg_color=backup_ppl_2)

        self.yung_kai_blue_holder = ctk.CTkButton(self.yung_kai_blue_wrapper ,text=" ",
                                                   command=lambda: play_music(
                                                   self, "Musics/yung kai - blue.mp3",
                                                   "Yung Kai - Blue",
                                                   self.yung_kai_image_pl                                                   ),
                                                   image=self.yung_kai_image,fg_color=backup_ppl_2,hover_color=tlr_purple_1)
        self.yung_kai_artist = customtkinter.CTkLabel(self.yung_kai_blue_wrapper, text="Yung Kai", font=(fn_PM, 15),
                                                       text_color=w_pure_white)
        self.yung_kai_title = customtkinter.CTkLabel(self.yung_kai_blue_wrapper, text="Blue", font=(fn_PR, 12),
                                                      text_color="gray")

        self.yung_kai_blue_wrapper.pack_propagate(False)
        self.yung_kai_blue_wrapper.grid(row=0,column=1,padx=10)
        self.yung_kai_blue_holder.pack()
        self.yung_kai_artist.pack(padx=(0,60))
        self.yung_kai_title.pack(padx=(0,100))




        # APT
        self.apt_image = ctk.CTkImage(light_image=Image.open("Albums/APT.png"),
                                           dark_image=Image.open("Albums/APT.png"),
                                           size=(150, 150))

        self.apt_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/APT.png"),
                                                        dark_image=Image.open("Albums/APT.png"),
                                                        size=(220, 200))

        self.apt_wrapper = ctk.CTkFrame(self.trends_recom_music_feed_wrapper, width=150, height=200,
                                                  fg_color=backup_ppl_2)

        self.apt_wrapper_holder = ctk.CTkButton(self.apt_wrapper,text="",
                                                  command=lambda: play_music(
                                                  self, "Musics/ROSÉ & Bruno Mars - APT..mp3",
                                                  "ROSÉ & Bruno Mars - APT.mp3",
                                                  self.apt_image_pl),
                                                  image=self.apt_image,fg_color=backup_ppl_2,hover_color=tlr_purple_1)
        self.apt_artist = customtkinter.CTkLabel(self.apt_wrapper , text="Rose,Bruno Mars", font=(fn_PM, 15),
                                                  text_color=w_pure_white)
        self.apt_title = customtkinter.CTkLabel(self.apt_wrapper , text="APT", font=(fn_PR, 12),
                                                 text_color="gray")

        self.apt_wrapper.pack_propagate(False)
        self.apt_wrapper.grid(row=0, column=2, pady=(4, 2),padx=10)
        self.apt_wrapper_holder.pack()
        self.apt_artist.pack(padx=(0))
        self.apt_title.pack(padx=(0, 100))




        # DIE WITH A SMILE
        self.dwas_image = ctk.CTkImage(light_image=Image.open("Albums/Death With A Smile.png"),
                                           dark_image=Image.open("Albums/Death With A Smile.png"),
                                           size=(150, 150))

        self.dwas_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Death With A Smile.png"),
                                                   dark_image=Image.open("Albums/Death With A Smile.png"),
                                                   size=(220, 200))

        self.dwas_wrapper = ctk.CTkFrame(self.trends_recom_music_feed_wrapper, width=150, height=200,
                                        fg_color=backup_ppl_2)

        self.dwas_holder = ctk.CTkButton(   self.dwas_wrapper,text="",
                                                command=lambda: play_music(
                                                self, "Musics/Lady Gaga, Bruno Mars - Die With A Smile.mp3",
                                                "Lady Gaga, Bruno Mars - Die With A Smile",
                                                self.dwas_image_pl),
                                                image=self.dwas_image, fg_color=backup_ppl_2,hover_color=tlr_purple_1)
        self.dwas_artist = customtkinter.CTkLabel( self.dwas_wrapper , text="Lady Gaga,Bru", font=(fn_PM, 15),
                                                      text_color=w_pure_white)
        self.dwas_title = customtkinter.CTkLabel( self.dwas_wrapper , text="Die With A Smile", font=(fn_PR, 12),
                                                     text_color="gray")

        self.dwas_wrapper.pack_propagate(False)
        self.dwas_wrapper.grid(row=0, column=3, pady=(4, 2), padx=10)
        self.dwas_holder.pack()
        self.dwas_artist.pack(padx=(0,13))
        self.dwas_title.pack(padx=(0,23))




        # MULTO
        self.multo_image = ctk.CTkImage(light_image=Image.open("Albums/Multo.png"),
                                       dark_image=Image.open("Albums/Multo.png"),
                                       size=(150, 150))

        self.multo_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Multo.png"),
                                       dark_image=Image.open("Albums/Multo.png"),
                                                    size=(220, 200))

        self.multo_wrapper = ctk.CTkFrame(self.trends_recom_music_feed_wrapper, width=150, height=200,
                                        fg_color=backup_ppl_2)


        self.multo_holder = ctk.CTkButton(self.multo_wrapper, text="",
                                                command=lambda: play_music(self,
                                                "Musics/Multo - Cup of Joe.mp3",
                                                "Cup of Joe - Multo",
                                                self.multo_image_pl),

                                                image=self.multo_image, fg_color=backup_ppl_2,hover_color=tlr_purple_1)
        self.multo_artist = customtkinter.CTkLabel( self.multo_wrapper, text="Cup Of Joe", font=(fn_PM, 15),
                                                  text_color=w_pure_white)
        self.multo_title = customtkinter.CTkLabel( self.multo_wrapper , text="Multo", font=(fn_PR, 12),
                                                 text_color="gray")

        self.multo_wrapper.pack_propagate(False)
        self.multo_wrapper.grid(row=0, column=4, pady=(4, 2), padx=10)
        self.multo_holder.pack()
        self.multo_artist.pack(padx=(0, 38))
        self.multo_title.pack(padx=(0, 85))



        # ANXIETY
        self.anxiety_image = ctk.CTkImage(light_image=Image.open("Albums/Anxiety.png"),
                                        dark_image=Image.open("Albums/Anxiety.png"),
                                        size=(150, 150))

        self.anxiety_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Anxiety.png"),
                                                     dark_image=Image.open("Albums/Anxiety.png"),
                                                     size=(220, 200))

        self.anxiety_wrapper = ctk.CTkFrame(self.trends_recom_music_feed_wrapper, width=150, height=200,
                                          fg_color=backup_ppl_2)

        self.anxiety_holder = ctk.CTkButton(self.anxiety_wrapper, text="",
                                          command=lambda: play_music(
                                          self, "Musics/Doechii - Anxiety.mp3",
                                          "Doechii - Anxiety",
                                          self.anxiety_image_pl),
                                          image=self.anxiety_image, fg_color=backup_ppl_2,hover_color=tlr_purple_1)
        self.anxiety_artist = customtkinter.CTkLabel(self.anxiety_wrapper, text="Doechii", font=(fn_PM, 15),
                                                   text_color=w_pure_white)
        self.anxiety_title = customtkinter.CTkLabel(self.anxiety_wrapper, text="Anxiety", font=(fn_PR, 12),
                                                  text_color="gray")

        self.anxiety_wrapper.pack_propagate(False)
        self.anxiety_wrapper.grid(row=1, column=1, pady=(4, 2), padx=10)
        self.anxiety_holder.pack()
        self.anxiety_artist.pack(padx=(0, 60))
        self.anxiety_title.pack(padx=(0, 73))



        # BYE BYE
        self.Bye_Bye_image = ctk.CTkImage(light_image=Image.open("Albums/Bye Bye.png"),
                                          dark_image=Image.open("Albums/Bye Bye.png"),
                                          size=(150, 150))

        self.Bye_Bye_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Bye Bye.png"),
                                                       dark_image=Image.open("Albums/Bye Bye.png"),
                                                       size=(220, 200))

        self.Bye_Bye_wrapper = ctk.CTkFrame(self.trends_recom_music_feed_wrapper, width=150, height=200,
                                            fg_color=backup_ppl_2)

        self.Bye_Bye_holder = ctk.CTkButton(self.Bye_Bye_wrapper, text="",
                                            command=lambda: play_music(
                                            self, "Musics/_NSYNC - Bye Bye Bye.mp3",
                                            "_NSYNC - Bye Bye Bye",
                                            self.Bye_Bye_image_pl),
                                            image=self.Bye_Bye_image, fg_color=backup_ppl_2,hover_color=tlr_purple_1)
        self.Bye_Bye_artist = customtkinter.CTkLabel(self.Bye_Bye_wrapper, text="_NSYNC", font=(fn_PM, 15),
                                                     text_color=w_pure_white)
        self.Bye_Bye_title = customtkinter.CTkLabel(self.Bye_Bye_wrapper, text="Bye Bye", font=(fn_PR, 12),
                                                    text_color="gray")

        self.Bye_Bye_wrapper.pack_propagate(False)
        self.Bye_Bye_wrapper.grid(row=1, column=2, pady=(4, 2), padx=10)
        self.Bye_Bye_holder.pack()
        self.Bye_Bye_artist.pack(padx=(0, 55))
        self.Bye_Bye_title.pack(padx=(0, 77))





        # SHE KNOWS
        self.she_knows_image = ctk.CTkImage(light_image=Image.open("Albums/She Knows.png"),
                                          dark_image=Image.open("Albums/She Knows.png"),
                                          size=(150, 150))

        self.she_know_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/She Knows.png"),
                                                       dark_image=Image.open("Albums/She Knows.png"),
                                                       size=(220, 200))

        self.she_knows_wrapper = ctk.CTkFrame(self.trends_recom_music_feed_wrapper, width=150, height=200,
                                            fg_color=backup_ppl_2)

        self.she_knows_holder = ctk.CTkButton(self.she_knows_wrapper, text="",
                                              command=lambda: play_music(
                                              self, "Musics/J. Cole - She Knows.mp3",
                                              "J. Cole - She Knows",
                                              self.she_know_image_pl),
                                              image=self.she_knows_image, fg_color=backup_ppl_2,hover_color=tlr_purple_1)
        self.she_knows_artist = customtkinter.CTkLabel(self.she_knows_wrapper, text="J.Cole", font=(fn_PM, 15),
                                                     text_color=w_pure_white)
        self.she_knows_title = customtkinter.CTkLabel(self.she_knows_wrapper, text="She_knows", font=(fn_PR, 12),
                                                    text_color="gray")

        self.she_knows_wrapper.pack_propagate(False)
        self.she_knows_wrapper.grid(row=1, column=3, pady=(4, 2), padx=10)
        self.she_knows_holder.pack()
        self.she_knows_artist.pack(padx=(0, 70))
        self.she_knows_title.pack(padx=(0, 50))



        # POP LIKE THIS

        self.pop_like_this_image = ctk.CTkImage(light_image=Image.open("Albums/Pop Like This.png"),
                                                dark_image=Image.open("Albums/Pop Like This.png"),
                                                size=(150, 150))

        self.pop_like_this_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Pop Like This.png"),
                                                        dark_image=Image.open("Albums/Pop Like This.png"),
                                                        size=(220, 200))


        self.pop_like_this_wrapper = ctk.CTkFrame(self.trends_recom_music_feed_wrapper, width=150, height=200,
                                                  fg_color=backup_ppl_2)

        self.pop_like_this_holder = ctk.CTkButton(self.pop_like_this_wrapper, text="",
                                                  command=lambda: play_music(
                                                  self, "Musics/CPK Shawn - Pop like this Pt. 2.mp3",
                                                  "CPK Shawn - Pop like this Pt. 2",
                                                  self.pop_like_this_image_pl),
                                                  image=self.pop_like_this_image, fg_color=backup_ppl_2,hover_color=tlr_purple_1)
        self.pop_like_this_artist = customtkinter.CTkLabel(self.pop_like_this_wrapper, text="CPK Shawn",
                                                           font=(fn_PM, 15),
                                                           text_color=w_pure_white)
        self.pop_like_this_title = customtkinter.CTkLabel(self.pop_like_this_wrapper, text="Pop like this",
                                                          font=(fn_PR, 12),
                                                          text_color="gray")

        self.pop_like_this_wrapper.pack_propagate(False)
        self.pop_like_this_wrapper.grid(row=1, column=4, pady=(4, 2), padx=10)
        self.pop_like_this_holder.pack()
        self.pop_like_this_artist.pack(padx=(0, 30))
        self.pop_like_this_title.pack(padx=(0, 50))







        # ALIBI
        self.alibi_image = ctk.CTkImage(light_image=Image.open("Albums/Alibi.png"),
                                                dark_image=Image.open("Albums/Alibi.png"),
                                                size=(150, 150))
        self.alibi_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Alibi.png"),
                                                        dark_image=Image.open("Albums/Alibi.png"),
                                                        size=(220, 200))

        self.alibi_wrapper = ctk.CTkFrame(self.trends_recom_music_feed_wrapper, width=150, height=200,
                                                  fg_color=backup_ppl_2)

        self.alibi_holder = ctk.CTkButton(self.alibi_wrapper, text="",
                                              command=lambda: play_music(
                                              self, "Musics/SEVDALIZA FT. PABLLO VITTAR & YSEULT - ALIBI.mp3",
                                              "SEVDALIZA FT. PABLLO VITTAR & YSEULT - ALIBI",
                                              self.alibi_image_pl),
                                              image=self.alibi_image, fg_color=backup_ppl_2,hover_color=tlr_purple_1)
        self.alibi_artist = customtkinter.CTkLabel(self.alibi_wrapper, text="SEVDALIZA FT. -",
                                                           font=(fn_PM, 15),
                                                           text_color=w_pure_white)
        self.alibi_title = customtkinter.CTkLabel(self.alibi_wrapper, text="ALIBI",
                                                          font=(fn_PR, 12),
                                                          text_color="gray")

        self.alibi_wrapper.pack_propagate(False)
        self.alibi_wrapper.grid(row=2, column=1, pady=(4, 2), padx=10)
        self.alibi_holder.pack()
        self.alibi_artist.pack(padx=(10))
        self.alibi_title.pack(padx=(0, 95))






        # PASSO BEM SOLTO
        self.pbs_image = ctk.CTkImage(light_image=Image.open("Albums/PASSO BEM SOLTO.png"),
                                        dark_image=Image.open("Albums/PASSO BEM SOLTO.png"),
                                        size=(150, 150))
        self.pbs_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/PASSO BEM SOLTO.png"),
                                                     dark_image=Image.open("Albums/PASSO BEM SOLTO.png"),
                                                     size=(220, 200))

        self.pbs_wrapper = ctk.CTkFrame(self.trends_recom_music_feed_wrapper, width=150, height=200,
                                          fg_color=backup_ppl_2)

        self.pbs_holder = ctk.CTkButton(self.pbs_wrapper, text="",
                                            command=lambda: play_music(
                                            self, "Musics/ATLXS - PASSO BEM SOLTO.mp3",
                                            "ATLXS - PASSO BEM SOLTO",
                                            self.pbs_image_pl),

                                            image=self.pbs_image, fg_color=backup_ppl_2,hover_color=tlr_purple_1)
        self.pbs_artist = customtkinter.CTkLabel(self.pbs_wrapper, text="ATLXS",
                                                   font=(fn_PM, 15),
                                                   text_color=w_pure_white)
        self.pbs_title = customtkinter.CTkLabel(self.pbs_wrapper, text="PASSO BEM SOLTO",
                                                  font=(fn_PR, 12),
                                                  text_color="gray")



        self.pbs_wrapper.pack_propagate(False)
        self.pbs_wrapper.grid(row=2, column=2, pady=(4, 2), padx=10)
        self.pbs_holder.pack()
        self.pbs_artist.pack(padx=(0, 75))
        self.pbs_title.pack(padx=(0,12))




        # LA LA LA
        self.la_la_la_image = ctk.CTkImage(light_image=Image.open("Albums/LA LA LA.png"),
                                      dark_image=Image.open("Albums/LA LA LA.png"),
                                      size=(150, 150))
        self.la_la_la_pl = customtkinter.CTkImage(light_image=Image.open("Albums/LA LA LA.png"),
                                                   dark_image=Image.open("Albums/LA LA LA.png"),
                                                   size=(220, 200))


        self.la_la_la_wrapper = ctk.CTkFrame(self.trends_recom_music_feed_wrapper, width=150, height=200,
                                        fg_color=backup_ppl_2)

        self.la_la_la_holder = ctk.CTkButton(self.la_la_la_wrapper, text="",
                                                 command=lambda: play_music(
                                                 self, "Musics/Naughty Boy, Sam Smith - La La La.mp3",
                                                 "Naughty Boy, Sam Smith - La La La",
                                                 self.la_la_la_pl),
                                        image=self.la_la_la_image, fg_color=backup_ppl_2,hover_color=tlr_purple_1)
        self.la_la_la_artist = customtkinter.CTkLabel(self.la_la_la_wrapper, text="Naughty Boy",
                                                 font=(fn_PM, 15),
                                                 text_color=w_pure_white)
        self.la_la_la_title = customtkinter.CTkLabel(self.la_la_la_wrapper, text="LA LA LA",
                                                font=(fn_PR, 12),
                                                text_color="gray")

        self.la_la_la_wrapper.pack_propagate(False)
        self.la_la_la_wrapper.grid(row=2, column=3, pady=(4, 2), padx=10)
        self.la_la_la_holder.pack()
        self.la_la_la_artist.pack(padx=(0,20))
        self.la_la_la_title.pack(padx=(0,70))



        # ILTWYKM
        self.iltwykm_image = ctk.CTkImage(light_image=Image.open("Albums/Like the way you kiss me.png"),
                                      dark_image=Image.open("Albums/Like the way you kiss me.png"),
                                      size=(150, 150))
        self.iltwykm_image_pl = customtkinter.CTkImage(light_image=Image.open("Albums/Like the way you kiss me.png"),
                                                  dark_image=Image.open("Albums/Like the way you kiss me.png"),
                                                  size=(220, 200))

        self.iltwykm_wrapper = ctk.CTkFrame(self.trends_recom_music_feed_wrapper, width=150, height=200,
                                        fg_color=backup_ppl_2)

        self.iltwykm_holder = ctk.CTkButton(self.iltwykm_wrapper, text="",
                                                command=lambda:play_music(
                                                self,"Musics/Artemas - i like the way you kiss me.mp3",
                                                "Artemas - I Like The Way You Kiss Me",
                                                self.iltwykm_image_pl),

                                        image=self.iltwykm_image, fg_color=backup_ppl_2,hover_color=tlr_purple_1)
        self.iltwykm_artist = customtkinter.CTkLabel(self.iltwykm_wrapper, text="Artemas",
                                                 font=(fn_PM, 15),
                                                 text_color=w_pure_white)
        self.iltwykm_title = customtkinter.CTkLabel(self.iltwykm_wrapper, text="Like The Way",
                                                font=(fn_PR, 12),
                                                text_color="gray")

        self.iltwykm_wrapper.pack_propagate(False)
        self.iltwykm_wrapper.grid(row=2, column=4, pady=(4, 2), padx=10)
        self.iltwykm_holder.pack()
        self.iltwykm_artist.pack(padx=(0, 55))
        self.iltwykm_title.pack(padx=(0,44))






        # PACKING ======= ========= ======================   ================    ============    ===================
        self.trends_hero_content_wrapper.pack_propagate(False)
        self.trends_hero_content_wrapper.pack(fill="both",expand=True,pady=(0,10))

        self.trends_cat_frame.grid_propagate(False)
        self.trends_track_hero_wrapper.grid_propagate(False)
        self.trends_cat_frame.pack(fill="x",pady=5)
        self.trends_cat_lbl.grid(row=0,column=1,padx=(10, 0),pady=(2,0))

        self.trend_track_holder.pack_propagate(False)
        self.trends_track_infos.pack_propagate(False)

        self.trends_track_hero_wrapper.pack(fill="both",expand=True)

        self.trend_track_holder.grid(row=0,column=1,pady=0)

        self.trends_track_infos.pack_propagate(False)
        self.trends_track_infos.grid(row=0,column=2)

        self.trend_info_a.grid_propagate(False)
        self.trend_info_a.pack(fill="both",expand=True,padx=(5,0))
        self.trend_info_a_left.pack_propagate(False)
        self.trend_info_a_left.grid(row=0,column=1)
        self.artist_profile_holder.pack(fill="both",padx=(0,20))
        self.artist_heart_button.pack(padx=(2,90),pady=(10,0))

        self.trend_info_a_right.pack_propagate(False)
        self.trend_info_a_right.grid(row=0,column=2)

        self.artist_follow_button.pack(pady=5,padx=(0,60))
        self.trend_artist_name.pack(anchor="w",pady=(5,0))
        self.artist_listener_numbers.pack(anchor="w")

        self.trend_info_b.pack_propagate(False)
        self.trend_info_b.pack(pady=5, padx=5,fill="both",expand=True)
        self.trend_artist_song_b.pack(side=ctk.LEFT,pady=(8,0),padx=(35,0))
        self.trend_artist_name_b.pack(side=ctk.LEFT,pady=(14,0),padx=(5,10))




        self.trends_recom_music_feed_wrapper.pack_propagate(False)
        self.trends_recom_music_feed_wrapper.pack(padx=0, pady=(0, 10), fill="both", expand=True)
        







def show_library(self):

    # SIDEBAR  ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ====
    for widget in self.button_frame.winfo_children():
        widget.destroy()

        # SIDEBAR BUTTONS
    self.feed_btn = customtkinter.CTkButton(self.button_frame, text="Feed",
                                            command=lambda: show_plays(self),
                                            font=(fn_PM, 12),
                                            hover_color=tlr_purple_4,
                                            fg_color=tlr_dark)

    self.trends_btn = customtkinter.CTkButton(self.button_frame, text="Trends",
                                              command=lambda: show_trends(self),
                                              font=(fn_PM, 12),
                                              hover_color=tlr_purple_4,
                                              fg_color=tlr_dark)

    self.library_btn = customtkinter.CTkButton(self.button_frame, text="Library",
                                               command=lambda: show_library(self),
                                               font=(fn_PM, 12),
                                               hover_color=tlr_purple_4,
                                               fg_color=tlr_purple_3, )

    self.playlist_frame = ctk.CTkFrame(self.button_frame,fg_color=tlr_dark)
    self.playlist_text = ctk.CTkLabel(self.playlist_frame,text="PLAYLISTS",font=(fn_PM,12),text_color="grey")
    self.playlist_scroll = ctk.CTkScrollableFrame(self.playlist_frame,
                                                  fg_color=tlr_dark,
                                                  scrollbar_button_color=tlr_dark,
                                                  scrollbar_button_hover_color=tlr_dark)

    # PACKING ================================

    self.feed_btn.pack(pady=10, padx=10, fill="x")
    self.trends_btn.pack(pady=10, padx=10, fill="x")
    self.library_btn.pack(pady=10, padx=10, fill="x")

    self.playlist_frame.pack_propagate(False)
    self.playlist_frame.pack(pady=(10,30), fill="both", expand=True)
    self.playlist_text.pack(pady=10,padx=(0,105))
    self.playlist_scroll.pack(fill="both",expand=True)


    # PLAYLIST ========  ========  ========  ========  ========  ======== ========  ========  ========

    emo_title = "Emo Core"
    emo_info = "10 Songs . 35 mins"
    # EMO CORE ============ ============ ============= =============== =============
    self.emo_core_frame = ctk.CTkFrame(self.playlist_scroll,fg_color=tlr_dark,width=150, height=50)
    self.emo_data_frame = ctk.CTkFrame(self.emo_core_frame,fg_color=tlr_purple_1,width=100,corner_radius=0)
    self.emo_core_button = ctk.CTkButton(self.emo_core_frame,text="",corner_radius=0,
                                         command=lambda:show_emo_core(self),
                                         fg_color=tlr_purple_1,hover_color=tlr_purple_4,width=50,height=50)

    self.emo_core_text = ctk.CTkLabel(self.emo_data_frame, text=emo_title ,text_color=w_main_white, font=(fn_PM, 13))
    self.emo_core_info = ctk.CTkLabel(self.emo_data_frame, text=emo_info , text_color="grey",
                                      font=(fn_PM, 10))

    self.emo_core_frame.pack_propagate(False)
    self.emo_core_frame.pack(pady=10, fill="x",padx=(8,0))

    self.emo_data_frame.pack_propagate(False)
    self.emo_data_frame.pack(side=ctk.LEFT,fill="y")
    self.emo_core_button.pack(side=ctk.LEFT,fill="y")

    self.emo_core_text.pack(anchor="w",padx=(5,0))
    self.emo_core_info.pack(anchor="w",padx=(5,0))






    cc_title = "Content Creat"
    cc_info = "5 Songs . 16 mins"

    # CONTENT CREATION CORE ============ ============ ============= =============== =============
    self.cc_core_frame = ctk.CTkFrame(self.playlist_scroll, fg_color=tlr_purple_1, width=150, height=50)
    self.cc_data_frame = ctk.CTkFrame(self.cc_core_frame, fg_color=tlr_dark, width=100,corner_radius=0)
    self.cc_core_button = ctk.CTkButton(self.cc_core_frame, text="",
                                         command=lambda: show_cc_core(self),
                                         fg_color=tlr_dark,hover_color=tlr_purple_4,
                                         width=50, height=50,corner_radius=0)

    self.cc_core_text = ctk.CTkLabel(self.cc_data_frame, text=cc_title , text_color=w_main_white, font=(fn_PM, 13))
    self.cc_core_info = ctk.CTkLabel(self.cc_data_frame, text=cc_info, text_color="grey",
                                      font=(fn_PM, 10))

    self.cc_core_frame.pack_propagate(False)
    self.cc_core_frame.pack(pady=10, fill="x", padx=(8, 0))

    self.cc_data_frame.pack_propagate(False)
    self.cc_data_frame.pack(side=ctk.LEFT, fill="y")
    self.cc_core_button.pack(side=ctk.LEFT, fill="y")

    self.cc_core_text.pack(anchor="w", padx=(5, 0))
    self.cc_core_info.pack(anchor="w", padx=(5, 0))






    sadindie_title = "Sad Indie"
    sadindie_info = "6 Songs . 20 mins"

    # SAD INDIE  ============ ============ ============= =============== =============
    self.sadindie_core_frame = ctk.CTkFrame(self.playlist_scroll, fg_color=tlr_purple_1, width=150, height=50)
    self.sadindie_data_frame = ctk.CTkFrame(self.sadindie_core_frame, fg_color=tlr_dark, width=100,corner_radius=0)
    self.sadindie_core_button = ctk.CTkButton(self.sadindie_core_frame, text="",
                                         command=lambda: show_sad_indie(self),
                                         fg_color=tlr_dark,hover_color=tlr_purple_4,
                                         width=50, height=50,corner_radius=0)

    self.sadindie_core_text = ctk.CTkLabel(self.sadindie_data_frame, text=sadindie_title , text_color=w_main_white, font=(fn_PM, 13))
    self.sadindie_core_info = ctk.CTkLabel(self.sadindie_data_frame, text=sadindie_info, text_color="grey",
                                      font=(fn_PM, 10))

    self.sadindie_core_frame.pack_propagate(False)
    self.sadindie_core_frame.pack(pady=10, fill="x", padx=(8, 0))

    self.sadindie_data_frame.pack_propagate(False)
    self.sadindie_data_frame.pack(side=ctk.LEFT, fill="y")
    self.sadindie_core_button.pack(side=ctk.LEFT, fill="y")

    self.sadindie_core_text.pack(anchor="w", padx=(5, 0))
    self.sadindie_core_info.pack(anchor="w", padx=(5, 0))



    def show_emo_core(self):


        self.emo_data_frame.configure(fg_color=tlr_purple_1)
        self.emo_core_button.configure(fg_color=tlr_purple_1)

        self.cc_data_frame.configure(fg_color=tlr_dark)
        self.cc_core_button.configure(fg_color=tlr_dark)


        for widget in self.main_music_feed_wrapper.winfo_children():
            widget.destroy()

        self.lib_content_frame = ctk.CTkFrame(self.main_music_feed_wrapper, fg_color=tlr_dark)

        self.lib_content_frame.pack_propagate(False)
        self.lib_content_frame.pack(fill="both", expand=True)

        #
        self.emo_core_title_frame = ctk.CTkFrame(self.lib_content_frame,height=100,fg_color=tlr_dark)
        self.emo_hero_title = ctk.CTkLabel(self.emo_core_title_frame,
                                           text=emo_title,
                                           font=(fn_PM,60),
                                           text_color=w_f5)
        self.emo_hero_info = ctk.CTkLabel(self.emo_core_title_frame,
                                           text=emo_info,
                                           font=(fn_PM, 12),
                                           text_color="grey")
        self.emo_core_sframe = ctk.CTkScrollableFrame(self.lib_content_frame,height=200,
                                                      fg_color=tlr_dark,
                                                      orientation="horizontal",
                                                      scrollbar_button_color=tlr_dark,
                                                      scrollbar_button_hover_color=tlr_purple_2)


        # Emo Sframe Musics
        # BNB
        self.bulls_in_bronx_wrapper = ctk.CTkFrame(self.emo_core_sframe,width=170,height=200,
                                                   fg_color=tlr_dark)

        self.bulls_in_bronx_image = ctk.CTkImage(light_image=Image.open("Albums/Collide With The Sky 2.png"),
                                                   dark_image=Image.open("Albums/Collide With The Sky 2.png"),
                                                   size=(150,150))
        self.bulls_in_bronx_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Collide With The Sky BCKPPL2.png"),
                                                   dark_image=Image.open("Albums/Collide With The Sky BCKPPL2.png"),
                                                    size=(220, 200))

        self.bulls_in_bronx_holder = ctk.CTkButton(self.bulls_in_bronx_wrapper,text="",
                                                   command=lambda:play_music(self,"Musics/Bulls in the Bronx - Pierce the Veil.mp3",
                                                    "Pierce The Veil - Bulls In Bronx",self.bulls_in_bronx_image_pl),
                                                   image=self.bulls_in_bronx_image,
                                                   fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.bulls_in_bronx_artist = ctk.CTkLabel(self.bulls_in_bronx_wrapper,
                                                  text="Pierce The Veil",
                                                  text_color=w_f5,
                                                  font=(fn_PM,15))
        self.bulls_in_bronx_title = ctk.CTkLabel(self.bulls_in_bronx_wrapper,
                                                  text="Bulls In Bronx",
                                                  text_color="grey",
                                                  font=(fn_PR,12))

        self.bulls_in_bronx_wrapper.pack_propagate(False)
        self.bulls_in_bronx_wrapper.grid(row=0,column=1,pady=(0,10),padx=(0,10))
        self.bulls_in_bronx_holder.pack(fill="both",expand=True)
        self.bulls_in_bronx_artist.pack(anchor="w",padx=(24,0))
        self.bulls_in_bronx_title.pack(anchor="w",padx=(24,0))



        # DEAR MARIA COUNT ME IN
        self.dearmcmi_wrapper = ctk.CTkFrame(self.emo_core_sframe,width=170,height=200,
                                                   fg_color=tlr_dark)
        self.dearmcmi_image = ctk.CTkImage(light_image=Image.open("Albums/All Time Low A.png"),
                                                   dark_image=Image.open("Albums/All Time Low A.png"),
                                                   size=(150,150))
        self.dearmcmi_image_pl = ctk.CTkImage(light_image=Image.open("Albums/All Time Low A 2.png"),
                                                    dark_image=Image.open("Albums/All Time Low A 2.png"),
                                                    size=(220, 200))

        self.dearmcmi_holder = ctk.CTkButton(self.dearmcmi_wrapper,text="",
                                                   command=lambda:play_music(self,"Musics/Dear Maria Count Me In.mp3",
                                                   "All Time lOW - Dear Maria Count Me In",self.dearmcmi_image_pl),
                                                   image=self.dearmcmi_image,
                                                   fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.dearmcmi_artist = ctk.CTkLabel(self.dearmcmi_wrapper,
                                                  text="ALL Time Low",
                                                  text_color=w_f5,
                                                  font=(fn_PM,15))
        self.dearmcmi_title = ctk.CTkLabel(self.dearmcmi_wrapper,
                                                  text="Dear Maria Count Me In",
                                                  text_color="grey",
                                                  font=(fn_PR,12))

        self.dearmcmi_wrapper.pack_propagate(False)
        self.dearmcmi_wrapper.grid(row=0,column=2,pady=(0,10),padx=(10,10))
        self.dearmcmi_holder.pack(fill="both",expand=True)
        self.dearmcmi_artist.pack(anchor="w",padx=(24,0))
        self.dearmcmi_title.pack(anchor="w",padx=(24,0))




        # ALL WE KNOW IS FALLING
        self.allwekif_wrapper = ctk.CTkFrame(self.emo_core_sframe, width=170, height=200,
                                             fg_color=tlr_dark)
        self.allwekif_image = ctk.CTkImage(light_image=Image.open("Albums/All We Know Is Falling.png"),
                                           dark_image=Image.open("Albums/All We Know Is Falling.png"),
                                           size=(150, 150))
        self.allwekif_image_pl = ctk.CTkImage(light_image=Image.open("Albums/All We Know Is Falling B 2.png"),
                                              dark_image=Image.open("Albums/All We Know Is Falling B 2.png"),
                                              size=(220, 200))
        self.allwekif_holder = ctk.CTkButton(self.allwekif_wrapper, text="",
                                             command=lambda: play_music(self, "Musics/Paramore - My Heart.mp3",
                                                                        "Paramore - My Heart",
                                                                        self.allwekif_image_pl),
                                             image=self.allwekif_image,
                                             fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.allwekif_artist = ctk.CTkLabel(self.allwekif_wrapper,
                                            text="Paramore",
                                            text_color=w_f5,
                                            font=(fn_PM, 15))
        self.allwekif_title = ctk.CTkLabel(self.allwekif_wrapper,
                                           text="My Heart",
                                           text_color="grey",
                                           font=(fn_PR, 12))

        self.allwekif_wrapper.pack_propagate(False)
        self.allwekif_wrapper.grid(row=0, column=3, pady=(0, 10), padx=(10, 10))
        self.allwekif_holder.pack(fill="both", expand=True)
        self.allwekif_artist.pack(anchor="w",padx=(24,0))
        self.allwekif_title.pack(anchor="w",padx=(24,0))




        # APOLOGY
        self.apology_wrapper = ctk.CTkFrame(self.emo_core_sframe, width=170, height=200,
                                             fg_color=tlr_dark)
        self.apology_image = ctk.CTkImage(light_image=Image.open("Albums/Apology.png"),
                                           dark_image=Image.open("Albums/Apology.png"),
                                           size=(150, 150))
        self.apology_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Apology 2 .png"),
                                              dark_image=Image.open("Albums/Apology 2 .png"),
                                              size=(220, 200))
        self.apology_holder = ctk.CTkButton(self.apology_wrapper, text="",
                                             command=lambda: play_music(self, "Musics/Alesana - Apology (Punk Goes Acoustic Vol. 2).mp3",
                                             "Alesana - Apology",
                                             self.apology_image_pl),
                                             image=self.apology_image,
                                             fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.apology_artist = ctk.CTkLabel(self.apology_wrapper,
                                            text="Alesana",
                                            text_color=w_f5,
                                            font=(fn_PM, 15))
        self.apology_title = ctk.CTkLabel(self.apology_wrapper,
                                           text="Apology",
                                           text_color="grey",
                                           font=(fn_PR, 12))

        self.apology_wrapper.pack_propagate(False)
        self.apology_wrapper.grid(row=0, column=4, pady=(0, 10), padx=(10, 10))
        self.apology_holder.pack(fill="both", expand=True)
        self.apology_artist.pack(anchor="w",padx=(24,0))
        self.apology_title.pack(anchor="w",padx=(24,0))



        # Remembering Sunday
        self.remsun_wrapper = ctk.CTkFrame(self.emo_core_sframe, width=170, height=200,
                                            fg_color=tlr_dark)
        self.remsun_image = ctk.CTkImage(light_image=Image.open("Albums/All Time Low B .png"),
                                          dark_image=Image.open("Albums/All Time Low B .png"),
                                          size=(150, 150))
        self.remsun_image_pl = ctk.CTkImage(light_image=Image.open("Albums/All Time Low B 2 .png"),
                                             dark_image=Image.open("Albums/All Time Low B 2 .png"),
                                             size=(220, 200))
        self.remsun_holder = ctk.CTkButton(self.remsun_wrapper, text="",
                                           command=lambda: play_music(self,
                                           "Musics/All Time Low - Remembering Sunday ft. Juliet.mp3",
                                           "All Time Low - Remembering Sunday",
                                           self.remsun_image_pl),
                                           image=self.remsun_image,
                                           fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.remsun_artist = ctk.CTkLabel(self.remsun_wrapper,
                                           text="All Time Low",
                                           text_color=w_f5,
                                           font=(fn_PM, 15))
        self.remsun_title = ctk.CTkLabel(self.remsun_wrapper,
                                          text="Remembering Sunday",
                                          text_color="grey",
                                          font=(fn_PR, 12))

        self.remsun_wrapper.pack_propagate(False)
        self.remsun_wrapper.grid(row=0, column=5, pady=(0, 10), padx=(10, 10))
        self.remsun_holder.pack(fill="both", expand=True)
        self.remsun_artist.pack(anchor="w",padx=(24,0))
        self.remsun_title.pack(anchor="w",padx=(24,0))




        # DECEMBER
        self.dec_wrapper = ctk.CTkFrame(self.emo_core_sframe, width=170, height=200,
                                            fg_color=tlr_dark)
        self.dec_image = ctk.CTkImage(light_image=Image.open("Albums/December.png"),
                                          dark_image=Image.open("Albums/December.png"),
                                          size=(150, 150))
        self.dec_image_pl = ctk.CTkImage(light_image=Image.open("Albums/December.png"),
                                            dark_image=Image.open("Albums/December.png"),
                                            size=(220, 200))
        self.dec_holder = ctk.CTkButton(self.dec_wrapper, text="",
                                            command=lambda: play_music(self,
                                            "Musics/Neck Deep - December.mp3",
                                            "Neck Deep - December",
                                            self.dec_image_pl),
                                            image=self.dec_image,
                                            fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.dec_artist = ctk.CTkLabel(self.dec_wrapper,
                                           text="Neck Deep",
                                           text_color=w_f5,
                                           font=(fn_PM, 15))
        self.dec_title = ctk.CTkLabel(self.dec_wrapper,
                                          text="December",
                                          text_color="grey",
                                          font=(fn_PR, 12))

        self.dec_wrapper.pack_propagate(False)
        self.dec_wrapper.grid(row=0, column=6, pady=(0, 10), padx=(10, 10))
        self.dec_holder.pack(fill="both", expand=True)
        self.dec_artist.pack(anchor="w",padx=(24,0))
        self.dec_title.pack(anchor="w",padx=(24,0))



        # Flair Of The Dramatic
        self.fotd_wrapper = ctk.CTkFrame(self.emo_core_sframe, width=170, height=200,
                                            fg_color=tlr_dark)
        self.fotd_image = ctk.CTkImage(light_image=Image.open("Albums/Flair Of The Dramatic.png"),
                                          dark_image=Image.open("Albums/Flair Of The Dramatic.png"),
                                          size=(150, 150))
        self.fotd_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Flair Of The Dramatic.png"),
                                         dark_image=Image.open("Albums/Flair Of The Dramatic.png"),
                                         size=(220, 200))
        self.fotd_holder = ctk.CTkButton(self.fotd_wrapper, text="",
                                            command=lambda: play_music(self,
                                            "Musics/Pierce The Veil _Yeah Boy And Doll Face.mp3",
                                            "Pierce The Veil - Yeah Boy And Doll Face",
                                            self.fotd_image_pl),
                                            image=self.fotd_image,
                                            fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.fotd_artist = ctk.CTkLabel(self.fotd_wrapper,
                                           text="Pierce The Veil",
                                           text_color=w_f5,
                                           font=(fn_PM, 15))
        self.fotd_title = ctk.CTkLabel(self.fotd_wrapper,
                                          text="Yeah Boy And Doll Face",
                                          text_color="grey",
                                          font=(fn_PR, 12))

        self.fotd_wrapper.pack_propagate(False)
        self.fotd_wrapper.grid(row=0, column=7, pady=(0, 10), padx=(10, 10))
        self.fotd_holder.pack(fill="both", expand=True)
        self.fotd_artist.pack(anchor="w",padx=(24,0))
        self.fotd_title.pack(anchor="w",padx=(24,0))




        # Make Damn Sure
        self.mds_wrapper = ctk.CTkFrame(self.emo_core_sframe, width=170, height=200,
                                         fg_color=tlr_dark)
        self.mds_image = ctk.CTkImage(light_image=Image.open("Albums/Make Damn Sure.png"),
                                       dark_image=Image.open("Albums/Make Damn Sure.png"),
                                       size=(150, 150))
        self.mds_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Make Damn Sure.png"),
                                         dark_image=Image.open("Albums/Make Damn Sure.png"),
                                         size=(220, 200))
        self.mds_holder = ctk.CTkButton(self.mds_wrapper, text="",
                                         command = lambda: play_music(self,
                                         "Musics/Taking Back Sunday - MakeDamnSure.mp3",
                                         "Taking Back Sunday - MakeDamnSure",
                                         self.mds_image_pl),
                                         image=self.mds_image,
                                         fg_color=tlr_dark,hover_color=tlr_purple_1)
        
        self.mds_artist = ctk.CTkLabel(self.mds_wrapper,
                                        text="Taking Back Sun",
                                        text_color=w_f5,
                                        font=(fn_PM, 15))
        self.mds_title = ctk.CTkLabel(self.mds_wrapper,
                                       text="Make Damn Sure",
                                       text_color="grey",
                                       font=(fn_PR, 12))

        self.mds_wrapper.pack_propagate(False)
        self.mds_wrapper.grid(row=0, column=8, pady=(0, 10), padx=(10, 10))
        self.mds_holder.pack(fill="both", expand=True)
        self.mds_artist.pack(anchor="w",padx=(24,0))
        self.mds_title.pack(anchor="w",padx=(24,0))



    
        # Roger Rabit
        self.rr_wrapper = ctk.CTkFrame(self.emo_core_sframe, width=170, height=200,
                                        fg_color=tlr_dark)
        self.rr_image = ctk.CTkImage(light_image=Image.open("Albums/Roger Rabbit.png"),
                                      dark_image=Image.open("Albums/Roger Rabbit.png"),
                                      size=(150, 150))
        self.rr_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Roger Rabbit.png"),
                                         dark_image=Image.open("Albums/Roger Rabbit.png"),
                                         size=(220, 200))
        self.rr_holder = ctk.CTkButton(self.rr_wrapper, text="",
                                        command=lambda: play_music(self,
                                        "Musics/Sleeping With Sirens - Roger Rabbit.mp3",
                                        "Sleeping With Sirens - Roger Rabbit",
                                        self.rr_image_pl),
                                        image=self.rr_image,
                                        fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.rr_artist = ctk.CTkLabel(self.rr_wrapper,
                                       text="Sleeping With Sir",
                                       text_color=w_f5,
                                       font=(fn_PM, 15))
        self.rr_title = ctk.CTkLabel(self.rr_wrapper,
                                      text="Roger Rabit",
                                      text_color="grey",
                                      font=(fn_PR, 12))

        self.rr_wrapper.pack_propagate(False)
        self.rr_wrapper.grid(row=0, column=9, pady=(0, 10), padx=(10, 10))
        self.rr_holder.pack(fill="both", expand=True)
        self.rr_artist.pack(anchor="w",padx=(24,0))
        self.rr_title.pack(anchor="w",padx=(24,0))




        # Wish You Were Here
        self.wywh_wrapper = ctk.CTkFrame(self.emo_core_sframe, width=170, height=200,
                                       fg_color=tlr_dark)
        self.wywh_image = ctk.CTkImage(light_image=Image.open("Albums/Wish You Were Here.png"),
                                     dark_image=Image.open("Albums/Wish You Were Here.png"),
                                     size=(150, 150))
        self.wywh_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Wish You Were Here.png"),
                                        dark_image=Image.open("Albums/Wish You Were Here.png"),
                                        size=(220, 200))
        self.wywh_holder = ctk.CTkButton(self.wywh_wrapper, text="",
                                       command=lambda: play_music(self,
                                       "Musics/Wish You Were Here.mp3",
                                       "Neck Deep - Wish You Were Here",
                                        self.wywh_image_pl),
                                       image=self.wywh_image,
                                       fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.wywh_artist = ctk.CTkLabel(self.wywh_wrapper,
                                      text="Neck Deep",
                                      text_color=w_f5,
                                      font=(fn_PM, 15))
        self.wywh_title = ctk.CTkLabel(self.wywh_wrapper,
                                     text="Wish You Were Here",
                                     text_color="grey",
                                     font=(fn_PR, 12))

        self.wywh_wrapper.pack_propagate(False)
        self.wywh_wrapper.grid(row=0, column=10, pady=(0, 10), padx=(10, 10))
        self.wywh_holder.pack(fill="both", expand=True)
        self.wywh_artist.pack(anchor="w",padx=(24,0))
        self.wywh_title.pack(anchor="w",padx=(24,0))




        # EMO MUSIC LIST ===========  ===========   ===========  ===========  ===========  ===========
        self.emo_core_music_list = ctk.CTkFrame(self.lib_content_frame,height=500,fg_color=tlr_dark)
        self.emo_core_list_title_frame = ctk.CTkFrame(self.emo_core_music_list,fg_color=tlr_dark,height=50)
        self.emo_core_title = ctk.CTkLabel(self.emo_core_list_title_frame,
                                           text="All Songs",text_color=w_f5,font=(fn_PM,20))

        self.emo_core_scroll_frame = ctk.CTkScrollableFrame(self.emo_core_music_list,fg_color=tlr_dark,
                                                            scrollbar_button_color=tlr_dark,
                                                            scrollbar_button_hover_color=tlr_purple_2,
                                                            height=450)

        self.emo_core_list_title_frame.pack_propagate(False)
        self.emo_core_scroll_frame.pack_propagate(False)
        self.emo_core_list_title_frame.pack(fill="x",expand=True)
        self.emo_core_title.pack(side=ctk.LEFT,pady=10,padx=25)
        self.emo_core_scroll_frame.pack(fill="both",expand=True)





        # BULLS IN BRONX
        self.bnb_list_wrapper = ctk.CTkFrame(self.emo_core_scroll_frame,height=50,width=655,
                                             corner_radius=20,fg_color=tlr_dark)
        self.bnb_list_image = ctk.CTkImage(light_image=Image.open("Albums/Collide With The Sky 2.png"),
                                           dark_image=Image.open("Albums/Collide With The Sky 2.png"),
                                           size=(50,50))
        self.bnb_list_holder = ctk.CTkButton(self.bnb_list_wrapper,text=f"4:27",
                                            command=lambda: play_music(self,
                                            "Musics/Bulls in the Bronx - Pierce the Veil.mp3",
                                            "Pierce The Veil - Bulls In Bronx",
                                            self.bulls_in_bronx_image_pl),
                                            text_color="grey",font=(fn_PR,12),
                                            fg_color=tlr_dark,hover_color=tlr_purple_1,
                                            corner_radius=20,width=655,height=50)
        self.bnb_image_holder = ctk.CTkButton(self.bnb_list_holder,text="",
                                              command=lambda: play_music(self,
                                              "Musics/Bulls in the Bronx - Pierce the Veil.mp3",
                                              "Pierce The Veil - Bulls In Bronx",
                                              self.bulls_in_bronx_image_pl),
                                              image=self.bnb_list_image,width=50,
                                              fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.bnb_list_info_frame = ctk.CTkButton(self.bnb_list_holder,text="",
                                                 command=lambda: play_music(self,
                                                 "Musics/Bulls in the Bronx - Pierce the Veil.mp3",
                                                 "Pierce The Veil - Bulls In Bronx",
                                                 self.bulls_in_bronx_image_pl),
                                                 width=150,height=50,hover_color=tlr_purple_1,fg_color=tlr_dark)
        self.bnb_list_author = ctk.CTkLabel(self.bnb_list_info_frame,text="Pircce The Veil",
                                            text_color=w_f5,font=(fn_PM, 15))
        self.bnb_list_title = ctk.CTkLabel(self.bnb_list_info_frame, text="Bulls In Bronx",
                                           text_color="grey",
                                           font=(fn_PR, 12))


        self.bnb_list_wrapper.pack_propagate(False)
        self.bnb_list_holder.pack_propagate(False)
        self.bnb_list_info_frame.pack_propagate(False)
        self.bnb_list_wrapper.grid(padx=10,pady=10)
        self.bnb_list_holder.pack(fill="both",expand=True)
        self.bnb_image_holder.pack(anchor="w",side=ctk.LEFT)
        self.bnb_list_info_frame.pack(anchor="w",side=ctk.LEFT)
        self.bnb_list_author.pack(anchor="w")
        self.bnb_list_title.pack(anchor="w")





        # DEAR MARIA COUNT ME IN
        self.dearm_list_wrapper = ctk.CTkFrame(self.emo_core_scroll_frame, height=50, width=655,
                                             corner_radius=20, fg_color=tlr_dark)
        self.dearm_list_image = ctk.CTkImage(light_image=Image.open("Albums/All Time Low A.png"),
                                           dark_image=Image.open("Albums/All Time Low A.png"),
                                           size=(50, 50))
        self.dearm_list_holder = ctk.CTkButton(self.dearm_list_wrapper, text=f"3:02",
                                            command=lambda: play_music(self,
                                            "Musics/Dear Maria Count Me In.mp3",
                                            "All Time Low - Dear Maria Count Me In",
                                            self.dearmcmi_image_pl),
                                            text_color="grey", font=(fn_PR, 12),
                                            fg_color=tlr_dark, hover_color=tlr_purple_1,
                                            corner_radius=20, width=655, height=50)
        self.dearm_image_holder = ctk.CTkButton(self.dearm_list_holder, text="",
                                                command=lambda: play_music(self,
                                                                           "Musics/Dear Maria Count Me In.mp3",
                                                                           "All Time Low - Dear Maria Count Me In",
                                                                           self.dearmcmi_image_pl),
                                            image=self.dearm_list_image, width=50,
                                              fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.dearm_list_info_frame = ctk.CTkButton(self.dearm_list_holder, text="",
                                                   command=lambda: play_music(self,
                                                   "Musics/Dear Maria Count Me In.mp3",
                                                    "All Time Low - Dear Maria Count Me In",
                                                    self.dearmcmi_image_pl),
                                                    width=150, height=50, hover_color=tlr_purple_1, fg_color=tlr_dark)
        self.dearm_list_author = ctk.CTkLabel(self.dearm_list_info_frame, text="All Time Low",
                                            text_color=w_f5, font=(fn_PM, 15))
        self.dearm_list_title = ctk.CTkLabel(self.dearm_list_info_frame, text="Dear Maria Count Me In",
                                           text_color="grey",
                                           font=(fn_PR, 12))

        self.dearm_list_wrapper.pack_propagate(False)
        self.dearm_list_holder.pack_propagate(False)
        self.dearm_list_info_frame.pack_propagate(False)
        self.dearm_list_wrapper.grid(padx=10, pady=10)
        self.dearm_list_holder.pack(fill="both", expand=True)
        self.dearm_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.dearm_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.dearm_list_author.pack(anchor="w")
        self.dearm_list_title.pack(anchor="w")






        # MY HEART
        self.myheart_list_wrapper = ctk.CTkFrame(self.emo_core_scroll_frame, height=50, width=655,
                                               corner_radius=20, fg_color=tlr_dark)
        self.myheart_list_image = ctk.CTkImage(light_image=Image.open("Albums/All We Know Is Falling.png"),
                                             dark_image=Image.open("Albums/All We Know Is Falling.png"),
                                             size=(50, 50))
        self.myheart_list_holder = ctk.CTkButton(self.myheart_list_wrapper, text=f"4:27",
                                                 command=lambda: play_music(self,
                                                                            "Musics/Paramore - My Heart.mp3",
                                                                            "Paramore - My Heart",
                                                                            self.allwekif_image_pl),
                                                text_color="grey",
                                               font=(fn_PR, 12),
                                               fg_color=tlr_dark, hover_color=tlr_purple_1,
                                               corner_radius=20, width=655, height=50)
        self.myheart_image_holder = ctk.CTkButton(self.myheart_list_holder, text="",
                                                command=lambda: play_music(self,
                                                                             "Musics/Paramore - My Heart.mp3",
                                                                             "Paramore - My Heart",
                                                                             self.allwekif_image_pl),
                                                image=self.myheart_list_image, width=50,
                                                fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.myheart_list_info_frame = ctk.CTkButton(self.myheart_list_holder, text="",
                                                     command=lambda: play_music(self,
                                                                                "Musics/Paramore - My Heart.mp3",
                                                                                "Paramore - My Heart",
                                                                                self.allwekif_image_pl),
                                                   width=150, height=50, hover_color=tlr_purple_1, fg_color=tlr_dark)
        self.myheart_list_author = ctk.CTkLabel(self.myheart_list_info_frame, text="Paramore",
                                              text_color=w_f5, font=(fn_PM, 15))
        self.myheart_list_title = ctk.CTkLabel(self.myheart_list_info_frame, text="My Heart",
                                             text_color="grey",
                                             font=(fn_PR, 12))

        self.myheart_list_wrapper.pack_propagate(False)
        self.myheart_list_holder.pack_propagate(False)
        self.myheart_list_info_frame.pack_propagate(False)
        self.myheart_list_wrapper.grid(padx=10, pady=10)
        self.myheart_list_holder.pack(fill="both", expand=True)
        self.myheart_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.myheart_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.myheart_list_author.pack(anchor="w")
        self.myheart_list_title.pack(anchor="w")





        # APOLOGY
        self.apology_list_wrapper = ctk.CTkFrame(self.emo_core_scroll_frame, height=50, width=655,
                                                 corner_radius=20, fg_color=tlr_dark)
        self.apology_list_image = ctk.CTkImage(light_image=Image.open("Albums/Apology.png"),
                                               dark_image=Image.open("Albums/Apology.png"),
                                               size=(50, 50))
        self.apology_list_holder = ctk.CTkButton(self.apology_list_wrapper, text=f"3:59",
                                                 command=lambda: play_music(self,
                                                                            "Musics/Alesana - Apology (Punk Goes Acoustic Vol. 2).mp3",
                                                                            "Alesana - Apology",
                                                                            self.apology_image_pl),
                                                 text_color="grey",
                                                 font=(fn_PR, 12),
                                                 fg_color=tlr_dark, hover_color=tlr_purple_1,
                                                 corner_radius=20, width=655, height=50)
        self.apology_image_holder = ctk.CTkButton(self.apology_list_holder, text="",
                                                  command=lambda: play_music(self,
                                                                             "Musics/Alesana - Apology (Punk Goes Acoustic Vol. 2).mp3",
                                                                             "Alesana - Apology",
                                                                             self.apology_image_pl),
                                                  image=self.apology_list_image,
                                                  width=50,
                                                  fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.apology_list_info_frame = ctk.CTkButton(self.apology_list_holder, text="",
                                                     command=lambda: play_music(self,
                                                                                "Musics/Alesana - Apology (Punk Goes Acoustic Vol. 2).mp3",
                                                                                "Alesana - Apology",
                                                                                self.apology_image_pl),
                                                     width=150, height=50, hover_color=tlr_purple_1, fg_color=tlr_dark)
        self.apology_list_author = ctk.CTkLabel(self.apology_list_info_frame, text="Alesana",
                                                text_color=w_f5, font=(fn_PM, 15))
        self.apology_list_title = ctk.CTkLabel(self.apology_list_info_frame, text="Apology",
                                               text_color="grey",
                                               font=(fn_PR, 12))

        self.apology_list_wrapper.pack_propagate(False)
        self.apology_list_holder.pack_propagate(False)
        self.apology_list_info_frame.pack_propagate(False)
        self.apology_list_wrapper.grid(padx=10, pady=10)
        self.apology_list_holder.pack(fill="both", expand=True)
        self.apology_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.apology_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.apology_list_author.pack(anchor="w")
        self.apology_list_title.pack(anchor="w")


        # REMEMBERING SUNDAY
        self.remsun_list_wrapper = ctk.CTkFrame(self.emo_core_scroll_frame, height=50, width=655,
                                                corner_radius=20, fg_color=tlr_dark)
        self.remsun_list_image = ctk.CTkImage(light_image=Image.open("Albums/All Time Low B .png"),
                                              dark_image=Image.open("Albums/All Time Low B .png"),
                                              size=(50, 50))
        self.remsun_list_holder = ctk.CTkButton(self.remsun_list_wrapper, text=f"4:16",
                                                command=lambda: play_music(self,
                                                                           "Musics/All Time Low - Remembering Sunday ft. Juliet.mp3",
                                                                           "All Time Low - Remembering Sunday",
                                                                           self.remsun_image_pl),
                                                text_color="grey",
                                                font=(fn_PR, 12),
                                                fg_color=tlr_dark, hover_color=tlr_purple_1,
                                                corner_radius=20, width=655, height=50)
        self.remsun_image_holder = ctk.CTkButton(self.remsun_list_holder, text="",
                                                 command=lambda: play_music(self,
                                                                            "Musics/All Time Low - Remembering Sunday ft. Juliet.mp3",
                                                                            "All Time Low - Remembering Sunday",
                                                                            self.remsun_image_pl),
                                                 image=self.remsun_list_image,
                                                 width=50,
                                                 fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.remsun_list_info_frame = ctk.CTkButton(self.remsun_list_holder, text="",
                                                    command=lambda: play_music(self,
                                                                               "Musics/All Time Low - Remembering Sunday ft. Juliet.mp3",
                                                                               "All Time Low - Remembering Sunday",
                                                                               self.remsun_image_pl),
                                                    width=150, height=50, hover_color=tlr_purple_1, fg_color=tlr_dark)
        self.remsun_list_author = ctk.CTkLabel(self.remsun_list_info_frame, text="All Time Low",
                                               text_color=w_f5, font=(fn_PM, 15))
        self.remsun_list_title = ctk.CTkLabel(self.remsun_list_info_frame, text="Remembering Sunday",
                                              text_color="grey",
                                              font=(fn_PR, 12))

        self.remsun_list_wrapper.pack_propagate(False)
        self.remsun_list_holder.pack_propagate(False)
        self.remsun_list_info_frame.pack_propagate(False)
        self.remsun_list_wrapper.grid(padx=10, pady=10)
        self.remsun_list_holder.pack(fill="both", expand=True)
        self.remsun_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.remsun_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.remsun_list_author.pack(anchor="w")
        self.remsun_list_title.pack(anchor="w")




        # DECEMBER
        self.dec_list_wrapper = ctk.CTkFrame(self.emo_core_scroll_frame, height=50, width=655,
                                             corner_radius=20, fg_color=tlr_dark)
        self.dec_list_image = ctk.CTkImage(light_image=Image.open("Albums/December.png"),
                                           dark_image=Image.open("Albums/December.png"),
                                           size=(50, 50))
        self.dec_list_holder = ctk.CTkButton(self.dec_list_wrapper, text=f"3:39",
                                             command=lambda: play_music(self,
                                                                        "Musics/Neck Deep - December.mp3",
                                                                        "Neck Deep - December", self.dec_image_pl),
                                             text_color="grey",
                                             font=(fn_PR, 12),
                                             fg_color=tlr_dark, hover_color=tlr_purple_1,
                                             corner_radius=20, width=655, height=50)
        self.dec_image_holder = ctk.CTkButton(self.dec_list_holder, text="",
                                              command=lambda: play_music(self,
                                                                         "Musics/Neck Deep - December.mp3",
                                                                         "Neck Deep - December",self.dec_image_pl),
                                              image=self.dec_list_image,
                                              width=50,
                                              fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.dec_list_info_frame = ctk.CTkButton(self.dec_list_holder, text="",
                                                 command=lambda: play_music(self,
                                                "Musics/Neck Deep - December.mp3",
                                                "Neck Deep - December",
                                                self.dec_image_pl),
                                                width=150, height=50, hover_color=tlr_purple_1, fg_color=tlr_dark)
        self.dec_list_author = ctk.CTkLabel(self.dec_list_info_frame, text="Neck Deep",
                                            text_color=w_f5, font=(fn_PM, 15))
        self.dec_list_title = ctk.CTkLabel(self.dec_list_info_frame, text="December",
                                           text_color="grey",
                                           font=(fn_PR, 12))

        self.dec_list_wrapper.pack_propagate(False)
        self.dec_list_holder.pack_propagate(False)
        self.dec_list_info_frame.pack_propagate(False)
        self.dec_list_wrapper.grid(padx=10, pady=10)
        self.dec_list_holder.pack(fill="both", expand=True)
        self.dec_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.dec_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.dec_list_author.pack(anchor="w")
        self.dec_list_title.pack(anchor="w")



        # YEAH BOY AND DOLL FACE
        self.yeahboy_list_wrapper = ctk.CTkFrame(self.emo_core_scroll_frame, height=50, width=655,
                                             corner_radius=20, fg_color=tlr_dark)
        self.yeahboy_list_image = ctk.CTkImage(light_image=Image.open("Albums/Flair Of The Dramatic.png"),
                                           dark_image=Image.open("Albums/Flair Of The Dramatic.png"),
                                           size=(50, 50))
        self.yeahboy_list_holder = ctk.CTkButton(self.yeahboy_list_wrapper, text=f"4:24",
                                            command=lambda: play_music(self,
                                                                            "Musics/Pierce The Veil _Yeah Boy And Doll Face.mp3",
                                                                            "Pierce The Veil - Yeah Boy And Doll Face",
                                                                            self.fotd_image_pl),
                                             text_color="grey",
                                             font=(fn_PR, 12),
                                             fg_color=tlr_dark, hover_color=tlr_purple_1,
                                             corner_radius=20, width=655, height=50)
        self.yeahboy_image_holder = ctk.CTkButton(self.yeahboy_list_holder, text="",
                                              command=lambda: play_music(self,
                                                                             "Musics/Pierce The Veil _Yeah Boy And Doll Face.mp3",
                                                                             "Pierce The Veil - Yeah Boy And Doll Face",
                                                                             self.fotd_image_pl),
                                              image=self.yeahboy_list_image,
                                              width=50,
                                              fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.yeahboy_list_info_frame = ctk.CTkButton(self.yeahboy_list_holder, text="",
                                                     command=lambda: play_music(self,
                                                                                "Musics/Pierce The Veil _Yeah Boy And Doll Face.mp3",
                                                                                "Pierce The Veil - Yeah Boy And Doll Face",
                                                                                self.fotd_image_pl),
                                                 width=150, height=50, hover_color=tlr_purple_1, fg_color=tlr_dark)
        self.yeahboy_list_author = ctk.CTkLabel(self.yeahboy_list_info_frame, text="Pierce The Veil",
                                            text_color=w_f5, font=(fn_PM, 15))
        self.yeahboy_list_title = ctk.CTkLabel(self.yeahboy_list_info_frame, text="Yeah Boy And Doll Face",
                                           text_color="grey",
                                           font=(fn_PR, 12))



        self.yeahboy_list_wrapper.pack_propagate(False)
        self.yeahboy_list_holder.pack_propagate(False)
        self.yeahboy_list_info_frame.pack_propagate(False)
        self.yeahboy_list_wrapper.grid(padx=10, pady=10)
        self.yeahboy_list_holder.pack(fill="both", expand=True)
        self.yeahboy_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.yeahboy_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.yeahboy_list_author.pack(anchor="w")
        self.yeahboy_list_title.pack(anchor="w")





        # MAKE DAMN SURE
        self.makedamnsure_list_wrapper = ctk.CTkFrame(self.emo_core_scroll_frame, height=50, width=655,
                                                 corner_radius=20, fg_color=tlr_dark)
        self.makedamnsure_list_image = ctk.CTkImage(light_image=Image.open("Albums/Make Damn Sure.png"),
                                               dark_image=Image.open("Albums/Make Damn Sure.png"),
                                               size=(50, 50))
        self.makedamnsure_list_holder = ctk.CTkButton(self.makedamnsure_list_wrapper, text=f"3:29",
                                                 command=lambda: play_music(self,
                                                 "Musics/Taking Back Sunday - MakeDamnSure.mp3",
                                                 "Taking Back Sunday - MakeDamnSure",   self.mds_image_pl),
                                                 text_color="grey",
                                                 font=(fn_PR, 12),
                                                 fg_color=tlr_dark, hover_color=tlr_purple_1,
                                                 corner_radius=20, width=655, height=50)
        self.makedamnsure_image_holder = ctk.CTkButton(self.makedamnsure_list_holder, text="",
                                                 command=lambda: play_music(self,
                                                 "Musics/Taking Back Sunday - MakeDamnSure.mp3",
                                                 "Taking Back Sunday - MakeDamnSure", self.mds_image_pl),
                                                 image=self.makedamnsure_list_image,
                                                 width=50,
                                                 fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.makedamnsure_list_info_frame = ctk.CTkButton(self.makedamnsure_list_holder, text="",
                                                command=lambda: play_music(self,
                                                "Musics/Taking Back Sunday - MakeDamnSure.mp3",
                                                "Taking Back Sunday - MakeDamnSure", self.mds_image_pl),
                                                width=150, height=50, hover_color=tlr_purple_1, fg_color=tlr_dark)
        self.makedamnsure_list_author = ctk.CTkLabel(self.makedamnsure_list_info_frame, text="Taking Back Sunday",
                                                text_color=w_f5, font=(fn_PM, 15))
        self.makedamnsure_list_title = ctk.CTkLabel(self.makedamnsure_list_info_frame, text="Make Damn Sure",
                                               text_color="grey",
                                               font=(fn_PR, 12))

        self.makedamnsure_list_wrapper.pack_propagate(False)
        self.makedamnsure_list_holder.pack_propagate(False)
        self.makedamnsure_list_info_frame.pack_propagate(False)
        self.makedamnsure_list_wrapper.grid(padx=10, pady=10)
        self.makedamnsure_list_holder.pack(fill="both", expand=True)
        self.makedamnsure_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.makedamnsure_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.makedamnsure_list_author.pack(anchor="w")
        self.makedamnsure_list_title.pack(anchor="w")



        # ROGER RABIT
        self.rr_list_wrapper = ctk.CTkFrame(self.emo_core_scroll_frame, height=50, width=655,
                                                      corner_radius=20, fg_color=tlr_dark)
        self.rr_list_image = ctk.CTkImage(light_image=Image.open("Albums/Roger Rabbit.png"),
                                                    dark_image=Image.open("Albums/Roger Rabbit.png"),
                                                    size=(50, 50))
        self.rr_list_holder = ctk.CTkButton(self.rr_list_wrapper, text=f"3:20", text_color="grey",
                                            command=lambda: play_music(self,
                                                                       "Musics/Sleeping With Sirens - Roger Rabbit.mp3",
                                                                       "Sleeping With Sirens - Roger Rabbit",
                                                                       self.rr_image_pl),
                                                      font=(fn_PR, 12),
                                                      fg_color=tlr_dark, hover_color=tlr_purple_1,
                                                      corner_radius=20, width=655, height=50)
        self.rr_image_holder = ctk.CTkButton(self.rr_list_holder, text="",
                                             command=lambda: play_music(self,
                                                                        "Musics/Sleeping With Sirens - Roger Rabbit.mp3",
                                                                        "Sleeping With Sirens - Roger Rabbit",
                                                                        self.rr_image_pl),
                                                       image=self.rr_list_image,
                                                       width=50,
                                                       fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.rr_list_info_frame = ctk.CTkButton(self.rr_list_holder, text="",
                                                command=lambda: play_music(self,
                                                                           "Musics/Sleeping With Sirens - Roger Rabbit.mp3",
                                                                             "Sleeping With Sirens - Roger Rabbit",
                                                                           self.rr_image_pl),
                                                          width=150, height=50, hover_color=tlr_purple_1,
                                                          fg_color=tlr_dark)
        self.rr_list_author = ctk.CTkLabel(self.rr_list_info_frame, text="Sleeping In Sirens",
                                                     text_color=w_f5, font=(fn_PM, 15))
        self.rr_list_title = ctk.CTkLabel(self.rr_list_info_frame, text="Roger Rabbit",
                                                    text_color="grey",
                                                    font=(fn_PR, 12))

        self.rr_list_wrapper.pack_propagate(False)
        self.rr_list_holder.pack_propagate(False)
        self.rr_list_info_frame.pack_propagate(False)
        self.rr_list_wrapper.grid(padx=10, pady=10)
        self.rr_list_holder.pack(fill="both", expand=True)
        self.rr_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.rr_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.rr_list_author.pack(anchor="w")
        self.rr_list_title.pack(anchor="w")




        # WISH YOU WERE HERE
        self.wywr_list_wrapper = ctk.CTkFrame(self.emo_core_scroll_frame, height=50, width=655,
                                            corner_radius=20, fg_color=tlr_dark)
        self.wywr_list_image = ctk.CTkImage(light_image=Image.open("Albums/Wish You Were Here.png"),
                                          dark_image=Image.open("Albums/Wish You Were Here.png"),
                                          size=(50, 50))
        self.wywr_list_holder = ctk.CTkButton(self.wywr_list_wrapper, text=f"4:08", text_color="grey",
                                             command=lambda: play_music(self,
                                             "Musics/Wish You Were Here.mp3",
                                             "Neck Deep - Wish You Were Here",
                                             self.wywh_image_pl),
                                             font=(fn_PR, 12),
                                             fg_color=tlr_dark, hover_color=tlr_purple_1,
                                             corner_radius=20, width=655, height=50)
        self.wywr_image_holder = ctk.CTkButton(self.wywr_list_holder, text="",
                                             command=lambda: play_music(self,
                                            "Musics/Wish You Were Here.mp3",
                                            "Neck Deep - Wish You Were Here",
                                             self.wywh_image_pl),
                                             image=self.wywr_list_image,
                                             width=50,
                                             fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.wywr_list_info_frame = ctk.CTkButton(self.wywr_list_holder, text="",
                                                command=lambda: play_music(self,
                                                "Musics/Wish You Were Here.mp3",
                                                "Neck Deep - Wish You Were Here",
                                                self.wywh_image_pl),
                                                width=150, height=50, hover_color=tlr_purple_1,
                                                fg_color=tlr_dark)
        self.wywr_list_author = ctk.CTkLabel(self.wywr_list_info_frame, text="Neck Deep",
                                           text_color=w_f5, font=(fn_PM, 15))
        self.wywr_list_title = ctk.CTkLabel(self.wywr_list_info_frame, text="Wish You Were Here",
                                          text_color="grey",
                                          font=(fn_PR, 12))

        self.wywr_list_wrapper.pack_propagate(False)
        self.wywr_list_holder.pack_propagate(False)
        self.wywr_list_info_frame.pack_propagate(False)
        self.wywr_list_wrapper.grid(padx=10, pady=10)
        self.wywr_list_holder.pack(fill="both", expand=True)
        self.wywr_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.wywr_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.wywr_list_author.pack(anchor="w")
        self.wywr_list_title.pack(anchor="w")





        # packing
        self.emo_core_title_frame.pack_propagate(False)
        self.emo_core_music_list.pack_propagate(False)

        self.emo_core_title_frame.pack(fill="x",expand=True)
        self.emo_hero_title.pack(anchor="w",side=ctk.LEFT,padx=(20,0))
        self.emo_hero_info.pack(anchor="w",side=ctk.LEFT,padx=(10,0),pady=(25,0))

        self.emo_core_sframe.pack(fill="x",expand=True)
        self.emo_core_music_list.pack(fill="both",expand=True)












    def show_cc_core(self):

        self.emo_data_frame.configure(fg_color=tlr_dark)
        self.emo_core_button.configure(fg_color=tlr_dark)

        self.cc_data_frame.configure(fg_color=tlr_purple_1)
        self.cc_core_button.configure(fg_color=tlr_purple_1)

        self.sadindie_data_frame.configure(fg_color=tlr_dark)
        self.sadindie_core_button.configure(fg_color=tlr_dark)

        for widget in self.main_music_feed_wrapper.winfo_children():
            widget.destroy()

        self.lib_content_frame = ctk.CTkFrame(self.main_music_feed_wrapper, fg_color=tlr_dark)
        self.lib_content_frame.pack_propagate(False)
        self.lib_content_frame.pack(fill="both", expand=True)

        #
        self.cc_core_title_frame = ctk.CTkFrame(self.lib_content_frame, height=100, fg_color=tlr_dark)
        self.cc_hero_title = ctk.CTkLabel(self.cc_core_title_frame,
                                           text="Content Creation",
                                           font=(fn_PM, 60),
                                           text_color=w_f5)
        self.cc_hero_info = ctk.CTkLabel(self.cc_core_title_frame,
                                          text="5 songs . 20 mins",
                                          font=(fn_PM, 12),
                                          text_color="grey")
        self.cc_core_sframe = ctk.CTkScrollableFrame(self.lib_content_frame, height=200,
                                                      fg_color=tlr_dark,
                                                      orientation="horizontal",
                                                      scrollbar_button_color=tlr_dark,
                                                      scrollbar_button_hover_color=tlr_purple_2)



        # CATS WALKING
        self.cats_walk_wrapper = ctk.CTkFrame(self.cc_core_sframe, width=170, height=200,
                                                   fg_color=tlr_dark)

        self.cats_walk_image = ctk.CTkImage(light_image=Image.open("Albums/Cats Walking.png"),
                                                 dark_image=Image.open("Albums/Cats Walking.png"),
                                                 size=(150, 150))
        self.cats_walk_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Cats Walking 2.png"),
                                                    dark_image=Image.open("Albums/Cats Walking 2.png"),
                                                    size=(220, 200))

        self.cats_walk_holder = ctk.CTkButton(self.cats_walk_wrapper, text="",
                                                   command=lambda: play_music(self,
                                                                              "Musics/Yomoti - Cats Walking.mp3",
                                                                              "Yomoti - Cats Walking",
                                                                              self.cats_walk_image_pl),
                                                   image=self.cats_walk_image,
                                                   fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.cats_walk_artist = ctk.CTkLabel(self.cats_walk_wrapper,
                                                  text="Yomoti",
                                                  text_color=w_f5,
                                                  font=(fn_PM, 15))
        self.cats_walk_title = ctk.CTkLabel(self.cats_walk_wrapper,
                                                 text="Cats Walking",
                                                 text_color="grey",
                                                 font=(fn_PR, 12))

        self.cats_walk_wrapper.pack_propagate(False)
        self.cats_walk_wrapper.grid(row=0, column=1, pady=(0, 10), padx=(0, 10))
        self.cats_walk_holder.pack(fill="both", expand=True)
        self.cats_walk_artist.pack(anchor="w",padx=(24,0))
        self.cats_walk_title.pack(anchor="w",padx=(24,0))




        # BLODD REN SUN RIOT
        self.orwar_wrapper = ctk.CTkFrame(self.cc_core_sframe, width=170, height=200,
                                             fg_color=tlr_dark)
        self.orwar_image = ctk.CTkImage(light_image=Image.open("Albums/BRS Orange Warning.png"),
                                           dark_image=Image.open("Albums/BRS Orange Warning.png"),
                                           size=(150, 150))
        self.orwar_image_pl = ctk.CTkImage(light_image=Image.open("Albums/BRS Orange Warning 2.png"),
                                              dark_image=Image.open("Albums/BRS Orange Warning 2.png"),
                                              size=(220, 200))

        self.orwar_holder = ctk.CTkButton(self.orwar_wrapper, text="",
                                             command=lambda: play_music(self, "Musics/Blood Red Sun - Orange Warnings.mp3",
                                                                        "Blood Red Sun - Orange Warnings",
                                                                        self.orwar_image_pl),
                                             image=self.orwar_image,
                                             fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.orwar_artist = ctk.CTkLabel(self.orwar_wrapper,
                                            text="Blood Red Sun",
                                            text_color=w_f5,
                                            font=(fn_PM, 15))
        self.orwar_title = ctk.CTkLabel(self.orwar_wrapper,
                                           text="Orange Warnings",
                                           text_color="grey",
                                           font=(fn_PR, 12))

        self.orwar_wrapper.pack_propagate(False)
        self.orwar_wrapper.grid(row=0, column=2, pady=(0, 10), padx=(10, 10))
        self.orwar_holder.pack(fill="both", expand=True)
        self.orwar_artist.pack(anchor="w", padx=(24,0))
        self.orwar_title.pack(anchor="w", padx=(24,0))





        # Wave Saver - Humbot
        self.humbot_wrapper = ctk.CTkFrame(self.cc_core_sframe, width=170, height=200,
                                             fg_color=tlr_dark)
        self.humbot_image = ctk.CTkImage(light_image=Image.open("Albums/Humbot.png"),
                                           dark_image=Image.open("Albums/Humbot.png"),
                                           size=(150, 150))
        self.humbot_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Humbot 2.png"),
                                              dark_image=Image.open("Albums/Humbot 2.png"),
                                              size=(220, 200))
        self.humbot_holder = ctk.CTkButton(self.humbot_wrapper, text="",
                                             command=lambda: play_music(self,"Musics/Wave Saver - Humbot (Royalty.mp3",
                                                                        "Wave Saver - Humbot",
                                                                        self.humbot_image_pl),
                                             image=self.humbot_image,
                                             fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.humbot_artist = ctk.CTkLabel(self.humbot_wrapper,
                                            text="Wave Saver",
                                            text_color=w_f5,
                                            font=(fn_PM, 15))
        self.humbot_title = ctk.CTkLabel(self.humbot_wrapper,
                                           text="Humbot",
                                           text_color="grey",
                                           font=(fn_PR, 12))

        self.humbot_wrapper.pack_propagate(False)
        self.humbot_wrapper.grid(row=0, column=3, pady=(0, 10), padx=(10, 10))
        self.humbot_holder.pack(fill="both", expand=True)
        self.humbot_artist.pack(anchor="w",padx=(24,0))
        self.humbot_title.pack(anchor="w",padx=(24,0))




        # RIOT
        self.riot_wrapper = ctk.CTkFrame(self.cc_core_sframe, width=170, height=200,
                                            fg_color=tlr_dark)
        self.riot_image = ctk.CTkImage(light_image=Image.open("Albums/BRS Riot.png"),
                                          dark_image=Image.open("Albums/BRS Riot.png"),
                                          size=(150, 150))
        self.riot_image_pl = ctk.CTkImage(light_image=Image.open("Albums/BRS Riot 2.png"),
                                             dark_image=Image.open("Albums/BRS Riot 2.png"),
                                             size=(220, 200))
        self.riot_holder = ctk.CTkButton(self.riot_wrapper, text="",
                                            command=lambda: play_music(self,
                                                                       "Musics/Blood Red Sun - Riot.mp3",
                                                                       "Blood Red Sun - Riot",
                                                                       self.riot_image_pl),
                                            image=self.riot_image,
                                            fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.riot_artist = ctk.CTkLabel(self.riot_wrapper,
                                           text="Blood Red Sun",
                                           text_color=w_f5,
                                           font=(fn_PM, 15))
        self.riot_title = ctk.CTkLabel(self.riot_wrapper,
                                          text="Riot",
                                          text_color="grey",
                                          font=(fn_PR, 12))

        self.riot_wrapper.pack_propagate(False)
        self.riot_wrapper.grid(row=0, column=4, pady=(0, 10), padx=(10, 10))
        self.riot_holder.pack(fill="both", expand=True)
        self.riot_artist.pack(anchor="w",padx=(24,0))
        self.riot_title.pack(anchor="w",padx=(24,0))



        # Shake Down
        self.shaked_wrapper = ctk.CTkFrame(self.cc_core_sframe, width=170, height=200,
                                           fg_color=tlr_dark)
        self.shaked_image = ctk.CTkImage(light_image=Image.open("Albums/Shake Down.png"),
                                         dark_image=Image.open("Albums/Shake Down.png"),
                                         size=(150, 150))
        self.shaked_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Shake Down 2.png"),
                                            dark_image=Image.open("Albums/Shake Down 2.png"),
                                            size=(220, 200))
        self.shaked_holder = ctk.CTkButton(self.shaked_wrapper, text="",
                                           command=lambda: play_music(self,
                                                                      "Musics/Shake Down.mp3",
                                                                      "Jules Gaia - Shake Down",
                                                                      self.shaked_image_pl),
                                           image=self.shaked_image,
                                           fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.shaked_artist = ctk.CTkLabel(self.shaked_wrapper,
                                          text="Jules Gaia",
                                          text_color=w_f5,
                                          font=(fn_PM, 15))
        self.shaked_title = ctk.CTkLabel(self.shaked_wrapper,
                                         text="Shake Down",
                                         text_color="grey",
                                         font=(fn_PR, 12))

        self.shaked_wrapper.pack_propagate(False)
        self.shaked_wrapper.grid(row=0, column=5, pady=(0, 10), padx=(10, 10))
        self.shaked_holder.pack(fill="both", expand=True)
        self.shaked_artist.pack(anchor="w",padx=(24,0))
        self.shaked_title.pack(anchor="w",padx=(24,0))





        # EMO MUSIC LIST ===========  ===========   ===========  ===========  ===========  ===========
        self.cc_core_music_list = ctk.CTkFrame(self.lib_content_frame, height=500, fg_color=tlr_dark)
        self.cc_core_list_title_frame = ctk.CTkFrame(self.cc_core_music_list, fg_color=tlr_dark, height=50)
        self.cc_core_title = ctk.CTkLabel(self.cc_core_list_title_frame,
                                           text="All Songs", text_color=w_f5, font=(fn_PM, 20))

        self.cc_core_scroll_frame = ctk.CTkScrollableFrame(self.cc_core_music_list, fg_color=tlr_dark,
                                                            scrollbar_button_color=tlr_dark,
                                                            scrollbar_button_hover_color=tlr_purple_2,
                                                            height=450)

        self.cc_core_list_title_frame.pack_propagate(False)
        self.cc_core_scroll_frame.pack_propagate(False)
        self.cc_core_list_title_frame.pack(fill="x", expand=True)
        self.cc_core_title.pack(side=ctk.LEFT, pady=10, padx=25)
        self.cc_core_scroll_frame.pack(fill="both", expand=True)



        # CATS WALING
        self.cats_walk_list_wrapper = ctk.CTkFrame(self.cc_core_scroll_frame, height=50, width=655,
                                             corner_radius=20, fg_color=tlr_dark)
        self.cats_walk_list_image = ctk.CTkImage(light_image=Image.open("Albums/Cats Walking.png"),
                                           dark_image=Image.open("Albums/Cats Walking.png"),
                                           size=(50, 50))
        self.cats_walk_list_holder = ctk.CTkButton(self.cats_walk_list_wrapper, text=f"4:27",
                                                   command=lambda: play_music(self,
                                                                              "Musics/Yomoti - Cats Walking.mp3",
                                                                              "Yomoti - Cats Walking",
                                                                              self.cats_walk_image_pl),
                                             text_color="grey", font=(fn_PR, 12),
                                             fg_color=tlr_dark, hover_color=tlr_purple_1,
                                             corner_radius=20, width=655, height=50)
        self.cats_walk_image_holder = ctk.CTkButton(self.cats_walk_list_holder, text="",
                                                    command=lambda: play_music(self,
                                                                               "Musics/Yomoti - Cats Walking.mp3",
                                                                               "Yomoti - Cats Walking",
                                                                               self.cats_walk_image_pl),
                                              image=self.cats_walk_list_image, width=50,
                                              fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.cats_walk_list_info_frame = ctk.CTkButton(self.cats_walk_list_holder, text="",
                                                       command=lambda: play_music(self,
                                                                                  "Musics/Yomoti - Cats Walking.mp3",
                                                                                  "Yomoti - Cats Walking",
                                                                                  self.cats_walk_image_pl),
                                                 width=150, height=50, hover_color=tlr_purple_1, fg_color=tlr_dark)
        self.cats_walk_list_author = ctk.CTkLabel(self.cats_walk_list_info_frame, text="Yomoti",
                                            text_color=w_f5, font=(fn_PM, 15))
        self.cats_walk_list_title = ctk.CTkLabel(self.cats_walk_list_info_frame, text="Cats Walking",
                                           text_color="grey",
                                           font=(fn_PR, 12))

        self.cats_walk_list_wrapper.pack_propagate(False)
        self.cats_walk_list_holder.pack_propagate(False)
        self.cats_walk_list_info_frame.pack_propagate(False)
        self.cats_walk_list_wrapper.grid(padx=10, pady=10)
        self.cats_walk_list_holder.pack(fill="both", expand=True)
        self.cats_walk_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.cats_walk_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.cats_walk_list_author.pack(anchor="w")
        self.cats_walk_list_title.pack(anchor="w")



        # ORANGE WARNINGS
        self.orwar_list_wrapper = ctk.CTkFrame(self.cc_core_scroll_frame, height=50, width=655,
                                               corner_radius=20, fg_color=tlr_dark)
        self.orwar_list_image = ctk.CTkImage(light_image=Image.open("Albums/BRS Orange Warning.png"),
                                             dark_image=Image.open("Albums/BRS Orange Warning.png"),
                                             size=(50, 50))
        self.orwar_list_holder = ctk.CTkButton(self.orwar_list_wrapper, text=f"3:02",
                                               command=lambda: play_music(self,
                                                                          "Musics/Blood Red Sun - Orange Warnings.mp3",
                                                                          "Blood Red Sun - Orange Warnings",
                                                                          self.orwar_image_pl),
                                               text_color="grey", font=(fn_PR, 12),
                                               fg_color=tlr_dark, hover_color=tlr_purple_1,
                                               corner_radius=20, width=655, height=50)
        self.orwar_image_holder = ctk.CTkButton(self.orwar_list_holder, text="",
                                                command=lambda: play_music(self,
                                                                           "Musics/Blood Red Sun - Orange Warnings.mp3",
                                                                           "Blood Red Sun - Orange Warnings",
                                                                           self.orwar_image_pl),
                                                image=self.orwar_list_image, width=50,
                                                fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.orwar_list_info_frame = ctk.CTkButton(self.orwar_list_holder, text="",
                                                   command=lambda: play_music(self,
                                                                              "Musics/Blood Red Sun - Orange Warnings.mp3",
                                                                              "Blood Red Sun - Orange Warnings",
                                                                              self.orwar_image_pl),
                                                   width=150, height=50, hover_color=tlr_purple_1, fg_color=tlr_dark)
        self.orwar_list_author = ctk.CTkLabel(self.orwar_list_info_frame, text="Blood Ren Sun",
                                              text_color=w_f5, font=(fn_PM, 15))
        self.orwar_list_title = ctk.CTkLabel(self.orwar_list_info_frame, text="Orange Warnings",
                                             text_color="grey",
                                             font=(fn_PR, 12))

        self.orwar_list_wrapper.pack_propagate(False)
        self.orwar_list_holder.pack_propagate(False)
        self.orwar_list_info_frame.pack_propagate(False)
        self.orwar_list_wrapper.grid(padx=10, pady=10)
        self.orwar_list_holder.pack(fill="both", expand=True)
        self.orwar_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.orwar_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.orwar_list_author.pack(anchor="w")
        self.orwar_list_title.pack(anchor="w")

        # HUMBOT
        self.humbot_list_wrapper = ctk.CTkFrame(self.cc_core_scroll_frame, height=50, width=655,
                                                 corner_radius=20, fg_color=tlr_dark)
        self.humbot_list_image = ctk.CTkImage(light_image=Image.open("Albums/Humbot.png"),
                                               dark_image=Image.open("Albums/Humbot.png"),
                                               size=(50, 50))
        self.humbot_list_holder = ctk.CTkButton(self.humbot_list_wrapper, text=f"4:27",
                                                command=lambda: play_music(self,
                                                                           "Musics/Wave Saver - Humbot (Royalty.mp3",
                                                                           "Wave Saver - Humbot",
                                                                           self.humbot_image_pl),
                                                 text_color="grey",
                                                 font=(fn_PR, 12),
                                                 fg_color=tlr_dark, hover_color=tlr_purple_1,
                                                 corner_radius=20, width=655, height=50)
        self.humbot_image_holder = ctk.CTkButton(self.humbot_list_holder, text="",
                                                 command=lambda: play_music(self,
                                                                            "Musics/Wave Saver - Humbot (Royalty.mp3",
                                                                            "Wave Saver - Humbot",
                                                                            self.humbot_image_pl),
                                                  image=self.humbot_list_image, width=50,
                                                  fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.humbot_list_info_frame = ctk.CTkButton(self.humbot_list_holder, text="",
                                                    command=lambda: play_music(self,
                                                                               "Musics/Wave Saver - Humbot (Royalty.mp3",
                                                                               "Wave Saver - Humbot",
                                                                               self.humbot_image_pl),
                                                     width=150, height=50, hover_color=tlr_purple_1, fg_color=tlr_dark)
        self.humbot_list_author = ctk.CTkLabel(self.humbot_list_info_frame, text="Wave Saver",
                                                text_color=w_f5, font=(fn_PM, 15))
        self.humbot_list_title = ctk.CTkLabel(self.humbot_list_info_frame, text="Humbot",
                                               text_color="grey",
                                               font=(fn_PR, 12))

        self.humbot_list_wrapper.pack_propagate(False)
        self.humbot_list_holder.pack_propagate(False)
        self.humbot_list_info_frame.pack_propagate(False)
        self.humbot_list_wrapper.grid(padx=10, pady=10)
        self.humbot_list_holder.pack(fill="both", expand=True)
        self.humbot_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.humbot_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.humbot_list_author.pack(anchor="w")
        self.humbot_list_title.pack(anchor="w")




        # RIOT
        self.riot_list_wrapper = ctk.CTkFrame(self.cc_core_scroll_frame, height=50, width=655,
                                                 corner_radius=20, fg_color=tlr_dark)
        self.riot_list_image = ctk.CTkImage(light_image=Image.open("Albums/BRS Riot.png"),
                                               dark_image=Image.open("Albums/BRS Riot.png"),
                                               size=(50, 50))
        self.riot_list_holder = ctk.CTkButton(self.riot_list_wrapper, text=f"3:59",
                                              command=lambda: play_music(self,
                                                                         "Musics/Blood Red Sun - Riot.mp3",
                                                                         "Blood Red Sun - Riot",
                                                                         self.riot_image_pl),
                                                 text_color="grey",
                                                 font=(fn_PR, 12),
                                                 fg_color=tlr_dark, hover_color=tlr_purple_1,
                                                 corner_radius=20, width=655, height=50)
        self.riot_image_holder = ctk.CTkButton(self.riot_list_holder, text="",
                                               command=lambda: play_music(self,
                                                                          "Musics/Blood Red Sun - Riot.mp3",
                                                                          "Blood Red Sun - Riot",
                                                                          self.riot_image_pl),
                                                  image=self.riot_list_image,
                                                  width=50,
                                                  fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.riot_list_info_frame = ctk.CTkButton(self.riot_list_holder, text="",
                                                  command=lambda: play_music(self,
                                                                             "Musics/Blood Red Sun - Riot.mp3",
                                                                             "Blood Red Sun - Riot",
                                                                             self.riot_image_pl),
                                                     width=150, height=50, hover_color=tlr_purple_1, fg_color=tlr_dark)
        self.riot_list_author = ctk.CTkLabel(self.riot_list_info_frame, text="Blood Red Sun",
                                                text_color=w_f5, font=(fn_PM, 15))
        self.riot_list_title = ctk.CTkLabel(self.riot_list_info_frame, text="Riot",
                                               text_color="grey",
                                               font=(fn_PR, 12))

        self.riot_list_wrapper.pack_propagate(False)
        self.riot_list_holder.pack_propagate(False)
        self.riot_list_info_frame.pack_propagate(False)
        self.riot_list_wrapper.grid(padx=10, pady=10)
        self.riot_list_holder.pack(fill="both", expand=True)
        self.riot_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.riot_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.riot_list_author.pack(anchor="w")
        self.riot_list_title.pack(anchor="w")




        # SHAKE DOWN
        self.shaked_list_wrapper = ctk.CTkFrame(self.cc_core_scroll_frame, height=50, width=655,
                                                corner_radius=20, fg_color=tlr_dark)
        self.shaked_list_image = ctk.CTkImage(light_image=Image.open("Albums/Shake Down.png"),
                                              dark_image=Image.open("Albums/Shake Down.png"),
                                              size=(50, 50))
        self.shaked_list_holder = ctk.CTkButton(self.shaked_list_wrapper, text=f"4:16",
                                                command=lambda: play_music(self,
                                                                           "Musics/Shake Down.mp3",
                                                                           "Jules Gaia - Shake Down",
                                                                           self.shaked_image_pl),
                                                text_color="grey",
                                                font=(fn_PR, 12),
                                                fg_color=tlr_dark, hover_color=tlr_purple_1,
                                                corner_radius=20, width=655, height=50)
        self.shaked_image_holder = ctk.CTkButton(self.shaked_list_holder, text="",
                                                 command=lambda: play_music(self,
                                                                            "Musics/Shake Down.mp3",
                                                                            "Jules Gaia - Shake Down",
                                                                            self.shaked_image_pl),
                                                 image=self.shaked_list_image,
                                                 width=50,
                                                 fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.shaked_list_info_frame = ctk.CTkButton(self.shaked_list_holder, text="",
                                                    command=lambda: play_music(self,
                                                                               "Musics/Shake Down.mp3",
                                                                               "Jules Gaia - Shake Down",
                                                                               self.shaked_image_pl),
                                                    width=150, height=50, hover_color=tlr_purple_1, fg_color=tlr_dark)
        self.shaked_list_author = ctk.CTkLabel(self.shaked_list_info_frame, text="Jules Gaia",
                                               text_color=w_f5, font=(fn_PM, 15))
        self.shaked_list_title = ctk.CTkLabel(self.shaked_list_info_frame, text="Shake Down",
                                              text_color="grey",
                                              font=(fn_PR, 12))

        self.shaked_list_wrapper.pack_propagate(False)
        self.shaked_list_holder.pack_propagate(False)
        self.shaked_list_info_frame.pack_propagate(False)
        self.shaked_list_wrapper.grid(padx=10, pady=10)
        self.shaked_list_holder.pack(fill="both", expand=True)
        self.shaked_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.shaked_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.shaked_list_author.pack(anchor="w")
        self.shaked_list_title.pack(anchor="w")

        # PACKING
        self.cc_core_title_frame.pack_propagate(False)
        self.cc_core_music_list.pack_propagate(False)

        self.cc_core_title_frame.pack(fill="x", expand=True)
        self.cc_hero_title.pack(anchor="w", side=ctk.LEFT, padx=(20, 0))
        self.cc_hero_info.pack(anchor="w", side=ctk.LEFT, padx=(10, 0), pady=(25, 0))

        self.cc_core_sframe.pack(fill="x", expand=True)
        self.cc_core_music_list.pack(fill="both", expand=True)






    def show_sad_indie(self):

        self.emo_data_frame.configure(fg_color=tlr_dark)
        self.emo_core_button.configure(fg_color=tlr_dark)

        self.cc_data_frame.configure(fg_color=tlr_dark)
        self.cc_core_button.configure(fg_color=tlr_dark)

        self.sadindie_data_frame.configure(fg_color=tlr_purple_1)
        self.sadindie_core_button.configure(fg_color=tlr_purple_1)

        for widget in self.main_music_feed_wrapper.winfo_children():
            widget.destroy()

        self.lib_content_frame = ctk.CTkFrame(self.main_music_feed_wrapper, fg_color=tlr_dark)

        self.lib_content_frame.pack_propagate(False)
        self.lib_content_frame.pack(fill="both", expand=True)




        self.sadindie_core_title_frame = ctk.CTkFrame(self.lib_content_frame, height=100, fg_color=tlr_dark)
        self.sadindie_hero_title = ctk.CTkLabel(self.sadindie_core_title_frame,
                                           text="Sad Indie",
                                           font=(fn_PM, 60),
                                           text_color=w_f5)
        self.sadindie_hero_info = ctk.CTkLabel(self.sadindie_core_title_frame,
                                          text="6 Songs . 25 mins",
                                          font=(fn_PM, 12),
                                          text_color="grey")
        self.sadindie_core_sframe = ctk.CTkScrollableFrame(self.lib_content_frame, height=200,
                                                      fg_color=tlr_dark,
                                                      orientation="horizontal",
                                                      scrollbar_button_color=tlr_dark,
                                                      scrollbar_button_hover_color=tlr_purple_2)




        # WHERES MY LOVE
        self.wheres_my_l_wrapper = ctk.CTkFrame(self.sadindie_core_sframe, width=170, height=200,
                                              fg_color=tlr_dark)

        self.wheres_my_l_image = ctk.CTkImage(light_image=Image.open("Albums/Wheres My Love.png"),
                                            dark_image=Image.open("Albums/Wheres My Love.png"),
                                            size=(150, 150))
        self.wheres_my_l_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Wheres My Love 2.png"),
                                               dark_image=Image.open("Albums/Wheres My Love 2.png"),
                                               size=(220, 200))

        self.wheres_my_l_holder = ctk.CTkButton(self.wheres_my_l_wrapper, text="",
                                              command=lambda: play_music(self,
                                                                         "Musics/SYML - Where's My Love.mp3",
                                                                         "SYML - Where's My Love",
                                                                         self.wheres_my_l_image_pl),
                                              image=self.wheres_my_l_image,
                                              fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.wheres_my_l_artist = ctk.CTkLabel(self.wheres_my_l_wrapper,
                                             text="SYML",
                                             text_color=w_f5,
                                             font=(fn_PM, 15))
        self.wheres_my_l_title = ctk.CTkLabel(self.wheres_my_l_wrapper,
                                            text="Wheres My Love",
                                            text_color="grey",
                                            font=(fn_PR, 12))

        self.wheres_my_l_wrapper.pack_propagate(False)
        self.wheres_my_l_wrapper.grid(row=0, column=1, pady=(0, 10), padx=(0, 10))
        self.wheres_my_l_holder.pack(fill="both", expand=True)
        self.wheres_my_l_artist.pack(anchor="w",padx=(24,0))
        self.wheres_my_l_title.pack(anchor="w",padx=(24,0))





        # FIRST LOVE LATE SPRING
        self.mitski_wrapper = ctk.CTkFrame(self.sadindie_core_sframe, width=170, height=200,
                                          fg_color=tlr_dark)

        self.mitski_image = ctk.CTkImage(light_image=Image.open("Albums/Mitski.png"),
                                        dark_image=Image.open("Albums/Mitski.png"),
                                        size=(150, 150))
        self.mitski_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Mitski 2.png"),
                                           dark_image=Image.open("Albums/Mitski 2.png"),
                                           size=(220, 200))

        self.mitski_holder = ctk.CTkButton(self.mitski_wrapper, text="",
                                          command=lambda: play_music(self,
                                                                     "Musics/Mitski - First Love_Late Spring.mp3",
                                                                     "Mitski - First Love Late Spring",
                                                                     self.mitski_image_pl),
                                          image=self.mitski_image,
                                          fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.mitski_artist = ctk.CTkLabel(self.mitski_wrapper,
                                         text="Mitski",
                                         text_color=w_f5,
                                         font=(fn_PM, 15))
        self.mitski_title = ctk.CTkLabel(self.mitski_wrapper,
                                        text="First Love Late Spring",
                                        text_color="grey",
                                        font=(fn_PR, 12))

        self.mitski_wrapper.pack_propagate(False)
        self.mitski_wrapper.grid(row=0, column=2, pady=(0, 10), padx=(0, 10))
        self.mitski_holder.pack(fill="both", expand=True)
        self.mitski_artist.pack(anchor="w",padx=(24,0))
        self.mitski_title.pack(anchor="w",padx=(24,0))







        # Rises The Moon
        self.rises_the_moon_wrapper = ctk.CTkFrame(self.sadindie_core_sframe, width=170, height=200,
                                             fg_color=tlr_dark)

        self.rises_the_moon_image = ctk.CTkImage(light_image=Image.open("Albums/Rises The Moon.png"),
                                           dark_image=Image.open("Albums/Rises The Moon.png"),
                                           size=(150, 150))
        self.rises_the_moon_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Rises The Moon 2.png"),
                                              dark_image=Image.open("Albums/Rises The Moon 2.png"),
                                              size=(220, 200))

        self.rises_the_moon_holder = ctk.CTkButton(self.rises_the_moon_wrapper, text="",
                                             command=lambda: play_music(self,
                                                                        "Musics/liana flores - rises the moon.mp3",
                                                                        "Liana Flores - Rises The Moon",
                                                                        self.rises_the_moon_image_pl),
                                             image=self.rises_the_moon_image,
                                             fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.rises_the_moon_artist = ctk.CTkLabel(self.rises_the_moon_wrapper,
                                            text="Liana Flores",
                                            text_color=w_f5,
                                            font=(fn_PM, 15))
        self.rises_the_moon_title = ctk.CTkLabel(self.rises_the_moon_wrapper,
                                           text="Rises The Moon",
                                           text_color="grey",
                                           font=(fn_PR, 12))

        self.rises_the_moon_wrapper.pack_propagate(False)
        self.rises_the_moon_wrapper.grid(row=0, column=3, pady=(0, 10), padx=(0, 10))
        self.rises_the_moon_holder.pack(fill="both", expand=True)
        self.rises_the_moon_artist.pack(anchor="w",padx=(24,0))
        self.rises_the_moon_title.pack(anchor="w",padx=(24,0))
        
        
        
        
        
        

        # CHAMBER OF REFLECTION
        self.chamr_wrapper = ctk.CTkFrame(self.sadindie_core_sframe, width=170, height=200,
                                             fg_color=tlr_dark)

        self.chamr_image = ctk.CTkImage(light_image=Image.open("Albums/Chamber Of Reflection.png"),
                                           dark_image=Image.open("Albums/Chamber Of Reflection.png"),
                                           size=(150, 150))
        self.chamr_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Chamber Of Reflection 2.png"),
                                              dark_image=Image.open("Albums/Chamber Of Reflection 2.png"),
                                              size=(220, 200))

        self.chamr_holder = ctk.CTkButton(self.chamr_wrapper, text="",
                                             command=lambda: play_music(self,
                                                                        "Musics/Chamber Of Reflection.mp3",
                                                                        "Mac De Macro - Chamber of Reflection",
                                                                        self.chamr_image_pl),
                                             image=self.chamr_image,
                                             fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.chamr_artist = ctk.CTkLabel(self.chamr_wrapper,
                                            text="Mac De Macro",
                                            text_color=w_f5,
                                            font=(fn_PM, 15))
        self.chamr_title = ctk.CTkLabel(self.chamr_wrapper,
                                           text="Chamber of Reflection",
                                           text_color="grey",
                                           font=(fn_PR, 12))

        self.chamr_wrapper.pack_propagate(False)
        self.chamr_wrapper.grid(row=0, column=4, pady=(0, 10), padx=(0, 10))
        self.chamr_holder.pack(fill="both", expand=True)
        self.chamr_artist.pack(anchor="w",padx=(24,0))
        self.chamr_title.pack(anchor="w",padx=(24,0))




        # THE NIGHT WE MET

        self.tnwm_wrapper = ctk.CTkFrame(self.sadindie_core_sframe, width=170, height=200,
                                             fg_color=tlr_dark)

        self.tnwm_image = ctk.CTkImage(light_image=Image.open("Albums/The Night We Met.png"),
                                           dark_image=Image.open("Albums/The Night We Met.png"),
                                           size=(150, 150))
        self.tnwm_image_pl = ctk.CTkImage(light_image=Image.open("Albums/The Night We Met 2.png"),
                                              dark_image=Image.open("Albums/The Night We Met 2.png"),
                                              size=(220, 200))

        self.tnwm_holder = ctk.CTkButton(self.tnwm_wrapper, text="",
                                             command=lambda: play_music(self,
                                                                        "Musics/Lord Huron - The Night We Met.mp3",
                                                                        "Lord Huron - The Night We Met.mp3",
                                                                        self.tnwm_image_pl),
                                             image=self.tnwm_image,
                                             fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.tnwm_artist = ctk.CTkLabel(self.tnwm_wrapper,
                                            text="Lord Huron",
                                            text_color=w_f5,
                                            font=(fn_PM, 15))
        self.tnwm_title = ctk.CTkLabel(self.tnwm_wrapper,
                                           text="The Night We Met",
                                           text_color="grey",
                                           font=(fn_PR, 12))

        self.tnwm_wrapper.pack_propagate(False)
        self.tnwm_wrapper.grid(row=0, column=5, pady=(0, 10), padx=(0, 10))
        self.tnwm_holder.pack(fill="both", expand=True)
        self.tnwm_artist.pack(anchor="w",padx=(24,0))
        self.tnwm_title.pack(anchor="w",padx=(24,0))





        # BUBBLE Gum
        self.bubble_g_wrapper = ctk.CTkFrame(self.sadindie_core_sframe, width=170, height=200,
                                             fg_color=tlr_dark)

        self.bubble_g_image = ctk.CTkImage(light_image=Image.open("Albums/Bubble Gum.png"),
                                           dark_image=Image.open("Albums/Bubble Gum.png"),
                                           size=(150, 150))
        self.bubble_g_image_pl = ctk.CTkImage(light_image=Image.open("Albums/Bubble Gum 2.png"),
                                              dark_image=Image.open("Albums/Bubble Gum 2.png"),
                                              size=(220, 200))

        self.bubble_g_holder = ctk.CTkButton(self.bubble_g_wrapper, text="",
                                             command=lambda: play_music(self,
                                                                        "Musics/Clairo - Bubble Gum.mp3",
                                                                        "Clairo - Bubble Gum",
                                                                        self.bubble_g_image_pl),
                                             image=self.bubble_g_image,
                                             fg_color=tlr_dark,hover_color=tlr_purple_1)
        self.bubble_g_artist = ctk.CTkLabel(self.bubble_g_wrapper,
                                            text="Clairo",
                                            text_color=w_f5,
                                            font=(fn_PM, 15))
        self.bubble_g_title = ctk.CTkLabel(self.bubble_g_wrapper,
                                           text="Bubble Gum",
                                           text_color="grey",
                                           font=(fn_PR, 12))

        self.bubble_g_wrapper.pack_propagate(False)
        self.bubble_g_wrapper.grid(row=0, column=6, pady=(0, 10), padx=(0, 10))
        self.bubble_g_holder.pack(fill="both", expand=True)
        self.bubble_g_artist.pack(anchor="w",padx=(24,0))
        self.bubble_g_title.pack(anchor="w",padx=(24,0))




        self.sadindie_core_music_list = ctk.CTkFrame(self.lib_content_frame, height=500, fg_color=tlr_dark)
        self.sadindie_core_list_title_frame = ctk.CTkFrame(self.sadindie_core_music_list, fg_color=tlr_dark, height=50)
        self.sadindie_core_title = ctk.CTkLabel(self.sadindie_core_list_title_frame,
                                          text="All Songs", text_color=w_f5, font=(fn_PM, 20))

        self.sadindie_core_scroll_frame = ctk.CTkScrollableFrame(self.sadindie_core_music_list, fg_color=tlr_dark,
                                                           scrollbar_button_color=tlr_dark,
                                                           scrollbar_button_hover_color=tlr_purple_2,
                                                           height=450)
        self.wrapper = ctk.CTkFrame(self.sadindie_core_scroll_frame)

        self.sadindie_core_list_title_frame.pack_propagate(False)
        self.sadindie_core_scroll_frame.pack_propagate(False)
        self.sadindie_core_list_title_frame.pack(fill="x", expand=True)
        self.sadindie_core_title.pack(side=ctk.LEFT, pady=10, padx=25)
        self.sadindie_core_scroll_frame.pack(fill="both", expand=True)




        # SAD INDIE MUSIC LIST
        self.wml_list_wrapper = ctk.CTkFrame(self.sadindie_core_scroll_frame, height=50, width=655,
                                            corner_radius=20, fg_color=tlr_dark)
        self.wml_list_image = ctk.CTkImage(light_image=Image.open("Albums/Wheres My Love.png"),
                                          dark_image=Image.open("Albums/Wheres My Love.png"),
                                          size=(50, 50))
        self.wml_list_holder = ctk.CTkButton(self.wml_list_wrapper, text=f"4:00", text_color="grey",
                                            command=lambda: play_music(self,
                                                                       "Musics/SYML - Where's My Love.mp3",
                                                                       "SYML - Where's My Love",
                                                                       self.wheres_my_l_image_pl),
                                            font=(fn_PR, 12),
                                            fg_color=tlr_dark, hover_color=tlr_purple_1,
                                            corner_radius=20, width=655, height=50)
        self.wml_image_holder = ctk.CTkButton(self.wml_list_holder, text="",
                                             command=lambda: play_music(self,
                                                                         "Musics/SYML - Where's My Love.mp3",
                                                                         "SYML - Where's My Love",
                                                                         self.wheres_my_l_image_pl),
                                             image=self.wml_list_image,
                                             width=50,
                                             fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.wml_list_info_frame = ctk.CTkButton(self.wml_list_holder, text="",
                                                 command=lambda: play_music(self,
                                                                            "Musics/SYML - Where's My Love.mp3",
                                                                            "SYML - Where's My Love",
                                                                            self.wheres_my_l_image_pl),
                                                width=150, height=50, hover_color=tlr_purple_1,
                                                fg_color=tlr_dark)
        
        self.wml_list_author = ctk.CTkLabel(self.wml_list_info_frame, text="SYML",
                                           text_color=w_f5, font=(fn_PM, 15))
        self.wml_list_title = ctk.CTkLabel(self.wml_list_info_frame, text="Where's My Love",
                                          text_color="grey",
                                          font=(fn_PR, 12))

        self.wml_list_wrapper.pack_propagate(False)
        self.wml_list_holder.pack_propagate(False)
        self.wml_list_info_frame.pack_propagate(False)
        self.wml_list_wrapper.grid(padx=10, pady=10)
        self.wml_list_holder.pack(fill="both", expand=True)
        self.wml_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.wml_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.wml_list_author.pack(anchor="w")
        self.wml_list_title.pack(anchor="w")





        # MITSKI
        self.mitski_list_wrapper = ctk.CTkFrame(self.sadindie_core_scroll_frame, height=50, width=655,
                                             corner_radius=20, fg_color=tlr_dark)
        self.mitski_list_image = ctk.CTkImage(light_image=Image.open("Albums/Mitski.png"),
                                           dark_image=Image.open("Albums/Mitski.png"),
                                           size=(50, 50))
        self.mitski_list_holder = ctk.CTkButton(self.mitski_list_wrapper, text=f"4:38", text_color="grey",
                                             command=lambda: play_music(self,
                                                                        "Musics/Mitski - First Love_Late Spring.mp3",
                                                                        "Mitski - First Love Late Spring",
                                                                        self.mitski_image_pl),
                                             font=(fn_PR, 12),
                                             fg_color=tlr_dark, hover_color=tlr_purple_1,
                                             corner_radius=20, width=655, height=50)
        self.mitski_image_holder = ctk.CTkButton(self.mitski_list_holder, text="",
                                                 command=lambda: play_music(self,
                                                                            "Musics/Mitski - First Love_Late Spring.mp3",
                                                                            "Mitski - First Love Late Spring",
                                                                            self.mitski_image_pl),
                                              image=self.mitski_list_image,
                                              width=50,
                                              fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.mitski_list_info_frame = ctk.CTkButton(self.mitski_list_holder, text="",
                                                    command=lambda: play_music(self,
                                                                               "Musics/Mitski - First Love_Late Spring.mp3",
                                                                               "Mitski - First Love Late Spring",
                                                                               self.mitski_image_pl),
                                                 width=150, height=50, hover_color=tlr_purple_1,
                                                 fg_color=tlr_dark)

        self.mitski_list_author = ctk.CTkLabel(self.mitski_list_info_frame, text="Mitski",
                                            text_color=w_f5, font=(fn_PM, 15))
        self.mitski_list_title = ctk.CTkLabel(self.mitski_list_info_frame, text="First Love Late Spring",
                                           text_color="grey",
                                           font=(fn_PR, 12))

        self.mitski_list_wrapper.pack_propagate(False)
        self.mitski_list_holder.pack_propagate(False)
        self.mitski_list_info_frame.pack_propagate(False)
        self.mitski_list_wrapper.grid(padx=10, pady=10)
        self.mitski_list_holder.pack(fill="both", expand=True)
        self.mitski_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.mitski_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.mitski_list_author.pack(anchor="w")
        self.mitski_list_title.pack(anchor="w")




        # RISES THE MOON
        self.rtm_list_wrapper = ctk.CTkFrame(self.sadindie_core_scroll_frame, height=50, width=655,
                                             corner_radius=20, fg_color=tlr_dark)
        self.rtm_list_image = ctk.CTkImage(light_image=Image.open("Albums/Rises The Moon.png"),
                                           dark_image=Image.open("Albums/Rises The Moon.png"),
                                           size=(50, 50))
        self.rtm_list_holder = ctk.CTkButton(self.rtm_list_wrapper, text=f"2:42", text_color="grey",
                                             command=lambda: play_music(self,
                                                                        "Musics/liana flores - rises the moon.mp3",
                                                                        "Liana Flores - Rises The Moon",
                                                                        self.rises_the_moon_image_pl),
                                             font=(fn_PR, 12),
                                             fg_color=tlr_dark, hover_color=tlr_purple_1,
                                             corner_radius=20, width=655, height=50)
        self.rtm_image_holder = ctk.CTkButton(self.rtm_list_holder, text="",
                                              command=lambda: play_music(self,
                                                                         "Musics/liana flores - rises the moon.mp3",
                                                                         "Liana Flores - Rises The Moon",
                                                                         self.rises_the_moon_image_pl),
                                              image=self.rtm_list_image,
                                              width=50,
                                              fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.rtm_list_info_frame = ctk.CTkButton(self.rtm_list_holder, text="",
                                                 command=lambda: play_music(self,
                                                                            "Musics/liana flores - rises the moon.mp3",
                                                                            "Liana Flores - Rises The Moon",
                                                                            self.rises_the_moon_image_pl),
                                                 width=150, height=50, hover_color=tlr_purple_1,
                                                 fg_color=tlr_dark)

        self.rtm_list_author = ctk.CTkLabel(self.rtm_list_info_frame, text="Liana Flores",
                                            text_color=w_f5, font=(fn_PM, 15))
        self.rtm_list_title = ctk.CTkLabel(self.rtm_list_info_frame, text="Rises The Moon",
                                           text_color="grey",
                                           font=(fn_PR, 12))

        self.rtm_list_wrapper.pack_propagate(False)
        self.rtm_list_holder.pack_propagate(False)
        self.rtm_list_info_frame.pack_propagate(False)
        self.rtm_list_wrapper.grid(padx=10, pady=10)
        self.rtm_list_holder.pack(fill="both", expand=True)
        self.rtm_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.rtm_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.rtm_list_author.pack(anchor="w")
        self.rtm_list_title.pack(anchor="w")




        # CHAMBER OF REFLECTION
        self.chamberf_list_wrapper = ctk.CTkFrame(self.sadindie_core_scroll_frame, height=50, width=655,
                                             corner_radius=20, fg_color=tlr_dark)
        self.chamberf_list_image = ctk.CTkImage(light_image=Image.open("Albums/Chamber Of Reflection.png"),
                                           dark_image=Image.open("Albums/Chamber Of Reflection.png"),
                                           size=(50, 50))
        self.chamberf_list_holder = ctk.CTkButton(self.chamberf_list_wrapper, text=f"3:51", text_color="grey",
                                                  command=lambda: play_music(self,
                                                                             "Musics/Chamber Of Reflection.mp3",
                                                                             "Mac De Macro - Chamber of Reflection",
                                                                             self.chamr_image_pl),
                                             font=(fn_PR, 12),
                                             fg_color=tlr_dark, hover_color=tlr_purple_1,
                                             corner_radius=20, width=655, height=50)
        self.chamberf_image_holder = ctk.CTkButton(self.chamberf_list_holder, text="",
                                                   command=lambda: play_music(self,
                                                                              "Musics/Chamber Of Reflection.mp3",
                                                                              "Mac De Macro - Chamber of Reflection",
                                                                              self.chamr_image_pl),
                                              image= self.chamberf_list_image,
                                              width=50,
                                              fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.chamberf_list_info_frame = ctk.CTkButton(self.chamberf_list_holder, text="",
                                                      command=lambda: play_music(self,
                                                                                 "Musics/Chamber Of Reflection.mp3",
                                                                                 "Mac De Macro - Chamber of Reflection",
                                                                                 self.chamr_image_pl),
                                                 width=150, height=50, hover_color=tlr_purple_1,
                                                 fg_color=tlr_dark)

        self.chamberf_list_author = ctk.CTkLabel(self.chamberf_list_info_frame, text="Mac De Macro",
                                            text_color=w_f5, font=(fn_PM, 15))
        self.chamberf_list_title = ctk.CTkLabel(self.chamberf_list_info_frame, text="Chamber Of Reflection",
                                           text_color="grey",
                                           font=(fn_PR, 12))

        self.chamberf_list_wrapper.pack_propagate(False)
        self.chamberf_list_holder.pack_propagate(False)
        self.chamberf_list_info_frame.pack_propagate(False)
        self.chamberf_list_wrapper.grid(padx=10, pady=10)
        self.chamberf_list_holder.pack(fill="both", expand=True)
        self.chamberf_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.chamberf_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.chamberf_list_author.pack(anchor="w")
        self.chamberf_list_title.pack(anchor="w")





        # LORD HURON
        self.lordhuron_list_wrapper = ctk.CTkFrame(self.sadindie_core_scroll_frame, height=50, width=655,
                                                  corner_radius=20, fg_color=tlr_dark)
        self.lordhuron_list_image = ctk.CTkImage(light_image=Image.open("Albums/The Night We Met.png"),
                                                dark_image=Image.open("Albums/The Night We Met.png"),
                                                size=(50, 50))
        self.lordhuron_list_holder = ctk.CTkButton(self.lordhuron_list_wrapper, text=f"3:28", text_color="grey",
                                                  command=lambda: play_music(self,
                                                                             "Musics/Lord Huron - The Night We Met.mp3",
                                                                             "Lord Huron - The Night We Met",
                                                                             self.tnwm_image_pl),
                                                  font=(fn_PR, 12),
                                                  fg_color=tlr_dark, hover_color=tlr_purple_1,
                                                  corner_radius=20, width=655, height=50)
        self.lordhuron_image_holder = ctk.CTkButton(self.lordhuron_list_holder, text="",
                                                    command=lambda: play_music(self,
                                                                               "Musics/Lord Huron - The Night We Met.mp3",
                                                                               "Lord Huron - The Night We Met",
                                                                               self.tnwm_image_pl),
                                                    font=(fn_PR, 12),
                                                   image=self.lordhuron_list_image,
                                                   width=50,
                                                   fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.lordhuron_list_info_frame = ctk.CTkButton(self.lordhuron_list_holder, text="",
                                                       command=lambda: play_music(self,
                                                                                  "Musics/Lord Huron - The Night We Met.mp3",
                                                                                  "Lord Huron - The Night We Met",
                                                                                  self.tnwm_image_pl),
                                                       font=(fn_PR, 12),
                                                      width=150, height=50, hover_color=tlr_purple_1,
                                                      fg_color=tlr_dark)

        self.lordhuron_list_author = ctk.CTkLabel(self.lordhuron_list_info_frame, text="Lord Huron",
                                                 text_color=w_f5, font=(fn_PM, 15))
        self.lordhuron_list_title = ctk.CTkLabel(self.lordhuron_list_info_frame, text="The Night We Met",
                                                text_color="grey",
                                                font=(fn_PR, 12))

        self.lordhuron_list_wrapper.pack_propagate(False)
        self.lordhuron_list_holder.pack_propagate(False)
        self.lordhuron_list_info_frame.pack_propagate(False)
        self.lordhuron_list_wrapper.grid(padx=10, pady=10)
        self.lordhuron_list_holder.pack(fill="both", expand=True)
        self.lordhuron_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.lordhuron_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.lordhuron_list_author.pack(anchor="w")
        self.lordhuron_list_title.pack(anchor="w")






        # LORD HURON
        self.bubblegum_list_wrapper = ctk.CTkFrame(self.sadindie_core_scroll_frame, height=50, width=655,
                                                   corner_radius=20, fg_color=tlr_dark)
        self.bubblegum_list_image = ctk.CTkImage(light_image=Image.open("Albums/Bubble Gum.png"),
                                                 dark_image=Image.open("Albums/Bubble Gum.png"),
                                                 size=(50, 50))
        self.bubblegum_list_holder = ctk.CTkButton(self.bubblegum_list_wrapper, text=f"2:56", text_color="grey",
                                                   command=lambda: play_music(self,
                                                                              "Musics/Clairo - Bubble Gum.mp3",
                                                                              "Clairo - Bubble Gum",
                                                                              self.bubble_g_image_pl),
                                                   font=(fn_PR, 12),
                                                   fg_color=tlr_dark, hover_color=tlr_purple_1,
                                                   corner_radius=20, width=655, height=50)
        self.bubblegum_image_holder = ctk.CTkButton(self.bubblegum_list_holder, text="",
                                                    command=lambda: play_music(self,
                                                                               "Musics/Clairo - Bubble Gum.mp3",
                                                                               "Clairo - Bubble Gum",
                                                                               self.bubble_g_image_pl),
                                                    font=(fn_PR, 12),
                                                    image=  self.bubblegum_list_image,
                                                    width=50,
                                                    fg_color=tlr_dark, hover_color=tlr_purple_1)
        self.bubblegum_list_info_frame = ctk.CTkButton(self.bubblegum_list_holder, text="",
                                                       command=lambda: play_music(self,
                                                                                  "Musics/Clairo - Bubble Gum.mp3",
                                                                                  "Clairo - Bubble Gum",
                                                                                     self.bubble_g_image_pl),
                                                       font=(fn_PR, 12),
                                                       width=150, height=50, hover_color=tlr_purple_1,
                                                       fg_color=tlr_dark)

        self.bubblegum_list_author = ctk.CTkLabel(self.bubblegum_list_info_frame, text="Lord Huron",
                                                  text_color=w_f5, font=(fn_PM, 15))
        self.bubblegum_list_title = ctk.CTkLabel(self.bubblegum_list_info_frame, text="The Night We Met",
                                                 text_color="grey",
                                                 font=(fn_PR, 12))

        self.bubblegum_list_wrapper.pack_propagate(False)
        self.bubblegum_list_holder.pack_propagate(False)
        self.bubblegum_list_info_frame.pack_propagate(False)
        self.bubblegum_list_wrapper.grid(padx=10, pady=10)
        self.bubblegum_list_holder.pack(fill="both", expand=True)
        self.bubblegum_image_holder.pack(anchor="w", side=ctk.LEFT)
        self.bubblegum_list_info_frame.pack(anchor="w", side=ctk.LEFT)
        self.bubblegum_list_author.pack(anchor="w")
        self.bubblegum_list_title.pack(anchor="w")




        # PACKING
        self.sadindie_core_title_frame.pack_propagate(False)
        self.sadindie_core_music_list.pack_propagate(False)

        self.sadindie_core_title_frame.pack(fill="x", expand=True)
        self.sadindie_hero_title.pack(anchor="w", side=ctk.LEFT, padx=(20, 0))
        self.sadindie_hero_info.pack(anchor="w", side=ctk.LEFT, padx=(10, 0), pady=(25, 0))

        self.sadindie_core_sframe.pack(fill="x", expand=True)
        self.sadindie_core_music_list.pack(fill="both", expand=True)


    show_emo_core(self)


































    # # TOP NAV==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ====
    # for widget in self.cf_top_nav.winfo_children():
    #     widget.destroy()
    #
    # self.top_n_searchbar = customtkinter.CTkEntry(self.cf_top_nav,
    #                                               width=350,
    #                                               height=30,
    #                                               fg_color=backup_ppl_2,
    #                                               border_color=backup_ppl_1,
    #                                               font=(fn_PR, 12),
    #                                               placeholder_text="Search Anything......")
    #
    # self.top_n_searchbar.grid(row=0, column=1, pady=(9, 8), padx=10)
    #


