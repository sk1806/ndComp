import os
import ROOT
import fileTools


#def search_for_file(directory, contain, notcontain):
#    """
#    Searches for files in a given directory.
#    Allows you to specify a string or list of strings that the filename must contain.
#    Allows you to specify a string or list of strings that the filename must not contain.
#    Returns the files as a list.
#    """
#
#    #If the user specifies single strings, we put it into a list
#    if isinstance(contain, str):
#        contain = [contain]
#    if isinstance(notcontain, str):
#        notcontain = [notcontain]
#
#    found_files = []
#
#    # Iterate over files in the specified directory
#    for root, dirs, files in os.walk(directory):
#        for file in files:
#            file_path = os.path.join(root, file)
#            print(file_path)
#            # Check if the file name satisfies the conditions
#            if all(substring in file for substring in contain) and all(substring not in file for substring in notcontain):
#                found_files.append(file_path)
#
#    print found_files
#    return found_files



def check_tree_existence(file_name, tree_name, silentFound = False):

    root_file = ROOT.TFile.Open(file_name)

    if not root_file or root_file.IsZombie():
        print("Error opening file: "+ file_name)
        return False

    tree = root_file.Get(tree_name)
    if not tree:
        print("Tree " + tree_name + "  not found in file: " + file_name)
        return False

    if not silentFound:
      print("Tree "+ tree_name + " found in file" + file_name)

    root_file.Close()
    return True



def check_tree_existence_list(file_names, tree_name, silentFound = False):

    # If a single filename is provided, convert it to a list
    if isinstance(file_names, str):
        file_names = [file_names]

    f_out = open('dodgy_files.list', 'w')

    for file_name in file_names:
        tree = check_tree_existence(file_name, tree_name, silentFound = False)
        if not tree:
            f_out.write(file_name + '\n')

    f_out.close()





files = fileTools.search_for_file("./test", ["90317001-0028_bgb6", ".dat"], "elmc")
pyrootTools.check_tree_existence_list(files, "nRooTracker", "True")

files = fileTools.search_for_file("./", ["_numc_", ".root"])
pyrootTools.check_tree_existence_list(files, "nRooTracker", "True")

