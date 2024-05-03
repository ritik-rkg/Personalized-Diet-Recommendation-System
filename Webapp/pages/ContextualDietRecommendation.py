import streamlit as st
import pandas as pd
import numpy as np
from random import uniform as rnd
# from streamlit_echarts import st_echarts
breakfast = pd.read_csv('/Users/anshavikhanna/Desktop/SEM 6/RecSys/Endterm Project/Webapp/dataset/breakfast.csv')
lunch = pd.read_csv('/Users/anshavikhanna/Desktop/SEM 6/RecSys/Endterm Project/Webapp/dataset/lunch.csv')
dinner = pd.read_csv('/Users/anshavikhanna/Desktop/SEM 6/RecSys/Endterm Project/Webapp/dataset/dinner.csv')

st.set_page_config(page_title="Automatic Diet Recommendation", page_icon="🍲",layout="wide")


nutritions_values=['Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent']
# Streamlit states initialization
if 'person' not in st.session_state:
    st.session_state.generated = False
    st.session_state.recommendations=None
    st.session_state.person=None
    st.session_state.weight_loss_option=None


def make_context(user_df, cluster_combo_means, i, key):
        user_features = [user_df.loc[i, 'bmr'], user_df.loc[i, 'muscle'],  user_df.loc[i, 'weightloss'], user_df.loc[i, 'hearthealthy'], user_df.loc[i, 'physical_activity_level']]
        item_features = cluster_combo_means[key]
        user_features.extend(item_features)
        context = np.array(user_features)  
        if (np.dot(context.T, context)) > 1:
            context = context/np.dot(context.T, context)
        return context


