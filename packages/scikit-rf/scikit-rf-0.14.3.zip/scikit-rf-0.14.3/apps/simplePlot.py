
import skrf as rf
from pylab import draw,show, isinteractive,ioff,figure, tight_layout
import argparse

parser = argparse.ArgumentParser(description='Plot a touchstone.')
parser.add_argument('touchstones', metavar='filename.s?p', type=str, nargs='+',
                   help='an integer for the accumulator')




if __name__  == '__main__':
    args = parser.parse_args()
    
    rf.stylely()
    ioff()
    
    for k in args.touchstones:
        print k
        ntwk = rf.Network(k)
        figure(figsize=(8,8))
        ntwk.plot_it_all()
        tight_layout()
        draw()
        show()

