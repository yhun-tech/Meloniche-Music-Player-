import customtkinter
from __init__ import tlr_dark, tlr_purple_1,tlr_purple_2, tlr_purple_3,tlr_purple_4,\
    w_main_white,w_f5,w_pure_white,backup_ppl_1,backup_ppl_2,moonphased,fn_PM,fn_PR

from feed_contr import show_plays,show_trends,show_library,default_aside_right
import os
from tkinter import StringVar, Toplevel
from PIL import Image



class Feed(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Feed")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(BASE_DIR, "Images", "MELONICHE LOGO.ico")
        self.iconbitmap(icon_path)

        app_width = 1200
        app_height = 620

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (app_width / 2))
        y = int((screen_height / 2) - (app_height / 2))
        self.geometry(f"{app_width}x{app_height}+{x}+{y}")


        sidebar_width = 200
        content_frame_width = 700
        aside_width = 400

        # FEED Frame
        self.feed_hero = customtkinter.CTkFrame(self, fg_color=tlr_dark)
        self.feed_hero.pack(fill="both", expand=True)




        # SIDEBAR Frame =============================================
        self.my_sidebar = customtkinter.CTkFrame(self.feed_hero,
                                                 fg_color=tlr_dark,
                                                 height=screen_height,
                                                 width=sidebar_width)
        self.my_sidebar.grid(row=0,column=0)
        self.my_sidebar.pack_propagate(False)


        # Logo Frame
        self.my_logo_frame = customtkinter.CTkFrame(self.my_sidebar,
                                                    fg_color=tlr_dark,
                                                    height=50,
                                                    width=200)
        self.my_logo_frame.pack(pady=10, padx=10)
        self.my_logo_frame.pack_propagate(False)

        self.my_logo = customtkinter.CTkImage(
            light_image=Image.open("Images/MELONICHE LOGO.png"),
            dark_image=Image.open("Images/MELONICHE LOGO.png"),
            size=(30, 30)
        )

        self.my_logo_holder = customtkinter.CTkLabel(self.my_logo_frame, text="",
                                                     image=self.my_logo)
        self.my_logo_holder.place(relx=0.2, rely=0.5, anchor="e")

        self.my_logo_text = customtkinter.CTkLabel(self.my_logo_frame,
                                                   text="MELOniche",
                                                   text_color=w_main_white,
                                                   font=("Cropar", 20), height=50)
        self.my_logo_text.place(relx=0.25, rely=0.5, anchor="w")


        # BUTTON FRAME
        self.button_frame = customtkinter.CTkFrame(self.my_sidebar,fg_color=tlr_dark)
        # SIDEBAR BUTTONS
        self.feed_btn = customtkinter.CTkButton(self.button_frame, text="Feed",
                                               command=lambda:show_plays(self),
                                               font=(fn_PM, 12),
                                               hover_color=tlr_purple_4,
                                               fg_color=tlr_dark)
        self.trends_btn = customtkinter.CTkButton(self.button_frame, text="Trends",
                                               command=lambda:show_trends(self),
                                               font=(fn_PM, 12),
                                               hover_color=tlr_purple_4,
                                               fg_color=tlr_dark)
        self.library_btn = customtkinter.CTkButton(self.button_frame, text="Library",
                                               command=lambda:show_library(self),
                                               font=(fn_PM, 12),
                                               hover_color=tlr_purple_4,
                                               fg_color=tlr_dark)

        self.logout_btn = customtkinter.CTkButton(self.button_frame, text="Log Out",
                                                   command=lambda: show_library(self),
                                                   font=(fn_PM, 12),
                                                   hover_color=tlr_purple_4,
                                                   fg_color=tlr_dark)




        self.button_frame.pack(pady=10,padx=10,fill="both")
        self.feed_btn.pack(pady=10, padx=10, fill="x")
        self.trends_btn.pack(pady=10, padx=10, fill="x")
        self.library_btn.pack(pady=10, padx=10, fill="x")










        # Content Frame ==============================================
        self.content_frame = customtkinter.CTkFrame(self.feed_hero, width=content_frame_width,
                                                    fg_color=tlr_dark)

        # top nav bar
        self.cf_top_nav = customtkinter.CTkFrame(self.content_frame,
                                                 width=content_frame_width,height=50,
                                                 fg_color=backup_ppl_2)
        self.top_n_searchbar = customtkinter.CTkEntry(self.cf_top_nav,
                                                      width=200,
                                                      height=30,
                                                      fg_color=backup_ppl_2,
                                                      border_color=backup_ppl_1,
                                                      font=(fn_PR,12),
                                                      placeholder_text="Search Anything......")

        # music feed ==========================================
        self.main_music_feed_wrapper = customtkinter.CTkFrame(self.content_frame,
                                                 width=content_frame_width,
                                                 fg_color=tlr_dark)


        # ASIDE RIGHT ==============================================
        self.aside_right = customtkinter.CTkFrame(self.feed_hero, width=aside_width,
                                                  fg_color=tlr_dark)







        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(10))



        self.cf_top_nav.grid_propagate(False)
        self.cf_top_nav.pack(padx=0, pady=(10, 10), fill="x")
        self.top_n_searchbar.grid(row=0,column=1,pady=(9,8),padx=10)



        self.main_music_feed_wrapper.pack_propagate(False)
        self.main_music_feed_wrapper.pack(padx=0, pady=(10, 0), fill="both", expand=True)

        self.aside_right.grid(row=0, column=2, sticky="nsew", padx=0)







        show_plays(self)
        default_aside_right(self)

