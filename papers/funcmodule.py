import os
import glob
from .classmodule import Papers


def notability_export():
    path = './pdfs/*/*.pdf'
    pdfs = glob.glob(path)
    cmd = 'cp -f {} "{}"'
    papers = Papers('./data/papers.csv')._papers
    destination = "./notability/{}.pdf"

    for i in pdfs:
        dblp_id = i.split('/')[-1].split('.')[0]
        paper = papers.loc[papers['id'] == dblp_id].iloc[0]
        conf = i.split('/')[2]

        filename = paper['title']\
            .replace('/', '_')\
            .replace(' ', '_')\
            .replace('-', '_')\
            .replace('.', '')

        filename = '_'.join([
            str(paper['year']),
            conf,
            filename
        ])

        dst = destination.format(filename)
        os.system(cmd.format(i, dst))
        # print(cmd.format(i, dst))
