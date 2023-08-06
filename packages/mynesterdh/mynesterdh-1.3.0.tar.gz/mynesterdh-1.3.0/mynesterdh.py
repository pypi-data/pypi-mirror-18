"""这是《Head First Python》一书的示例代码"""
def print_lol(the_list, level = 0, indent = False):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1, indent)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end="")
            print(each_item)
