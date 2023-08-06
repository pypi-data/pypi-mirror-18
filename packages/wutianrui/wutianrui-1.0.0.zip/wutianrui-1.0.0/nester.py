def print_lol(abc):
        for each_item in abc:
                if isinstance(each_item,list):
                        print_lol(each_item)
                else:
                        print(each_item)
