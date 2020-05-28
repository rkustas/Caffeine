import os
import pymysql
import numpy as np
from flask import Flask, render_template, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text
from flask_cors import CORS
from config import MYSQLDATABASE_URL
from flask_sqlalchemy import SQLAlchemy

# Entering the DB env variable
# db_url = os.getenv("MYSQLDATABASE_URL")
db_url = MYSQLDATABASE_URL

# Testing the connection to the env variable for mysql
engine = create_engine(db_url)

# reflect an existing database into a new model
Base = automap_base()

# Reflect the tables from the db
Base.prepare(engine,reflect=True)

# Save references to tables
Drinks = Base.classes.drinks
Caff_info = Base.classes.caff_info
Supps = Base.classes.supplements
Food = Base.classes.food
Gum = Base.classes.gum_info

session = Session(engine)

app= Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = MYSQLDATABASE_URL
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
CORS(app)

# Define the home page and additional routes
@app.route("/")
def home():
    return (
        f"<h2>Welcome to the Caffeine Connoisseur's API!<h2/>"
        f"<h5>Available Routes:<h5/><br/>"
        f"/api/v1.0/drinklist<br/>"
        f"/api/v1.0/drinklist/ Please enter a drink name<drink><br/>"
        f"/api/v1.0/drinklist/caffeine/ Please enter a minimum caffeine content (Integer)<mincaff><br/>"
        f"/api/v1.0/drinklist/caffeine/ Please enter a minimum<mincaff> then / maximum caffeine content (Integer)<maxcaff><br/>"
        f"/api/v1.0/drinklist/serving/ Please enter a minimum serving size, this will be in OZ (Float)<minserv><br/>"
        f"/api/v1.0/caffeineinfo<br/>"
        f"/api/v1.0/caffeineinfo/ Please enter a strength level <strength><br/>"
        f"/api/v1.0/drinkspluscaffeine<br/>"
        f"/api/v1.0/supplements<br/>"
        f"/api/v1.0/food<br/>"
        f"/api/v1.0/food/ Please enter a minimum caffeine content per MG (Float)<min_caff_mg><br/>"
        f"/api/v1.0/food/ Please enter a minimum caffeine content per MG<min_caff_mg> then / max caffeine content per MG (Float)<max_caff_mg><br/>"
        f"/api/v1.0/gum"
    )
@app.route("/api/v1.0/drinklist")
def drinklist():
    all_drinks = session.query(Drinks).all()
    drink_list = []
    for d in all_drinks:
        drink ={}
        drink['Drink Name'] = d.drinks
        drink['Caffeine Content'] = d.caff_cont
        drink['Serving Size Fluid OZ'] = d.fluid_oz
        drink['MG per oz'] = d.mg_per_oz
        drink['Page URL'] = d.url
        drink_list.append(drink)

    return jsonify(drink_list)

# Canonicalized not working, need to enter exact string
@app.route("/api/v1.0/drinklist/<drink>")
def drinkchoice(drink):
    canonicalized = drink.replace(" ","").lower()
    choice_list = session.query(Drinks).\
        filter(Drinks.drinks == canonicalized).all()
    choicelist = []
    for c in choice_list:
        search_term = c.drinks.replace(" ","").lower()
        if search_term == canonicalized:
            choice = {}
            choice['Drink Name'] = c.drinks
            choice['Caffeine Content'] = c.caff_cont
            choice['Serving Size Fluid OZ'] = c.fluid_oz
            choice['MG per oz'] = c.mg_per_oz
            choice['Page URL'] = c.url
            choicelist.append(choice)

    return jsonify(choicelist)


@app.route("/api/v1.0/drinklist/caffeine/<mincaff>")
def caffminimum(mincaff):
    min_list = session.query(Drinks).\
        filter(Drinks.caff_cont >= mincaff).all()
    minlist = []
    for m in min_list:
        minitem = {}
        minitem['Drink Name'] = m.drinks
        minitem['Caffeine Content'] = m.caff_cont
        minitem['Serving Size Fluid OZ'] = m.fluid_oz
        minitem['MG per oz'] = m.mg_per_oz
        minitem['Page URL'] = m.url
        minlist.append(minitem)

    return jsonify(minlist)


@app.route("/api/v1.0/drinklist/caffeine/<mincaff>/<maxcaff>")
def minmaxlists(mincaff,maxcaff):
    min_maxlist = session.query(Drinks).\
        filter(Drinks.caff_cont >= mincaff).\
        filter(Drinks.caff_cont <= maxcaff).all()
    minmaxlist = []
    for minmax in min_maxlist:
        minmaxitem = {}
        minmaxitem['Drink Name'] = minmax.drinks
        minmaxitem['Caffeine Content'] = minmax.caff_cont
        minmaxitem['Serving Size Fluid OZ'] = minmax.fluid_oz
        minmaxitem['MG per oz'] = minmax.mg_per_oz
        minmaxitem['Page URL'] = minmax.url
        minmaxlist.append(minmaxitem)

    return jsonify(minmaxlist)


