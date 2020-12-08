from submit import evaluate
from helpers import get_name
import os

args = {}
args['model'] = 'elastic'
args['target'] = 'anthro_waist_cm'
args['split'] = 0

# Fixed
args['parcel'] = 'identity'
args['name'] = get_name(parcel=args['parcel'],
                        model=args['model'],
                        target=args['target'],
                        split=args['split'])
args['save_loc'] = os.path.join('results', args['name'] + '.npy')


# Run evaluate
evaluate(args=args, n_jobs=1)