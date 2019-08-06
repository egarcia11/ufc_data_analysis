#!/usr/bin/env python
# coding: utf-8
import os
import pandas as pd
from numpy import NaN

class identifyers(object):
    #Extract name, sex and births of every name in the names-files
    files = [f for f in os.listdir("./names") if os.path.isfile(os.path.join("./names", f))]
    namesFrame = pd.DataFrame()
    pieces = []
    for file in files:
        pieces.append(pd.read_csv(os.path.join("./names",file), names=['name','sex','births']))
    data = pd.concat(pieces,ignore_index=True)
    namesFrame = data[['name','sex','births']]

    #Group contents by name and stratify the dataset by male and female
    malesFrame = namesFrame[(namesFrame.sex == 'M')].groupby('name')
    femalesFrame = namesFrame[(namesFrame.sex == 'F')].groupby('name')

    #Get the intersection of the males and females sets. Intersection represents unisex names
    females_set = set(namesFrame[namesFrame.sex == 'F']['name'])
    males_set = set(namesFrame[namesFrame.sex == 'M']['name'])
    unisex_names = set(set(females_set) & set(males_set))

    #Remove unisex names from each set
    unique_males = males_set.difference(unisex_names)
    unique_females = females_set.difference(unisex_names)

    #Assign a probability to each unisex name and add the name back to their set if probability threshold is met
    ambiguous_names = set()
    for element in unisex_names:
        male_births = malesFrame.get_group(element).births.sum()
        female_births = femalesFrame.get_group(element).births.sum()
        total_births = male_births + female_births
        probability_m = male_births/total_births
        probability_f = 1 - probability_m

        if element == 'Esteban':
            print(male_births,female_births)

        #only add the name back to the male or female set if they meet the probability threshold
        threshold = .97
        if probability_m >= threshold:
            unique_males.add(element)
        elif probability_f >= threshold:
            unique_females.add(element)
        else:
            ambiguous_names.add(element)

    def sex_classifyer(self,name):
        if name in self.unique_males:
            return 'M'
        elif name in self.unique_females:
            return 'F'
        else:
            return NaN

#Validating algorithm
if __name__=="__main__":
    identifyer = identifyers()
    print(identifyer.sex_classifyer('Sergio'))


