# server.py
from folium import CustomIcon
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from dao import index_dao
from jinja2 import Template
from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle, folium
from folium.plugins import MarkerCluster
import js2py

# db 불러오기
with open(file='models/myDao.pkl', mode='rb') as f:
  myDao = pickle.load(f)

# 공원과 같은 자치구 내의 (편의시설/카페/음식점/교통) 추천
def recommend(df, place_gu,  topno=5):
   df_can = df[df['gu']==place_gu]
   count_vect_category = CountVectorizer(min_df=0, ngram_range=(1, 2))
   place_category = count_vect_category.fit_transform(df_can['cate_mix'])
   con_simi_cate = cosine_similarity(place_category, place_category)
   con_simi_cate_sorted_ind = con_simi_cate.argsort()[:, ::-1]
   similar_indexes = con_simi_cate_sorted_ind.reshape(-1)
   return df_can.iloc[similar_indexes, :].head(topno)

def recommend_place(df, place_gu, dong_name, topno=5):
   condition = "(gu== @place_gu)"
   df_can = df.query(condition)
   count_vect_category = CountVectorizer(min_df=0, ngram_range=(1, 2))
   place_category = count_vect_category.fit_transform(df_can['cate_mix'])
   con_simi_cate = cosine_similarity(place_category, place_category)
   con_simi_cate_sorted_ind = con_simi_cate.argsort()[:, ::-1]
   similar_indexes = con_simi_cate_sorted_ind.reshape(-1)
   return df_can.iloc[similar_indexes, :].head(topno)

def get_near_place(guname, dongname):
   cafe, food, pharm, clinic, toilet, tools, trans = myDao.cafe,myDao.food, myDao.pharm, myDao.toilet, myDao.clinic, myDao.tools, myDao.trans
   cafe_r = recommend_place(cafe, guname, dongname)
   food_r = recommend_place(food, guname, dongname)
   pharm_r = recommend(pharm, guname)
   clinic_r = recommend(clinic,guname)
   toilet_r = recommend(toilet,guname)
   tools_r = recommend(cafe, guname)
   trans_r = recommend(cafe, guname)
   recommend_df = pd.concat([cafe_r, food_r, pharm_r, clinic_r, toilet_r, tools_r, trans_r ])
   recommend_df.reset_index(inplace=True)
   return recommend_df


app = Flask(__name__)

@app.route('/')
@app.route('/html1_home.html')
def index():
   return render_template('html1_home.html')
@app.route('/html2_search.html')
def html():
   return render_template('html2_search.html')

@app.route('/html3_about.html')
def html3():
   return render_template('html3_about.html')


@app.route('/html4_team.html')
def html4():
   return render_template('html4_team.html')

@app.route('/park',methods = ['post'])
def get_park():
   
   global guname
   global dongname
   park = myDao.park
   guname = str(request.form['gu'])
   dongname = str(request.form['dong'])
   df = park[park['gu'] == guname]
   df.reset_index(inplace=True)
   map = folium.Map(location=(37.5665, 126.9780), zoom_start=11)
   # 선택한 자치구에  위치한 전체 공원 위치를 지도에 표기
   for n in df.index:
      icon1 = CustomIcon('data/icon_final/icon_1.png', icon_size=(50, 50), icon_anchor=(10, 20))
      folium.Marker([df.loc[n, 'lat'], df.loc[n, 'lng']], tooltip=df['name'][n], icon=icon1,
                    popup=folium.Popup(df['name'][n] + '</strong><br>' + '<a href="http://localhost:5000/near"> 공원선택 </a>',
                                       max_width=300)).add_to(map)

   return map._repr_html_()

@app.route('/near')
def show_near():
   df= get_near_place(guname, dongname)
   type_list = ['동물병원', '동물약국', '화장실', '동물용의료용구판매업', '교통', '카페', '음식점']

   map = folium.Map(location=[37.5502, 126.982], zoom_start=11)

   g1 = folium.FeatureGroup(type_list[0]);
   map.add_child(g1)
   g2 = folium.FeatureGroup(type_list[1]);
   map.add_child(g2)
   g3 = folium.FeatureGroup(type_list[2]);
   map.add_child(g3)
   g4 = folium.FeatureGroup(type_list[3]);
   map.add_child(g4)
   g5 = folium.FeatureGroup(type_list[4]);
   map.add_child(g5)
   g6 = folium.FeatureGroup(type_list[5]);
   map.add_child(g6)
   g7 = folium.FeatureGroup(type_list[6]);
   map.add_child(g7)

   folium.LayerControl(collasped=False).add_to(map)

   for n in df.index:
      if df['type'][n] == type_list[0]:
         icon2 = CustomIcon('data/icon_final/icon_2.png', icon_size=(50, 50), icon_anchor=(10, 20))
         folium.Marker([df.loc[n, 'lat'], df.loc[n, 'lng']], tooltip=df['name'][n], icon=icon2).add_to(g1)

      elif df['type'][n] == type_list[1]:
         icon3 = CustomIcon('data/icon_final/icon_3.png', icon_size=(50, 50), icon_anchor=(10, 20))
         folium.Marker([df.loc[n, 'lat'], df.loc[n, 'lng']], tooltip=df['name'][n], icon=icon3).add_to(g2)

      elif df['type'][n] == type_list[2]:
         icon4 = CustomIcon('data/icon_final/icon_4.png', icon_size=(50, 50), icon_anchor=(10, 20))
         folium.Marker([df.loc[n, 'lat'], df.loc[n, 'lng']], tooltip=df['name'][n], icon=icon4).add_to(g3)

      elif df['type'][n] == type_list[3]:
         icon5 = CustomIcon('data/icon_final/icon_5.png', icon_size=(50, 50), icon_anchor=(10, 20))
         folium.Marker([df.loc[n, 'lat'], df.loc[n, 'lng']], tooltip=df['name'][n], icon=icon5).add_to(g4)

      elif df['type'][n] == type_list[4]:
         icon6 = CustomIcon('data/icon_final/icon_6.png', icon_size=(50, 50), icon_anchor=(10, 20))
         folium.Marker([df.loc[n, 'lat'], df.loc[n, 'lng']], tooltip=df['name'][n], icon=icon6).add_to(g5)

      elif df['type'][n] == type_list[5]:
         icon7 = CustomIcon('data/icon_final/icon_7.png', icon_size=(50, 50), icon_anchor=(10, 20))
         folium.Marker([df.loc[n, 'lat'], df.loc[n, 'lng']], tooltip=df['name'][n], popup=folium.Popup(
            '<strong>' + df['name'][n] + '(' + df['typedetail'][n] + ')' + '</strong><br>' + '주소 : ' + df['address'][
               n] + '</strong><br>' + '동반조건 : ' + df['conditions'][n], max_width=300), icon=icon7).add_to(g7)

      elif df['type'][n] == type_list[6]:
         icon8 = CustomIcon('data/icon_final/icon_8.png', icon_size=(50, 50), icon_anchor=(10, 20))
         folium.Marker([df.loc[n, 'lat'], df.loc[n, 'lng']], tooltip=df['name'][n], popup=folium.Popup(

            '<strong>' + df['name'][n] + '(' + df['typedetail'][n] + ')' + '</strong><br>' + '주소 : ' + df['address'][
               n] + '</strong><br>' + '동반조건 : ' + df['conditions'][n], max_width=300), icon=icon8).add_to(g7)

   return map._repr_html_()


if __name__ == '__main__':
   app.run(debug = True)




