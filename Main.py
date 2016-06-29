from subprocess import check_output
from datetime import datetime
from time import sleep
import Map as Map
import shutil
import os


class AutoBackup():
    def __init__(self):
        self.drives = {}
        self.found = False
        self.directory = None
        self.drive_map = None
        self.file_type_map = None
        self.drives_number_constant = None
        self.destination_directory = 'C:\\Users\stefa\Pictures\\'
        self.init()

    def init(self):
        self.drive_map = Map.Drive_Map
        self.file_type_map = Map.File_Type_Map
        self.drives_number_constant = len(check_output('wmic logicaldisk get DeviceID, volumename').splitlines()[2:])
        self.main()

    def main(self):
        while True:
            output_list = check_output('wmic logicaldisk get DeviceID, volumename').decode('utf-8').splitlines()[2:]
            drives_number = len(output_list)
            if self.drives_number_constant < drives_number and not self.found:
                self.found = True
                for drive in range(0, drives_number):
                    drive_details_list = output_list[drive].split(":")
                    drive_letter = drive_details_list[0]
                    if drive_letter:
                        drive_name = drive_details_list[1].strip()
                        if drive_name:
                            self.drives[drive_name] = drive_letter
                        else:
                            self.drives['None'] = drive_letter
                for usb_drive_name in self.drives:
                    if usb_drive_name in self.drive_map:
                        root_directory = self.drives[usb_drive_name] + ':\\'
                        self.folder_finder(root_directory, usb_drive_name)
                self.found = False
            self.drives_number_constant = drives_number
            sleep(15)

    def folder_finder(self, directory, usb_drive_name):
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                ext_position = file.rfind('.') + 1
                extension = file[ext_position:]
                if extension in self.file_type_map:
                    source_folder = subdir + '\\'
                    date = datetime.now().strftime('%Y-%m-%d_%H.%M.%S.%MS')
                    dst = self.destination_directory + usb_drive_name + date
                    shutil.copytree(source_folder, dst)
                    sleep(0.2)
                    break


ab = AutoBackup()
