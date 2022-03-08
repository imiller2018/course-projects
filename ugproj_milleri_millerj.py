# UNDERGRADUATE PROJECT CODE -- PART 1 (Tree Construction + Inferencing)
# Submission by: Isaac Miller, Jacob Miller
# 

import csv
import math

# filename of training data
LOCAL_TABLE_FILENAME = "dining.tsv"
# filename of data to make an inference on
LOCAL_INFERENCE_FILENAME = "dining_inference.tsv"


# directed rooted tree data structure
class TreeNode:
    def __init__(self, data):
        # text to be displayed when node is printed
        self.data = data
        # if a node asks a query, this is its respective column number
        # to look for a value in. will be -1 if no query is present
        self.query = None
        # a node with a query will have children with different 'categories'
        # these correspond with different 'choices' to make in the
        # decision tree. will be 'None' if not linked with a query (i.e. root)
        self.category = None
        # a leaf node will have a 'result', such as true or false (represented
        # using a float between 0 (false) and 1 (true).
        self.result = None
        # list of references to child TreeNode objects
        self.children = []
        # reference to parent node, if one exists
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def print_tree(self):
        if self.children:
            # print current node data
            print("node: "+str(self.data)+"; column="+str(self.query)+", category="+str(self.category)+", result="+str(self.result))
            # print out all children...
            for child in self.children:
                print("\tchild: "+str(child.data))
                print("\t\tcolumn="+str(child.query)+", category="+str(child.category)+", result="+str(child.result))
            # ...only then recurse through the children
            for child in self.children:
                child.print_tree()

def get_info(t_before_split, f_before_split, t_after_split, f_after_split):

    if(t_after_split == 0):
        #ignore
        log_val_1 = 0
    else:
        log_val_1 = (-((t_after_split)/(t_after_split + f_after_split))
                    * math.log(((t_after_split)/(t_after_split + f_after_split)), 2))

    if(f_after_split == 0):
        #ignore
        log_val_2 = 0
    
    else:
        log_val_2 = (-((f_after_split)/(t_after_split + f_after_split))
                    * math.log(((f_after_split)/(t_after_split + f_after_split)), 2))
                
    total_log_val = log_val_1 + log_val_2

    number_we_want = ((t_after_split + f_after_split)/(t_before_split + f_before_split)) * total_log_val
    # print(number_we_want)
    return number_we_want

def ChooseAttribute(training_data, column_numbers, t_beforesplit, f_beforesplit):
    # cycle through each column of data in the database
    # (accounts for the first column being row numbers and
    # the last column being our target value, excluding these
    best_value = 1.0
    best_column = -1    
    
    for column in range(1, len(training_data[0][1:])):
        # get the categories
        categories = []
        category_info = 0.0
        for row in training_data[1:]:
            categories.append(row[column])
        categories = set(categories)
        # yeah we got our categories babey
        # print(categories)

        # next...............
        
        for cat in categories:
            t_aftersplit = 0
            f_aftersplit = 0
            for row in training_data[1:]:
                if row[column] == cat:
                    # NOTE TO SELF FUCKING CHANGE THIS T AND F TO 0 AND 1
                    # BEFORE WE SUMBIT THIS I GUESS!!!!!!!!!!!!!!!!!!!!!
                    if row[len(row)-1] == 'T':
                        t_aftersplit += 1
                    elif row[len(row)-1] == 'F':
                        f_aftersplit += 1

            # *do math shit with true_count and false_count*
            information = get_info(t_beforesplit, f_beforesplit, t_aftersplit, f_aftersplit)
            # sum up category info
            category_info += information

        if category_info < best_value:
            best_value = category_info
            best_column = column

    
    # return best info value + index of corresponding column 
    return [best_value, best_column]                   
                        


def BuildingTheTree(training_data, column_numbers, default_value):
    true_count = 0
    false_count = 0
    
    for row in training_data[1:]:
        if row[len(row)-1] == 'T':
            true_count += 1
        else:
            false_count += 1
    
    if not training_data:
        leaf_node = TreeNode(default_value)
        leaf_node.result = default_value
        return leaf_node
    if false_count == 0:
        leaf_node = TreeNode(True)
        leaf_node.result = 1.0
        return leaf_node
    if true_count == 0:
        leaf_node = TreeNode(False)
        leaf_node.result = 0.0
        return leaf_node
    result_average = true_count / (true_count + false_count)
    if not column_numbers:
        leaf_node = TreeNode(result_average)
        leaf_node.result = result_average
        return leaf_node


    else:
        best_attribute = ChooseAttribute(training_data, column_numbers, true_count, false_count)
        tree = TreeNode(training_data[0][best_attribute[1]])
        tree.data = tree.data + "?"
        tree.query = best_attribute[1]
        # get the categories
        categories = []
        for row in training_data[1:]:
            categories.append(row[best_attribute[1]])
        categories = set(categories)
        # iterate through categories
        for cat in categories:
            # get list of data that matches category
            data_split = []
            data_split.append(training_data[0])
            for row in training_data[1:]:
                if row[best_attribute[1]] == cat:
                    data_split.append(row)
            # make a subtree
            sub_attributes = column_numbers.copy()
            sub_attributes.remove(best_attribute[1])
            subtree = BuildingTheTree(data_split, sub_attributes, result_average)
            subtree.data = str(cat)+" --> "+str(subtree.data)
            subtree.category = str(cat)
            tree.add_child(subtree)

        return tree
        
        
def DoTheInference(inference_data, current_node):
    if current_node.result:
        return current_node.result
    else:
        for child in current_node.children:
            if inference_data[current_node.query] == child.category:
                return DoTheInference(inference_data, child)






def main():
    # read input .tsv file, store in input_table
    # (assuming row 0 holds the titles of each column)
    input_table = []
    with open(LOCAL_TABLE_FILENAME) as file:
        data = csv.reader(file, delimiter="\t")
        for row in data:
            input_table.append(row)

    # calculate column numbers of source table
    attributes_numbers = []
    for i in range(1, len(input_table[0][1:])):
        attributes_numbers.append(i)



    decision_tree = BuildingTheTree(input_table, attributes_numbers, 0.5)
    decision_tree.print_tree()

    inference_list = ""
    with open(LOCAL_INFERENCE_FILENAME) as file2:
        data = csv.reader(file2, delimiter="\t")
        for row in data:
            inference_list = row

    print(inference_list)

    print(DoTheInference(inference_list, decision_tree))


    return

main()
