import customtkinter as ctk
import webbrowser
import pyperclip
import requests
import tkinter
import tkinter.messagebox
import tkinter.ttk
import os
import csv
import ctypes
import time
import testAPI
from tkinter import filedialog
from howlongtobeatpy import HowLongToBeat
from CTkTable import *
from PIL import Image, ImageTk
import controlsAPI
import controlsUserID
import shutil
from datetime import datetime, timedelta

from language import LANGUAGES


CURRENT_LANGUAGE = 'ru'

class AuthWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        WIGHT = 480
        HEIGHT = 384

        self.CURRENT_LANGUAGE = 'ru'

        self.title(LANGUAGES[CURRENT_LANGUAGE]['auth_title'])
        self.geometry(f"{WIGHT}x{HEIGHT}")

        # Получаем размеры окна
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()

        # Вычисляем координаты для центрирования окна
        x = (window_width / 2) - (WIGHT / 2)
        y = (window_height / 2) - (HEIGHT / 2)

        # Устанавливаем координаты окна
        self.geometry(f"{WIGHT}x{HEIGHT}+{int(x)}+{int(y)}")

        # фрейм приветствия
        self.label_welcome = ctk.CTkLabel(self, text=LANGUAGES[CURRENT_LANGUAGE]['welcome_label'])
        self.label_welcome.place(relx=0.5, rely=0.1, anchor="center")

        # фрейм с ключом API 
        self.steam_api_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.steam_api_frame.place(relx=0.5, rely=0.3, anchor="center")
        self.label_api_key = ctk.CTkLabel(self.steam_api_frame, text=LANGUAGES[CURRENT_LANGUAGE]['api_key_label'])
        self.label_api_key.grid(row=0, column=0)
        self.entry_api_key = ctk.CTkEntry(self.steam_api_frame)
        self.entry_api_key.grid(row=0, column=1)
        self.button_confirm_api_key = ctk.CTkButton(self.steam_api_frame, text=LANGUAGES[CURRENT_LANGUAGE]['confirm_api_button'], command=self.confirm_api_button_event)
        self.button_confirm_api_key.grid(row=1, column=0, pady=(10,0))
        self.label_status = ctk.CTkLabel(self.steam_api_frame, text=LANGUAGES[CURRENT_LANGUAGE]['status_label'], text_color="red", font=("Arial", 12))
        self.label_status.grid(row=0, column=2)
        self.button_how_to_get = ctk.CTkButton(self.steam_api_frame, text=LANGUAGES[CURRENT_LANGUAGE]['how_to_get_button'], command=self.on_how_to_get_button_click)
        self.button_how_to_get.grid(row=1, column=1, pady=(10,0))
        self.entry_api_key.insert(0, controlsAPI.getAPI_Key())

        # фрейм с юзер айди
        self.user_id_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.user_id_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.label_steam_id = ctk.CTkLabel(self.user_id_frame, text=LANGUAGES[CURRENT_LANGUAGE]['steam_id_label'])
        self.label_steam_id.grid(row=0, column=0)
        self.entry_steam_id = ctk.CTkEntry(self.user_id_frame)
        self.entry_steam_id.grid(row=0, column=1)
        self.button_confirm_steam_id = ctk.CTkButton(self.user_id_frame, text=LANGUAGES[CURRENT_LANGUAGE]['confirm_steam_id_button'], command=self.confirm_user_id_button_event)
        self.button_confirm_steam_id.grid(row=1, column=0, pady=(10,0))
        self.button_confirm_steam_id.configure(state="disabled")
        self.entry_steam_id.insert(0, controlsUserID.getUser_ID())

        # фрейм перехода в гм
        self.button_next = ctk.CTkButton(self, text=LANGUAGES[CURRENT_LANGUAGE]['next_button'], command=self.on_next_button_click, width=200, height=50)
        self.button_next.place(relx=0.5, rely=0.7, anchor="center")
        self.button_next.configure(state="disabled")

        # фрейм со сменой языка
        self.russian_flag = ctk.CTkImage(Image.open("russian_flag.png"), size=(54, 36))
        self.american_flag = ctk.CTkImage(Image.open("american_flag.png"), size=(54, 36))
        self.language_btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.language_btn_frame.place(relx=0.5, rely=0.9, anchor="center")
        self.russian_btn = ctk.CTkButton(self.language_btn_frame, image=self.russian_flag,fg_color='transparent', text="", command=lambda: self.set_language('ru'), width=54, height=36)
        self.russian_btn.pack(side="left", padx=(0, 10))
        self.american_btn = ctk.CTkButton(self.language_btn_frame, image=self.american_flag,fg_color='transparent', text="", command=lambda: self.set_language('en'), width=54, height=36)
        self.american_btn.pack(side="left", padx=(10, 0))

    def confirm_user_id_button_event(self):
        userID = self.entry_steam_id.get()
        if(len(userID) != 17):
            self.entry_steam_id.configure(placeholder_text="Invalid length. Please Try Again")
            self.entry_steam_id.configure(fg_color='#B22222')
            return
        steamPath = "ISteamUser/GetPlayerSummaries/v0002/"
        url = f"{controlsAPI.steamAPIURL}{steamPath}/"
        extraFields = {"key":controlsAPI.getAPI_Key(), "steamids":{userID}}
        response = requests.get(url,params=extraFields)
        if(response.status_code == 200):
            self.entry_steam_id.configure(fg_color='#008000')
            controlsUserID.setUser_ID(self.entry_steam_id.get())
            self.button_next.configure(state="normal")
            return
        print('skip all, why?')
        self.entry_steam_id.configure(fg_color='#B22222')



    # смена текста сразу после нажатия на кнопку
    def update_ui_text(self):
        self.title(LANGUAGES[CURRENT_LANGUAGE]['auth_title'])
        self.label_welcome.configure(text=LANGUAGES[CURRENT_LANGUAGE]['welcome_label'])
        self.label_api_key.configure(text=LANGUAGES[CURRENT_LANGUAGE]['api_key_label'])
        self.button_confirm_api_key.configure(text=LANGUAGES[CURRENT_LANGUAGE]['confirm_api_button'])
        self.label_status.configure(text=LANGUAGES[CURRENT_LANGUAGE]['status_label'])
        self.button_how_to_get.configure(text=LANGUAGES[CURRENT_LANGUAGE]['how_to_get_button'])
        self.label_steam_id.configure(text=LANGUAGES[CURRENT_LANGUAGE]['steam_id_label'])
        self.button_confirm_steam_id.configure(text=LANGUAGES[CURRENT_LANGUAGE]['confirm_steam_id_button'])
        self.button_next.configure(text=LANGUAGES[CURRENT_LANGUAGE]['next_button'])

    # смена языка
    def set_language(self, language):
        global CURRENT_LANGUAGE
        CURRENT_LANGUAGE = language

        # Закрываем текущее окно
        self.destroy()

        # Создаем новое окно авторизации
        new_auth_window = AuthWindow()
        new_auth_window.update_ui_text()
        new_auth_window.mainloop()


    # функция нажатия на кнопку "Как получить веб API ключ Steam"
    def on_how_to_get_button_click(self):
        url = "https://steamcommunity.com/dev/apikey"
        message = f"Чтобы получить веб API ключ Steam вы должны перейти по этой ссылке и скопировать ключ там:\n\n{url}"
        self.show_info_message(message, url)

    # функция подтверждения веб Steam API ключа
    def confirm_api_button_event(self):
        works = testAPI.testAPI(self.entry_api_key.get())
        if works == True:
            controlsAPI.setAPI_Key(self.entry_api_key.get())
            self.entry_api_key.configure(fg_color='#008000')
            self.button_confirm_steam_id.configure(state="normal")
        else:
            self.entry_api_key.delete(0,'end')
            self.entry_api_key.configure(placeholder_text="Invalid API. Please Try Again")
            self.entry_api_key.configure(fg_color='#B22222')
    
    # функция отображения информационного окна
    def show_info_message(self, message, url):
        info_window = ctk.CTkToplevel(self)
        info_window.title("Как получить?")
        info_window.geometry("600x200")

        label_message = ctk.CTkLabel(info_window, text=message)
        label_message.pack(pady=10)

        button_copy = ctk.CTkButton(info_window, text="Скопировать ссылку", command=lambda: pyperclip.copy(url))
        button_copy.pack(pady=5)

        button_open = ctk.CTkButton(info_window, text="Открыть ссылку", command=lambda: webbrowser.open(url))
        button_open.pack(pady=5)

    # функция нажатия на кнопку перехода на окно главного меню
    def on_next_button_click(self):
            self.destroy()
            new_main_menu_window = MainMenuWindow()
            new_main_menu_window.mainloop()


class MainMenuWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        WIGHT = 1280
        HEIGHT = 720

        self.title(LANGUAGES[CURRENT_LANGUAGE]['main_menu_title'])
        self.geometry(f"{WIGHT}x{HEIGHT}")

        # Получаем размеры окна
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()

        # Вычисляем координаты для центрирования окна
        x = (window_width / 2) - (WIGHT / 2)
        y = (window_height / 2) - (HEIGHT / 2)

        # Устанавливаем координаты окна
        self.geometry(f"{WIGHT}x{HEIGHT}+{int(x)}+{int(y)}")

        userID = controlsUserID.getUser_ID()

        # фрейм для верхних кнопок
        self.top_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.top_frame.place(relx=0.5, rely=0, anchor="center", relwidth=1, relheight=0.15)
        self.button_change_user = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['change_user_button'], command=self.on_auth_button_click)
        self.button_change_user.place(relx=0.74, rely=0.6, relwidth=0.12, relheight=0.3)
        self.button_settings = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['settings_button'], command=self.on_settings_button_click)
        self.button_settings.place(relx=0.88, rely=0.6, relwidth=0.1, relheight=0.3)

        # фрейм для прво-нижних кнопок
        self.top_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.top_frame.place(relx=0.9, rely=0.9, anchor="center", relwidth=0.22, relheight=0.22)
        self.button_games_user = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['users_games_button'])
        self.button_games_user.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.3)
        self.button_ach_user = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['users_ach_button'])
        self.button_ach_user.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.3)

        # фрейм для данных о пользователе
        self.top_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.top_frame.place(relx=0.9, rely=0.43, anchor="center", relwidth=0.22, relheight=0.6)
        userDataValues = self.get_user_data()
        user_image = ctk.CTkImage(Image.open("C:\\ProgramData\\SteamAchHunt\\profile_pic.jpg"), size=(100, 100))
        self.user_image_label = ctk.CTkLabel(self, text="", image=user_image)
        self.user_image_label.place(relx=0.85, rely=0.15, relwidth=0.078, relheight=0.14)
        self.user_name_label = ctk.CTkLabel(self, text=userDataValues[2], fg_color="#2F4F4F", font=("Times New Roman",20,"bold"))
        self.user_name_label.place(relx=0.79, rely=0.29, relwidth=0.2, relheight=0.06)
        gameReturnValues = self.ownedGameData(userID,0)
        if gameReturnValues[0] == False:
            print("ERROR PULLING GAMES")
        self.number_games_label = ctk.CTkLabel(self, text=f"{LANGUAGES[CURRENT_LANGUAGE]['number_games_label']}{gameReturnValues[1]}", fg_color="#2F4F4F", font=("Times New Roman",20,"bold"))
        self.number_games_label.place(relx=0.79, rely=0.34, relwidth=0.2, relheight=0.06)
        # тут можно незаконченные и неначатые игры вписать
        user_level = self.get_user_level()
        self.user_level_label = ctk.CTkLabel(self, text=f"{LANGUAGES[CURRENT_LANGUAGE]['user_level']}{user_level[1]}", fg_color="#2F4F4F", font=("Times New Roman",20,"bold"))
        self.user_level_label.place(relx=0.79, rely=0.65, relwidth=0.2, relheight=0.06)

        # фрейм для Данных послежних запущенных игр
        self.main_table_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.main_table_frame.place(relx=0.55, rely=0.535, anchor="center", relwidth=0.4, relheight=0.8)
        recent_games = self.get_recent_games(controlsUserID.getUser_ID(), controlsAPI.getAPI_Key())
        values = [("Название", "Всего", "За последние\n2 недели")]
        values.extend([(game[0], f"{game[2] // 60} ч", f"{game[3] // 60} ч") for game in recent_games])
        self.main_table = CTkTable(self.main_table_frame, column=3, row=len(values), values=values)
        self.main_table.pack(expand=True, fill="both", padx=10, pady=(60,10))
        self.last_games_label = ctk.CTkLabel(self, text=f"{LANGUAGES[CURRENT_LANGUAGE]['last_games_label']}", fg_color="#2F4F4F", font=("Times New Roman",20,"bold"))
        self.last_games_label.place(relx=0.4, rely=0.15, relwidth=0.3, relheight=0.06)

        # фрейм для данных о последних полученных достижениях
        self.main_table_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.main_table_frame.place(relx=0.17, rely=0.535, anchor="center", relwidth=0.3, relheight=0.8)
        self.last_achievements_disc_label = ctk.CTkLabel(self, text=f"{LANGUAGES[CURRENT_LANGUAGE]['last_achievements_disc_label']}", fg_color="#2F4F4F", font=("Times New Roman",16,"bold"))
        self.last_achievements_disc_label.place(relx=0.05, rely=0.4, relwidth=0.25, relheight=0.3)
        self.last_achievements_label = ctk.CTkLabel(self, text=f"{LANGUAGES[CURRENT_LANGUAGE]['last_achievements_label']}", fg_color="#2F4F4F", font=("Times New Roman",20,"bold"))
        self.last_achievements_label.place(relx=0.07, rely=0.15, relwidth=0.2, relheight=0.06)



    # функция получения имени пользователя и автарки
    def get_user_data(self):
        userID = controlsUserID.getUser_ID()
        steamPath = "ISteamUser/GetPlayerSummaries/v0002/"
        url = f"{controlsAPI.steamAPIURL}{steamPath}/"
        extraFields = {"key":controlsAPI.getAPI_Key(), "steamids":{userID}}

        try:
            response = requests.get(url,params=extraFields)
            if(response.status_code == 200):
                jdata = response.json()

                #Check if User Exists
                try:
                    personalData = jdata["response"]["players"][0]
            
                except IndexError:
                    print(IndexError)
                    return [False,"",""]
            
                #download picture
                url = personalData["avatarfull"]
                response=requests.get(url,stream=True)
                with open("C:\\ProgramData\\SteamAchHunt\\profile_pic.jpg","wb") as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response

                return [True,"C:\\ProgramData\\SteamAchHunt\\profile_pic.jpg",personalData["personaname"]]
            
            else:
                return [False,"",""]
        
        except Exception as e:
            print(f"Error in owned Game Data: {e} userID: {userID}")


    #  функция получения данных по играм на аккаунте
    def ownedGameData(self,userID: str, attempt: int):
        if attempt == 4:
            print('here 264')
            return [False,"",[]]
        steamPath = "IPlayerService/GetOwnedGames/v0001/"
        url = f"{controlsAPI.steamAPIURL}{steamPath}/"
        extraFields = {"key":controlsAPI.getAPI_Key(), "steamid":userID,
                    "include_appinfo":"true","include_played_free_games":"true"}
        try:
            response = requests.get(url,params=extraFields)
            if(response.status_code == 200):
                jdata = response.json()

                return [True, str(jdata['response']['game_count']),jdata['response']['games']]

            else:
                print('here 123')
                return [False,"",[]]
                
        
        except Exception as e:
            print(e)


    # функция получения лвла юзера
    def get_user_level(self):
        userID = controlsUserID.getUser_ID()
        steamPath = "IPlayerService/GetSteamLevel/v1/"
        url = f"{controlsAPI.steamAPIURL}{steamPath}/"
        extraFields = {"key":controlsAPI.getAPI_Key(), "steamid":{userID}}

        try:
            response = requests.get(url,params=extraFields)
            if(response.status_code == 200):
                jdata = response.json()

                try:
                    personalData = jdata["response"]["player_level"]
            
                except IndexError:
                    return [False,222222]
            
                response=requests.get(url,stream=True)
                del response

                return [True, personalData]
            
            else:
                return [False, 123123]
        
        except Exception as e:
            print(f"Error in owned Game Data: {e} userID: {userID}")

    # функция получения последних 5 запущенных игр на аккаунте
    def get_recent_games(self,steam_id, api_key):
        url = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={api_key}&steamid={steam_id}&format=json"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка на ошибки
            games_data = response.json()["response"]["games"]

            recent_games = []
            for game in games_data[:5]:  # Берем только первые 5 игр
                game_name = game["name"]
                game_icon = game["img_icon_url"]
                playtime_forever = game["playtime_forever"]
                playtime_2weeks = game["playtime_2weeks"]
                recent_games.append((game_name, game_icon, playtime_forever, playtime_2weeks))

            return recent_games

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении данных из SteamAPI: {e}")
            return []


    # функция нажатия на кнопку перехода на окно авторизации
    def on_auth_button_click(self):
        self.destroy()
        auth_window = AuthWindow()
        auth_window.mainloop()

    # функция нажатия на кнопку перехода на окно настроек
    def on_settings_button_click(self):
        self.destroy()
        auth_window = SettingsWindow()
        auth_window.mainloop()


class AllGamesWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        WIGHT = 1280
        HEIGHT = 720

        self.title(LANGUAGES[CURRENT_LANGUAGE]['all_games_title'])
        self.geometry(f"{WIGHT}x{HEIGHT}")

        # Получаем размеры окна
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()

        # Вычисляем координаты для центрирования окна
        x = (window_width / 2) - (WIGHT / 2)
        y = (window_height / 2) - (HEIGHT / 2)

        # Устанавливаем координаты окна
        self.geometry(f"{WIGHT}x{HEIGHT}+{int(x)}+{int(y)}")

        userID = controlsUserID.getUser_ID()

        # фрейм для верхних кнопок
        self.top_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.top_frame.place(relx=0.5, rely=0, anchor="center", relwidth=1, relheight=0.15)
        self.button_change_user = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['change_user_button'], command=self.on_auth_button_click)
        self.button_change_user.place(relx=0.74, rely=0.6, relwidth=0.12, relheight=0.3)
        self.button_settings = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['main_menu_button'], command=self.on_main_menu_button_click)
        self.button_settings.place(relx=0.88, rely=0.6, relwidth=0.1, relheight=0.3)

        # фрейм для списка всех игр пользователя
        self.main_table_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.main_table_frame.place(relx=0.5, rely=0.535, anchor="center", relwidth=0.7, relheight=0.8)
        self.last_games_label = ctk.CTkLabel(self, text=f"{LANGUAGES[CURRENT_LANGUAGE]['all_games_label']}", fg_color="#2F4F4F", font=("Times New Roman",20,"bold"))
        self.last_games_label.place(relx=0.35, rely=0.15, relwidth=0.3, relheight=0.06) 
        values = [("Название", "Всего часов", "Всего достижений", "Достижений получено", "Дата последнего\nзахода в игру")]
        self.main_table = CTkTable(self.main_table_frame, column=5, row=len(values), values=values)
        self.main_table.pack(expand=True, fill="both", padx=10, pady=(60,10))
        self.last_games_label = ctk.CTkLabel(self, text=f"{LANGUAGES[CURRENT_LANGUAGE]['last_games_label']}", fg_color="#2F4F4F", font=("Times New Roman",20,"bold"))
        self.last_games_label.place(relx=0.4, rely=0.15, relwidth=0.3, relheight=0.06)
        
    def get_user_games(self):
        url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={controlsAPI.getAPI_Key()}&steamid={controlsUserID.getUser_ID()}&include_appinfo=1"
        response = requests.get(url)
        data = response.json()
        games = data["response"].get("games", [])
        return games


    # функция нажатия на кнопку перехода на окно авторизации
    def on_auth_button_click(self):
        self.destroy()
        auth_window = AuthWindow()
        auth_window.mainloop()

    # функция нажатия на кнопку перехода на окно гм
    def on_main_menu_button_click(self):
        self.destroy()
        auth_window = MainMenuWindow()
        auth_window.mainloop()

class SettingsWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        WIGHT = 1280
        HEIGHT = 720

        self.title(LANGUAGES[CURRENT_LANGUAGE]['settings_title'])
        self.geometry(f"{WIGHT}x{HEIGHT}")

        # Получаем размеры окна
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()

        # Вычисляем координаты для центрирования окна
        x = (window_width / 2) - (WIGHT / 2)
        y = (window_height / 2) - (HEIGHT / 2)

        # Устанавливаем координаты окна
        self.geometry(f"{WIGHT}x{HEIGHT}+{int(x)}+{int(y)}")

        # фрейм для верхних кнопок
        self.top_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.top_frame.place(relx=0.5, rely=0, anchor="center", relwidth=1, relheight=0.15)
        self.button_change_user = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['change_user_button'], command=self.on_auth_button_click)
        self.button_change_user.place(relx=0.74, rely=0.6, relwidth=0.12, relheight=0.3)
        self.button_main_menu = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['main_menu_button'], command=self.on_main_menu_button_click)
        self.button_main_menu.place(relx=0.88, rely=0.6, relwidth=0.1, relheight=0.3)

        # фрейм для настроек
        self.russian_flag = ctk.CTkImage(Image.open("russian_flag.png"), size=(96, 64))
        self.american_flag = ctk.CTkImage(Image.open("american_flag.png"), size=(96, 64))
        self.language_btn_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.language_btn_frame.place(relx=0.2, rely=0.5, anchor="center", relwidth=0.22, relheight=0.5)
        self.language_label = ctk.CTkLabel(self.language_btn_frame, text=LANGUAGES[CURRENT_LANGUAGE]['language_lable'], font=("Times New Roman",20,"bold"))
        self.language_label.place(relx=0.1, rely=0.4, relwidth=0.4, relheight=0.2)
        self.russian_btn = ctk.CTkButton(self.language_btn_frame, image=self.russian_flag,fg_color='transparent', text="", command=lambda: self.set_language('ru'), width=54, height=36)
        self.russian_btn.place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.3)
        self.american_btn = ctk.CTkButton(self.language_btn_frame, image=self.american_flag,fg_color='transparent', text="", command=lambda: self.set_language('en'), width=54, height=36)
        self.american_btn.place(relx=0.5, rely=0.6, relwidth=0.4, relheight=0.3)

        
    # функция нажатия на кнопку перехода на окно главного меню
    def on_main_menu_button_click(self):
        self.destroy()
        auth_window = MainMenuWindow()
        auth_window.mainloop()

    # функция нажатия на кнопку перехода на окно авторизации
    def on_auth_button_click(self):
        self.destroy()
        auth_window = AuthWindow()
        auth_window.mainloop()

    def update_ui_text(self):
        self.title(LANGUAGES[CURRENT_LANGUAGE]['auth_title'])
        self.button_change_user.configure(text=LANGUAGES[CURRENT_LANGUAGE]['change_user_button'])
        self.button_main_menu.configure(text=LANGUAGES[CURRENT_LANGUAGE]['main_menu_button'])
        self.language_label.configure(text=LANGUAGES[CURRENT_LANGUAGE]['language_lable'])

    # смена языка
    def set_language(self, language):
        global CURRENT_LANGUAGE
        CURRENT_LANGUAGE = language

        # Закрываем текущее окно
        self.destroy()

        # Создаем новое окно авторизации
        new_settings_window = SettingsWindow()
        new_settings_window.update_ui_text()
        new_settings_window.mainloop()

if __name__ == "__main__":
    # РАССКОММЕНТИТЬ!
    #auth_window = AuthWindow()
    #auth_window = MainMenuWindow()
    auth_window = AllGamesWindow()
    #auth_window = SettingsWindow()
    auth_window.mainloop()
