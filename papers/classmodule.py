import requests
import pandas as pd
from fuzzywuzzy import fuzz


class paper():
    def __init__(self, info):
        self.authors = ', '.join(info['authors']['author']) if \
            type(info['authors']) is dict else info['authors']
        self.doi = info.get('doi', '')
        self.title = info['title']
        self.venue = info['venue']
        self.year = info['year']
        self.dblp = info['dblp'] if 'dblp' in info.keys() else info['url']
        self.url = info['url'] if 'dblp' in info.keys() else info['ee']

    def __repr__(self):
        x = "\n   title: {}\
             \n authors: {}\
             \n   venue: {} {}\
             \n     doi: {}\
             \n     url: {}\
             \n    dblp: {}\n"\
            .format(
            self.title,
            self.authors,
            self.year,
            self.venue,
            self.doi,
            self.url,
            self.dblp,
        )
        return x


class dblp():
    """
    q	The query string to search for, as described on a separate page.		...?q=test+search
    format	The result format of the search. Recognized values are "xml", "json", and "jsonp".	xml	...?q=test&format=json
    h	Maximum number of search results (hits) to return. For bandwidth reasons, this number is capped at 1000.	30	...?q=test&h=100
    f	The first hit in the numbered sequence of search results (starting with 0) to return. In combination with the h parameter, this parameter can be used for pagination of search results.	0	...?q=test&h=100&f=300
    c	Maximum number of completion terms (see below) to return. For bandwidth reasons, this number is capped at 1000.	10	...?q=test&c=0
    """

    def __init__(self):
        pass

    def dblpapi(self, type):
        DBLP_API = {
            'publ': 'http://dblp.org/search/publ/api',
            'author': 'http://dblp.org/search/author/api',
            'venue': 'http://dblp.org/search/venue/api',
        }
        return DBLP_API[type]

    def make_params(self, params={}):
        params['q'] = params.get('q')
        params['format'] = 'json'
        params['h'] = params.get('h', 5)
        params['f'] = params.get('f', 0)
        params['c'] = params.get('c', 100)
        return params

    def search(self, type, params):
        response = requests.get(
            self.dblpapi(type),
            params=params
        )
        try:
            assert response.ok
        except AssertionError as e:
            print("###\n{}\n{}\n".format(response.request.url, response.json()))

        hits = response.json()['result']['hits']
        for hit in hits['hit']:
            yield paper(hit['info'])

    def get_publ(self, title):
        """
        search publications: title
        """
        params = self.make_params({
            'q': title
        })
        return self.search('publ', params)

    def get_author(self, name):
        """
        search author: author name
        """
        params = self.make_params({
            'q': name
        })
        return self.search('author', params)

    def get_venue(self, venue):
        """
        search venue
        """
        params = self.make_params({
            'q': venue
        })
        return self.search('venue', params)


class Papers():
    def __init__(self, f):
        self._file = open(f, 'a+')
        self._papers = pd.read_csv(f, '\t')

    def papers(self):
        for index, row in self._papers.iterrows():
            yield paper(row.to_dict())

    def print_papers(self):
        for paper in self.papers():
            print(paper)

    def paper_exists(self, p):
        exist = False
        for paper in self.papers():
            if fuzz.ratio(p, paper.title) > 80:
                exist = True
                print(paper)
        return exist

    def update_papers(self, np, yes):
        with open(np, 'r+') as new_papers:
            papers = new_papers.readlines()
            db = dblp()

            for i in papers:
                print("\nChecking: {}".format(i.strip()))
                if self.paper_exists(i):
                    print("Already present")
                    continue
                else:
                    print("Searching...")
                    search_results = db.get_publ(i.strip())

                    for result in search_results:
                        print(result)
                        if not yes:
                            update = input('Add ? (y/n)')
                            if 'y' not in update.lower():
                                continue

                        # year	venue	title	authors	doi	url
                        csv_row = '{}\t{}\t{}\t{}\t{}\t{}\t{}'
                        print(csv_row.format(
                            result.year,
                            result.venue,
                            result.title,
                            result.authors,
                            result.doi,
                            result.url,
                            result.dblp,
                        ), file=self._file)
                        self._file.flush()
                        break

            print('Saved')

    def write_to_readme(self, readme):
        self._papers.sort_values(['year', 'venue'], ascending=[True, True], inplace=True)

        readme_header = """
# Linux Security Papers

NOTE: Do **NOT** edit this file manually.


## List of papers
"""

        readme_table = """
year | venue | title | authors | doi | url | dblp
-----|-------|-------|---------|-----|-----|-----"""

        table_row = '{} | {} | {} | {} | {} | {} | {}'


        with open(readme, 'w') as r:
            print(readme_header, file=r)
            print(readme_table, file=r)
            for p in self.papers():
                print(table_row.format(
                    p.year,
                    p.venue,
                    p.title,
                    p.authors,
                    p.doi,
                    p.url,
                    p.dblp,
                ), file=r)
