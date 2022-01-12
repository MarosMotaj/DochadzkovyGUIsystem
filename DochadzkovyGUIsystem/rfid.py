#!/usr/bin/env python

import RPi.GPIO as GPIO
import mfrc522 as MFRC522
from mysql_connection import SQL
from clock import Clock
import signal
import time


class RFID:

    def __init__(self, device_name):

        self.device_name = device_name
        self.detected_chip_number = None
        self.line_name = None
        GPIO.setwarnings(False)
        self.continue_reading = True
        self.signal = signal.signal(signal.SIGINT, self.end_read)
        self.MIFAREReader = MFRC522.MFRC522()
        self.sql = SQL("34.116.128.160", "rpi_i_s_u", "rpi_i_s_u", "RPI_ATTEND")
        self.clock = Clock()
        self.date, self.time, self.hour, self.minutes = self.clock.clock_time()

    def end_read(self):
        self.continue_reading = False
        GPIO.cleanup()

    def run_rfid(self):

        while self.continue_reading:
            # print("Pripojene na SQL server?: " + str(self.sql.mysql_database.is_connected()))
            # Skenuj karty
            (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

            # Ak sa nasla karta
            if status == self.MIFAREReader.MI_OK:
                print("Karta bola detekovana")

            # Get the UID of the card
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()

            # Ak mas UID tak pokracuj
            if status == self.MIFAREReader.MI_OK:

                try:
                    self.detected_chip_number = str(uid[0]) + "-" + str(uid[1]) + "-" + str(uid[2]) + "-" + str(
                        uid[3]) + "-" + str(uid[4])
                    if self.sql.check_chip_number(self.detected_chip_number)[1] is False:
                        print("Karta nerozpoznana")
                        print("ID:" + str(uid[0]) + "-" + str(uid[1]) + "-" + str(uid[2]) + "-" + str(
                            uid[3]) + '-' + str(
                            uid[4]))
                        return False

                    else:
                        print("ID:" + str(uid[0]) + "-" + str(uid[1]) + "-" + str(uid[2]) + "-" + str(
                            uid[3]) + '-' + str(
                            uid[4]))
                        print("Karta rozpoznana")
                        return True

                        # self.lcd.lcd_print_data("Stlac prichod/odchod", 0, 2)
                        # while True:
                        #     if self.login_button.button_callback() is True:
                        #         print("tlacitko prihlasenie bolo stlacene")
                        #         self.sql.login_operator(self.sql.get_line_name(), detected_chip_number)
                        #         time.sleep(1)
                        #         break
                        #     if self.logoff_button.button_callback() is True:
                        #         print("Tlacitko odhlasenie bolo stlacene")
                        #         self.sql.logoff_operator(self.sql.get_line_name(), detected_chip_number)
                        #         time.sleep(1)
                        #         break
                        #
                        # self.lcd.clear()
                        # self.check_if_somebody_is_logged()
                        #
                        # print(self.sql.print_table_data())


                except Exception as e:
                    print(e)
                    self.lcd.lcd_print_data("Nejde siet/SQL?", 2, 2)
                    while True:
                        try:
                            self.sql.sql_check_if_somebody_is_logged()
                            break
                        except:
                            self.lcd.lcd_print_data("Pokus o pripojenie", 2, 2)
                            self.lcd.clear()
                            time.sleep(2)
                    self.check_if_somebody_is_logged()

