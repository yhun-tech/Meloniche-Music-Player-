import customtkinter
from customtkinter import CTkImage
from index_contr import go_to_feed,close_feed
import os
from __init__ import tlr_dark,tlr_purple_1,tlr_purple_2,tlr_purple_3,tlr_purple_4,\
    backup_ppl_1,backup_ppl_2,w_f5,w_main_white,w_pure_white

from __init__ import fn_PR,fn_PM

from tkinter import StringVar, Toplevel, Image
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk

customtkinter.set_appearance_mode("dark")

class Index(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")

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

        # HERO - background
        self.my_auth_hero = customtkinter.CTkFrame(self,fg_color=tlr_dark)
        self.my_auth_hero.pack(fill="both", expand=True)


        # AUH TAB VIEW
        self.my_tab_nav = customtkinter.CTkTabview(self.my_auth_hero
                                                   ,fg_color=tlr_dark,
                                                   text_color=w_main_white,
                                                   segmented_button_fg_color=tlr_dark,
                                                   segmented_button_unselected_color=tlr_dark,
                                                   segmented_button_selected_color=tlr_purple_3,
                                                   segmented_button_selected_hover_color=tlr_purple_4,
                                                   segmented_button_unselected_hover_color=tlr_purple_4
                                                   )


        self.my_tab_nav.pack(fill="both", expand=True,pady=0,padx=0)

        self.sgn_tab = self.my_tab_nav.add("Sign Up")
        self.lgn_tab = self.my_tab_nav.add("Login")


        # SIGN UP ================================================== ============================



        # VECTOR FRAME
        self.my_auth_vector_frame = customtkinter.CTkFrame(self.lgn_tab,
                                                     width=500, height=600, fg_color=backup_ppl_1)
        self.my_auth_vector_frame.place(relx=0.4, rely=0.5, anchor="e")





        # MY SIGN UP WRAPPER
        self.my_sgn_auth_wrapper = customtkinter.CTkFrame(self.sgn_tab,
                                                      width=450, height=500,
                                                      corner_radius=20,
                                                      fg_color=backup_ppl_2)

        self.my_sgn_auth_wrapper.place(relx=0.6, rely=0.5, anchor="w")
        self.my_sgn_auth_wrapper.pack_propagate(False)



        # SIGN UP TITLE
        self.my_sgn_up_title = customtkinter.CTkLabel(self.my_sgn_auth_wrapper,text="SIGN UP",
                                               font=("Cropar",40))
        self.my_sgn_up_title.pack(pady=(50, 3))
        self.my_sgn_up_descr = customtkinter.CTkLabel(self.my_sgn_auth_wrapper,
                                                      text="Create your Melodic Account",
                                                      text_color=w_main_white,
                                                      font=("Poppins", 12))
        self.my_sgn_up_descr.pack(pady=(3,0))


        # Username
        self.my_sgn_username = customtkinter.CTkEntry(self.my_sgn_auth_wrapper,
                                                  font=("Poppins", 12),
                                                  fg_color=backup_ppl_2,
                                                  placeholder_text="Username",placeholder_text_color=w_main_white,
                                                  width=250,height=30)
        self.my_sgn_username.pack(pady=(50,10))

        self.my_sgn_email = customtkinter.CTkEntry(self.my_sgn_auth_wrapper,
                                                   font=("Poppins", 12),
                                                   placeholder_text="Email", placeholder_text_color=w_main_white,
                                                   fg_color=backup_ppl_2,
                                                   width=250, height=30)
        self.my_sgn_email.pack(pady=(10))

        # Password
        self.my_sgn_password = customtkinter.CTkEntry(self.my_sgn_auth_wrapper,
                                                  font=("Poppins",12),
                                                  placeholder_text="Password",placeholder_text_color=w_main_white,
                                                  fg_color=backup_ppl_2,
                                                  width=250,height=30)
        self.my_sgn_password.pack(pady=(10))



        # SIGN UP BUTTON
        self.my_sgnup_button = customtkinter.CTkButton(self.my_sgn_auth_wrapper,
                                                  command=lambda:go_to_feed(self),
                                                  text="Sign Up",
                                                  hover_color=tlr_purple_4,
                                                  font=("Poppins",13),
                                                  fg_color=tlr_purple_3,
                                                  width=250,height=35)
        self.my_sgnup_button.pack(pady=(20,10))





















        # LOGIN ================================================== ============================

        # VECTOR FRAME
        self.my_auth_vector_frame = customtkinter.CTkFrame(self.lgn_tab,
                                                     width=500, height=600, fg_color=backup_ppl_1)
        self.my_auth_vector_frame.place(relx=0.4, rely=0.5, anchor="e")


        # MY LOGIN WRAPPER
        self.my_auth_wrapper = customtkinter.CTkFrame(self.lgn_tab,
                                                      width=450, height=500,
                                                      corner_radius=20,
                                                      fg_color=backup_ppl_2)

        self.my_auth_wrapper.place(relx=0.6, rely=0.5, anchor="w")
        self.my_auth_wrapper.pack_propagate(False)

        # LOGIN TITLE
        self.my_title = customtkinter.CTkLabel(self.my_auth_wrapper,text="LOGIN",
                                               font=("Cropar",40))
        self.my_title.pack(pady=(50, 3))
        self.my_lgn_descr = customtkinter.CTkLabel(self.my_auth_wrapper, text="Welcome back to Meloniche!",
                                               font=("Poppins", 12))
        self.my_lgn_descr.pack(pady=(3, 0))

        # Username
        self.my_username = customtkinter.CTkEntry(self.my_auth_wrapper,
                                                  font=("Poppins", 12),
                                                  fg_color=backup_ppl_2,
                                                  placeholder_text="Username",placeholder_text_color=w_main_white,
                                                  width=250,height=30)
        self.my_username.pack(pady=(50,10))


        # Password
        self.my_password = customtkinter.CTkEntry(self.my_auth_wrapper,
                                                  font=("Poppins",12),
                                                  placeholder_text="Password",placeholder_text_color=w_main_white,
                                                  fg_color=backup_ppl_2,
                                                  width=250,height=30)
        self.my_password.pack(pady=(10))



        # LOGIN BUTTON
        self.my_login_button = customtkinter.CTkButton(self.my_auth_wrapper,
                                                  command=lambda:go_to_feed(self),
                                                  text="Login",
                                                  hover_color=tlr_purple_4,
                                                  font=("Poppins",13),
                                                  fg_color=tlr_purple_3,
                                                  width=250,height=35)
        self.my_login_button.pack(pady=(20,10))

        self.login_case_frame = customtkinter.CTkFrame(self.my_auth_wrapper,
                                                       width=250,height=30,
                                                       fg_color=backup_ppl_2)
        self.login_case_frame.pack(pady=2)
        self.login_case_frame.pack_propagate(False)





if __name__ == "__main__":
    index = Index()
    index.mainloop()

