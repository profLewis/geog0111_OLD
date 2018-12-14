
.. raw:: html

   <h1>

Table of Contents

.. raw:: html

   </h1>

.. container:: toc

   .. raw:: html

      <ul class="toc-item">

   .. raw:: html

      <li>

   1.2.3 help

   .. raw:: html

      </li>

   .. raw:: html

      <li>

   1.3.3 Arrays: np.array

   .. raw:: html

      </li>

   .. raw:: html

      </ul>

#1. ``help``

You can get help on an object using the ``help()`` method. This will
return a full manual page of the class documentation.

.. code:: python

    #the method help()
    help(list)


.. parsed-literal::

    Help on class list in module builtins:
    
    class list(object)
     |  list() -> new empty list
     |  list(iterable) -> new list initialized from iterable's items
     |  
     |  Methods defined here:
     |  
     |  __add__(self, value, /)
     |      Return self+value.
     |  
     |  __contains__(self, key, /)
     |      Return key in self.
     |  
     |  __delitem__(self, key, /)
     |      Delete self[key].
     |  
     |  __eq__(self, value, /)
     |      Return self==value.
     |  
     |  __ge__(self, value, /)
     |      Return self>=value.
     |  
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __gt__(self, value, /)
     |      Return self>value.
     |  
     |  __iadd__(self, value, /)
     |      Implement self+=value.
     |  
     |  __imul__(self, value, /)
     |      Implement self*=value.
     |  
     |  __init__(self, /, *args, **kwargs)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  __iter__(self, /)
     |      Implement iter(self).
     |  
     |  __le__(self, value, /)
     |      Return self<=value.
     |  
     |  __len__(self, /)
     |      Return len(self).
     |  
     |  __lt__(self, value, /)
     |      Return self<value.
     |  
     |  __mul__(self, value, /)
     |      Return self*value.
     |  
     |  __ne__(self, value, /)
     |      Return self!=value.
     |  
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  __repr__(self, /)
     |      Return repr(self).
     |  
     |  __reversed__(...)
     |      L.__reversed__() -- return a reverse iterator over the list
     |  
     |  __rmul__(self, value, /)
     |      Return value*self.
     |  
     |  __setitem__(self, key, value, /)
     |      Set self[key] to value.
     |  
     |  __sizeof__(...)
     |      L.__sizeof__() -- size of L in memory, in bytes
     |  
     |  append(...)
     |      L.append(object) -> None -- append object to end
     |  
     |  clear(...)
     |      L.clear() -> None -- remove all items from L
     |  
     |  copy(...)
     |      L.copy() -> list -- a shallow copy of L
     |  
     |  count(...)
     |      L.count(value) -> integer -- return number of occurrences of value
     |  
     |  extend(...)
     |      L.extend(iterable) -> None -- extend list by appending elements from the iterable
     |  
     |  index(...)
     |      L.index(value, [start, [stop]]) -> integer -- return first index of value.
     |      Raises ValueError if the value is not present.
     |  
     |  insert(...)
     |      L.insert(index, object) -- insert object before index
     |  
     |  pop(...)
     |      L.pop([index]) -> item -- remove and return item at index (default last).
     |      Raises IndexError if list is empty or index is out of range.
     |  
     |  remove(...)
     |      L.remove(value) -> None -- remove first occurrence of value.
     |      Raises ValueError if the value is not present.
     |  
     |  reverse(...)
     |      L.reverse() -- reverse *IN PLACE*
     |  
     |  sort(...)
     |      L.sort(key=None, reverse=False) -> None -- stable sort *IN PLACE*
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  __hash__ = None
    


You can get a shorter set of basic help by putting ``?`` after the
object.

In a notebook, this will show in a new window at the bottom of the book.
You can get rid of this by clicking the x.

.. code:: python

    list?

Another useful thing is to see a list of potential methods in a class.
This is achieved by hitting the ``<tab>`` key, e.g.

.. code:: python

    # place the cursor after the `.` below
    # hit the <tab> key, rather than <return> in this cell
    # Dont run this cell
    list.

Really, this is just using the fact that ``<tab>`` key performs variable
name completion.

This means that if you e.g. have variables called ``the_long_one`` and
``the_long_two`` set:

.. code:: python

    the_long_one = 1
    the_long_two = 2

The next time you want to refer to this string in code, you need only
type as many letters needed to distinguish this from other variable
names, then hit ``<tab>`` to complete the name as far as possible.

**E1.3.5 Exercise**

-  in the cell below, place the cursor after the letter t and hit
   ``<tab>``. It should show you a list of things that begin with ``t``.
-  Use this to write the line of code ``the_long_one = 1000``
-  in the cell below, place the cursor after the letters ``th`` and hit
   ``<tab>``. It should show you a list of things that begin with
   ``th``. In this case it should just give you the options of
   ``the_long_one`` or ``the_long_two``.
-  If you hit ``<tab>`` again, the variable name will be completed as
   far as it can, here, up to ``the_long_``. Use this to write the line
   of code ``the_long_two = 2000``

.. code:: python

    # do exercise here ... put the cursor after the t or th and
    # use <tab> for completion. Dont run this cell
    t
    th
