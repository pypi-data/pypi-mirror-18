import os
import shutil  # Library For Work With File In High Level Like Copy
import datetime  # For Adding System Time To Homepage
import webbrowser
from .params import *
def create_folder():  # This Function Create Empty Folder At Begin
    folder_flag = 0
    list_of_folders = os.listdir(work_dir)
    if "doc" not in list_of_folders:
        os.mkdir("doc")
        file = open(os.path.join(doc_dir, "index.txt"), "w")
        file.write("This is For First Page . . .")
        file.close()
        folder_flag += 1
    if "image" not in list_of_folders:
        os.mkdir("image")
        folder_flag += 1
    if "output" not in list_of_folders:
        os.mkdir("output")
        folder_flag += 1
    if "font" not in list_of_folders:
        os.mkdir("font")
        folder_flag += 1
    if folder_flag > 0:
        return True
    else:
        return False


def page_name_update():  # This Function Update Page Names
    for i in os.listdir(doc_dir):
        if i.find(".txt") != -1 and i[:-4].upper() != "INDEX":
            actual_name.append(i[:-4])
            page_name.append(i[:-4])


def menu_maker():  # Top Menu Maker In each html page
    result = "<center>"
    for i in range(len(page_name)):
        if page_name[i] == "Home":
            targets_blank = ""
        else:
            targets_blank = 'target="blank"'
        result = result + '\t<a href="' + actual_name[i] + '.html"' + targets_blank + '>' + page_name[
            i] + "</a>\n"  # Hyper Link To Each Page In HTML File
        result += "&nbsp\n"
    result += "</center>"
    result = result + "\t\t" + break_line  # Add Break line to End Of The Menu
    return result  # Return All Of The Menu


def menu_writer():  # Write menu_maker output in html file
    message = menu_maker()
    for i in range(len(page_name)):
        file = open(os.path.join(out_dir, actual_name[i] + ".html"), "a")
        file.write(message)
        file.close()


def print_meta():
    meta_input = input("Please Enter Your Name : ")
    static_meta = '<meta name="description" content="Welcome to homepage of ' + meta_input + '"/>'
    if len(meta_input) < 4:
        warnings.append("[Warning] Your input for name is too short!!")
    return static_meta


def html_init(name):  # Create Initial Form Of each Html Page Like Title And HTML  And Body Tag
    html_name = os.path.join(out_dir, name + ".html")
    file = open(html_name, "w")
    file.write("<html>\n")
    file.write("\t<head>\n")
    if name == "index":
        file.write("\t\t<title>Welcome To My Homepage</title>\n")
    else:
        file.write("\t\t<title>" + name.upper() + "</title>\n")
    file.write('<link rel="stylesheet" href="styles.css" type="text/css"/>\n')
    css_link = 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css'
    file.write('<link rel="stylesheet" href= ' + css_link + ' type="text/style"/>\n')

    if name == 'index':  # Add meta only for index page
        file.write(print_meta())

    file.write("\t</head>\n")
    file.write('\t<body class="body_tag">\n')
    file.close()


def html_end(name):  # Create End Of The Html file
    html_name = os.path.join(out_dir, name + ".html")
    file = open(html_name, "a")
    file.write("\t</body>\n")
    file.write("</html>")
    file.close()


def close_files():
    for i in files:
        i.close()


def print_text(text_file, file, center=False, close=False):  # Write Text Part Of Each Page
    text_code = ""
    header_start = '<h4 class="color_tag">'
    header_end = "</h4>"
    space = "&nbsp\n"
    for line in text_file:
        header_start = '<h4 class="color_tag">'
        header_end = "</h4>"
        line.strip()
        text = line
        if len(line) == 1:  # For Detecting White Space
            text_code = space
        else:  # Detecting Font Size
            if line.find("[L]") != -1:
                header_start = '<h2 class="color_tag">'
                header_end = "</h2>"
                text = line[3:]
            elif line.find("[S]") != -1:
                header_start = '<h5 class="color_tag">'
                header_end = "</h5>"
                text = line[3:]
            elif line.find("[M]") != -1:
                text = line[3:]
        if center:  # Centerizes Text If Condition Is True For Manual Centering
            header_start = "<center>" + header_start
            header_end += "</center>"
        if text.find("[center]") != -1:  # Find Center Tag In Each Line
            header_start = "<center>" + header_start
            header_end += "</center>"
            text = text[:text.find("[center]")]
        text_code = header_start + text + header_end + "\n"
        file.write(text_code)
    if close:
        file.close()


def print_image(file, close=False, imformat="jpg"):  # Write Image Part OF The Page
    for i in range(len(size_box)):
        print(i, "-", size_box[i])
    image_size = int(input("Please Enter Profile Image Size : "))  # Choose Profile Image Size
    image_size_string = size_box[2]  # Getting Html String From size_box list default mode (Medium)
    if 0 <= image_size < len(size_box):
        image_size_string = size_box[image_size]
    image_code = '<center><img src="image.' + imformat + '"' + ', width=' + image_size_string + '></img></center>\n'
    file.write(image_code)
    if close:
        file.close()


def print_download(file, name, link, center=False, close=False):  # Create Download Link In Page
    link_code = "<a href=" + '"' + link + '"' + target_blank + '>' + name + "</a>"
    if center:
        link_code = "<center>" + link_code + "</center>"
    file.write(link_code + "\n")
    file.write(break_line)
    if close:
        file.close()


