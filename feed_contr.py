import customtkinter
from __init__ import tlr_dark, tlr_purple_1,tlr_purple_2, tlr_purple_3, tlr_purple_4, w_main_white,\
    backup_ppl_1,backup_ppl_2,w_f5,w_main_white,w_pure_white,moonphased,moonphasec

from PIL import Image
from __init__ import fn_PR,fn_PM

sidebar_width = 200
content_frame_width = 700
aside_width = 400


def default_aside_right(self):

    for widget in self.aside_right.winfo_children():
        widget.destroy()

    self.asr_top_nav = customtkinter.CTkFrame(self.aside_right, width=aside_width, height=50,
                                              fg_color=backup_ppl_2)

    self.asr_username = customtkinter.CTkLabel(self.asr_top_nav,text="Username",font=(fn_PM,12),height=50)

    self.asr_image_track_div = customtkinter.CTkFrame(self.aside_right, width=aside_width, height=250,
                                                      fg_color=backup_ppl_2)
    self.asr_music_progress_div = customtkinter.CTkFrame(self.aside_right, width=aside_width, height=100,
                                                         fg_color=backup_ppl_2)
    self.asr_songs_div = customtkinter.CTkScrollableFrame(self.aside_right, width=aside_width,
                                                          fg_color=backup_ppl_2)


    self.asr_top_nav.pack(padx=0, pady=(10, 10), fill="x")
    self.asr_username.grid(row=0,column=5,padx=(200))
    self.asr_image_track_div.pack(padx=0, pady=(10, 10), fill="x")
    self.asr_music_progress_div.pack(padx=0, pady=(0, 10), fill="x")
    self.asr_songs_div.pack(padx=0, fill="both", expand=True)












