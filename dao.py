import pandas as pd
import pickle

class index_dao():

    def __init__(self, cafe, food, park, pharm, clinic, toilet, tools, trans):
        self.cafe =cafe
        self.food = food
        self.park = park
        self.pharm = pharm
        self.clinic = clinic
        self.toilet = toilet
        self.tools = tools
        self.trans = trans

if __name__ == '__main__':
    cafe = pd.read_csv('data/data_cafe.csv', encoding='utf-8')
    food = pd.read_csv('data/data_food.csv', encoding='utf-8')
    park = pd.read_csv('data/data_park.csv', encoding='utf-8')
    pharm = pd.read_csv('data/data_pharm.csv', encoding='utf-8')
    clinic = pd.read_csv('data/data_clinic.csv', encoding='utf-8')
    toilet = pd.read_csv('data/data_toilet.csv', encoding='utf-8')
    tools = pd.read_csv('data/data_tools.csv', encoding='utf-8')
    trans = pd.read_csv('data/data_transportation.csv', encoding='utf-8')

    myDao = index_dao(cafe, food, park, pharm, clinic, toilet, tools, trans)

    pickle.dump(myDao, open('models/myDao.pkl','wb'))
