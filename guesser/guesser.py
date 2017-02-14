import pickle
import pandas as pd
import numpy as np


def create_data(input_file='artists_data.csv'):
    """
    Parse csv file to format:
    {
        "feature1": [
            "val1",
            "val2",
            ...
        ],
        "feature2": [
            "val1",
            "val2",
            ...
        ]
    }
    :param input_file: string, path to csv file containing people data.
    :return: dict, with format as specified above.
    """
    df = pd.read_csv(input_file)
    return {col_name: df[col_name].values for col_name in list(df)}


def probabilities(data, attrs, result):
    """
    Returns probabilities for given attributes.
    :param data:
    :param attrs:
    :param result:
    :return:
    """
    print data
    if type(data) == np.float64:
        result.append((attrs, data))
    else:
        for i in xrange(len(data)):
            probabilities(data[i], attrs+[i], result)
    return result


def clean_probs(probs):
    """

    :param probs:
    :return:
    """
    return [p for p in probs if p[1] != 1./15]


def ask_question(attr_ind, cpd, prob):
    """

    :param attr_ind:
    :param cpd:
    :param prob:
    :return:
    """
    attr_name = cpd.variables[attr_ind]
    print "Select " + attr_name + ":"
    avail_answers = [x[0][attr_ind] for x in prob]
    for res_no, res in enumerate(cpd.state_names[attr_name]):
        if res_no in avail_answers:
            print str(res_no) + ":  " + res
    response = raw_input("> ")
    return int(response)


def reduce_probs(probs, response, attr_ind):
    """

    :param probs:
    :param response:
    :param attr_ind:
    :return:
    """
    probs_red = [p for p in probs if p[0][attr_ind] == response]
    return probs_red


def print_temp_results(prob, names):
    """

    :param prob:
    :param names:
    :return:
    """
    person_prob = [sum([p[1] for p in prob if p[0][0] == person_id])
                   for person_id in xrange(len(names))]
    sum_prob = sum(person_prob)
    if sum_prob > 0:
        prob = [p / sum_prob for p in person_prob]
    result_count = 0
    if len(prob) == 0:
        print "\nNO MATCHES"
        exit(0)
    for person_idx in range(15):
        if prob[person_idx] > 0:
            result_count += 1
            print names[person_idx], prob[person_idx]
    print
    if result_count < 2:
        exit(0)


def guess(prob, names, cpd):
    """

    :param prob:
    :param names:
    :param cpd:
    :return:
    """
    prob = clean_probs(prob)
    for j in range(1, 8):
        i = 9-j
        response = ask_question(i, cpd, prob)
        prob = reduce_probs(prob, response, i)
        print_temp_results(prob, names)


def main():
    with open("model_dump_15.pkl", 'rb') as f_in:
        params = pickle.load(f_in)

    prob = probabilities(params.values, [], [])
    names = params.state_names['identity']

    guess(prob, names, params)


if __name__ == '__main__':
    main()
