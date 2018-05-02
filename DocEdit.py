#CD Edit


#####################
#[-][<>][X]   CDEdit#
#-------------------#
#B I U {} "" @ i [S]#
#-------------------#
#|!ln: Lib Name    |#
#|!t: Some Title   |#
#|!s: ...          |#
#|                 |#
#|                 |#
#|!h: A Heading    |#
#|!p: Some text    |#
#|                 |#
#-------------------#
#[filename][x words]#
#[last saved: HH:MM]#
#                   #
#[Open File]        #
#####################


import tkinter, time, screens, re
from tkinter import font
import tkinter.filedialog as tfile
import Documentationizer

file_name = "File Name: New File"
word_count = "Words: 0"
last_save = "Last Saved: Never"
have_saved = "No unsaved changes"
save_contents = ""
location = ""
in_pre = False


formatted_pattern = re.compile("(\*|\`|\_|\~)([^\n]*?)(\\1)")


window = tkinter.Tk()
win_width = window.winfo_reqwidth()
win_height = window.winfo_reqheight()

window.minsize(width=1300, height=690)
editor = tkinter.Text()
file_display = tkinter.Label(window, text=file_name)
count_display = tkinter.Label(window, text=word_count)
save_display = tkinter.Label(window, text=last_save)
changes_display = tkinter.Label(window, text=have_saved)


bold_text = font.Font(family="Helvetica", size=12, weight=font.BOLD)
normal_text = font.Font(family="Helvetica", size=12)
code_text = font.Font(family="Courier", size=12)
italic_text = font.Font(family="Helvetica", size=12, slant=font.ITALIC)
underline_text = font.Font(family="Helvetica", size=12, underline=1)
long_code = font.Font(family="Courier", size=12)
link_text = font.Font(family="Helvetica", size=12, underline=1)

def bold():
    ranges = editor.tag_ranges("sel")
    editor.replace(ranges[0], ranges[1],
                   editor.get(ranges[0], ranges[1]).replace(\
        editor.selection_get(), "*" + editor.selection_get() + "*"))

    hlight()

def italics():
    ranges = editor.tag_ranges("sel")
    editor.replace(ranges[0], ranges[1],
                   editor.get(ranges[0], ranges[1]).replace(\
        editor.selection_get(), "_" + editor.selection_get() + "_"))
    hlight()

def underline():
    ranges = editor.tag_ranges("sel")
    editor.replace(ranges[0], ranges[1],
                   editor.get(ranges[0], ranges[1]).replace(\
        editor.selection_get(), "~" + editor.selection_get() + "~"))

    hlight()


def snippet():
    ranges = editor.tag_ranges("sel")
    if editor.get(ranges[0], ranges[1]).count("\n"):
        for line in range(int(str(ranges[0])[:str(ranges[0]).find(".")]),
                          int(str(ranges[1])[:str(ranges[1]).find(".")]) + 1):
            
            editor.insert("{0}.0".format(line), "\t")

        editor.selection_clear()
        hlight()
        return
    editor.replace(ranges[0], ranges[1],
                   editor.get(ranges[0], ranges[1]).replace(\
        editor.selection_get(), "`" + editor.selection_get() + "`"))

    hlight()


def quote():
    ranges = editor.tag_ranges("sel")
    editor.replace(ranges[0], ranges[1],
                   "!q:" + editor.get(ranges[0], ranges[1]))

    hlight()


def link():
    if popup.hidden:
        main.hide()
        popup.show()
         
def image():
    pass

def save():
    global file_name, last_save, location, save_contents, have_saved
    if file_name == "File Name: New File":
        location = tfile.asksaveasfilename()
        if location == "":
            return
        location += ".txt"
        temp = open(location, "w", encoding="utf-8")
        temp.write(editor.get("0.0", tkinter.END))
        temp.close()

        Documentationizer.main(location)

        file_name = "File Name: " + location
        now = time.localtime()
        last_save = "Last Saved : {0}/{1}/{2} {3}:{4}:{5}"\
                    .format(now.tm_mday, now.tm_mon, now.tm_year,
                            now.tm_hour, now.tm_min, now.tm_sec)

        save_contents = editor.get("0.0", tkinter.END)

    else:
        temp = open(location, "w", encoding="utf-8")
        temp.write(editor.get("0.0", tkinter.END))
        temp.close()

        Documentationizer.main(location)

        now = time.localtime()
        last_save = "Last Saved : {0}/{1}/{2} {3}:{4}:{5}"\
                    .format(now.tm_mday, now.tm_mon, now.tm_year,
                            now.tm_hour, now.tm_min, now.tm_sec)

        save_contents = editor.get("0.0", tkinter.END)
                   
    have_saved = "No unsaved changes"
    update_labels()

def update_labels():
    file_display.config(text=file_name)
    count_display.config(text=word_count)
    save_display.config(text=last_save)
    changes_display.config(text=have_saved)

