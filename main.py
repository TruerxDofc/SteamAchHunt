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
import textwrap
from typing import List, Dict

from language import LANGUAGES

SORT_ORDER_ALLGAMES = "Ascending"
SORT_ORDER_ALLACHIEVEMENTS = "Ascending"
CURRENT_LANGUAGE = 'russian'
SELECTEDGAMESTR = ''
SELECTEDGAMEID = 440
SELECTEDACHNAME = ''

# для бд


class AuthWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        WIGHT = 480
        HEIGHT = 384

        self.CURRENT_LANGUAGE = 'ru'

        self.title(LANGUAGES[CURRENT_LANGUAGE]['auth_title'])
        self.geometry(f"{WIGHT}x{HEIGHT}")

        self.minsize(480, 384)

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
        self.russian_btn = ctk.CTkButton(self.language_btn_frame, image=self.russian_flag,fg_color='transparent', text="", command=lambda: self.set_language('russian'), width=54, height=36)
        self.russian_btn.pack(side="left", padx=(0, 10))
        self.american_btn = ctk.CTkButton(self.language_btn_frame, image=self.american_flag,fg_color='transparent', text="", command=lambda: self.set_language('english'), width=54, height=36)
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

        self.minsize(1280, 720)

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
        self.button_games_user = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['users_games_button'],command=self.on_all_games_button_click)
        self.button_games_user.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.3)
        self.button_ach_user = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['users_ach_button'], command=self.on_all_ach_button_click)
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
        self.country_label = ctk.CTkLabel(self, text=f"{LANGUAGES[CURRENT_LANGUAGE]['country_label']}{userDataValues[3]}", fg_color="#2F4F4F", font=("Times New Roman",20,"bold"))
        self.country_label.place(relx=0.79, rely=0.45, relwidth=0.2, relheight=0.06)
        self.user_level_label = ctk.CTkLabel(self, text=f"{LANGUAGES[CURRENT_LANGUAGE]['user_level']}{user_level[1]}", fg_color="#2F4F4F", font=("Times New Roman",20,"bold"))
        self.user_level_label.place(relx=0.79, rely=0.65, relwidth=0.2, relheight=0.06)

        # фрейм для данных о последних полученных достижениях
        self.main_table_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.main_table_frame.place(relx=0.11, rely=0.535, anchor="center", relwidth=0.2, relheight=0.8)
        self.last_achievements_disc_label = ctk.CTkLabel(self, text=f"{LANGUAGES[CURRENT_LANGUAGE]['last_achievements_disc_label']}", fg_color="#2F4F4F", font=("Times New Roman",12,"bold"))
        self.last_achievements_disc_label.place(relx=0.01, rely=0.4, relwidth=0.2, relheight=0.3)
        self.last_achievements_label = ctk.CTkLabel(self, text=f"{LANGUAGES[CURRENT_LANGUAGE]['last_achievements_label']}", fg_color="#2F4F4F", font=("Times New Roman",20,"bold"))
        self.last_achievements_label.place(relx=0.01, rely=0.15, relwidth=0.2, relheight=0.06)

        # фрейм для Данных послежних запущенных игр
        recent_games = self.get_recent_games(controlsUserID.getUser_ID(), controlsAPI.getAPI_Key())
        user_image = ctk.CTkImage(Image.open("C:\\ProgramData\\SteamAchHunt\\game_icon1.jpg"), size=(150, 70))
        self.icon1_label = ctk.CTkLabel(self, text="", fg_color="#2F4F4F", image=user_image,corner_radius = 15)
        self.icon1_label.place(relx=0.22, rely=0.345, relwidth=0.14, relheight=0.117)
        user_image = ctk.CTkImage(Image.open("C:\\ProgramData\\SteamAchHunt\\game_icon2.jpg"), size=(150, 70))
        self.icon2_label = ctk.CTkLabel(self, text="", fg_color="#2F4F4F", image=user_image,corner_radius = 15)
        self.icon2_label.place(relx=0.22, rely=0.460, relwidth=0.14, relheight=0.117)
        user_image = ctk.CTkImage(Image.open("C:\\ProgramData\\SteamAchHunt\\game_icon3.jpg"), size=(150, 70))
        self.icon3_label = ctk.CTkLabel(self, text="", fg_color="#2F4F4F", image=user_image,corner_radius = 15)
        self.icon3_label.place(relx=0.22, rely=0.575, relwidth=0.14, relheight=0.117)
        user_image = ctk.CTkImage(Image.open("C:\\ProgramData\\SteamAchHunt\\game_icon4.jpg"), size=(150, 70))
        self.icon4_label = ctk.CTkLabel(self, text="", fg_color="#2F4F4F", image=user_image,corner_radius = 15)
        self.icon4_label.place(relx=0.22, rely=0.690, relwidth=0.14, relheight=0.117)
        user_image = ctk.CTkImage(Image.open("C:\\ProgramData\\SteamAchHunt\\game_icon5.jpg"), size=(150, 70))
        self.icon5_label = ctk.CTkLabel(self, text="", fg_color="#2F4F4F", image=user_image,corner_radius = 15)
        self.icon5_label.place(relx=0.22, rely=0.805, relwidth=0.14, relheight=0.117)
        self.main_table_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.main_table_frame.place(relx=0.55, rely=0.535, anchor="center", relwidth=0.4, relheight=0.8)
        values = [("Название", "Всего", "За последние\n2 недели")]
        values.extend([(game[0], f"{game[2] // 60} ч", f"{game[3] // 60} ч") for game in recent_games])
        self.main_table = CTkTable(self.main_table_frame, column=3, row=len(values), values=values)
        self.main_table.pack(expand=True, fill="both", padx=10, pady=(60,10))
        self.last_games_label = ctk.CTkLabel(self, text=f"{LANGUAGES[CURRENT_LANGUAGE]['last_games_label']}", fg_color="#2F4F4F", font=("Times New Roman",20,"bold"))
        self.last_games_label.place(relx=0.4, rely=0.15, relwidth=0.3, relheight=0.06)



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
                    personalData = jdata["response"]["players"][0   ]
            
                except IndexError:
                    print(IndexError)
                    return [False,"","",""]
            
                #download picture
                url = personalData["avatarfull"]
                response=requests.get(url,stream=True)
                with open("C:\\ProgramData\\SteamAchHunt\\profile_pic.jpg","wb") as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response

                try:
                    country = personalData["loccountrycode"]
                    return [True,"C:\\ProgramData\\SteamAchHunt\\profile_pic.jpg",personalData["personaname"],country]
                except: 
                    return [True,"C:\\ProgramData\\SteamAchHunt\\profile_pic.jpg",personalData["personaname"],"нет"]


                
            
            else:
                return [False,"","",""]
        
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
            count = 1

            recent_games = []
            for game in games_data[:5]:  # Берем только первые 5 игр
                game_name = game["name"]
                appid = game["appid"]
                playtime_forever = game["playtime_forever"]
                playtime_2weeks = game["playtime_2weeks"]
                recent_games.append((game_name, appid, playtime_forever, playtime_2weeks))
                self.download_game_icons(appid,count)
                count += 1

            return recent_games

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении данных из SteamAPI: {e}")
            return []
        
    def download_game_icons(self,appid,pos):
        url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg"
        filename = f"C:\\ProgramData\\SteamAchHunt\\game_icon{pos}.jpg"
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"Изображение успешно сохранено в файл {filename}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при скачивании изображения: {e}")




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

    # функция нажатия на кнопку перехода на окно всех игр пользовтеля
    def on_all_games_button_click(self):
        self.destroy()
        auth_window = AllGamesWindow()
        auth_window.mainloop()

    # функция нажатия на кнопку перехода на окно всех достижений
    def on_all_ach_button_click(self):
        self.destroy()
        auth_window = AllAchievementsWindow()
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

        self.minsize(1280, 720)

        # фрейм для верхних кнопок
        self.top_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.top_frame.place(relx=0.5, rely=0, anchor="center", relwidth=1, relheight=0.15)
        self.button_change_user = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['change_user_button'], command=self.on_auth_button_click)
        self.button_change_user.place(relx=0.74, rely=0.6, relwidth=0.12, relheight=0.3)
        self.button_settings = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['main_menu_button'], command=self.on_main_menu_button_click)
        self.button_settings.place(relx=0.88, rely=0.6, relwidth=0.1, relheight=0.3)

        # фрейм для списка всех игр пользователя
        self.last_games_label = ctk.CTkLabel(self, text=f"{LANGUAGES[CURRENT_LANGUAGE]['all_games_label']}",bg_color="transparent", fg_color="#2F4F4F", font=("Times New Roman",20,"bold"), corner_radius = 15)
        self.last_games_label.place(relx=0.25, rely=0.09, relwidth=0.35, relheight=0.08)
        self.main_table_frame = ctk.CTkScrollableFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.main_table_frame.place(relx=0.4, rely=0.55, anchor="center", relwidth=0.7, relheight=0.8)
        self.games = self.get_user_games()
        total_hrs_played = 0
        most_played = 0
        name_of_most_played = ""
        # Формируем данные для таблицы
        values = [["Название игры", "Всего часов", "Всего достижений", "Достижений получено", "Дата последнего\nзахода в игру"]]
        for game in self.games:
            name = game["name"]
            playtime_forever = game["playtime_forever"] // 60
            total_hrs_played += playtime_forever
            if(most_played <= playtime_forever):
                most_played = playtime_forever
                name_of_most_played = name
            # расскомментировать как надо будет включить (на моем аккаунте считает минуты 2)
            #total_achievements, achieved_achievements = self.get_game_achievements_count(controlsUserID.getUser_ID(), game['appid'], controlsAPI.getAPI_Key())
            total_achievements, achieved_achievements = 0, 0
            # Обработка случая, когда ключа 'rtime_last_played' нет в словаре
            try:
                if 'rtime_last_played' in game:
                    if game['rtime_last_played'] == 0:
                        last_played = "Never"
                    else:
                        last_played = datetime.fromtimestamp(game["rtime_last_played"]).strftime("%d.%m.%Y")
                else:
                    last_played = "Unknown"
            except Exception as e:
                print(f"Ошибка: {e}")
                pass
            values.append([name, playtime_forever, total_achievements, achieved_achievements, last_played])
        self.main_table = CTkTable(self.main_table_frame, column=5, row=len(values), values=values, command=self.select_table_game)
        self.main_table.pack(expand=True, fill="both", padx=10, pady=(40, 10))

        # фрейм для прво-нижних кнопок
        self.right_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.right_frame.place(relx=0.9, rely=0.55, anchor="center", relwidth=0.22, relheight=0.8)
        self.statistic_label = ctk.CTkLabel(self.right_frame, text=f"{LANGUAGES[CURRENT_LANGUAGE]['statistic_label']}",bg_color="transparent", fg_color="#2F4F4F", font=("Times New Roman",20,"bold","underline"))
        self.statistic_label.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.1)
        self.total_hrs_label = ctk.CTkLabel(self.right_frame, text=f"{LANGUAGES[CURRENT_LANGUAGE]['total_hrs_label']}{total_hrs_played}",bg_color="transparent", fg_color="#2F4F4F", font=("Times New Roman",16,"bold"))
        self.total_hrs_label.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.1)
        self.most_played_game_label = ctk.CTkLabel(self.right_frame, text=f"{LANGUAGES[CURRENT_LANGUAGE]['most_played_label']}{name_of_most_played}",bg_color="transparent", fg_color="#2F4F4F", font=("Times New Roman",16,"bold"))
        self.most_played_game_label.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.1)
        
    def get_user_games(self):
        url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={controlsAPI.getAPI_Key()}&steamid={controlsUserID.getUser_ID()}&include_appinfo=1&include_played_free_games=1"
        response = requests.get(url)
        data = response.json()
        games = data["response"].get("games", [])
        return games
    
    def select_table_game(self,cell):
        if cell["row"] == 0 and cell["column"] != 4:
            self.sortTable(col=cell["column"], table="AllGames")
        else: 
            first_column_value = self.main_table.values[cell["row"]][0]
            for game in self.games:
                print(game["appid"])
                if str(game["name"]) == first_column_value:
                    global SELECTEDGAMEID
                    SELECTEDGAMEID = game["appid"]
                    break
            print(SELECTEDGAMEID)
            self.to_the_selected_game(col=first_column_value)

    def sortTable(self, col: int, table: str):
        global SORT_ORDER_ALLGAMES
        global SORT_ORDER_ALLACHIEVEMENTS

        if table == "AllGames":
            print("sort all games")
            if(SORT_ORDER_ALLGAMES == "Descending"):
                sortBool = True
                SORT_ORDER_ALLGAMES = "Ascending"
            else:
                sortBool = False
                SORT_ORDER_ALLGAMES = "Descending"

            tableValues = self.main_table.get()
            tableValues[1:] = sorted(tableValues[1:], reverse=sortBool, key=lambda i: i[col])
            self.main_table.update_values(tableValues)

        else:
            print("sort all ach")
            if(SORT_ORDER_ALLACHIEVEMENTS == "Descending"):
                sortBool = True
                SORT_ORDER_ALLACHIEVEMENTS = "Ascending"
            else:
                sortBool = False
                SORT_ORDER_ALLACHIEVEMENTS = "Descending"
                
            tableValues = self.main_table.get()
            tableValues[1:] = sorted(tableValues[1:], reverse=sortBool, key=lambda i: i[col])

            self.main_table.update_values(tableValues)

    # функция подсчёта всех достижений игры и количество полученных достижений игры
    def get_game_achievements_count(self, steam_id, app_id, api_key):
        url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
        global CURRENT_LANGUAGE
        params = {
            "key": api_key,
            "steamid": steam_id,
            "appid": app_id,
            "l": CURRENT_LANGUAGE
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data["playerstats"]["success"]:
            total_achievements = 0
            achieved_achievements = 0

            try:
                achievements = data["playerstats"]["achievements"]
                total_achievements = len(achievements)
                achieved_achievements = sum(ach["achieved"] for ach in achievements)
            except:
                pass
        else:
            total_achievements = 0
            achieved_achievements = 0

        return total_achievements, achieved_achievements
    
    def to_the_selected_game(self, col: str):
        global SELECTEDGAMESTR
        SELECTEDGAMESTR = col
        self.destroy()
        auth_window = SelectedGame()
        auth_window.mainloop()


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

class SelectedGame(ctk.CTk):
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

        self.minsize(1280, 720)

        # фрейм для верхних кнопок
        self.top_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.top_frame.place(relx=0.5, rely=0, anchor="center", relwidth=1, relheight=0.15)
        self.button_change_user = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['change_user_button'], command=self.on_auth_button_click)
        self.button_change_user.place(relx=0.74, rely=0.6, relwidth=0.12, relheight=0.3)
        self.button_main_menu = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['main_menu_button'], command=self.on_main_menu_button_click)
        self.button_main_menu.place(relx=0.88, rely=0.6, relwidth=0.1, relheight=0.3)
        self.button_main_menu = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['users_games_button'], command=self.on_all_games_button_click)
        self.button_main_menu.place(relx=0.05, rely=0.6, relwidth=0.13, relheight=0.3)

        # фрейм с данными по игре
        self.game_data_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 25)
        self.game_data_frame.place(relx=0.8, rely=0.55, anchor="center", relwidth=0.35, relheight=0.8)
        self.game_data_title_label = ctk.CTkLabel(self.game_data_frame, text=SELECTEDGAMESTR, font=("Times New Roman",20,"bold"))
        self.game_data_title_label.place(relx=0.0, rely=0.05, relwidth=1, relheight=0.1)
        self.download_game_icon(SELECTEDGAMEID)
        game_details = self.get_game_details(SELECTEDGAMEID)
        game_image = ctk.CTkImage(Image.open("C:\\ProgramData\\SteamAchHunt\\game_icon_selected.jpg"), size=(225, 105))
        self.icon_label = ctk.CTkLabel(self.game_data_frame, text="", image=game_image,corner_radius = 15)
        self.icon_label.place(relx=0.0, rely=0.16, relwidth=1, relheight=0.17)
        text=f"{LANGUAGES[CURRENT_LANGUAGE]['short_description']}{game_details['short_description']}"
        wrapped_text = textwrap.fill(text, width=50)
        self.game_data_description_label = ctk.CTkLabel(self.game_data_frame, text=wrapped_text, font=("Times New Roman",14,"bold"))
        self.game_data_description_label.place(relx=0.0, rely=0.35, relwidth=1, relheight=0.35)
        self.game_data_developers_label = ctk.CTkLabel(self.game_data_frame, text=f"{LANGUAGES[CURRENT_LANGUAGE]['developers']}{game_details['developers']}", font=("Times New Roman",14,"bold"))
        self.game_data_developers_label.place(relx=0.0, rely=0.75, relwidth=1, relheight=0.05)
        self.game_data_publisher_label = ctk.CTkLabel(self.game_data_frame, text=f"{LANGUAGES[CURRENT_LANGUAGE]['publishers']}{game_details['publishers']}", font=("Times New Roman",14,"bold"))
        self.game_data_publisher_label.place(relx=0.0, rely=0.8, relwidth=1, relheight=0.05)
        self.game_data_total_label = ctk.CTkLabel(self.game_data_frame, text=f"{LANGUAGES[CURRENT_LANGUAGE]['total_achievements']}{game_details['total_achievements']}", font=("Times New Roman",14,"bold"))
        self.game_data_total_label.place(relx=0.0, rely=0.85, relwidth=1, relheight=0.05)
        self.game_data_release_label = ctk.CTkLabel(self.game_data_frame, text=f"{LANGUAGES[CURRENT_LANGUAGE]['release_date']}{game_details['release_date']}", font=("Times New Roman",14,"bold"))
        self.game_data_release_label.place(relx=0.0, rely=0.9, relwidth=1, relheight=0.05)

        # фрейм с достижениями
        self.game_ach_title_label = ctk.CTkLabel(self, text=f"{LANGUAGES[CURRENT_LANGUAGE]['game_ach_title']}",bg_color="transparent", fg_color="#2F4F4F", font=("Times New Roman",20,"bold"), corner_radius = 15)
        self.game_ach_title_label.place(relx=0.125, rely=0.09, relwidth=0.35, relheight=0.08)
        self.game_ach_frame = ctk.CTkScrollableFrame(self, fg_color="#2F4F4F", corner_radius = 25)
        self.game_ach_frame.place(relx=0.3, rely=0.55, anchor="center", relwidth=0.45, relheight=0.8)
        self.values, self.apinames = self.get_player_achievements(controlsUserID.getUser_ID(), SELECTEDGAMEID, controlsAPI.getAPI_Key())
        self.main_table = CTkTable(self.game_ach_frame, column=3, row=len(self.values), values=self.values,command=self.select_table_ach)
        self.main_table.pack(expand=True, fill="both", padx=10, pady=(40, 10))


        
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

    # функция нажатия на кнопку перехода на окно всех игр пользовтеля
    def on_all_games_button_click(self):
        self.destroy()
        auth_window = AllGamesWindow()
        auth_window.mainloop()

    def select_table_ach(self,cell):
        global SELECTEDACHNAME
        if cell["row"] == 0 and cell["column"] != 2:
            self.sortTable(col=cell["column"], table="AllAch")
        else: 
            first_column_value = self.main_table.values[cell["row"]][0]
            count = -1
            for ach in self.values:
                if str(ach[0]) == first_column_value:
                    SELECTEDACHNAME = self.apinames[count]
                    break
                count += 1
            self.to_the_selected_ach(col=first_column_value)

    def to_the_selected_ach(self, col: str):
        self.destroy()
        auth_window = SelectedAchievement()
        auth_window.mainloop()

    def sortTable(self, col: int, table: str):
        global SORT_ORDER_ALLGAMES
        global SORT_ORDER_ALLACHIEVEMENTS

        if table == "AllGames":
            print("sort all games")
            if(SORT_ORDER_ALLGAMES == "Descending"):
                sortBool = True
                SORT_ORDER_ALLGAMES = "Ascending"
            else:
                sortBool = False
                SORT_ORDER_ALLGAMES = "Descending"

            tableValues = self.main_table.get()
            tableValues[1:] = sorted(tableValues[1:], reverse=sortBool, key=lambda i: i[col])
            self.main_table.update_values(tableValues)

        else:
            print("sort all ach")
            if(SORT_ORDER_ALLACHIEVEMENTS == "Descending"):
                sortBool = True
                SORT_ORDER_ALLACHIEVEMENTS = "Ascending"
            else:
                sortBool = False
                SORT_ORDER_ALLACHIEVEMENTS = "Descending"
                
            tableValues = self.main_table.get()
            tableValues[1:] = sorted(tableValues[1:], reverse=sortBool, key=lambda i: i[col])

            self.main_table.update_values(tableValues)

    # функция получения данных по игре
    def get_game_details(self, appid):
        global CURRENT_LANGUAGE
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l={CURRENT_LANGUAGE}"
        response = requests.get(url)
        data = response.json()

        info = {}

        if data[str(appid)]["success"]:
            game_data = data[str(appid)]["data"]

            info["short_description"] = game_data.get("short_description", "")

            developers = [dev.strip() for dev in game_data.get("developers", []) if dev.strip()]
            info["developers"] = ", ".join(developers)

            publishers = [pub.strip() for pub in game_data.get("publishers", []) if pub.strip()]
            info["publishers"] = ", ".join(publishers)

            achievements = game_data.get("achievements", {})
            info["total_achievements"] = achievements.get("total", 0)

            release_date = game_data.get("release_date", {})
            info["release_date"] = release_date.get("date", "")
        else:
            info = {
            "short_description": LANGUAGES[CURRENT_LANGUAGE]['none_game_info'],
            "developers": LANGUAGES[CURRENT_LANGUAGE]['none_game_info'],
            "publishers": LANGUAGES[CURRENT_LANGUAGE]['none_game_info'],
            "total_achievements": LANGUAGES[CURRENT_LANGUAGE]['none_game_info'],
            "release_date": LANGUAGES[CURRENT_LANGUAGE]['none_game_info']}
        
        return info
    
    # функция формирования данных табилцы с достижениями игры
    def get_player_achievements(self,steam_id, app_id, api_key):
        url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
        global CURRENT_LANGUAGE
        print(CURRENT_LANGUAGE)
        params = {
            "key": api_key,
            "steamid": steam_id,
            "appid": app_id,
            "l": CURRENT_LANGUAGE
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data["playerstats"]["success"]:

            achievements_data = [LANGUAGES[CURRENT_LANGUAGE]['ach_name'], LANGUAGES[CURRENT_LANGUAGE]['ach_achieved'], LANGUAGES[CURRENT_LANGUAGE]['ach_date_gain']]

            apiname_data = []

            try:
                achievements = data["playerstats"]["achievements"]
                for ach in achievements:
                    achieved = ach["achieved"]
                    if achieved == 0:
                        achieved = LANGUAGES[CURRENT_LANGUAGE]['achieved_false']
                    else: 
                        achieved = LANGUAGES[CURRENT_LANGUAGE]['achieved_true']
                    unlocktime = ach["unlocktime"]
                    if unlocktime == 0:
                        unlocktime_str = LANGUAGES[CURRENT_LANGUAGE]['unlocktime_str']
                    else:
                        unlocktime_str = datetime.fromtimestamp(unlocktime).strftime("%d.%m.%Y")
                    name = ach["name"]
                    achievements_data.append([name,achieved, unlocktime_str])

                    apiname = ach["apiname"]
                    apiname_data.append([apiname])

            except:
                name = "Достижения отсутствуют"
                achieved = "Достижения отсутствуют"
                unlocktime_str = "Достижения отсутствуют"
                achievements_data.append([name,achieved, unlocktime_str])
                apiname_data.append([0])
        else:
            achievements_data = [["Данные отсутствуют", "Данные отсутствуют", "Данные отсутствуют"]]
            apiname_data = [0]

        return achievements_data, apiname_data
        

    def download_game_icon(self, appid):
        url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg"
        filename = f"C:\\ProgramData\\SteamAchHunt\\game_icon_selected.jpg"
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"Изображение успешно сохранено в файл {filename}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при скачивании изображения: {e}")


