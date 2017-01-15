from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.estimators import ParameterEstimator, ExhaustiveSearch, BicScore, HillClimbSearch

import pandas as pd


def main():
    data_csv = '/home/joanna/studia/ekspertowe/se-guess-who/data/people_data.csv'
    df = pd.read_csv(data_csv)

    nodes = list(df)
    # nodes = [tuple([node]) for node in nodes]
    print nodes

    hc = HillClimbSearch(df, scoring_method=BicScore(df))
    best_model = hc.estimate()
    print(best_model.edges())

if __name__ == '__main__':
    main()
