import name_parser
import parserator
from imp import reload

if __name__ == '__main__':

    p = name_parser.Parser()

    parserator.training.train(p)
    
    reload(name_parser)