class Person:

    def __init__(self,age,height,weight,gender,activity,muscle,weightloss,hearthealthy):
        self.age=age
        self.height=height
        self.weight=weight
        self.gender=gender
        self.activity=activity
        self.muscle=muscle
        self.weightloss=weightloss
        self.hearthealthy=hearthealthy

    def calculate_bmi(self,):
        bmi=round(self.weight/((self.height/100)**2),2)
        return bmi

    def display_result(self,):
        bmi=self.calculate_bmi()
        bmi_string=f'{bmi} kg/m²'
        if bmi<18.5:
            category='Underweight'
            color='Red'
        elif 18.5<=bmi<25:
            category='Normal'
            color='Green'
        elif 25<=bmi<30:
            category='Overweight'
            color='Yellow'
        else:
            category='Obesity'    
            color='Red'
        return bmi_string,category,color

    def calculate_bmr(self):
        if self.gender=='Male':
            bmr=10*self.weight+6.25*self.height-5*self.age+5
        else:
            bmr=10*self.weight+6.25*self.height-5*self.age-161
        return bmr
    
    def men_bmr(self):
        return 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)

    def women_bmr(self):
        return 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.330 * self.age)
    
    def nutrient_count(self):
        if (gender == 1):
            bmr = self.men_bmr()
        else:
            bmr = self.women_bmr()
        cal_factor = {0: 1.2, 1:1.375, 2:1.465, 3:1.55, 4:1.725, 5:1.9}
        protein_factor = {0: 0.8, 1:1, 2:1.2, 3: 1.4, 4:1.6, 5:1.8}
        calories = cal_factor[self.activity]*bmr
        protein = protein_factor[self.activity]*weight
        fiber = 0.014*calories
        carbohydrates = 0.45*calories/4
        fat = 0.2*calories/9
        return [bmr, calories, protein, fat, fiber, carbohydrates]

    def recommend_diet(self, w):
        new_user = {}
        new_user['gender'] = self.gender
        new_user['height'] = self.height
        new_user['weight'] = self.weight
        new_user['age'] = self.age
        new_user['physical_activity_level'] = self.activity
        new_user['muscle'] = self.muscle
        new_user['weightloss'] = self.weightloss
        new_user['hearthealthy'] = self.hearthealthy
        nutrient_list = self.nutrient_count()
        new_user['bmr'] = nutrient_list[0]
        new_user['calories'] = nutrient_list[1]
        new_user['protein'] = nutrient_list[2]
        new_user['fat'] = nutrient_list[3]
        new_user['fiber'] = nutrient_list[4]
        new_user['carbohydrates'] = nutrient_list[5]
        new_user = pd.DataFrame([new_user])
        p = {}
        cluster_combo_means={0: [64.55524468957142,
                                38.00633583943506,
                                27.42278526908157,
                                108.9025014739753,
                                12.969818101105215],
                                1: [44.86585804210138,
                                37.560872642972285,
                                31.61828404092015,
                                132.4572908264375,
                                12.69692743673332],
                                2: [49.73368905147081,
                                45.78008845806606,
                                27.592248799392546,
                                107.42148178685217,
                                16.6252196823982],
                                3: [63.95508682106501,
                                59.06948101784589,
                                6.116234043147061,
                                55.942095157482655,
                                21.197074694816042],
                                4: [44.26570017359496,
                                58.62401782138311,
                                10.311732814985643,
                                79.49688450994485,
                                20.924184030444145],
                                5: [49.13353118296439,
                                66.84323363647688,
                                6.285697573458037,
                                54.46107547035951,
                                24.852476276109023],
                                6: [59.64023954623104,
                                43.75143857075103,
                                9.939003162228136,
                                95.83783007315955,
                                15.381608795398302],
                                7: [39.950852898760985,
                                43.30597537428826,
                                14.134501934066716,
                                119.39261942562175,
                                15.108718131026407],
                                8: [44.81868390813042,
                                51.52519118938203,
                                10.10846669253911,
                                94.35681038603641,
                                19.037010376691285],
                                9: [78.3726689034189,
                                47.93931710307668,
                                7.226852884788804,
                                64.3742393733517,
                                17.05508234519372],
                                10: [58.683282255948846,
                                47.49385390661391,
                                11.422351656627384,
                                87.9290287258139,
                                16.782191680821825],
                                11: [63.55111326531828,
                                55.71306972170768,
                                7.39631641509978,
                                62.893219686228555,
                                20.710483926486702],
                                12: [57.3790560421066,
                                23.328039444757458,
                                33.63676370993721,
                                151.73949812462476,
                                5.810880595593137],
                                13: [37.689669394636546,
                                22.88257624829469,
                                37.83226248177579,
                                175.29428747708695,
                                5.537989931221242],
                                14: [42.55750040400598,
                                31.10179206338846,
                                33.806227240248184,
                                150.25847843750162,
                                9.466282176886121],
                                15: [56.778898173600176,
                                44.391184623168286,
                                12.330212484002704,
                                98.77909180813211,
                                14.038137189303963],
                                16: [37.089511526130124,
                                43.94572142670551,
                                16.525711255841284,
                                122.3338811605943,
                                13.765246524932069],
                                17: [41.957342535499556,
                                52.16493724179928,
                                12.499676014313678,
                                97.29807212100897,
                                17.69353877059695],
                                18: [52.4640508987662,
                                29.073142176073432,
                                16.152981603083777,
                                138.674826723809,
                                8.222671289886224],
                                19: [32.77466425129615,
                                28.627678979610657,
                                20.348480374922357,
                                162.2296160762712,
                                7.949780625514329],
                                20: [37.642495260665584,
                                36.846894794704426,
                                16.32244513339475,
                                137.19380703668585,
                                11.878072871179208],
                                21: [71.19648025595407,
                                33.26102070839908,
                                13.440831325644446,
                                107.21123602400115,
                                9.896144839681641],
                                22: [51.50709360848401,
                                32.815557511936305,
                                17.636330097483025,
                                130.76602537646335,
                                9.623254175309746],
                                23: [56.374924617853445,
                                41.03477332703008,
                                13.61029485595542,
                                105.73021633687802,
                                13.551546420974624],
                                24: [56.952383101454885,
                                30.20962586124117,
                                28.49524872602443,
                                133.90284449107074,
                                9.408985967061717],
                                25: [37.262996453984826,
                                29.764162664778397,
                                32.69074749786301,
                                157.45763384353296,
                                9.136095302689823],
                                26: [42.130827463354265,
                                37.98337847987217,
                                28.664712256335406,
                                132.4218248039476,
                                13.064387548354702],
                                27: [56.35222523294846,
                                51.272771039652,
                                7.18869750008992,
                                80.9424381745781,
                                17.636242560772544],
                                28: [36.66283858547841,
                                50.827307843189224,
                                11.3841962719285,
                                104.4972275270403,
                                17.36335189640065],
                                29: [41.53066959484784,
                                59.04652365828299,
                                7.358161030400896,
                                79.46141848745496,
                                21.29164414206553],
                                30: [52.03737795811449,
                                35.95472859255714,
                                11.011466619170992,
                                120.838173090255,
                                11.820776661354804],
                                31: [32.34799131064444,
                                35.509265396094364,
                                15.206965391009573,
                                144.3929624427172,
                                11.54788599698291],
                                32: [37.21582232001387,
                                43.72848121118814,
                                11.180930149481968,
                                119.35715340313186,
                                15.476178242647789],
                                33: [70.76980731530236,
                                40.14260712488279,
                                8.29931634173166,
                                89.37458239044715,
                                13.494250211150222],
                                34: [51.0804206678323,
                                39.69714392842001,
                                12.494815113570242,
                                112.92937174290934,
                                13.221359546778327],
                                35: [55.94825167720173,
                                47.91635974351378,
                                8.468779872042637,
                                87.89356270332401,
                                17.14965179244321]}
        
        for key, value in cluster_combo_means.items():
            context = make_context(new_user, cluster_combo_means, 0, key)
            p_t_a = np.dot(w.T, context)
            p[key] = p_t_a
        chosen_arm = max(p, key=p.get)
        # return new_user, chosen_arm

        c = 0
        indices = []
        for i in range (3):
            for j in range (4):
                for k in range (3):
                    if (c == chosen_arm):
                        indices = [i, j ,k]
                        break
                    c += 1
        breakfast_options = breakfast[breakfast['Cluster'] == indices[0]].sample(n=5)
        lunch_options = lunch[lunch['Cluster'] == indices[1]].sample(n=5)
        dinner_options = dinner[dinner['Cluster'] == indices[2]].sample(n=5)
        cols_to_scale = ['Servings Per Recipe', 'calories',
        'protein', 'carbohydrates', 'fat', 'saturated_fat', 'cholesterol',
        'fiber', 'Sodium',]
        for col in cols_to_scale:
            breakfast_options[col] = breakfast_options[col]*(new_user.loc[0, 'calories']/1000)*0.3
            lunch_options[col] = lunch_options[col]*(new_user.loc[0, 'calories']/1000)*0.4
            dinner_options[col] = dinner_options[col]*(new_user.loc[0, 'calories']/1000)*0.3
        return [breakfast_options, lunch_options, dinner_options]

