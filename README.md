<h1>Formatting Documents with CodeDoc</h1>
<em>documentation.txt</em>

<h2>1. Introduction</h2>
So you want to make documentations for your programs, do you? Well, you've come to the right place. *CodeDoc* allows you to create a simple text file with typical forum style formatting and convert it into a `.html` file that contains your styled documentation. In this document, we'll look at the different flags used as well as some of the underlying systems so that you can easily document your files.

<h2> 2. The Basics </h2>
<h3> 2.1. What Are Flags? </h3>
*Flags* are identifiers placed at the start of a line to tell the styler what each line is. For example, the `!t:` flag indicates that the line being processed is the title of the document. Flags follow this format: `!indentifier:`, where `identifier` is replaceable by any valid flag letter. The table below shows all the current flags that can be used:

!nt: Flags and Their Meaning
!#:
!tc: Letter
!tc: Meaning
!#:
!tr: Library Name Flag
!td: `!ln:`
!td: Declares the library name being documented. If left blank, `self` is set as the value
!#:
!tr: Title Name Flag
!td: `!t:`
!td: Creates a level 1 heading ( `<h1>` ) with any text after the `:` at the top of the page. Only reccommended to be used once
!#:
!tr: Source Flag
!td: `!s:`
!td: Stores the location of the library documented with a solid border at the bottom. Like `!t:`, only reccommended to be used once
!#:
!tr: Heading Flag
!td: `!h:`
!td: Creates a level 2 heading ( `<h2>` ) with any other text after the `:`. Unlike `!t:`, it can be used several times, with each usage creating a link in the navigation side bar
!#:
!tr: Subheading Flag
!td: `!sh:`
!td: Creates a level 3 heading ( `<h3>` ) with any other text after the `:`. Pretty much the same as `!h:` but just smaller on screen and in the nav bar
!#:
!tr: Class Flag
!td: `!c:`
!td: Creates a snippet allowing for a class to be defined and henceforth documented. _See below for more on how to use the !c flag_
!#:
!tr: Method Flag
!td: `!m:`
!td: Like the `!c:` flag, but instead of having a class defined, a method is defined
!#:
!tr: Variable Flag
!td: `!v:`
!td: Same as `!m:` but with a variable
!#:
!tr: Description Flag
!td: `!d:`
!td: Creates a description that relates to either a `!c:` flag, a `!m:` flag or a `!v:` flag.
!#:
!tr: New Table Flag
!td: `!nt:`
!td: Defines the start of a new table. Same as `<table>` tag in HTML
!#:
!tr: Table Column Flag
!td: `!tc:`
!td: Creates a table column. Same as `<th>` tag in HTML
!#:
!tr: Table Row Flag
!td: `!tr:`
!td: Creates a table row. Same as `<tr>` tag in HTML
!#:
!tr: Table Data Flag
!td: `!td:`
!td: Creates a cell in a table. Same as `<td>` tag in HTML
!#:
!tr: End Table Flag
!td: `!et:`
!td: Signifies the end of a table. Same as `</table>` tag in HTML
!#:
!tr: Long Snippet Lang Flag
!td: `!lc:`
!td: Purely for human readability of plain text / _behind the scenes_ documentation. Used to specify the language of a following long snippet. Probably should use `!#:` instead
!#:
!tr: Paragraph Flag
!td: `!p:`
!td: Like the `!d:` flag, but more general purpose and reccommended if not describing a method/variable/class
!#:
!tr: Quote Flag
!td: `!q:`
!td: Acts the same as the `<blockquote>` tag in HTML, in the way that it creates a quote looking box
!#:
!tr: Escape Text Flag
!td: `!pre:`
!td: Allows for easy and convienient use of formatting symbols _(see section 2.3)_
!tr: New List Flag
!td: `!nl:`
!td: Defines the start of a new list. Same as `<ul>` tag in HTML. _There may be support for ordered lists in the future_
!#:
!tr: List Item Flag
!td: `!li:`
!td: Equivalent of HTML's `<li>` tag. Creates a list item
!#:
!tr: End List Flag
!td: `!el:`
!td: Signifies the end of a list. Same as `</ul>` tag in HTML
!#:
!tr: Comment Flag
!td: `!#:`
!td: Allows for the creater of the documentation to leave a helpful comment without having it seen by everyone viewing the final product
!#:
!tr: Blank Line
!td: `! :`
!td: Places a blank line/ `\n` / `<br>` into the page.
!et: Flags and Their Meaning
! :
!sh: 2.2. Usage of Flags
!p: Most flags are easy to use: just state the flag then any text, like so:
! :
	!t: Title Name
	!s: Source Code Location

	!h: My Great Heading
	!sh: Hello World

	!p: Some text here
