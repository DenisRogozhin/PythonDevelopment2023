from cowsay import cowsay, list_cows, make_bubble, cowthink, COW_PEN, THOUGHT_OPTIONS
import cmd
import shlex
import pyreadline3


class CowsayShell(cmd.Cmd):
    intro = 'Welcome to the Cowsay shell!! Moooouu....'
    prompt = 'cowsay: '
    
    def do_list_cows(self, arg):
        """
        list all cowfiles on the current COWPATH
        list_cows [cow_path]
        cow_path: path to cow files
        """
        arg = shlex.split(arg)
        if arg:
            cow_path = arg[0]
        else:
            cow_path = COW_PEN
        print(list_cows(cow_path))
        
    def do_cowsay(self, arg):       
        """
        print cow saying something
        cowsay message [cow] [eyes] [tongue]
        message: words said by cow
        cow: the available cows; can be found by calling list_cows : default is 'default'
        eyes: eye_string : default is 'OO'
        tongue: tongue_string: default is '__'
        """
        msg, *params = shlex.split(arg)
        if len(params) == 3:
            cow, eyes, tongue = params
        elif len(params) == 2:
            cow, eyes = params
            tongue = '__'
        else:
            eyes = 'OO'
            tongue = '__'
            if len(params) == 1:
                cow = params[0]
            else:
                cow = 'default'
        print(cowsay(msg, cow = cow, eyes = eyes, tongue = tongue))
        
    def complete_cowsay(self, pfx, line, begin, end):
        parsed_string = shlex.split(line)
        if len(parsed_string) > 2:
            complete = dict()
            complete[0] = list_cows()
            complete[1] = ["oo", "XX", "00", "ee", "**", "OO", "DD", ".."]
            complete[2] = ["||", "U", "W", "V", "J", "L"]
            if begin != end:
                idx = len(parsed_string) - 3
            else:
                idx = len(parsed_string) - 2
            return [s for s in complete[idx] if s.startswith(pfx)]
        elif len(parsed_string) == 2 and (line.endswith(' ') or line.endswith('\t')):
            return list_cows()
        else:
            return []

        
    def do_make_bubble(self, arg):
        """
        print bubble with written message
        make_bubble [width] [wrap_text]
        brackets : type of bubble - cowsay or cowthink: default is cowsay 
        width: width of bubble: default is 40        
        wrap_text: whether to wrap the text: default is True
        """
        msg, *params = shlex.split(arg)
        if len(params) == 3:
            brackets, width, wrap_text = params
            wrap_text = wrap_text == 'True'
        elif len(params) == 2:
            brackets, width = params
            wrap_text = True
        else:
            width = 40
            wrap_text = True
            if len(params) == 1:
                brackets = params[0]
            else:
                brackets = 'cowsay'
        print(make_bubble(msg, brackets = THOUGHT_OPTIONS[brackets], width = int(width), wrap_text = wrap_text))
        
    def complete_make_bubble(self, pfx, line, begin, end):
        parsed_string = shlex.split(line)
        if len(parsed_string) > 2:
            complete = dict()
            complete[0] = ["cowsay", "cowthink"]
            complete[1] = [str(i) for i in range(10, 100)]
            complete[2] = ["True", "False"]
            if begin != end:
                idx = len(parsed_string) - 3
            else:
                idx = len(parsed_string) - 2
            return [s for s in complete[idx] if s.startswith(pfx)]
        elif len(parsed_string) == 2 and (line.endswith(' ') or line.endswith('\t')):
            return ["cowsay", "cowthink"]
        else:
            return []    
        
        
    def do_cowthink(self, arg):
        """
        print cow thinking about something
        cowthink message [cow] [eyes] [tongue]
        message: words said by cow
        cow: the available cows; can be found by calling list_cows
        eyes: eye_string
        tongue: tongue_string
        """
        msg, *params = shlex.split(arg)
        if len(params) == 3:
            cow, eyes, tongue = params
        elif len(params) == 2:
            cow, eyes = params
            tongue = '__'
        else:
            eyes = 'OO'
            tongue = '__'
            if len(params) == 1:
                cow = params[0]
            else:
                cow = 'default'
        print(cowthink(msg, cow = cow, eyes = eyes, tongue = tongue))
        
    def complete_cowthink(self, pfx, line, begin, end):
        parsed_string = shlex.split(line)
        if len(parsed_string) > 2:
            complete = dict()
            complete[0] = list_cows()
            complete[1] = ["oo", "XX", "00", "ee", "**", "OO", "DD", ".."]
            complete[2] = ["||", "U", "W", "V", "J", "L"]
            if begin != end:
                idx = len(parsed_string) - 3
            else:
                idx = len(parsed_string) - 2
            return [s for s in complete[idx] if s.startswith(pfx)]
        elif len(parsed_string) == 2 and (line.endswith(' ') or line.endswith('\t')):
            return list_cows()
        else:
            return []
        
    def do_exit(self, arg):
        'Exit from cow shell'
        return 100500
        
if __name__ == '__main__':
    CowsayShell().cmdloop()
