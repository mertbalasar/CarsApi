from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from datetime import datetime
from os import path
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy import inspect
import pymysql, json, os

class EndPoint:

    # DIALOG ENUMS
    LOG = "LOG >"
    ERROR = "ERROR >"
    WARNING = "WARNING >"
    INFO = "INFO >"
    # OUTPUT FORMAT ENUMS
    JSON = ".json"
    CSV = ".csv"

    def __init__(self):
        self.data = None

        self.file_control()
    
    def get_data(self):
        return self.data
    
    def file_control(self):
        if path.exists("result.json"): os.remove("result.json")
    
    def fill_data(self):
        with open("result.json") as json_file:
            self.data = [json.loads(line) for line in json_file.read().splitlines()]
            self.show_status("Data Recevied", message_type=self.INFO)
        self.file_control()

    def run_spiders(self, LOG_LEVEL="ERROR"):
        setting = get_project_settings()
        setting["FEED_URI"] = "result.json" 
        setting["FEED_FORMAT"] = "jsonlines"
        setting["LOG_LEVEL"] = LOG_LEVEL
        process = CrawlerProcess(setting)

        for spider_name in process.spider_loader.list():
            self.show_status("Running Spider -> " + spider_name)
            process.crawl(spider_name)

        process.start()
        self.show_status("All Spiders Ran", message_type=self.INFO)
        self.fill_data()
    
    def fill_database(self, db_name=None, user_name=None, password=None, host=None, port=None):
        succ = True
        try:
            # create engine
            engine = create_engine(f"mysql+pymysql://{user_name}:{password}@{host}:{port}/{db_name}?")
            # create database diagram mapper
            base = automap_base()
            base.prepare(engine, reflect=True)
            # create session
            session = Session(engine)
        except:
            succ = False
        if succ: self.show_status("Database Connection Successfuly", message_type=EndPoint.INFO)
        else: self.show_status("Database Connection Failed", message_type=EndPoint.ERROR)
        succ = True
        try:
            # get table
            cars = base.classes.cars
        except:
            succ = False
        if succ: self.show_status("Table Load Successfuly", message_type=EndPoint.INFO)
        else: self.show_status("Table Load Failed", message_type=EndPoint.ERROR)
        succ = True
        try:
            # remove all data from table
            session.query(cars).delete()
            session.commit()
        except:
            succ = False
        if succ: self.show_status("Delete All Records From Table Successfuly", message_type=EndPoint.INFO)
        else: self.show_status("Delete All Records From Table Failed", message_type=EndPoint.ERROR)
        succ = True
        try:
            # insert all data into table
            for item in self.data:
                session.add(cars(
                    brand = item["brand"],
                    model = item["model"],
                    year = item["year"],
                    package = item["package"],
                    price = item["price"],
                    currency = item["currency"],
                ))
                session.commit()
        except:
            succ = False
        if succ: self.show_status("Insert All Records Into Table Successfuly", message_type=EndPoint.INFO)
        else: self.show_status("Insert All Records Into Table Failed", message_type=EndPoint.ERROR)
        succ = True
        try:
            # reset ids from table
            table = session.query(cars).all()
            id_no = 1
            for record in table:
                record.id = id_no
                id_no += 1
            session.commit()
        except:
            succ = False
        if succ: self.show_status("Reset Ids From Table Successfuly", message_type=EndPoint.INFO)
        else: self.show_status("Reset Ids From Table Failed", message_type=EndPoint.ERROR)

    def show_status(self, message, message_type=None, show_date=True):
        if not message_type: message_type = self.LOG

        s_date = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
        if not show_date: s_date = " "

        reformed_message = s_date + " " + message_type + " " + message
        print(reformed_message.strip())
    
end_point = EndPoint()

end_point.run_spiders()

user_name = "" # contains @ symbol
password = ""
host = "" # contains database.azure.com domain
port = ""
database = ""
end_point.fill_database(db_name=database, user_name=user_name, password=password, host=host, port=port) # input database name

