import requests
import json
from db_models import Rectangle
from os import environ

class Rectangle_service:
    
    def __init__(self, env):
        # environment = environ.get('ASPNETCORE_ENVIRONMENT')
        if env=='Production':
            file_path = 'c:/Users/tkowa/OneDrive/Dokumenty/Studia/Informaryka EE/Semestr5/Programowanie API Mobi Web/RectangleApi/L3/Services/end_points_client_product.json'
            with open(file_path, 'r') as plik:
                self.url_map = json.load(plik)
        else:
            file_path = 'c:/Users/tkowa/OneDrive/Dokumenty/Studia/Informaryka EE/Semestr5/Programowanie API Mobi Web/RectangleApi/L3/Services/end_points_client.json'
            with open(file_path, 'r') as plik:
                self.url_map = json.load(plik)
        pass
    
    def get_all_rectangles(self):
        url = self.url_map['base_URL'] + self.url_map['get_all_rectabgles_end_point']
        all_rectangles_json = requests.get(url).json()
        rectengle_models = []
        for single in all_rectangles_json:
           rectengle_models.append(Rectangle(**single))
        return rectengle_models
    
    def get_single_rectangle(self, id):
        url = self.url_map['base_URL'] + self.url_map['get_one_rectangle_end_point']
        url = url.replace('<int:id>',str(id))
        rectangle_json = requests.get(url).json()
        rectangle_model = Rectangle(**rectangle_json)
        return rectangle_model
    
    def create_new_rectangle(self, len, hei):
        url = self.url_map['base_URL'] + self.url_map['create_rectangle_end_point']
        data_json = {
            "height": hei,
            "length": len
        }
        rectangle_json = requests.post(url,json=data_json).json()
        # print(rectangle_json)
        rectangle_model = Rectangle(**rectangle_json)
        return rectangle_model
    
    def update_one_rectangle(self, id, len, hei):
        url = self.url_map['base_URL'] + self.url_map['update_rectangle_end_point']
        url = url.replace('<int:id>',str(id))
        data_json = {
            "height": hei,
            "length": len
        }
        rectangle_json = requests.patch(url, json=data_json).json()
        rectangle_model = Rectangle(**rectangle_json)
        return rectangle_model
    
    def deleta_rectangle(self, id):
        url = self.url_map['base_URL'] + self.url_map['delete_rectangle_end_point']
        url = url.replace('<int:id>',str(id))
        info_json = requests.delete(url).json()
        info = info_json['info']
        return info
        
                
        