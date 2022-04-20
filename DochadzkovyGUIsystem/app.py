#!/usr/bin/env python
import time
from tkinter import messagebox
import tkinter as tk
from mysql_connection import SQL
from rfid import RFID


class App(tk.Tk):

    def __init__(self):

        super().__init__()
        # Dizajn okna
        self.title("Logovanie na linku")
        self.geometry("+450+300")
        self.geometry("345x200")

        # objekty
        self.sql = SQL("", "", "", "")
        self.rfid = RFID("AA1")

        # premenne
        self.line_name = None
        self.action_text = tk.StringVar()
        self.ops_id = tk.StringVar()
        self.tag_to = tk.StringVar()
        self.tag_since = tk.StringVar()
        self.chip_id = tk.StringVar()

        # nacitanie parametrov z sql do premennych
        self.ops_id.set(self.sql.sql_check_if_somebody_is_logged()[1])

        # popisky
        self.view_action = tk.Label(self, textvariable=self.action_text, height=2, width=35, borderwidth=3,
                                    relief="sunken")
        self.view_action.grid(row=0, column=1, padx=5, sticky=tk.EW)

        self.view_ops_id = tk.Label(self, textvariable=self.ops_id, height=2, width=35, borderwidth=3,
                                    relief="sunken")
        self.view_ops_id.grid(row=1, column=1, padx=5, sticky=tk.EW)

        # tlacitka
        self.button_line_login = tk.Button(self, text="Prihlasenie na linku", height=2, width=15, bg="silver",
                                           fg="blue")
        self.button_line_login['command'] = lambda: self.log_on_line()
        self.button_line_login.grid(row=2, column=1, padx=5, sticky=tk.EW)

        self.button_line_log_off = tk.Button(self, text="Odhlasenie z linky", height=2, width=15, bg="silver",
                                           fg="blue")
        self.button_line_log_off['command'] = lambda: self.log_off_line()
        self.button_line_log_off.grid(row=3, column=1, padx=5, sticky=tk.EW)

    # def check_if_somebody_is_logged(self):
    #     self.sql.connect_to_sql()
    #     self.line_name = self.sql.get_line_name()
    #     self.ops_id.set("pokus")

    def log_off_line(self):
        messagebox.showinfo("", "Stlač OK a potom prilož kartu ku čítačke")
        # odstrani zamrznute okno messageboxu
        self.action_text.set("Caka sa na kartu")
        self.update()

        if self.rfid.run_rfid() is True:
            self.action_text.set("Karta presla")
            self.update()
            time.sleep(2)
            self.sql.logoff_operator(self.sql.get_line_name(), self.rfid.detected_chip_number)
            self.ops_id.set(self.sql.sql_check_if_somebody_is_logged()[1])
            self.sql.print_table_data()
        else:
            self.action_text.set("Karta nepresla, zopakuj prihlasenie")
            self.update()
            time.sleep(2)

        self.clear_action_view()

    def log_on_line(self):
        messagebox.showinfo("", "Stlač OK a potom prilož kartu ku čítačke")
        # odstrani zamrznute okno messageboxu
        self.action_text.set("Caka sa na kartu")
        self.update()

        if self.rfid.run_rfid() is True:
            self.action_text.set("Karta presla")
            self.update()
            time.sleep(2)
            self.sql.login_operator(self.sql.get_line_name(), self.rfid.detected_chip_number)
            self.ops_id.set(self.sql.sql_check_if_somebody_is_logged()[1])
            self.sql.print_table_data()
        else:
            self.action_text.set("Karta nepresla, zopakuj prihlasenie")
            self.update()
            time.sleep(2)

        self.clear_action_view()

    def clear_action_view(self):
        self.action_text.set("")
        print("Pripojene na SQL server?: " + str(self.sql.mysql_database.is_connected()))


