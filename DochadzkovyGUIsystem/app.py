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
        self.geometry("345x150")

        # objekty
        self.sql = SQL("34.116.128.160", "rpi_i_s_u", "rpi_i_s_u", "RPI_ATTEND")
        self.rfid = RFID("AA1")

        # premenne
        self.line_name = None
        self.ops_id = tk.StringVar()
        self.chip_id = tk.StringVar()

        # popisky
        self.view = tk.Label(self, textvariable=self.chip_id, height=2, width=15, borderwidth=3,
                                        relief="sunken")
        self.view.grid(row=0, column=1, padx=5, sticky=tk.EW)

        # tlacitka
        self.button_start_dht22 = tk.Button(self, text="Linka1", height=2, width=15, bg="silver", fg="blue")
        self.button_start_dht22['command'] = lambda: self.log_on_line1()
        self.button_start_dht22.grid(row=1, column=1, padx=5, sticky=tk.EW)

        # metody spustene pri vytvarani TK objektu
        self.ops_id.set(self.sql.sql_check_if_somebody_is_logged()[1])

    # def check_if_somebody_is_logged(self):
    #     self.sql.connect_to_sql()
    #     self.line_name = self.sql.get_line_name()
    #     self.ops_id.set("pokus")

    def log_on_line1(self):
        messagebox.showinfo("", "Stlač OK a potom prilož kartu ku čítačke")
        # odstrani zamrznute okno messageboxu
        self.chip_id.set("Caka sa na kartu")
        self.update()

        if self.rfid.run_rfid() is True:
            self.chip_id.set("Karta presla")
        else:
            self.chip_id.set("Karta nepresla")
