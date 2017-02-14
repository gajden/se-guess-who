import json
import os
from dircache import listdir
from os.path import join, basename

import shutil
import wget


def read_json(path):
    with open(path, 'r') as f_in:
        data = json.load(f_in)
    return data


class WikiDataCrawler(object):
    def __init__(self, mapping_path=None):
        self.url = 'https://www.wikidata.org/'
        self.api = 'w/api.php'
        self.query = {
            'action': 'wbgetentities',
            'languages': 'en',
            'format': 'json'
        }
        self.data_dir = '../data'
        self.filtered_dir = '../data/filtered'
        self.tmp_dir = '../data/tmp'
        self.mapping_path = mapping_path
        if self.mapping_path is None:
            self.mapping_path = join(self.data_dir, 'ids_mapping.json')
        self.mapping = None

    def get_mapping_for_known_ids(self, ids_list):
        ids_mapping = {}
        for query_id in ids_list:
            print query_id
            if not self.__check_if_id_file_exists(query_id):
                query_data = self.query.copy()
                query_data['ids'] = query_id

                query_url = '%s%s?action=%s&ids=%s&languages=%s&format=%s' % (self.url, self.api, query_data['action'],
                                                                              query_data['ids'], query_data['languages'],
                                                                              query_data['format'])
                filename = wget.download(query_url, out=join(self.tmp_dir, '%s.json' % query_id))
            else:
                filename = join(self.tmp_dir, '%s.json' % query_id)
            with open(filename, 'r') as f_in:
                query_data = json.load(f_in)
                try:
                    ids_mapping[query_id] = query_data['entities'][query_id]['labels']['en']['value']
                except Exception:
                    pass
        self.mapping = ids_mapping
        with open(self.mapping_path, 'w') as f_out:
            json.dump(self.mapping, f_out, indent=4)

    def crawl_ids(self, ids_list):
        result_ids = []
        for query_id in ids_list:
            print query_id
            if not self.__check_if_id_file_exists(query_id):
                query_data = self.query.copy()
                query_data['ids'] = query_id

                query_url = '%s%s?action=%s&ids=%s&languages=%s&format=%s' % (self.url, self.api, query_data['action'],
                                                                              query_data['ids'], query_data['languages'],
                                                                              query_data['format'])
                filename = wget.download(query_url, out=join(self.tmp_dir, '%s.json' % query_id))
            else:
                filename = join(self.tmp_dir, '%s.json' % query_id)
            with open(filename, 'r') as f_in:
                data = json.load(f_in)
                try:
                    if data['entities'][query_id]['claims']['P31'][0]['mainsnak']['datavalue']['value']['id'] == 'Q5':
                        shutil.copy(filename, join(self.filtered_dir, basename(filename)))
                        result_ids.append(query_id)
                    else:
                        os.remove(filename)
                except Exception:
                    pass
        return result_ids

    def get_ids_for_mapping(self):
        known_ids = []

        filenames = [join(self.filtered_dir, name) for name in listdir(self.filtered_dir)]
        for filename in filenames:
            data = read_json(filename)
            id = data['entities'].keys()[0]
            claims = data['entities'][id]['claims']

            for claim, values in claims.iteritems():
                known_ids.append(claim)
                for value in values:
                    try:
                        known_ids.append(value['mainsnak']['datavalue']['value']['id'])
                    except Exception:
                        pass
        return known_ids

    def parse_json(self, id):
        person_data = {}

        data = read_json(join(self.filtered_dir, '%s.json' % id))
        person = data['entities'][id]['labels']['en']['value']

        claims = data['entities'][id]['claims']
        for claim, values in claims.iteritems():
            claim_dict = []

            for value in values:
                try:
                    claim_dict.append(self.mapping[value['mainsnak']['datavalue']['value']['id']])
                except Exception:
                    pass
            person_data[self.mapping[claim]] = claim_dict

        with open(join(self.data_dir, 'person_data', '%s.json' % person), 'w') as f_out:
            json.dump(person_data, f_out, indent=4)
        return person, person_data

    def __check_if_id_file_exists(self, id):
        print os.path.exists(join(self.tmp_dir, '%s.json' % id))
        return os.path.exists(join(self.tmp_dir, '%s.json' % id))


def generate_ids(min=10000, max=12000):
    ids = []
    for i in xrange(min, max):
        ids.append('Q%d' % i)
    return ids


if __name__ == '__main__':
    crawler_ids = generate_ids()

    crawler = WikiDataCrawler()
    crawled_ids = crawler.crawl_ids(crawler_ids)
    ids = crawler.get_ids_for_mapping()
    crawler.get_mapping_for_known_ids(ids)
    for id in crawled_ids:
        crawler.parse_json(id)