@app.route("/api/v1.0/drinklist/serving/<minserv>")
def servingsize(minserv):
    servings = session.query(Drinks).\
        filter(Drinks.fluid_oz >= minserv).all()
    serv_list = []
    for serv in servings:
        ss = {}
        ss['Drink Name'] = serv.drinks
        ss['Caffeine Content'] = serv.caff_cont
        ss['Serving Size Fluid OZ'] = serv.fluid_oz
        ss['MG per oz'] = serv.mg_per_oz
        ss['Page URL'] = serv.url
        serv_list.append(ss)

    return jsonify(serv_list)


@app.route("/api/v1.0/drinkspluscaffeine")
def drinkspluscaffeine():
    masterlist = session.query(Drinks,Caff_info).join(Caff_info,Drinks.drinks == Caff_info.drink_name).all()
    master = []
    for m,c in masterlist:
        eache = {}
        eache['Drink Name'] = m.drinks
        eache['Caffeine Content'] = m.caff_cont
        eache['Fluid OZ'] = m.fluid_oz
        eache['MG per oz'] = m.mg_per_oz
        eache['Page URL'] = m.url
        eache['Caffeine Strength'] = c.caff_str
        eache['Item Image URL'] = c.item_img
        master.append(eache)
    return jsonify(master)

@app.route("/api/v1.0/caffeineinfo")
def caffinfolist():
    caff_info_list = session.query(Caff_info).all()
    cainli= []
    for ca in caff_info_list:
        eachca = {}
        eachca['Caffeine Strength'] = ca.caff_str
        eachca['Item Image URL'] = ca.item_img
        eachca['Drink Name'] = ca.drink_name
        cainli.append(eachca)

    return jsonify(cainli)

# Need to add functionality to trim the search
@app.route("/api/v1.0/caffeineinfo/<strength>")
def strengthlistquery(strength):
    canonicalized = strength.replace(" ","").lower()
    st_list = session.query(Caff_info).\
        filter(Caff_info.caff_str == canonicalized).all()
    strengthlist= []
    for s in st_list:
        search_term = s.caff_str.replace(" ","").lower()
        if search_term == canonicalized:
            eachst = {}
            eachst['Caffeine Strength'] = s.caff_str
            eachst['Item Image URL'] = s.item_img
            eachst['Drink Name'] = s.drink_name
            strengthlist.append(eachst)

    return jsonify(strengthlist)

@app.route("/api/v1.0/supplements")
def supplementlist():
    supps = session.query(Supps).all()
    supp_list = []
    for supp in supps:
        supplement = {}
        supplement['Supplement'] = supp.supp
        supplement['Caffeine per serving(Mg)'] = supp.caff_per_serv
        supplement['Caffeine Source'] = supp.caff_source
        supp_list.append(supplement)

    return jsonify(supp_list)

@app.route("/api/v1.0/food")
def foodlist():
    foods = session.query(Food).all()
    food_list = []
    for f in foods:
        food = {}
        food['Food Name'] = f.food_name
        food['Caffeine per MG'] = f.caff_per_mg
        food['Serving Size'] = f.serving_size
        food['URL'] = f.url
        food['Image URL'] = f.img_url
        food_list.append(food)

    return jsonify(food_list)

@app.route("/api/v1.0/food/<min_caff_mg>")
def food_min_caff(min_caff_mg):
    foodsmincaff = session.query(Food).\
        filter(Food.caff_per_mg >= min_caff_mg).all()
    food_listmincaff = []
    for fo in foodsmincaff:
        food_dict = {}   
        food_dict['Food Name'] = fo.food_name
        food_dict['Caffeine per MG'] = fo.caff_per_mg
        food_dict['Serving Size'] = fo.serving_size
        food_dict['URL'] = fo.url
        food_dict['Image URL'] = fo.img_url
        food_listmincaff.append(food_dict)

    return jsonify(food_listmincaff)

@app.route("/api/v1.0/food/<min_caff_mg>/<max_caff_mg>")
def food_minmax_caff(min_caff_mg,max_caff_mg):
    foodsminmaxcaff = session.query(Food).\
        filter(Food.caff_per_mg >= min_caff_mg).\
        filter(Food.caff_per_mg <= max_caff_mg).all()
    food_listminmaxcaff = []
    for fod in foodsminmaxcaff:
        foods_dict = {}   
        foods_dict['Food Name'] = fod.food_name
        foods_dict['Caffeine per MG'] = fod.caff_per_mg
        foods_dict['Serving Size'] = fod.serving_size
        foods_dict['URL'] = fod.url
        foods_dict['Image URL'] = fod.img_url
        food_listminmaxcaff.append(foods_dict)

    return jsonify(food_listminmaxcaff)

@app.route("/api/v1.0/gum")
def gumlist():
    gums = session.query(Gum).all()
    gum_list = []
    for g in gums:
        gum = {}
        gum['Gum Name'] = g.gum_name
        gum['Caffeine per piece'] = g.caff_per_piece
        gum['Flavor'] = g.flavor
        gum['Price Per Pack'] = g.price_per_pack
        gum['Page URL'] = g.page_url
        gum_list.append(gum)

    return jsonify(gum_list)


if __name__ == "__main__":
    app.run(debug=True)