def print_adv(file, close=True):
    file.write(break_line)
    file.write(
        '<center><a href=' + '"' + homepage + '"' + target_blank + '>' + "Generated " + today_time + " By" + "QPage " + version + "</a> </center>")
    if close:
        file.close()


def contain(name):  # main function That Open Each Page HTML File and call other function to write data in it
    file = open(os.path.join(out_dir, name + ".html"), "a")
    text_file = open(os.path.join(doc_dir, name + ".txt"), "r")
    files.append(file)
    files.append(text_file)
    resume_name = ""
    image_name = ""
    imformat = "jpg"
    if name == "index":
        file_of_images = os.listdir(image_dir)
        for i in range(len(file_of_images)):
            for form in imformat_box:
                if file_of_images[i].find("." + form) != -1:
                    image_name = os.path.join(image_dir, file_of_images[i])
                    imformat = form
                    break
        shutil.copyfile(image_name, os.path.join(out_dir, "image." + imformat))
        print_image(file, imformat=imformat)
        print_text(text_file, file)
        print_adv(file)
    elif name == "Resume":
        file_of_docs = os.listdir(doc_dir)
        for i in range(len(file_of_docs)):
            if file_of_docs[i].find(".pdf") != -1:
                resume_name = os.path.join(doc_dir, file_of_docs[i])
                break
        shutil.copyfile(resume_name, os.path.join(out_dir, "Resume.pdf"))
        print_download(file, "Download Full Version", "Resume.pdf", center=True)
        print_text(text_file, file)
        # print_adv(file)
    else:
        print_text(text_file, file)
        # print_adv(file)


def clear_folder(path):  # This Function Get Path Of Foldr And Delte Its Contains
    if os.path.exists(path):
        list_of_files = os.listdir(path)
        for file in list_of_files:
            os.remove(os.path.join(path, file))
    else:
        os.mkdir(path)


def print_warning():
    print(str(len(warnings)) + " Warning , 0 Error")
    for i in range(len(warnings)):
        print(str(i + 1) + "-" + warnings[i])


def css_creator():  # Ask For background and text color in
    font_flag = 0  # 0 If there is no font file in font_folder
    font_section = 'font-family : Georgia , serif;\n'
    for i in range(len(color_box)):
        print(i, "-", color_box[i])
    back_color_code = int(input("Please enter your background color : "))
    if back_color_code not in range(7):
        back_color_code = 0
    text_color_code = int(input("Please enter your text color : "))
    if text_color_code not in range(7):
        text_color_code = 1
    if text_color_code == back_color_code:
        warnings.append("[Warning] Your text color and background color are same!!")
    background_color = color_box[back_color_code]  # convert code to color string in color_box
    text_color = color_box[text_color_code]  # convert code to color string in color_box
    font_folder = os.listdir(font_dir)
    for i in font_folder:
        for j in range(len(font_format)):  # search for other font format in font box
            if i.lower().find(font_format[j]) != -1:  # If there is a font in font folder
                shutil.copyfile(os.path.join(font_dir, i),
                                os.path.join(out_dir, "qpage" + font_format[j]))  # copy font file to output folder
                font_flag = 1  # Turn Flag On
                current_font_format = font_format[j]  # font format of current selected font for css editing
    css_file = open(os.path.join(out_dir, "styles.css"), "w")  # open css file
    if font_flag == 1:  # check flag if it is 1
        css_file.write(
            "@font-face{\nfont-family:qpagefont;\nsrc:url(qpage" + current_font_format + ");\n}\n")  # wrtie font-face in html
        font_section = "font-family:qpagefont;\n"  # Update Font Section For Body Tag
        for i in range(len(fontstyle_box)):
            print(i, "-", fontstyle_box[i])
        font_style = int(input(" Please choose your font style "))
        if font_style < len(fontstyle_box):
            font_style = fontstyle_box[font_style]
        else:
            font_style = "normal"
        font_section = font_section + "font-style:" + font_style + ";\n"
    css_file.write(
        ".body_tag{\n" + "background-color:" + background_color + ";\n" + font_section + css_margin + "}\n")  # write body tag
    css_file.write(".color_tag{\n" + "color:" + text_color + ";\n}")  # write color_tag in css
    css_file.close()  # close css file


def preview():
    webbrowser.open(os.path.join(out_dir, "index.html"))


def error_finder():
    error_vector = []
    pass_vector = []
    pdf_counter = 0
    image_counter = 0
    image_list = os.listdir(image_dir)
    doc_list = os.listdir(doc_dir)
    if len(image_list) == 0:
        error_vector.append("[Error] Where is your profile image file? it should be in image folder")
    else:
        for i in imformat_box:
            for j in image_list:
                if j.find(i) != -1:
                    image_counter = 1
                    break
        if image_counter == 1:
            pass_vector.append("[Pass] Your profile image in OK!!")
        else:
            error_vector.append("[Error] Your profile image is not in correct format")
    if len(doc_list) == 0:
        error_vector.append("[Error] There is no file in doc folder ( index.txt and .pdf file in necessary)")
    else:
        if "index.txt" in doc_list:
            pass_vector.append("[Pass] index.txt file OK!")
        else:
            error_vector.append("[Error] index.txt is not in doc folder!")
        for j in doc_list:
            if j.find(".pdf") != -1:
                pdf_counter = 1
                break
        if pdf_counter == 0:
            error_vector.append("[Error] Where Is Your Resume File? It should be in doc folder")
        else:
            pass_vector.append("[Pass] Your Resume File is OK!!")
    return [error_vector, pass_vector]