def Open():
    global file_name, last_save, location, save_contents
    file = tfile.askopenfilename()
    if file == "":
        return

    contents = open(file, "r", encoding="utf-8")
    editor.delete("0.0", tkinter.END)
    save_contents = contents.read()
    editor.insert("0.0", save_contents)
    
    contents.close()

    location = file
    file_name = "File Name: " + file
    last_save = "Last Saved: Never"
    update_labels()
    hlight()


def New():
    save()
    global file_name, last_save, word_count, have_saved
    global location, save_contents
    file_name = "File Name: New File"
    word_count = "Words: 0"
    last_save = "Last Saved: Never"
    have_saved = "No unsaved changes"
    save_contents = ""
    location = ""

    editor.delete("0.0", tkinter.END)
    update_labels()
    

def highlight(event):
    global word_count, in_pre, have_saved
    contents = editor.get("0.0", tkinter.END)
    word_count = "Words: {0}".format(len(contents.split()))

    if contents != save_contents:
        have_saved = "You have unsaved changes"
    
    update_labels()

    last = 0
    matches = list()

    editor.tag_add("nt", "0.0", tkinter.END)
    
    while last <= len(contents):
        match = formatted_pattern.search(contents, last)
        if match is None:
            break

        first, last = match.span()
        if first == last:
            last = first + 1

        matches.append(match)

    editor.tag_remove("it", "0.0", tkinter.END)
    editor.tag_remove("ut", "0.0", tkinter.END)
    editor.tag_remove("bt", "0.0", tkinter.END)
    editor.tag_remove("ct", "0.0", tkinter.END)

    for match in reversed(matches):
        tag_map = {"*" : "bt", "_" : "it",
                   "~" : "ut", "`" : "ct"}

        editor.tag_add(tag_map[match.groups()[0]],
                       "0.0 + %dc" % match.start(),
                       "0.0 + %dc" % match.end())

    tab = re.compile(r"\t[^\n]*?\n") #Might as well use some more REGEX!!!

    last = 0
    matches = list()
    
    
    while last <= len(contents):
        match = tab.search(contents, last)
        if match is None:
            break

        first, last = match.span()
        if first == last:
            last = first + 1

        matches.append(match)

    editor.tag_remove("lc", "0.0", tkinter.END)
    for match in reversed(matches):
        editor.tag_add("lc",
                       "0.0 + %dc" % match.start(),
                       "0.0 + %dc" % match.end())

    hlight_flags()
    hlight_links()

    

def hlight_links():
    link_pattern = re.compile("\[([^\]]*?)\]\[([^\]]*?)\]")

    last = 0
    nmatches = 0
    matches = list()
    source = editor.get("0.0", tkinter.END)

    while last <= len(source):
        results = link_pattern.search(source, last)
        if results is None:
            break

        first, last = results.span()
        if last == first:
            last = first + 1

        nmatches += 1
        matches.append(results)

    editor.tag_remove("link", "0.0", tkinter.END)
    for _link in reversed(matches):
        editor.tag_add("link", "0.0 + {0}c".format(_link.start()),
                       "0.0 + {0}c".format(_link.end()))

       
        

            

def hlight():
    global word_count, in_pre, have_saved
    contents = editor.get("0.0", tkinter.END)
    word_count = "Words: {0}".format(len(contents.split()))

    if contents != save_contents:
        have_saved = "You have unsaved changes"
    
    update_labels()

    last = 0
    matches = list()

    editor.tag_add("nt", "0.0", tkinter.END)
    
    while last <= len(contents):
        match = formatted_pattern.search(contents, last)
        if match is None:
            break

        first, last = match.span()
        if first == last:
            last = first + 1

        matches.append(match)

    editor.tag_remove("it", "0.0", tkinter.END)
    editor.tag_remove("ut", "0.0", tkinter.END)
    editor.tag_remove("bt", "0.0", tkinter.END)
    editor.tag_remove("ct", "0.0", tkinter.END)

    for match in reversed(matches):
        tag_map = {"*" : "bt", "_" : "it",
                   "~" : "ut", "`" : "ct"}

        editor.tag_add(tag_map[match.groups()[0]],
                       "0.0 + %dc" % match.start(),
                       "0.0 + %dc" % match.end())

    tab = re.compile(r"\t[^\n]*?\n") #Might as well use some more REGEX!!!

    last = 0
    matches = list()
    
    
    while last <= len(contents):
        match = tab.search(contents, last)
        if match is None:
            break

        first, last = match.span()
        if first == last:
            last = first + 1

        matches.append(match)

    editor.tag_remove("lc", "0.0", tkinter.END)
    for match in reversed(matches):
        editor.tag_add("lc",
                       "0.0 + %dc" % match.start(),
                       "0.0 + %dc" % match.end())

    hlight_flags()
    hlight_links()
    
