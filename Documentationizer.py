import tkinter.filedialog as tfile
import os, _io
import html as HTML
from io import BytesIO
import re #as reeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
import unicodedata as unicode



class NotAFileError(Exception):
    '''
    Raised when the file provided to the main function doesn't exist or is
    invalid
    '''

    pass

def get_links(line):
    '''
    Takes: A line of text
    Does: Runs a regex on the line seeing if there are any link patterns
    Returns: The positions of any links in the text
    '''

    link_pattern = re.compile("\[([^\]]*?)\]\[([^\]]*?)\]")
                              #Looks like something that came
                              #from a ><> program           .

    matches = list()
    last = 0

    while last <= len(line):
        result = link_pattern.search(line, last)
        if result is None:
            break

        first, last = result.span()
        if last == first:
            last = first + 1

        matches.append(result)

    return matches
    
    

def html(text):
    '''
    Takes: A block of text
    Does: Turns the text into html
    Returns: The transformed text
    '''

    formatted_pattern = re.compile("(\*|\`|\_|\~)([^\n]*?)(\\1)")

    last = 0
    matches = list()

    while last <= len(text):
        match = formatted_pattern.search(text, last)
        if match is None:
            break

        first, last = match.span()
        if first == last:
            last = first + 1

        matches.append(match)

    #This is where the core service of this function works -- HTMLifying
    #words where neccessary                                            .

    for match in reversed(matches):
        tag_map = {"*" : ("<strong>", "</strong>"), "_" : ("<em>", "</em>"),
                   "~" : ("<span class='underline'>", "</span>"),
                   "`" : ("<code class='short'>", "</code>")}


        
        text = text[:match.start()] + tag_map[text[match.start()]][0] +\
               text[match.start() + 1 : match.end() - 1]+\
               tag_map[text[match.end() - 1]][1] + text[match.end():]
        
    #Now, change any character that would otherwise be lost in HTML
    #(due to how HTML shows spaces etc...), change the spaces to
    #things like &nbsp; and <br>                                  .
    text = text.replace("\n", "<br>").replace("\t", "&nbsp;" * 4)
        

    #Now, go through and linkify everything
    links = get_links(text)
    result_list = list(text)


    if len(links) == 0:
        return text


    else:
        for link in reversed(links):
            del result_list[link.start() : link.end()]
            result_list.insert(link.start(), "<a href='{0}'>{1}</a>"\
                     .format(link.groups()[1], link.groups()[0]))


        return "".join(result_list)

def prettify(code):
    '''
    Takes: A block of code
    Does: Prepares the code to be 'prettified' by the javascript file
    Returns: The transformed code
    '''

    code = HTML.escape(code.rstrip("\n"))
    code = code.replace(" ", "&nbsp;")
    code = code.replace("\n", "<br>").replace("\r", "<br>")
    return code