class SelectedAchievement(ctk.CTk):
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

        self.minsize(1280, 720)

        # фрейм для верхних кнопок
        self.top_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.top_frame.place(relx=0.5, rely=0, anchor="center", relwidth=1, relheight=0.15)
        self.button_change_user = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['change_user_button'], command=self.on_auth_button_click)
        self.button_change_user.place(relx=0.74, rely=0.6, relwidth=0.12, relheight=0.3)
        self.button_main_menu = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['main_menu_button'], command=self.on_main_menu_button_click)
        self.button_main_menu.place(relx=0.88, rely=0.6, relwidth=0.1, relheight=0.3)
        self.button_main_menu = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['selected_game'], command=self.on_selected_game_button_click)
        self.button_main_menu.place(relx=0.02, rely=0.6, relwidth=0.13, relheight=0.3)

        # фрейм с данными достижения
        global SELECTEDACHNAME, SELECTEDGAMEID
        ach_info = self.get_achievement_details(SELECTEDACHNAME, SELECTEDGAMEID)
        self.ach_data_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 25)
        self.ach_data_frame.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.4, relheight=0.8)
        self.ach_data_title_label = ctk.CTkLabel(self.ach_data_frame, text=ach_info["displayName"], font=("Times New Roman",20,"bold"))
        self.ach_data_title_label.place(relx=0.0, rely=0.05, relwidth=1, relheight=0.1)
        ach_image = ctk.CTkImage(Image.open("C:\\ProgramData\\SteamAchHunt\\ach_icon_selected.jpg"), size=(75, 75))
        self.icon_label = ctk.CTkLabel(self.ach_data_frame, text="", image=ach_image,corner_radius = 15)
        self.icon_label.place(relx=0.0, rely=0.16, relwidth=1, relheight=0.17)
        text=f"{LANGUAGES[CURRENT_LANGUAGE]['short_description']}{ach_info['description']}"
        wrapped_text = textwrap.fill(text, width=25)
        self.ach_data_desc_label = ctk.CTkLabel(self.ach_data_frame, text=wrapped_text, font=("Times New Roman",20,"bold"))
        self.ach_data_desc_label.place(relx=0.0, rely=0.45, relwidth=1, relheight=0.2)
        print(ach_info["percent"])
        self.ach_data_percent_label = ctk.CTkLabel(self.ach_data_frame, text=ach_info["percent"], font=("Times New Roman",20,"bold"))
        self.ach_data_percent_label.place(relx=0.0, rely=0.6, relwidth=1, relheight=0.2)

        
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

    # функция нажатия на кнопку перехода на окно всех игр пользовтеля
    def on_selected_game_button_click(self):
        self.destroy()
        auth_window = SelectedGame()
        auth_window.mainloop()

    def get_achievement_details(self,apiname, appid):
        global CURRENT_LANGUAGE
        url = f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={controlsAPI.getAPI_Key()}&appid={appid}&l={CURRENT_LANGUAGE}"
        response = requests.get(url)
        data = response.json()

        if data["game"]["availableGameStats"] is None:
            print("Нет доступных достижений для этой игры.")
            return

        achievements = data["game"]["availableGameStats"]["achievements"]


        global SELECTEDACHNAME, SELECTEDGAMEID
        percent_ach = self.get_global_achievement_percentage(SELECTEDGAMEID, SELECTEDACHNAME)

        info = {}

        for achievement in achievements:
            if(achievement["name"] == apiname[0]):
                info["displayName"] = achievement.get("displayName", "")

                info["description"] = achievement.get("description", "")

                self.download_ach_icon(achievement.get("icon", ""))

                info["percent"] = percent_ach

                return info
            
    def get_global_achievement_percentage(self, appid, achid):
        url = "https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2"
        params = {
            "gameid": appid
        }
        response = requests.get(url, params=params)
        data = response.json()
        if "achievements" in data["achievementpercentages"]:
            for achievement in data["achievementpercentages"]["achievements"]:
                if achievement["name"] == achid[0]:
                    global_percentage = round(achievement["percent"], 2)
                    global_percentage_str = str(global_percentage) + "%"
                    return global_percentage_str
        else:
            return []
            

    def download_ach_icon(self, url):
        filename = f"C:\\ProgramData\\SteamAchHunt\\ach_icon_selected.jpg"
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"Изображение успешно сохранено в файл {filename}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при скачивании изображения: {e}")

