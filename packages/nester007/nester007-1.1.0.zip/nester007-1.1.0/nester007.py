'''This is the "nester.py" mpdule and it provides one function called print_lol
   which prints lists that may or may not include nested lists.'''
def print_lol(the_list, level=0):
    '''This function takes one positional argument called "the list". which 
       is any python list (of-possibly nested list).Each data item in the provided list is printed
       to the screen on it's own line，the second argument is used to print tab space '''
    for each_item in the_list:
        if isinstance(each_item， list):
            print_lol(each_item, level)
        else:
            for tab_space in level:
                print('\t', end='')
            print(each_item)