def split(text):
    global in_pre
    words = list()
    temp = ""
    current_symbol = ""
    do_split = True

    for letter in text:
        if letter in "_*`~":
            if current_symbol == "":
                current_symbol = letter
                do_split = False
                
                words.append(temp)
                temp = ""
                temp += letter

            elif letter == current_symbol:
                current_symbol = ""
                do_split = True

                temp += letter
                words.append(temp)
                temp = ""

            else:
                temp += letter

        else:
            if do_split and letter == "\n":
                
                words.append(temp)
                words.append(letter)
                temp = ""

            else:
                temp += letter

    if temp != "":
        words.append(temp)

    return words

def hlight_flags():
    pattern = re.compile("^!([a-z]|[#]|[ ])*:", re.MULTILINE)

    last = 0
    matches = list()

    contents = editor.get("0.0", tkinter.END)
    
    
    while last <= len(contents):
        match = pattern.search(contents, last)
        if match is None:
            break

        first, last = match.span()
        if first == last:
            last = first + 1
        matches.append(match)

    editor.tag_remove("kw", "0.0", tkinter.END)
    for match in reversed(matches):
        editor.tag_add("kw",
                       "0.0 + %dc" % match.start(),
                       "0.0 + %dc" % match.end())


def confirm_link():
    link_name = link_box.get()
    display_text = text.get()
 
    if link_name == "" or display_text == "":
        flash_red(16)

    else:
        index = editor.index(tkinter.INSERT)
        editor.insert(index, "[{0}][{1}]".format(display_text, link_name))

        popup.hide()
        main.show()


def flash_red(x):
    if x == 0:
        no_flash()
        return
    text.config(background="red")
    link_box.config(background="white")
    window.after(100, flash_white, x - 1)
    

def flash_white(x):
    if x == 0:
        no_flash()
        return

    text.config(background="white")
    link_box.config(background="red")
    window.after(100, flash_red, x - 1)

def no_flash():
    link_box.config(background="white")
    text.config(background="white")


editor.bind('<Key>', highlight)
editor.tag_config("kw", font=code_text, foreground="blue")
editor.tag_config("bt", font=bold_text)
editor.tag_config("nt", font=normal_text)
editor.tag_config("ct", font=code_text)
editor.tag_config("it", font=italic_text)
editor.tag_config("ut", font=underline_text)
editor.tag_config("lc", font=long_code, background="#eeffcc")
editor.tag_raise("kw")
editor.tag_lower("nt")
editor.tag_config("link", font=link_text, foreground="blue")


bold_button = tkinter.Button(window, text="B", command=bold, font=bold_text)
italic_button = tkinter.Button(window, text="I", command=italics,
                               font=italic_text)
underline_button = tkinter.Button(window, text="U", command=underline,
                                  font=underline_text)

code_button = tkinter.Button(window, text="{}", command=snippet, font=code_text)
quote_button = tkinter.Button(window, text="“”", command=quote,
                              font=normal_text)

link_button = tkinter.Button(window, text="@", command=link, font=normal_text)

image_button = tkinter.Button(window, text="i", command=image,
                              font=normal_text)

save_button = tkinter.Button(window, text="<", command=save,
                             font=("Wingdings", 12))

open_button = tkinter.Button(window, text="1", command=Open,
                             font=("Wingdings", 12))

new_button = tkinter.Button(window, text="2", command=New,
                            font=("Wingdings", 12))


buttons = [bold_button, italic_button, underline_button, code_button,
           quote_button, link_button, image_button, save_button, open_button,
           new_button]

button_x, button_y = 400, 5

main = screens.ScreenXY("DocEdit", window)

for button in buttons:
    button.config(width=1)
    button.config(height=1)
    button.config(relief=tkinter.FLAT)
    main.add_item(button, button_x, button_y)
    button_x += button.winfo_width() + 50



main.add_item(editor, 7, 40)
main.add_item(file_display, 75, 655)
main.add_item(count_display, 575, 655)
main.add_item(save_display, 75, 675)
main.add_item(changes_display, 575, 675)


heading = tkinter.Label(window, text="Add A Link", font=("Helvetica", 15))

text_label = tkinter.Label(window, text="Display Text: ")
text = tkinter.Entry(window, width=100)

link_label = tkinter.Label(window, text="Address: ")
link_box = tkinter.Entry(window, width=100)

submit = tkinter.Button(window, text="Submit", command=confirm_link)


popup = screens.Screen("Add A Link", window)
popup.add_item(heading, 0, 0)
popup.add_item(text_label, 1, 0)
popup.add_item(text, 1, 1)
popup.add_item(link_label, 2, 0)
popup.add_item(link_box, 2, 1)
popup.add_item(submit, 3, 1)


editor.config(width=168)
editor.config(height=38)



main.show()
window.mainloop()

