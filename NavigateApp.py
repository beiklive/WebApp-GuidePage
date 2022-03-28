# -*- coding: utf-8 -*-  
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import tldextract
import json
import os,base64

import math
import logging


define("port", default=6638, help="运行端口", type=int)

LOG_FORMAT = "[%(asctime)s] \033[;32;5m[%(levelname)s]\033[0m %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.DEBUG, datefmt=DATE_FORMAT, format=LOG_FORMAT)

def LoadJson():
    filename = 'GuideJson.json'
    JsonList = ''
    with open(filename, encoding='utf-8') as f:
        line = f.read()
        if line == '':
            JsonList = {'ImageData': [{'Name': 'default', 'CreateTime': 'default', 'Tags': ['default'], 'url': 'default'}]}
        else:
            JsonList = json.loads(line)
        f.close()
    logging.info("Load {} finish".format(filename))
    return JsonList['Data']

def BuildJson():
    Jsondata = LoadJson()
    GuideData = []
    colcount = 3
    length = len(Jsondata)
    LineCount = 1
    if length > colcount:
        LineCount = math.ceil(length/colcount)
    GuideData += [
        {
            "ColCount": colcount,
            "LineCount": LineCount,
            "SumCount": length
        }
    ]
    index = 0
    for data in Jsondata:
        url = data['Url']
        name = data['Name']
        ico = data['Icon']
        GuideData += [
            {
                "Name" : name,
                "Icon" : ico,
                "Url" : url,
                "index" : index
            }
        ]
        index += 1
    logging.info("Build Json finish ----> [ LineCount: {} ColCount: {} ]".format(LineCount, colcount))
    return GuideData



class StaticFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class MainHandler(tornado.web.RequestHandler):
    # 允许跨域
    def set_default_headers(self):
        # print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE, PUT')
        self.set_header("Access-Control-Allow-Headers", "token, content-type, user-token")
    def get(self):
        logging.info('Recvive [Get] request')
        build = BuildJson()
        logging.info('Start render')
        self.render("index.html", data=build)


    def post(self):
        logging.info('Recvive [Post] request')

        # Imgtype = self.get_argument("type")

        

class BK_tornado():
    __port_ = 0
    __uarg_ = ''
    __make_ = ''
    def __init__(self):
        self.__port_ = options.port

    def make_app(self):
        settings = {
            'debug' : True,
            "static_path": os.path.join(os.path.dirname(__file__), "templates"),        # 静态文件目录， 储存html的CSS和js
            "template_path" : os.path.join(os.path.dirname(__file__), "templates"),        # 储存html模板
        }
        self.__make_ =  tornado.web.Application([
            (r'/', MainHandler),
        ],
        **settings
        )

    def listen(self):
        self.__make_.listen(self.__port_)
        logging.info("Server is listening on port {port}".format(port=self.__port_))
    
    def start(self):
        logging.info("Now open address: localhost:{port}".format(port=self.__port_))
        tornado.ioloop.IOLoop.current().start()
        


if __name__ == "__main__":
    try:
        BK_T = BK_tornado()
        BK_T.make_app()
        BK_T.listen()
        BK_T.start()
    except KeyboardInterrupt:
        logging.info("See You!")