class AllAchievementsWindow(ctk.CTk):
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

        self.minsize(1280, 720)

        # фрейм для верхних кнопок
        self.top_frame = ctk.CTkFrame(self, fg_color="#2F4F4F", corner_radius = 15)
        self.top_frame.place(relx=0.5, rely=0, anchor="center", relwidth=1, relheight=0.15)
        self.button_change_user = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['change_user_button'], command=self.on_auth_button_click)
        self.button_change_user.place(relx=0.74, rely=0.6, relwidth=0.12, relheight=0.3)
        self.button_settings = ctk.CTkButton(self.top_frame, text=LANGUAGES[CURRENT_LANGUAGE]['main_menu_button'], command=self.on_main_menu_button_click)
        self.button_settings.place(relx=0.88, rely=0.6, relwidth=0.1, relheight=0.3)

        # Фрейм с таблицей достижений
        self.all_ach_title_label = ctk.CTkLabel(self, text=f"{LANGUAGES[CURRENT_LANGUAGE]['game_ach_title']}", bg_color="transparent", fg_color="#2F4F4F", font=("Times New Roman", 20, "bold"), corner_radius=15)
        self.all_ach_title_label.place(relx=0.12, rely=0.09, relwidth=0.35, relheight=0.08)
        self.all_ach_frame = ctk.CTkScrollableFrame(self, fg_color="#2F4F4F", corner_radius=25)
        self.all_ach_frame.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.8, relheight=0.8)
        global SELECTEDGAMEID
        self.appids = self.get_user_games()
        self.all_values = [["Игра","Название", "Получено", "Время получения","Процент получения"]]
        self.all_apinames = []
        for appid, game_name in self.appids:
            # Добавляем игру в список достижений
            self.values, self.apinames = self.get_player_achievements(controlsUserID.getUser_ID(), appid, controlsAPI.getAPI_Key())
            for value in self.values:
                if(value[1] != ""):
                    value[0] = game_name
                self.all_values.append(value)
            self.all_apinames.append(self.apinames)
        self.main_table = CTkTable(self.all_ach_frame, column=5, row=len(self.all_values), values=self.all_values,command=self.select_table_ach)
        self.main_table.pack(expand=True, fill="both", padx=10, pady=(40, 10))

        # поиск
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Введите текст для поиска")
        self.search_entry.place(relx=0.49, rely=0.1, relwidth=0.3, relheight=0.05)
        self.search_button = ctk.CTkButton(self, text="Поиск", command=self.filter_achievements)
        self.search_button.place(relx=0.79, rely=0.1, relwidth=0.1, relheight=0.05)

    
    # функция формирования данных табилцы с достижениями игры
    def get_player_achievements(self,steam_id, app_id, api_key):
        url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
        print(app_id)
        global CURRENT_LANGUAGE
        print(CURRENT_LANGUAGE)
        params = {
            "key": api_key,
            "steamid": steam_id,
            "appid": app_id,
            "l": CURRENT_LANGUAGE
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data["playerstats"]["success"]:

            apiname_data = []

            achievements_data = []

            global_achievement_percentages = self.get_global_achievement_percentages(app_id)

            try:
                achievements = data["playerstats"]["achievements"]
                for ach, global_ach in zip(achievements, global_achievement_percentages):
                    achieved = ach["achieved"]
                    if achieved == 0:
                        achieved = LANGUAGES[CURRENT_LANGUAGE]['achieved_false']
                    else: 
                        achieved = LANGUAGES[CURRENT_LANGUAGE]['achieved_true']
                    unlocktime = ach["unlocktime"]
                    if unlocktime == 0:
                        unlocktime_str = LANGUAGES[CURRENT_LANGUAGE]['unlocktime_str']
                    else:
                        unlocktime_str = datetime.fromtimestamp(unlocktime).strftime("%d.%m.%Y")
                    name = ach["name"]
                    global_percentage = round(global_ach.get("percent", 0), 2)
                    global_percentage_str = str(global_percentage) + "%"
                    achievements_data.append(["", name, achieved, unlocktime_str, global_percentage_str])

                    apiname = ach["apiname"]
                    apiname_data.append([apiname])

            except:
                name = "Empty"
                achieved = "Empty"
                unlocktime_str = "Empty"
                achievements_data.append(["Empty",name,achieved, unlocktime_str,"Empty"])
                apiname_data.append([0])
        else:
            achievements_data = [["Empty","Empty", "Empty", "Empty", "Empty"]]
            apiname_data = [0]

        return achievements_data, apiname_data
    
    def filter_achievements(self):
        search_text = self.search_entry.get().lower()
        filtered_values = [row for row in self.all_values if search_text in row[1].lower()]
        self.main_table.update_values(filtered_values)

        
    def get_user_games(self):
        url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={controlsAPI.getAPI_Key()}&steamid={controlsUserID.getUser_ID()}&include_appinfo=1&include_played_free_games=1"
        response = requests.get(url)
        data = response.json()
        # Изменение здесь: получаем и название игры тоже
        game_ids = [(game["appid"], game["name"]) for game in data["response"].get("games", [])]
        return game_ids
    
    def get_global_achievement_percentages(self, appid):
        url = "https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2"
        params = {
            "gameid": appid
        }
        response = requests.get(url, params=params)
        data = response.json()

        if "achievements" in data["achievementpercentages"]:
            achievements = data["achievementpercentages"]["achievements"]
            return achievements
        else:
            return []
    
    def select_table_ach(self,cell):
        global SELECTEDACHNAME, SELECTEDGAMEID
        if cell["row"] == 0:
            self.sortTable(col=cell["column"], table="AllAch")
        else:
            pass
    
    def sortTable(self, col: int, table: str):
        global SORT_ORDER_ALLGAMES
        global SORT_ORDER_ALLACHIEVEMENTS

        if table == "AllGames":
            print("sort all games")
            if(SORT_ORDER_ALLGAMES == "Descending"):
                sortBool = True
                SORT_ORDER_ALLGAMES = "Ascending"
            else:
                sortBool = False
                SORT_ORDER_ALLGAMES = "Descending"

            tableValues = self.main_table.get()
            tableValues[1:] = sorted(tableValues[1:], reverse=sortBool, key=lambda i: i[col])
            self.main_table.update_values(tableValues)

        else:
            print("sort all ach")
            if(SORT_ORDER_ALLACHIEVEMENTS == "Descending"):
                sortBool = True
                SORT_ORDER_ALLACHIEVEMENTS = "Ascending"
            else:
                sortBool = False
                SORT_ORDER_ALLACHIEVEMENTS = "Descending"
                
            tableValues = self.main_table.get()
            if col == 4:  # Если сортируем по пятому столбцу (процент достижений)
                tableValues[1:] = sorted(tableValues[1:], reverse=sortBool, key=lambda i: float(i[col][:-1]) if i[col][-1] == '%' else 0)
            else:
                tableValues[1:] = sorted(tableValues[1:], reverse=sortBool, key=lambda i: i[col])

            self.main_table.update_values(tableValues)


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

        self.minsize(1280, 720)

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
        self.russian_btn = ctk.CTkButton(self.language_btn_frame, image=self.russian_flag,fg_color='transparent', text="", command=lambda: self.set_language('russian'), width=54, height=36)
        self.russian_btn.place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.3)
        self.american_btn = ctk.CTkButton(self.language_btn_frame, image=self.american_flag,fg_color='transparent', text="", command=lambda: self.set_language('english'), width=54, height=36)
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

    # функция нажатия на кнопку перехода на окно всех игр пользовтеля
    def on_all_games_button_click(self):
        self.destroy()
        auth_window = AllGamesWindow()
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
    auth_window = AuthWindow()
    #auth_window = MainMenuWindow()
    #auth_window = AllGamesWindow()
    #auth_window = SettingsWindow()
    #auth_window = SelectedGame()
    #auth_window = AllAchievementsWindow()
    auth_window.mainloop()
