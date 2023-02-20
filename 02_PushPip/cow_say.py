from cowsay import cowsay, list_cows

import argparse

parser = argparse.ArgumentParser(
                    prog = 'cowsay',
                    description = 'Drawing cow and it`s words')

parser.add_argument('msg', nargs='?') 
parser.add_argument('-e', '--eyes', help = 'select the appearance of the cows eyes', default = 'OO', type = str)
parser.add_argument('-l', '--list', help = 'list all cowfiles on the current COWPATH', action = 'store_true')
parser.add_argument('-T', '--tongue', help = 'select the appearance of the cows tongue', default = '  ', type = str)
parser.add_argument('-n', '--wrapped', help = 'message will be word-wrapped', action = 'store_false')
parser.add_argument('-W', '--width', help = 'specifies roughly (where the message should be wrapped', default = 40, type = int)
parser.add_argument('-f', '--cowfile', help = 'specifies a particular cow picture file to use', default = "" , type = str)
parser.add_argument('-b', dest = 'apearence', help = 'initiates Borg mode', action = 'append_const', const = 'b')
parser.add_argument('-g', dest = 'apearence', help = 'invokes greedy mode', action = 'append_const', const = 'g')
parser.add_argument('-d', dest = 'apearence', help = 'causes the cow to appear dead', action = 'append_const', const = 'd')
parser.add_argument('-p', dest = 'apearence', help = 'causes a state of paranoia to come over the cow', action = 'append_const', const = 'p')
parser.add_argument('-s', dest = 'apearence', help = 'makes the cow appear thoroughly stoned', action = 'append_const', const = 's')
parser.add_argument('-t', dest = 'apearence', help = 'yields a tired cow', action = 'append_const', const = 't')
parser.add_argument('-w', dest = 'apearence', help = 'initiates wired mode', action = 'append_const', const = 'w')
parser.add_argument('-y', dest = 'apearence', help = 'brings on the cows youthful appearance', action = 'append_const', const = 'y')


args = parser.parse_args()
if args.list:
    print(list_cows())
else:
    if '/' in args.cowfile:  
        cowfile_path = args.cowfile
        cow = 'default'
    else:
        cowfile_path = None
        if args.cowfile in list_cows():
            cow = args.cowfile
        else:
            cow = 'default'
    print(cowsay(message = args.msg, eyes = args.eyes[:2], tongue = args.tongue[:2], width = args.width, wrap_text = args.wrapped,
                cowfile = cowfile_path, cow = cow, preset = max(args.apearence)))