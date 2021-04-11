import pandas as pd
import numpy

file = 'result_batches/Batch_4403340_batch_results_algo2.csv'


def get_column_names(df):
    head = df.head(0)
    return [x for x in head]


def filter_df_columns(df, coulmn_name_filter):
    names = [x for x in get_column_names(df) if coulmn_name_filter(x)]
    return df.filter(names)


def is_train_question(question):
    gold_trap = 'is the bank of england a private'
    return 'will there be coming of the?' in question or gold_trap in question or question.count('<h4>') > 1


def qual_filter(name):
    name = name.lower()
    return name.startswith('worker') or (name.startswith('answer.qual') and not is_train_question(name))


def diff_filter(name):
    name = name.lower()
    return name.startswith('worker') or (name.startswith('answer.diff') and not is_train_question(name))


def df_to_worker_id_ratings_dict(df):
    keys, worker_id_to_list_of_scores = _process_single_df(df)

    return {worker_id: get_scores(worker_id, keys, worker_id_to_list_of_scores) for worker_id in
            worker_id_to_list_of_scores}


def get_scores(worker_id, keys, id_to_list_of_scores):
    scores_dict = id_to_list_of_scores[worker_id]
    return [scores_dict[k] for k in keys]


def _process_single_df(df):
    d_list = df.to_dict(orient='records')
    worker_id_to_list_of_scores = {}  # dict from worker id to questions_score

    def add_to_dict(worker_id, scores_dict,
                    worker_id_to_list_of_scores=worker_id_to_list_of_scores):  # scores_dict is dict[question]=score
        if worker_id not in worker_id_to_list_of_scores:
            worker_id_to_list_of_scores[worker_id] = scores_dict
            return
        current_scores_dict = worker_id_to_list_of_scores[worker_id]
        for key, value in scores_dict.items():
            current_value = current_scores_dict[key]
            if value > 0:
                assert not current_value > 0
                current_scores_dict[key] = value
            else:
                assert current_value > 0

    for d in d_list:
        worker_id = d.pop('WorkerId')
        add_to_dict(worker_id, d)
    keys = list(d.keys())
    return keys, worker_id_to_list_of_scores


def print_dict_as_matlab(d):
    for key in d:
        scores = [str(x) if x >= 0 else '-1.0' for x in d[key]]
        print('\t'.join(scores))


def print_mean_and_std(d):
    scores = sum(d.values(), [])
    mean = numpy.nanmean(scores)
    print('mean', mean)
    print('std', numpy.nanstd(scores))
    return mean


measures = {'difficulty': diff_filter, 'relevancy': qual_filter}


def process_file(df):
    print(df)
    print('\n\n')
    means = {}
    for measure in measures:
        print('file:', file, 'Measure ', measure)
        measure_df = filter_df_columns(df, measures[measure])
        measure_dict = df_to_worker_id_ratings_dict(measure_df)
        mean = print_mean_and_std(measure_dict)

        print('questions answered:', sum([sum([1 for x in v if x > 0]) for v in measure_dict.values()]))
        print_dict_as_matlab(measure_dict)
        means[measure] = mean
    print(means)
    return measure_df


df = pd.read_csv(file, index_col=0)
print('file', file)
last_measure_df = process_file(df)
