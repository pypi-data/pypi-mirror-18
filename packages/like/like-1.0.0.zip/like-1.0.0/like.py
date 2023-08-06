"""hahahaha"""
def print_lol2(the_list):
    """dasdadadada"""
    for each_item in the_list:
        if isinstance (each_item,list):
                print_lol2(each_item)
        else:
                print (each_item)
