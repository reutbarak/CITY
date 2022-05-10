from flask import Flask, render_template, url_for, request, send_from_directory
import CITY_algorithm as CT

app = Flask(__name__, static_url_path='/templates')

# use this to extract form info inserted by the user
@app.route('/', methods = ['GET', 'POST'])
def Chosen_city():
    CITY_algorithm_result = False
    if request.method == 'POST':
        form = request.form
        CITY_algorithm_result = calc_CITY_algorithm(form)

    return render_template('Cities.html', CITY_algorithm_result=CITY_algorithm_result)

# use this to extract variables from the form and run CITY algorithm
def calc_CITY_algorithm(form):
    religion_pref = int(request.form['religion_pref'])
    district_pref = request.form['district_pref']
    param1 = request.form['param1']
    param1_rank = int(request.form['param1_rank'])
    param2 = request.form['param2']
    param2_rank = int(request.form['param2_rank'])
    param3 = request.form['param3']
    param3_rank = int(request.form['param3_rank'])
    chosen_city = CT.recommend_CITY(religion_pref, district_pref, param1, param1_rank, param2, param2_rank,  param3, param3_rank)
    return chosen_city

app.run()