def main(file_path):
    output = ""
    libname = "self" #This can be changed using the !ln: flag
    classname = "" #Also, changed by !c:
    headers = list() #Used for the sidebar
    in_code = False
    h_count = 0
    long_code = ""
    tablename = ""
    in_table = False
    has_prev_row = False
    in_list = False
    file = file_path
    #First step: Write the head and start of body

    output += '''
    <!DOCTYPE html>
    <html>
        <head>
            <style>
                .main {
                    background-color: #fffff;
                    margin-left: 1em;
                    margin-right: 1em;
                    font-family: sans-serif;
                    padding-left: 20%;
                    width: 80%;
                    float: right;
                }

                .sidebar {
                    background-color: #eee;
                    font-family: sans-serif;
                    width: 15%;
                    height: 100%;
                    float: left;
                    position: fixed;
                }

                .sidebar > h3, .sidebar > h4 {
                    position: relative;
                }

                code {
                    font-family: monospace, sans-serif;
                    font-size: 96.5%;
                }

                .long {
                    border-radius: 3px;
                    border: 1px solid #ac9;
                    background: #eeffcc;
                }

                .short {
                    background-color: #eee;
                }

                h1 {
                    color: #1a1a1a;
                    margin-top: 0;
                    font-size: 200%;
                }

                .method-name {font-weight:bold; font-size:1.2em;}

                p {
                    line-height: 130%;
                    text-align: justify;
                    font-size: 1em;
                }

                .method, .variable {
                    margin-bottom: 1%:
                }

                .source {
                    border-bottom: 1px solid #ccc;
                }

                h2 {
                    font-size: 150%;
                    margin-bottom: 3%;
                }

                blockquote {
                    background-color: #efefef;
                    font-family: serif;
                    font-style: italic;
                    font-size: 1.4em;
                    border-left: 5px solid #dedede;
                }

                td {

                    border: gray 1px solid;
                    text-align: center;

                }

            </style>
            <script src="code.js"></script>
            <link href="c.css" type="text/css" rel="stylesheet">
        </head>
        <body>
            <div class='main'>
    '''

    for line in open(file, encoding="utf-8").readlines():
        #Newlines in code
        if line in ["\n", "\r"] and in_code:
            long_code += "\n"
            continue

        #End of long snippet
        if in_code and not (line.startswith("    ") or\
                            line.startswith("\t")):
            in_code = False

            output += "<code class='prettyprint'>"
            output += prettify(long_code)
            output += "</code></div><br>"

            long_code = ""
            continue

        #!ln: flag (Library Name)
        if line.startswith("!ln:"):
            libname = line[line.find("!ln:") + 4:]
            libname = libname[:-1] #Remove any space at the end

        #Check to see if this belongs with a long snippet
        elif line.startswith("    ") or line.startswith("\t"):
            if not in_code:
                in_code = True
                output += "<div class='long'>"
            
    
            long_code += line.replace("\t", "", 1)

        #!t: flag (Title)
        elif line.startswith("!t:"):
            output += line.replace("!t:", "<h1>", 1)
            output += "</h1>"

        #!s: flag (Source Code Location)
        elif line.startswith("!s:"):
            output += line.replace("!s:", "<p class='source'>"\
                                 + " Source Code: ")

            output += "</p>"

        #!h: flag (Heading)
        elif line.startswith("!h:"):
            output += html(line)\
                      .replace("!h:", "<h2 id='{0}'>".format(h_count),
                                1) #Makes the sidebar be able to jump
                                   #To the appropriate heading

            output += "</h2>"
            headers.append(line[line.find("!h:") + 4:])
            h_count += 1
            classname = ""

        #!m: flag (Method / Function)
        elif line.startswith("!m:"):
            method = line[line.find("self.") + 5 : line.find("(")]
            parameters = line[line.find("(") + 1 : line.find("(")]

            if classname == "":
                owner = libname

            else:
                owner = classname

            output += "<div class='method'><code>{0}".format("self.".replace\
                                                           ("self", owner))

            output += "<span class='method-name'>{0}</span>(<em>{1}</em>)"\
                    .format(method, parameters)

            output += "</code></div>"

        #!v: flag (Variable)
        elif line.startswith("!v:"):
            name = line[line.find("self.") + 5:]

            if classname == "":
                owner = libname

            else:
                owner = classname

            output += "<div class='variable'><code>{0}"\
                    .format("self.".replace("self", owner))

            output += "<span class='method-name'>{0}</span></code></div>"\
                    .format(name)

        #!d: flag (description of method/variable/class)
        elif line.startswith("!d:"):
            output += "<p>"+html(line[3:])+"</p>"

        #!q: flag (quote)
        elif line.startswith("!q:"):
            output += html(line).replace("!q:", "<blockquote>", 1)
            output += "</blockquote>"

        #!c: flag (Class)
        elif line.startswith("!c:"):
            method = line[line.find("self.") + 5:line.find("(")]
            parameters = line[line.find("(") + 1:line.find(")")]

            classname = method
            output += "<div class='method'><em class='class'> class </em>"
            output += "<code>{0}<span class='method-name'>{1}</span>"\
                    .format(self.replace("self", libname), method)

            output += "(<em>{0}</em>)</code></div>".format(parameters)

        #!sh: flag (Subheadings)
        elif line.startswith("!sh:"):
            output += html(line).replace("!sh:", "<h3 id='{0}'>"\
            .format(h_count), 1)
            output += "</h3>"
            headers.append({"sh" : html(line[line.find("!:sh") + 4:])})
            h_count += 1

        #!p: flag (Paragraph. Used when not describing instead of !d:
        elif line.startswith("!p:"):
            output += html(line[3:])

        #!#: flag (Comment)
        elif line.startswith("!#:"):
            pass

        #! : flag (new line)
        elif line.startswith("! :"):
            output += "<br>"

        #!lc: flag (long snippet language)
        elif line.startswith("!lc:"):
            pass

        #!nt: flag (new table)
        elif line.startswith("!nt:"):
            if not in_table:
                in_table = True
            output += "<table>"

        #!tc: flag (table column)
        elif line.startswith("!tc:"):
            if not in_table:
                print("Warning: !tc flag when there's no previous !nt flag",
                      "line = {0}".format(line))

            else:
                output += "<th>" + html(line[4:]) + "</th>"

        #!tr: flag (table row)
        elif line.startswith("!tr:"):
            if not in_table:
                print("Warning: !tr flag when there's no previous !nt flag",
                      "line = {0}".format(line))

            else:
                if has_prev_row:
                    output += "</tr>"

                output += "<tr>"
                has_prev_row = True

        #!td: flag (table data)
        elif line.startswith("!td:"):
            if not has_prev_row:
                print("Warning: !td flag when there is no previous !tr flag",
                      "line = {0}".format(line))

            else:
                output += "<td>" + html(line[4:]) + "</td>"

        #!et: flag (end table)
        elif line.startswith("!et:"):
            if not in_table:
                print("Warning: !et flag when there's no previous !nt flag",
                      "line = {0}".format(line))

            else:
                output += "</tr>"
                output += "</table>"

        #!nl: flag (new list)
        elif line.startswith("!nl:"):
            if not in_list:
                in_list = True

            output += "<ul>"


        #!li: flag (list item)
        elif line.startswith("!li:"):
            if not in_list:
                print("Warning: !li flag when there's no previous !nl flag",
                      "line = {0}".format(line))

            else:
                line = line.replace("!li:", "<li>", 1)
                line += "</li>"

                output += line

        #!el: flag (end list)
        elif line.startswith("!el:"):
            if not in_list:
                print("Warning: !el flag when there's no previous !nl flag",
                      "line = {0}".format(line))

            else:
                output += "</ul>"
                in_list = False


        #!pre: flag (pre formatted text)
        elif line.startswith("!pre:"):
            output += line.replace("!pre:", "<p>", 1)
            output += "</p>"

        #!l: flag (horizontal line)
        elif line.startswith("!l:"):
            output += "<hr>"


        else:
            output += "<p>" + html(line) + "</p>"

        output += "\n"



    output += '''
            </div>
            <div class='sidebar'>
                <h3> {0} </h3>
                <br>
            '''.format(libname)

    h_count = 0
    for header in headers:
        if type(header) != dict:
            output += '<a href="#{0}"><h4>{1}</h4></a>'.format(h_count,
                                                               header)

        else:
            output += '<a href="#{0}"><h5>{1}</h5></a>'.format(h_count,
                                                             header['sh'])

        h_count += 1

    output += "</div>"
    output += "</body>"
    path = file[:file.rfind(".")]
    try: os.mkdir(path)
    except: pass

    #Write the neccesary files (like js and css)

    js = open("scripts/code.js")
    x = open("{0}/code.js".format(path), "w")
    x.write(js.read())
    x.close(); js.close()

    css = open("scripts/c.css")
    x = open("{0}/c.css".format(path), "w")
    x.write(css.read())
    x.close(); css.close()
    
    o_file =  path + "/" + file[file.rfind("/")+1:file.rfind(".")]\
             + ".html"
    o_file = open(o_file, "w", encoding="utf-8")
    o_file.write(output)
    o_file.close()

    

