"""这是《Head First Python》一书的示例代码"""
import sys
def print_lol(the_list, level = 0, indent = False, fh=sys.stdout):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1, indent, fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end="", file=fh)
            print(each_item, file=fh)
