import argparse
from .classmodule import Papers


new_papers = './newpapers.txt'
papers_csv = './data/papers.csv'
readme = './readme.md'

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--exists', help='check if a paper is already included')
parser.add_argument('-l', '--list', action='store_true',
                    help='list all papers')
parser.add_argument('-r', '--readme', action='store_true',
                    help='update the readme')
parser.add_argument('-u', '--update', action='store_true',
                    help='update list of papers')
parser.add_argument('-y', action='store_true',
                    help='doesnt ask for confirmation while updating')
args = parser.parse_args()


def main():

    papers = Papers(papers_csv)

    if args.exists:
        print(papers.paper_exists(args.exists))

    if args.list:
        papers.list_papers()

    if args.update:
        papers.update_papers(new_papers, args.y)

    if args.readme:
        papers.write_to_readme(readme)


if __name__ == '__main__':
    main()
