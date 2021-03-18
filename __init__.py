# Authors: Victor Camacho Artavia <joscamachoartavia@gmail.com>,
#         Jimmy Mok Zhgen <jimmymokz14@gmail.com>

import argparse
from Indexacion import Indexer

def cli():
    parser = argparse.ArgumentParser(description='Process queries given a collection',prog='Indexer', usage='%(prog)s [options]')
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('--sw', metavar='Stopwords', nargs=1,
                        help='stopwords file', required=True)
    required.add_argument('--c', metavar='Colection', nargs=1,
                        help='Colection file', required=True)  
    parser._action_groups.append(optional) #https://stackoverflow.com/questions/24180527/argparse-required-arguments-listed-under-optional-arguments/24181138
    return parser.parse_args()

def main():
    parsed_args = cli()
    indexer = Indexer(parsed_args.sw[0],parsed_args.c[0])
    indexer.index_colection()

if __name__ == '__main__':
    main()