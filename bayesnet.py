# Bayes Net

import pandas as pd
import json

OBS = 'data/hmm.csv'


class BayesNet():

    def __init__(self):
        self.init_obs(OBS)

    def init_obs(self, OBS):
        obs = pd.read_csv(OBS)
        symptoms = list(obs.Symptom.unique())

        self.obs = {}
        for i, symptom in enumerate(symptoms):
            if symptom != 'nan':
                count_dis_sym = obs[obs['Symptom'] == str(symptom)]
                count_dis_sym = count_dis_sym['Occurance']
                probs = self.normalise(count_dis_sym)
                diseases = obs[obs['Symptom'] == str(symptom)]
                diseases = diseases['Disease']
                self.obs[symptom] = dict(
                    zip(diseases, probs))

    def normalise(self, table):

        total = float(sum([i for i in table]))
        return [float(i) / total for i in table]

    def probability(self, symptom):

        try:
            return self.obs[symptom]
        except KeyError:
            return None

    def prob_symptoms(self, symptoms):
        prev = set([])
        prob = {}
        for symptom in symptoms:
            if self.probability(symptom):
                prob[symptom] = self.probability(symptom)
                prev = set(prob[symptom].keys())

        psym = {}
        expected = list(prev)

        for i in range(0, len(symptoms)):
            try:
                set1 = set(prob[symptoms[i]].keys())
                prev = set1.intersection(prev)
                expected = list(set(prev))
            except KeyError:
                pass

        expected_probs = []
        for dis in list(set(expected)):

            p = sum([prob[symptom][dis]
                     for symptom in symptoms if symptom in prob.keys()])
            expected_probs.append(p)

        psym['_'.join(symptoms)] = dict(
            zip(expected, self.normalise(expected_probs)))

        if psym['_'.join(symptoms)] == {}:
            return None
        return psym


if __name__ == '__main__':
    net = BayesNet()
    print "Probability of influenza given syncope is: "
    net.probability('syncope')
    net.probability('rale')
    net.probability('snore')

    print net.prob_symptoms(['worry'])
