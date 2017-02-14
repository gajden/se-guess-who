from pgmpy.estimators import BicScore, HillClimbSearch

import pandas as pd


def main():
    """
    Greedy approach to choosing edges in bayes network using hill climb algorithm.
    :return:
    """
    data_csv = '/home/joanna/studia/ekspertowe/se-guess-who/data/people_data.csv'
    df = pd.read_csv(data_csv)

    nodes = list(df)
    print nodes

    hc = HillClimbSearch(df, scoring_method=BicScore(df))
    best_model = hc.estimate()
    print(best_model.edges())

if __name__ == '__main__':
    main()
