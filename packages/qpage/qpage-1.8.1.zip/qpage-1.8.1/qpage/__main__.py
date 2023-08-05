from .qpage import *
import sys

try:
    response = create_folder()
    print("QPAGE By S.Haghighi & M.M.Rahimi")
    print("Version : " + version)
    if response:
        print(
            "At least one of the folders create for the first time ,\n"
            " please put your data in proper order and run program again")
        sys.exit()
    clear_folder(out_dir)  # clear all of files in output directory
    page_name_update()  # update page names
    for i in actual_name:
        html_init(i)  # create pages html files
    menu_writer()  # write menu for each html file

    for i in actual_name:
        contain(i)  # write contains of each page
        html_end(i)  # end tags of each page
    css_creator()  # create css file
    close_files()
    print("Homepage is ready")
    print("Upload output folder contains directly to your host")
    print("Please Don't Change HTML Files Name")
    print_warning()
    browse = int(input("Preview Homepage?[1] or Not[2]"))
    if browse == 1:
        preview()
        close_files()

except FileNotFoundError:  # error exception in FileNotFound ( When Something Missed)
    close_files()
    vector_2 = error_finder()
    error_vector = vector_2[0]
    pass_vector = vector_2[1]
    print(str(len(error_vector)) + " Error")
    print("Please Check Following :\n")
    for i in range(len(error_vector)):
        print(str(i + 1) + "-" + error_vector[i])
    for i in range(len(pass_vector)):
        print(str(i + len(error_vector) + 1) + "-" + pass_vector[i])
    input("")
except ValueError:
    print("Bad Input")
    input("")
