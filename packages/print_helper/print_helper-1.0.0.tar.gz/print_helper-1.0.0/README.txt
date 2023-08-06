Print Helper
============

This project write some useful functions related to print:

::

    p, pp, pl, ppl, length, size,
    p_format, pp_format, pl_format, ppl_format.

github: https://github.com/jichen3000/py_print_helper

pypi: https://pypi.python.org/pypi/print_helper

--------------

Author
------

Colin Ji jichen3000@gmail.com

How to install
--------------

::

    pip install print_helper

How to use
----------

p, pp, pl, ppl, length, size, p\_format, pp\_format, pl\_format,
ppl\_format these functions could been used by any object.

p, print with title. This function will print variable name as the
title. code:

::

    import print_helper

    value = "Minitest"
    value.p()
                                    
    value.p("It is a value:")   
                                    
    value.p(auto_get_title=False)    

print result:

::

    value : 'Minitest'

    It is a value: 'Minitest'

    'Minitest'

pp, pretty print with title. This function will print variable name as
the title in the first line, then pretty print the content of variable
below the title. code:

::

    import print_helper

    value = "Minitest"
    value.pp()
                                    
    value.pp("It is a value:")   
                                    
    value.pp(auto_get_title=False)    

print result:

::

    value :
    'Minitest'

     It is a value:
    'Minitest'

    'Minitest'

pl, print with title and code loction. This function just like pt, but
will print the code location at the first line. And some editors support
to go to the line of that file, such as Sublime2. code:

::

    import print_helper

    value = "Minitest"
    value.pl()
                                    
    value.pl("It is a value:")   
                                    
    value.pl(auto_get_title=False)    

print result:

::

        File "/Users/Colin/work/minitest/test.py", line 76
    value : 'Minitest'


        File "/Users/Colin/work/minitest/test.py", line 77
     It is a value: 'Minitest'


        File "/Users/Colin/work/minitest/test.py", line 78
    'Minitest'

ppl, pretty print with title and code loction. This function just like
ppt, but will print the code location at the first line. Notice: it will
print a null line firstly. code:

::

    import print_helper

    value = "Minitest"
    value.ppl()
                                    
    value.ppl("It is a value:")   
                                    
    value.ppl(auto_get_title=False)    

print result:

::

        File "/Users/Colin/work/minitest/test.py", line 76
    value :
    'Minitest'


        File "/Users/Colin/work/minitest/test.py", line 77
     It is a value:
    'Minitest'


        File "/Users/Colin/work/minitest/test.py", line 78
    'Minitest'

p\_format, get the string just like p function prints. I use it in
debugging with log, like: logging.debug(value.p\_format()) code:

::

    import print_helper

    value = "Minitest"
    value.p_format()

return result:

::

    value : 'Minitest'

pp\_format, get the string just like pp function prints. I use it in
debugging with log, like: logging.debug(value.pp\_format()) code:

::

    import print_helper

    value = "Minitest"
    value.pp_format()

return result:

::

    value :\n'Minitest'

pl\_format, get the string just like pl function prints. I use it in
debugging with log, like: logging.debug(value.pl\_format()) code:

::

    import print_helper

    value = "Minitest"
    value.pl_format()

return result:

::

    line info: File "/Users/Colin/work/minitest/test.py", line 76, in <module>\nvalue : 'Minitest'

ppl\_format, get the string just like ppl function prints. I use it in
debugging with log, like: logging.debug(value.ppl\_format()) code:

::

    import print_helper

    value = "Minitest"
    value.ppl_format()

return result:

::

    line info: File "/Users/Colin/work/minitest/test.py", line 76, in <module>\nvalue :\n'Minitest'

length and size will invoke len function for the caller's object. code:

::

    [1,2].length()                  # 2, just like len([1,2])
    (1,2).size()                    # 2, just like len((1,2))