class Display:
    def __init__(self):
        self.goals=["Muscle Gain","Weight loss","Cardiac (Heart Healthy)"]
        self.activities=['Sedentary: little or no exercise', 
                         'Exercise 1-3 times/week', 
                         'Exercise 4-5 times/week', 
                         'Daily exercise or intense exercise 3-4 times/week', 
                         'Intense exercise 6-7 times/week',
                         'Very intense exercise daily, or physical job']
        pass

    def display_bmi(self,person):
        st.header('BMI CALCULATOR')
        bmi_string,category,color = person.display_result()
        st.metric(label="Body Mass Index (BMI)", value=bmi_string)
        new_title = f'<p style="font-family:sans-serif; color:{color}; font-size: 25px;">{category}</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.markdown(
            """
            ( Healthy BMI range: 18.5 kg/m² - 25 kg/m² )
            """)   
        
    def display_calories(self,person):
        maintain_calories = person.nutrient_count()[1]
        st.header(f'Optimal Calorie Intake (per day): {round(maintain_calories)} calories') 

    def meal_index_to_name(self,index):
        if index == 0:
            return "Breakfast"
        elif index == 1:
            return "Lunch   "
        elif index == 2:
            return "Dinner  "
        else:
            return "Unknown "
    
    def display_meal_plan(self,person,recommendations):
        num_days = len(recommendations[0])  # Assuming all meals have the same number of options
        num_meals = len(recommendations)

        for day_index in range(num_days):
            st.write(f"### Recommendation {day_index + 1}")
            for meal_index in range(num_meals):
                with st.expander(f"{self.meal_index_to_name(meal_index)} :  {recommendations[meal_index].iloc[day_index]['Name']}"):
                    st.write(recommendations[meal_index].iloc[day_index][['Name', 'calories', 'protein', 'carbohydrates', 'fat', 'cholesterol', 'fiber', 'URL']])
            st.write("")  # Add some space between expanders

w=np.array([-1.83658519e+02,  1.55509438e+05, -9.32485546e+04, -3.72363155e+05,
       -1.63900244e+04,  9.16672161e+03, -2.62563842e+04, -5.34776040e+03,
        3.57282232e+03,  3.73422050e+04])
display=Display()
title="<h1 style='text-align: center;'>Diet Recommendation System</h1>"
st.markdown(title, unsafe_allow_html=True)

with st.form("recommendation_form"):
    age = st.number_input('Age',min_value=2, max_value=120, step=1)
    height = st.number_input('Height(cm)',min_value=50, max_value=300, step=1)
    weight = st.number_input('Weight(kg)',min_value=10, max_value=300, step=1)
    gender_option = st.radio('Gender',('Male','Female'))
    if gender_option == 'Male':
        gender = 0
    else:
        gender = 1
    muscle=0
    weightloss=0
    hearthealthy=0
    activity_option = st.selectbox('Choose your activity level:',display.activities)
    activity=display.activities.index(activity_option)
    goal_option = st.selectbox('Choose your weight loss plan:',display.goals)
    if(display.goals.index(goal_option)==0):
        muscle=1
    elif(display.goals.index(goal_option)==1):
        weightloss=1
    elif(display.goals.index(goal_option)==1):
        hearthealthy=1
    generated = st.form_submit_button("Generate")

if generated:
    st.session_state.generated=True
    person = Person(age,height,weight,gender,activity,muscle,weightloss,hearthealthy)
    with st.container():
        display.display_bmi(person)
    with st.container():
        display.display_calories(person)
    with st.spinner('Generating recommendations...'): 
        recommendations=person.recommend_diet(w)
        st.session_state.recommendations=recommendations
        st.session_state.person=person

if st.session_state.generated:
    with st.container():
        display.display_meal_plan(st.session_state.person,st.session_state.recommendations)
        st.success('Recommendation Generated Successfully !', icon="✅")
