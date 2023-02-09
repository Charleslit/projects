rendering templates using jinja 2 template engine .The templates to be renderd need to be stored in a folder named templates--------
||         | |   | |   
\|         | |   | |
\|         | |   | |
\|         | |   | |
\|_____    | |   | |
|______|   | |   | |  


example of types recognized by jinja 2
<p>A value from a dictionary: {{ mydict['key'] }}.</p>
<p>A value from a list: {{ mylist[3] }}.</p>
<p>A value from a list, with a variable index: {{ mylist[myintvar] }}.</p>
<p>A value from an object's method: {{ myobj.somemethod() }}.</p>
 variable filters supported
//==================================================================================================\
||safe       ||  Renders the value without applying escaping                                         \
||capitalize ||  Converts the first character of the value to uppercase and the rest to lowercase     \
||lower      ||  Converts the value to lowercase characters                                            |
||upper      ||  Converts the value to uppercase characters                                            |
||title      ||  Capitalizes each word in the value                                                    |
||trim       ||  Removes leading and trailing whitespace from the value                                /
||striptags  ||  Removes any HTML tags from the value before rendering                                /
=====================================================================================================/