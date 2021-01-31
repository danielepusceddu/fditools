from sys import argv
import algorithms


helpstr = ''
if len(argv) <= 2:
    print(helpstr)

method = argv[1]
if method.startswith('base'):
    method = method.replace('base', '')
    method = method.replace('to', ' ')
    basesrc, basedest = map(int, method.split())
    n = argv[2]
    algorithms.baseconversion(basesrc, basedest, n)
elif method == 'sum':
    diff = 'diff' in argv
    algorithms.sum_dec(int(argv[2]), int(argv[3]), int(argv[4]), diff, print_procedure=True)