#Now, onto the main show!

if __name__ == "__main__":
    #TODO: Add support for passing files as arguments in shell

    i_file = tfile.askopenfilenames() #Make it a batch convert

    for file in i_file:
        output = ""
        libname = "self" #This can be changed using the !ln: flag
        classname = "" #Also, changed by !c:
        headers = list() #Used for the sidebar
        in_code = False
        h_count = 0
        long_code = ""
        tablename = ""
        in_table = False
        has_prev_row = False
        in_list = False

        #First step: Write the head and start of body

        output += '''
        <!DOCTYPE html>
        <html>
            <head>
                <style>
                    .main {
                        background-color: #fffff;
                        margin-left: 1em;
                        margin-right: 1em;
                        font-family: sans-serif;
                        padding-left: 20%;
                        width: 80%;
                        float: right;
                    }

                    .sidebar {
                        background-color: #eee;
                        font-family: sans-serif;
                        width: 15%;
                        height: 100%;
                        float: left;
                        position: fixed;
                    }

                    .sidebar > h3, .sidebar > h4 {
                        position: relative;
                    }

                    code {
                        font-family: monospace, sans-serif;
                        font-size: 96.5%;
                    }

                    .long {
                        border-radius: 3px;
                        border: 1px solid #ac9;
                        background: #eeffcc;
                    }

                    .short {
                        background-color: #eee;
                    }

                    h1 {
                        color: #1a1a1a;
                        margin-top: 0;
                        font-size: 200%;
                    }

                    .method-name {font-weight:bold; font-size:1.2em;}

                    p {
                        line-height: 130%;
                        text-align: justify;
                        font-size: 1em;
                    }

                    .method, .variable {
                        margin-bottom: 1%:
                    }

                    .source {
                        border-bottom: 1px solid #ccc;
                    }

                    h2 {
                        font-size: 150%;
                        margin-bottom: 3%;
                    }

                    blockquote {
                        background-color: #efefef;
                        font-family: serif;
                        font-style: italic;
                        font-size: 1.4em;
                        border-left: 5px solid #dedede;
                    }

                    td {

                        border: gray 1px solid;
                        text-align: center;

                    }

                </style>
                <script src="code.js"></script>
                <link href="c.css" type="text/css" rel="stylesheet">
            </head>
            <body>
                <div class='main'>
        '''

        for line in open(file, encoding="utf-8").readlines():
            print(repr(line))
            #Newlines in code
            if line in ["\n", "\r"] and in_code:
                long_code += "\n"
                continue

            #End of long snippet
            if in_code and not (line.startswith("    ") or\
                                line.startswith("\t")):
                in_code = False

                output += "<code class='prettyprint'>"
                output += prettify(long_code)
                output += "</code></div><br>"

                long_code = ""
                continue

            #!ln: flag (Library Name)
            if line.startswith("!ln:"):
                libname = line[line.find("!ln:") + 4:]
                libname = libname[:-1] #Remove any space at the end

            #Check to see if this belongs with a long snippet
            elif line.startswith("    ") or line.startswith("\t"):
                
                if not in_code:
                    in_code = True
                    output += "<div class='long'>"
                
        
                long_code += line.replace("\t", "", 1)

            #!t: flag (Title)
            elif line.startswith("!t:"):
                output += line.replace("!t:", "<h1>", 1)
                output += "</h1>"

            #!s: flag (Source Code Location)
            elif line.startswith("!s:"):
                output += line.replace("!s:", "<p class='source'>"\
                                     + " Source Code: ")

                output += "</p>"

            #!h: flag (Heading)
            elif line.startswith("!h:"):
                output += html(line)\
                          .replace("!h:", "<h2 id='{0}'>".format(h_count),
                                    1) #Makes the sidebar be able to jump
                                       #To the appropriate heading

                output += "</h2>"
                headers.append(line[line.find("!h:") + 4:])
                h_count += 1
                classname = ""

            #!m: flag (Method / Function)
            elif line.startswith("!m:"):
                method = line[line.find("self.") + 5 : line.find("(")]
                parameters = line[line.find("(") + 1 : line.find("(")]

                if classname == "":
                    owner = libname

                else:
                    owner = classname

                output += "<div class='method'><code>{0}".format("self.".replace\
                                                               ("self", owner))

                output += "<span class='method-name'>{0}</span>(<em>{1}</em>)"\
                        .format(method, parameters)

                output += "</code></div>"

            #!v: flag (Variable)
            elif line.startswith("!v:"):
                name = line[line.find("self.") + 5:]

                if classname == "":
                    owner = libname

                else:
                    owner = classname

                output += "<div class='variable'><code>{0}"\
                        .format("self.".replace("self", owner))

                output += "<span class='method-name'>{0}</span></code></div>"\
                        .format(name)

            #!d: flag (description of method/variable/class)
            elif line.startswith("!d:"):
                output += "<p>"+html(line[3:])+"</p>"

            #!q: flag (quote)
            elif line.startswith("!q:"):
                output += html(line).replace("!q:", "<blockquote>", 1)
                output += "</blockquote>"

            #!c: flag (Class)
            elif line.startswith("!c:"):
                method = line[line.find("self.") + 5:line.find("(")]
                parameters = line[line.find("(") + 1:line.find(")")]

                classname = method
                output += "<div class='method'><em class='class'> class </em>"
                output += "<code>{0}<span class='method-name'>{1}</span>"\
                        .format(self.replace("self", libname), method)

                output += "(<em>{0}</em>)</code></div>".format(parameters)

            #!sh: flag (Subheadings)
            elif line.startswith("!sh:"):
                output += html(line).replace("!sh:", "<h3 id='{0}'>"\
                .format(h_count), 1)
                output += "</h3>"
                headers.append({"sh" : html(line[line.find("!:sh") + 4:])})
                h_count += 1

            #!p: flag (Paragraph. Used when not describing instead of !d:
            elif line.startswith("!p:"):
                output += html(line[3:])

            #!#: flag (Comment)
            elif line.startswith("!#:"):
                pass

            #! : flag (new line)
            elif line.startswith("! :"):
                output += "<br>"

            #!lc: flag (long snippet language)
            elif line.startswith("!lc:"):
                pass

            #!nt: flag (new table)
            elif line.startswith("!nt:"):
                if not in_table:
                    in_table = True
                output += "<table>"

            #!tc: flag (table column)
            elif line.startswith("!tc:"):
                if not in_table:
                    print("Warning: !tc flag when there's no previous !nt flag",
                          "line = {0}".format(line))

                else:
                    output += "<th>" + html(line[4:]) + "</th>"

            #!tr: flag (table row)
            elif line.startswith("!tr:"):
                if not in_table:
                    print("Warning: !tr flag when there's no previous !nt flag",
                          "line = {0}".format(line))

                else:
                    if has_prev_row:
                        output += "</tr>"

                    output += "<tr>"
                    has_prev_row = True

            #!td: flag (table data)
            elif line.startswith("!td:"):
                if not has_prev_row:
                    print("Warning: !td flag when there is no previous !tr flag",
                          "line = {0}".format(line))

                else:
                    output += "<td>" + html(line[4:]) + "</td>"

            #!et: flag (end table)
            elif line.startswith("!et:"):
                if not in_table:
                    print("Warning: !et flag when there's no previous !nt flag",
                          "line = {0}".format(line))

                else:
                    output += "</tr>"
                    output += "</table>"

            #!nl: flag (new list)
            elif line.startswith("!nl:"):
                if not in_list:
                    in_list = True

                output += "<ul>"


            #!li: flag (list item)
            elif line.startswith("!li:"):
                if not in_list:
                    print("Warning: !li flag when there's no previous !nl flag",
                          "line = {0}".format(line))

                else:
                    line = line.replace("!li:", "<li>", 1)
                    line += "</li>"

                    output += line

            #!el: flag (end list)
            elif line.startswith("!el:"):
                if not in_list:
                    print("Warning: !el flag when there's no previous !nl flag",
                          "line = {0}".format(line))

                else:
                    output += "</ul>"
                    in_list = False


            #!pre: flag (pre formatted text)
            elif line.startswith("!pre:"):
                output += line.replace("!pre:", "<p>", 1)
                output += "</p>"

            elif line.startswith("!l:"):
                output += "<hr>"


            else:
                output += "<p>" + html(line) + "</p>"

            output += "\n"



        output += '''
                </div>
                <div class='sidebar'>
                    <h3> {0} </h3>
                    <br>
                '''.format(libname)

        h_count = 0
        for header in headers:
            if type(header) != dict:
                output += '<a href="#{0}"><h4>{1}</h4></a>'.format(h_count,
                                                                   header)

            else:
                output += '<a href="#{0}"><h5>{1}</h5></a>'.format(h_count,
                                                                 header['sh'])

            h_count += 1

        output += "</div>"
        output += "</body>"
        path = file[:file.rfind(".")]
        try: os.mkdir(path)
        except: pass

        #Write the neccesary files (like js and css)

        js = open("scripts/code.js")
        x = open("{0}/code.js".format(path), "w")
        x.write(js.read())
        x.close(); js.close()

        css = open("scripts/c.css")
        x = open("{0}/c.css".format(path), "w")
        x.write(css.read())
        x.close(); css.close()
        
        o_file =  path + "/" + file[file.rfind("/")+1:file.rfind(".")]\
                 + ".html"
        o_file = open(o_file, "w", encoding="utf-8")
        o_file.write(output)
        o_file.close()