! :
!p: However, there are some flags which require special syntax, like the `!c:` flag and the `!m:` flag. Here is a full syntax list of all the flags and what they require (_note that optional parts are in [ ]'s and parts which are to be changed are in | |'s_)

!lc: CodeDoc

	!t: |Title Name|
	!s: |Source Location|

	!h: |Heading|
	!sh: |Subheading|

	!c: self.|Class Name|([parameters])
	!m: self.|Method Name|([parameters])
	!v: self.|Variable Name|

	!d: |Text here|
	!p: |Text here|
	!q: |Text here|
	!pre: |Text here|

	!nt: [Descriptive Name (not shown)]
	!tc: |Name|
	!tr: [Descriptive Name (not shown)]
	!td: |Data|
	!et: [Descriptive Name of table being closed (not shown)]

	!nl: [Descriptive Name (not shown)]
	!li: |Text|
	!el: [Descriptive Name of list being closed (not shown)]

	!#: [Comment]
	! : [Anything you want (not shown)

	!lc: |Language of Long Code Snippet|

!sh: 2.3. Text Formatting
!p: But there is more to this documentation tool than _just_ flags... there's also the feature of inline text formatting, something provided by most forums (such as _StackOverflow_ ).

!p: There are four ways to format text: using `_`(turns text into italics), `*` (turns text into bold), _`_ (turns text into inline `code` snippets) and using tabs (turns code into a long snippet). *[Edit: The `~` character adds an underline to any text]*

!p: For example, given the following `CodeDoc`
! :
!lc: CodeDoc
	!p: _Hello_ there, *this text* has been `very much` formatted.
	!lc: Python
	!#: Remember, the above line is only for readability
	! :
		for i in range(10):
		    print(i)

!p: Will turn into:
!p: _Hello_ there, *this text* has been `very much` formatted.
!lc: Python (as stated in the example, but just placed here for readability)
! :
	for i in range(10):
	    print(i)

!sh: 2.4. Further Details on `!c` and `!ln`
!p: The two flags `!c` and `!ln` require some discussion, mainly because of the way they affect the `!m` and `!v` flags. In the underlying program (written in _python_ by the way) are two variables: `libname` and `classname`. At the beginning of the program, these variables are initalised like so:
!lc: Python 3.x
! :
	classname = ""
	libname = "self"

!p: It's these variables that determin what `self` is replaced with in the `!m` and `!v` tags; if `classname` is not `""`, then `self` is replaced with whatever `classname` contains. For example:
! :
!lc: CodeDoc
	!ln: mylib
	!#: ...
	!c: self.myclass(self, x, y, z)
	!#: ...
	!m: self.myfunc(a, b, c)
	!#: ...
	!h: foo bar
	!#: ...
	!m: self.yourfunc(d,e,f)


!p: Will produce:


!p: mylib. *myclass* ( _self, x, y, z_ )
!p: myclass. *myfunc* ( _a, b, c_ )
!p: *foo bar*
! : 
!p: mylib. *yourfunc* ( _d,e,f_ )
! : 
!p: Which is why it's important to understand that using `!h` resets `classname` to `""` while using `!sh` doesn't






