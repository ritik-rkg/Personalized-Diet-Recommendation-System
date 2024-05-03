import numpy as np 
import pandas as pd 

class MultiArmBandit:
    def __init__(self, initial_epsilon, num_clusters, decay_rate):
        self.initial_epsilon = initial_epsilon
        self.epsilon = initial_epsilon
        self.num_clusters = num_clusters
        self.counts = [0] * num_clusters
        self.values = [2.0] * num_clusters
        self.decay_rate = decay_rate

    def choose_arm(self):
        if np.random.random() > self.epsilon:
            return np.argmax(self.values)
        else:
            return np.random.choice(self.num_clusters)

    def update(self, arm, reward):
        self.counts[arm] += 1
        n = self.counts[arm]
        value = self.values[arm]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm] = new_value

    def decay_epsilon(self):
        if(self.epsilon>0.2):
            self.epsilon *= self.decay_rate


heart_breakfast=pd.read_csv('/home/pranav/Downloads/csv files recsys/heart_breakfast_df.csv')
heart_lunch=pd.read_csv('/home/pranav/Downloads/csv files recsys/heart_lunch_df.csv')
heart_dinner=pd.read_csv('/home/pranav/Downloads/csv files recsys/heart_dinner_df.csv')
muscle_breakfast=pd.read_csv('/home/pranav/Downloads/csv files recsys/muscle_breakfast.csv')
muscle_lunch=pd.read_csv('/home/pranav/Downloads/csv files recsys/muscle_lunch_df.csv')
muscle_dinner=pd.read_csv('/home/pranav/Downloads/csv files recsys/muscle_dinner_df.csv')

name=input("Name: ")
print("Choose Goal:\n 1.Muscle building\n 2.Heart Healthy")
goal=int(input())
if(goal==1):
    df1=muscle_breakfast
    df2=muscle_lunch
    df3=muscle_dinner
    breakfastbandit=MultiArmBandit(1.0,df1['Cluster'].nunique(), decay_rate=0.99)
    lunchbandit=MultiArmBandit(1.0,df2['Cluster'].nunique(), decay_rate=0.99)
    dinnerbandit=MultiArmBandit(1.0,df3['Cluster'].nunique(), decay_rate=0.99)
else:
    df1=heart_breakfast
    df2=heart_lunch
    df3=heart_dinner
    breakfastbandit=MultiArmBandit(1.0,df1['Cluster'].nunique(), decay_rate=0.99)
    lunchbandit=MultiArmBandit(1.0,df2['Cluster'].nunique(), decay_rate=0.99)
    dinnerbandit=MultiArmBandit(1.0,df3['Cluster'].nunique(), decay_rate=0.99)
    

day=1
while(True):
        print("Day ",day)
        day=day+1
        cluster = breakfastbandit.choose_arm()
        cluster_df = df1[df1['Cluster'] == cluster]
        random_row_index = np.random.randint(0, len(cluster_df))
        recipe_name = cluster_df.iloc[random_row_index]['Name']
        print("Breakfast: ",recipe_name)
        reward=float(input("Rating: "))
        breakfastbandit.update(cluster, reward)
        breakfastbandit.decay_epsilon() 

        cluster = lunchbandit.choose_arm()
        cluster_df = df2[df2['Cluster'] == cluster]
        random_row_index = np.random.randint(0, len(cluster_df))
        recipe_name = cluster_df.iloc[random_row_index]['Name']
        print("Lunch: ",recipe_name)
        reward=float(input("Rating: "))
        lunchbandit.update(cluster, reward)
        lunchbandit.decay_epsilon()

        cluster = dinnerbandit.choose_arm()
        cluster_df = df3[df3['Cluster'] == cluster]
        random_row_index = np.random.randint(0, len(cluster_df))
        recipe_name = cluster_df.iloc[random_row_index]['Name']
        print("Dinner: ",recipe_name)
        reward=float(input("Rating: "))
        dinnerbandit.update(cluster, reward)
        dinnerbandit.decay_epsilon()

    