#
#
# def show_trends(self):
#
#
#
#     for widget in self.main_music_feed_wrapper.winfo_children():
#         widget.destroy()
#
#
#     self.trends_hero_track_wrapper = customtkinter.CTkFrame(self.main_music_feed_wrapper,
#                                                      width=content_frame_width, height=300,
#                                                      fg_color=tlr_purple_3)
#     self.trend_hero_track_lbl = customtkinter.CTkLabel(self.trends_hero_track_wrapper,
#                                                    text="TREND HERO TRACK WRAPPER",
#                                                    font=("Poppins", 30, "bold"),
#                                                    text_color=w_main_white)
#
#     self.trend_recom_music_feed_wrapper = customtkinter.CTkScrollableFrame(self.main_music_feed_wrapper,
#                                                                      width=content_frame_width,
#                                                                      fg_color=tlr_purple_2)
#
#     self.trend_recom_music_feed_lbl = customtkinter.CTkButton(self.trend_recom_music_feed_wrapper,
#                                                        text="TREND RECOM MUSIC FEED WRAPPER",
#                                                        font=(fn_PR, 12),
#                                                        width=30,height=30,
#                                                        text_color=w_main_white)
#
#
#     self.trends_hero_track_wrapper.pack(padx=0, pady=(0, 10), fill="x")
#     self.trends_hero_track_wrapper.pack_propagate(False)
#     self.trend_hero_track_lbl.pack()
#
#     self.trend_recom_music_feed_wrapper.pack(padx=0, pady=(0, 10),fill="both",expand=True)
#     self.trend_recom_music_feed_wrapper.pack_propagate(False)
#     self.trend_recom_music_feed_lbl.grid(row=0,column=1,padx=10,pady=10)
#
#











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
    self.trends_btn = customtkinter.CTkButton(self.button_frame , text="Trends",
                                           command=lambda:show_trends(self),
                                           font=(fn_PM, 12),
                                           hover_color=tlr_purple_4,
                                           fg_color=tlr_dark)
    self.library_btn = customtkinter.CTkButton(self.button_frame , text="Library",
                                           command=lambda: show_library(self),
                                           font=(fn_PM, 12),
                                           hover_color=tlr_purple_4,
                                           fg_color=tlr_dark)

    self.logout_btn = customtkinter.CTkButton(self.button_frame, text="Log Out",

                                              font=(fn_PM, 12),
                                              hover_color=tlr_purple_4,
                                              fg_color=tlr_dark)

    self.feed_btn.pack(pady=10, padx=10, fill="x")
    self.trends_btn.pack(pady=10, padx=10, fill="x")
    self.library_btn.pack(pady=10, padx=10, fill="x")
    self.logout_btn.pack(pady=(150, 10), padx=10, fill="x")





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
                                                 width=content_frame_width,height=300,
                                                 fg_color=tlr_dark)
    self.hero_track_cat_div = customtkinter.CTkFrame(self.main_music_feed_wrapper,
                                                 width=content_frame_width,height=25,
                                                 fg_color=tlr_dark)
    self.hero_track_cat_lbl = customtkinter.CTkLabel(self.hero_track_cat_div,text="Most Played Song",
                                                 font=(fn_PR,15))


    # IMAGE FRAME
    self.hero_track_image_frame = customtkinter.CTkFrame(self.hero_track_wrapper,
                                                 width=400,height=300,
                                                 fg_color=tlr_dark)

    self.hero_track_image = customtkinter.CTkImage(light_image=Image.open("Images/REQUIEM KESHI.jpg"),
                                                   dark_image=Image.open("Images/REQUIEM KESHI.jpg"),
                                                   size=(350,310))

    self.hero_track_img_lbl = customtkinter.CTkLabel(self.hero_track_image_frame,text="",
                                                     image=self.hero_track_image)


    # IMAGE DETAILS
    self.hero_track_image_details = customtkinter.CTkFrame(self.hero_track_wrapper,
                                                 width=400,height=300,
                                                fg_color=tlr_dark,corner_radius=20)




    self.hero_track_name = customtkinter.CTkFrame(self.hero_track_image_details,
                                                  width=340,height=150,
                                                  fg_color=tlr_dark,
                                                  corner_radius=20)


    self.htn_category_div = customtkinter.CTkFrame(self.hero_track_name,
                                               height=150,
                                               corner_radius=10,
                                               fg_color=backup_ppl_2,
                                               width=100)
    self.ht_title_cat_div = customtkinter.CTkFrame(self.htn_category_div,
                                               width=100,height=50,fg_color=backup_ppl_2)
    self.ht_title_lbl = customtkinter.CTkLabel(self.ht_title_cat_div,text="Title",
                                               text_color=moonphased,font=(fn_PR,11))

    self.ht_author_cat_div = customtkinter.CTkFrame(self.htn_category_div,
                                               width=100, height=50,fg_color=backup_ppl_2)
    self.ht_author_lbl = customtkinter.CTkLabel(self.ht_author_cat_div, text="Author",
                                               text_color=moonphased, font=(fn_PR, 11))

    self.ht_album_cat_div = customtkinter.CTkFrame(self.htn_category_div,fg_color=backup_ppl_2,
                                                width=100, height=50)
    self.ht_album_lbl = customtkinter.CTkLabel(self.ht_album_cat_div, text="Album",
                                                text_color=moonphased, font=(fn_PR, 11))




    self.ht_data_div = customtkinter.CTkFrame(self.hero_track_name,corner_radius=10,
                                                   width=240, height=150,fg_color=backup_ppl_2)
    self.ht_title_div = customtkinter.CTkFrame(self.ht_data_div ,fg_color=backup_ppl_2,
                                                   width=200, height=50)
    self.ht_song_title_lbl = customtkinter.CTkLabel(self.ht_title_div,text="Soft Spot",
                                               font=(fn_PM, 13),text_color=w_pure_white)


    self.ht_author_div = customtkinter.CTkFrame(self.ht_data_div ,
                                                    width=200, height=50,fg_color=backup_ppl_2)
    self.ht_song_author_lbl = customtkinter.CTkLabel(self.ht_author_div, text="Keshi",
                                                    font=(fn_PM, 13),text_color=w_pure_white)

    self.ht_album_div = customtkinter.CTkFrame(self.ht_data_div,fg_color=backup_ppl_2,
                                                   width=200, height=50)
    self.ht_song_album_lbl = customtkinter.CTkLabel(self.ht_album_div, text="Requiem",
                                                     font=(fn_PM, 13),text_color=w_pure_white)





    self.hero_times_played = customtkinter.CTkFrame(self.hero_track_image_details,
                                                 width=340,height=150,
                                                 fg_color=backup_ppl_2,
                                                 corner_radius=10)

    self.htp_lbl_a = customtkinter.CTkFrame(self.hero_times_played,
                                            width=340,height=40,
                                            corner_radius=10,fg_color=backup_ppl_2)
    self.htp_lbl_a_text = customtkinter.CTkLabel(self.htp_lbl_a,text="You played It",font=(fn_PR,12),text_color=w_main_white)


    self.htp_played_count = customtkinter.CTkFrame(self.hero_times_played,
                                            width=340,height=60,
                                           corner_radius=10,fg_color=backup_ppl_2)
    self.htp_played_count_text = customtkinter.CTkLabel(self.htp_played_count,
                                            text="678",
                                            font=("Cropar",30),text_color=w_pure_white)



    self.htp_lbl_b = customtkinter.CTkFrame(self.hero_times_played,
                                            width=340,height=40,
                                            corner_radius=10,fg_color=backup_ppl_2)
    self.htp_lbl_b_text = customtkinter.CTkLabel(self.htp_lbl_b,text="times",font=(fn_PR,12),text_color=w_main_white)






    self.recom_music_feed_wrapper = customtkinter.CTkScrollableFrame(self.main_music_feed_wrapper,
                                                 corner_radius=10,
                                                 width=content_frame_width,
                                                 fg_color=backup_ppl_2)





    # IGNORANCE
    self.ignorance_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                                    width=150,height=200,
                                                     fg_color=backup_ppl_2)

    self.ignorance_image = customtkinter.CTkImage(light_image=Image.open("Albums/Brand New Eyes.png"),
                                                  dark_image=Image.open("Albums/Brand New Eyes.png"),
                                                  size=(145,143))

    self.ignorance_holder = customtkinter.CTkButton(self.ignorance_wrapper,
                                                    text="",
                                                    image=self.ignorance_image,
                                                    fg_color=backup_ppl_2,
                                                    hover_color=tlr_purple_4,
                                                    height=150)

    self.ignorance_artist = customtkinter.CTkLabel(self.ignorance_wrapper,text="Paramore",font=(fn_PM,15),text_color=w_pure_white)
    self.ignorance_title = customtkinter.CTkLabel(self.ignorance_wrapper,text="Ignorance",font=(fn_PR,12),text_color="gray")

    self.ignorance_wrapper.pack_propagate(False)
    self.ignorance_wrapper.grid(row=0,column=1,pady=(4,2),padx=10)
    self.ignorance_holder.pack()
    self.ignorance_artist.pack(padx=(5,63),pady=(3,5))
    self.ignorance_title.pack(padx=(2,75))




    # AWAKE WRAPPER
    self.awake_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                                         width=150,height=200,
                                                         fg_color=backup_ppl_2)

    self.awake_image = customtkinter.CTkImage(light_image=Image.open("Albums/Awake.png"),
                                                  dark_image=Image.open("Albums/Awake.png"),
                                                  size=(150,150))

    self.awake_holder = customtkinter.CTkButton(self.awake_wrapper,
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
    self.awake_wrapper.grid(row=0,column=2,pady=10,padx=10)
    self.awake_holder.pack()
    self.awake_artist.pack(padx=(0,50))
    self.awake_title.pack(padx=(2,100))




    # I SWEAR I NEVER LEAVE AGAIN
    self.like_i_need_u_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                                width=150, height=200,
                                                fg_color=backup_ppl_2)


    self.like_i_need_u_image = customtkinter.CTkImage(light_image=Image.open("Albums/Reaper.png"),
                                              dark_image=Image.open("Albums/Reaper.png"),
                                              size=(140, 140))

    self.like_i_need_u_holder = customtkinter.CTkButton(self.like_i_need_u_wrapper,
                                                text="",
                                                image= self.like_i_need_u_image,
                                                fg_color=backup_ppl_2,
                                                hover_color=tlr_purple_4,
                                                height=150)

    self.like_i_need_u_artist = customtkinter.CTkLabel(self.like_i_need_u_wrapper, text="Keshi", font=(fn_PM, 15),
                                               text_color=w_pure_white)
    self.like_i_need_u_title = customtkinter.CTkLabel(self.like_i_need_u_wrapper, text="Like I Need U", font=(fn_PR, 12),
                                               text_color="gray")


    self.like_i_need_u_wrapper.pack_propagate(False)
    self.like_i_need_u_wrapper.grid(row=0, column=3, pady=10, padx=10)
    self.like_i_need_u_holder.pack(pady=(3,0))
    self.like_i_need_u_artist.pack(padx=(2, 95))
    self.like_i_need_u_title.pack(padx=(2,65))


    self.kissing_scars_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                                 width=150, height=200,
                                                 fg_color=backup_ppl_2)

    self.kissing_scars_image = customtkinter.CTkImage(light_image=Image.open("Albums/Selfish Machine.png"),
                                                      dark_image=Image.open("Albums/Selfish Machine.png"),
                                                      size=(140,143))

    self.kissing_scars_holder = customtkinter.CTkButton(self.kissing_scars_wrapper,text="",
                                                image=self.kissing_scars_image,
                                                fg_color=backup_ppl_2,
                                                hover_color=tlr_purple_4,
                                                height=150)

    self.kissing_scars_artist = customtkinter.CTkLabel(self.kissing_scars_wrapper,text="Pierce The Veil",
                                                font=(fn_PM, 15),
                                                text_color=w_pure_white)
    self.kissing_scars_title = customtkinter.CTkLabel(self.kissing_scars_wrapper,text="Kissing in Scars",
                                                font=(fn_PR, 12),
                                                text_color="gray")


    self.kissing_scars_wrapper.pack_propagate(False)
    self.kissing_scars_wrapper.grid(row=0, column=4, pady=10, padx=10)
    self.kissing_scars_holder.pack(pady=2)
    self.kissing_scars_artist.pack(padx=(2, 30))
    self.kissing_scars_title.pack(padx=(2, 45))





    self.a_twist_in_my_story_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                                        width=150, height=200,
                                                        fg_color=backup_ppl_2)

    self.a_twist_in_my_story_image = customtkinter.CTkImage(light_image=Image.open("Albums/A Twist in my Story.png"),
                                                            dark_image=Image.open("Albums/A Twist in my Story.png"),
                                                            size=(150,150))

    self.a_twist_in_my_story_holder = customtkinter.CTkButton(self.a_twist_in_my_story_wrapper,text="",
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
    self.a_twist_in_my_story_wrapper.grid(row=1, column=1, pady=10, padx=10)
    self.a_twist_in_my_story_holder.pack()
    self.a_twist_in_my_story_artist.pack(padx=(2, 40))
    self.a_twist_in_my_story_title.pack(padx=(2, 80))







    self.blue_wrapper = customtkinter.CTkFrame(self.recom_music_feed_wrapper,
                                                              width=150, height=200,
                                                              fg_color=backup_ppl_2)

    self.blue_image = customtkinter.CTkImage(light_image=Image.open("Albums/Bandaids.png"),
                                                            dark_image=Image.open("Albums/Bandaids.png"),
                                                            size=(145, 150))

    self.blue_holder = customtkinter.CTkButton(self.blue_wrapper, text="",
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
    self.blue_wrapper.grid(row=1, column=2, pady=10, padx=10)
    self.blue_holder.pack()
    self.blue_artist.pack(padx=(0, 100))
    self.blue_title.pack(padx=(2, 115))










    self.hero_track_cat_div.grid_propagate(False)
    self.hero_track_cat_div.pack(fill="x",pady=(5))
    self.hero_track_cat_lbl.grid(row=0,column=1)

    self.hero_track_wrapper.pack_propagate(False)
    self.hero_track_wrapper.pack(fill="x")


    self.hero_track_image_frame.grid(row=1, column=0)
    self.hero_track_img_lbl.grid(row=0,column=1)

    self.hero_track_image_details.grid(row=1, column=1,padx=(10,10))
    self.hero_track_image_details.grid_propagate(False)

    self.hero_track_image_details.grid_columnconfigure(0, weight=1)
    self.hero_track_image_details.grid_columnconfigure(1, weight=1)

    self.hero_track_name.grid_propagate(False)
    self.hero_track_name.pack(pady=(0,5))



    self.htn_category_div.grid_propagate(False)
    self.htn_category_div.grid(row=0,column=1)
    self.ht_title_cat_div.pack_propagate(False)
    self.ht_title_cat_div.grid(row=0,column=1,padx=(20,0))
    self.ht_title_lbl.pack(padx=(10,0),pady=8)

    self.ht_author_cat_div.pack_propagate(False)
    self.ht_author_cat_div.grid(row=1,column=1,padx=(20,0))
    self.ht_author_lbl.pack(padx=(10,0),pady=8)

    self.ht_album_cat_div.pack_propagate(False)
    self.ht_album_cat_div.grid(row=2, column=1,padx=(20,0))
    self.ht_album_lbl.pack(padx=(10,0),pady=8)



    self.ht_data_div.grid_propagate(False)
    self.ht_data_div.grid(row=0,column=2)


    self.ht_title_div.grid_propagate(False)
    self.ht_title_div.grid(row=0, column=2)
    self.ht_song_title_lbl.grid(row=0,column=1,padx=(80,0),pady=8)

    self.ht_author_div.grid_propagate(False)
    self.ht_author_div.grid(row=1, column=2)
    self.ht_song_author_lbl.grid(row=0,column=1,padx=(80,0),pady=8)

    self.ht_album_div.grid_propagate(False)
    self.ht_album_div.grid(row=2, column=2)
    self.ht_song_album_lbl.grid(row=0,column=1,padx=(80,0),pady=8)


    self.hero_times_played.pack_propagate(False)
    self.hero_times_played.pack(pady=(5,0))

    self.htp_lbl_a.grid_propagate(False)
    self.htp_lbl_a.pack(pady=(20,0))
    self.htp_lbl_a_text.grid(row=0,column=1,padx=(80,0))

    self.htp_played_count.pack()
    self.htp_played_count_text.pack(pady=(0,10))

    self.htp_lbl_b.grid_propagate(False)
    self.htp_lbl_b.pack(pady=(5,8))
    self.htp_lbl_b_text.pack(padx=(100,20))



    self.recom_music_feed_wrapper.pack(padx=0, pady=(10),fill="both",expand=True)



def show_trends(self):

    for widget in self.button_frame.winfo_children():
        widget.destroy()

    # SIDEBAR BUTTONS
    self.feed_btn = customtkinter.CTkButton(self.button_frame,text="Feed",
                                            command=lambda:show_plays(self),
                                            font=(fn_PM, 12),
                                            hover_color=tlr_purple_4,
                                            fg_color=tlr_dark)

    self.trends_btn = customtkinter.CTkButton(self.button_frame , text="Trends",
                                           command=lambda:show_trends(self),
                                           font=(fn_PM, 12),
                                           hover_color=tlr_purple_4,
                                           fg_color=tlr_purple_3)

    self.library_btn = customtkinter.CTkButton(self.button_frame, text="Library",
                                           command=lambda: show_library(self),
                                           font=(fn_PM, 12),
                                           hover_color=tlr_purple_4,
                                           fg_color=tlr_dark)

    self.logout_btn = customtkinter.CTkButton(self.button_frame, text="Log Out",
                                           font=(fn_PM, 12),
                                           hover_color=tlr_purple_4,
                                           fg_color=tlr_dark)




    self.feed_btn.pack(pady=10, padx=10, fill="x")
    self.trends_btn.pack(pady=10, padx=10, fill="x")
    self.library_btn.pack(pady=10, padx=10, fill="x")
    self.logout_btn.pack(pady=(150, 10), padx=10, fill="x")






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

    self.trends_hero_track_wrapper = customtkinter.CTkFrame(self.main_music_feed_wrapper,
                                                     width=content_frame_width, height=300,
                                                     fg_color=tlr_purple_3)
    self.trend_hero_track_lbl = customtkinter.CTkLabel(self.trends_hero_track_wrapper,
                                                   text="TREND HERO TRACK WRAPPER",
                                                   font=("Poppins", 30, "bold"),
                                                   text_color=w_main_white)

    self.trend_recom_music_feed_wrapper = customtkinter.CTkScrollableFrame(self.main_music_feed_wrapper,
                                                                     width=content_frame_width,
                                                                     fg_color=tlr_purple_2)

    self.trend_recom_music_feed_lbl = customtkinter.CTkButton(self.trend_recom_music_feed_wrapper,
                                                       text="TREND RECOM MUSIC FEED WRAPPER",
                                                       font=(fn_PR, 12),
                                                       width=30,height=30,
                                                       text_color=w_main_white)


    self.trends_hero_track_wrapper.pack(padx=0, pady=(0, 10), fill="x")
    self.trends_hero_track_wrapper.pack_propagate(False)
    self.trend_hero_track_lbl.pack()

    self.trend_recom_music_feed_wrapper.pack(padx=0, pady=(0, 10),fill="both",expand=True)
    self.trend_recom_music_feed_wrapper.pack_propagate(False)
    self.trend_recom_music_feed_lbl.grid(row=0,column=1,padx=10,pady=10)




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

    self.trends_btn = customtkinter.CTkButton(self.button_frame , text="Trends",
                                           command=lambda: show_trends(self),
                                           font=(fn_PM, 12),
                                           hover_color=tlr_purple_4,
                                           fg_color=tlr_dark)

    self.library_btn = customtkinter.CTkButton(self.button_frame, text="Library",
                                           command=lambda: show_library(self),
                                           font=(fn_PM, 12),
                                           hover_color=tlr_purple_4,
                                           fg_color=tlr_purple_3,)

    self.logout_btn = customtkinter.CTkButton(self.button_frame, text="Log Out",

                                              font=(fn_PM, 12),
                                              hover_color=tlr_purple_4,
                                              fg_color=tlr_dark)


    self.feed_btn.pack(pady=10, padx=10, fill="x")
    self.trends_btn.pack(pady=10, padx=10, fill="x")
    self.library_btn.pack(pady=10, padx=10, fill="x")
    self.logout_btn.pack(pady=(150, 10), padx=10, fill="x")




    # TOP NAV  ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ====
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



    # MAIN MUSIC  ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ====
    for widget in self.main_music_feed_wrapper.winfo_children():
        widget.destroy()

    tab_3_content = customtkinter.CTkLabel(self.main_music_feed_wrapper, text="Content for Tab 3", font=("Arial", 20))
    tab_3_content.pack(pady=20)




