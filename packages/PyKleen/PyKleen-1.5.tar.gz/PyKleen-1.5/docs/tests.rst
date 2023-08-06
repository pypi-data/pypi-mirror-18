.. _tests:

Tests
=====

Schema
------

.. class:: Schema

  Schema is a :class:`.Param` -> :class:`.Test` container. This is usually
  your starting point, as most information you need to _kleen_ is user input
  in the form of a dictionary.

  .. class:: Param

    When defining a param in the :class:`.Schema`, you can use the `Param`
    class to mark the parameter as required or attach a default.


Tests
-----

.. function:: string

  Sanitize and validate a value as a string. When using a users input,
  HTML tags in the input are always a critical point. This function
  uses, by default, the `bleach` package to strip tags from the input.

  .. code-block:: python

    test = string(10, 150, strip_tags=True, allowed_tags=['a', 'p'])
    value = test('Some test here')  # 'Some test here'
    value = test('Some')  # 'Some test here'
    value = test(23)  # <Error 'Should not exceed 10.'>

  :param min_len: Minimum length of the string.
  :param max_len: Maximum length of the string.
  :param strip_tags: Should HTML-tags be stripped?
  :param allowed_tags: Which tags are allowed?
  :param allowed_attributes: Which attributes are allowed?
  :param strip: Should whitespace be stripped?
  :param min_len_error: Error for `min_len`.
  :param max_len_error: Error for `max_len`.

  :type min_len: int = None
  :type max_len: int = None
  :type strip_tags: bool = True
  :type allowed_tags: List[str] = None
  :type allowed_attributes: Dict[str, List[str]] = None
  :type strip: bool = True
  :type min_len_error: str = 'Too short.'
  :type max_len_error: str = 'Too long.'

.. function:: regex

  Validate a string based on the given regular expression. This
  test uses :func:`string` by default, but you can substitute
  your own.

  .. code-block:: python

    test = regex(r'^[a-z]+$', error='Only letters.')
    value = test('testtest')  # 'testtest'
    value = test(23)  # <Error 'Only letters.'>

  :param pattern: Regular expression.
  :param cast_to_string: Cast to string, ran before the pattern test.
  :param error: Error

  :type pattern: str
  :type cast_to_string: Callable = None
  :type error: str = 'Does not match.'

.. function:: email

  Validates an email address based on the RFC 2822 specifications.
  Also the email address should be at least 5 characters and at
  most 256 characters.

  .. code-block:: python

    test = email()
    value = test('example@domain.com')  # 'example@domain.com'
    value = test('test.com')  # <Error 'Invalid email address.'>

  :param error: Error

  :type error: str = 'Does not match.'

.. function:: password

  Validates a password on a set of rules. The score of the value
  should be at least the required strength (default 70). It uses
  14 tests to determine the strength.

  .. code-block:: python

    test = password()
    value = test('Test123!')  # 'Test123!'
    value = test('test')  # <Error 'Password is too weak.'>

  :param strength: Minimum required strength of the password.
  :param too_weak_error: Error

  :type strength: int = 70
  :type too_weak_error: str = 'Password is too weak.'

.. function:: numeric

  Validate and sanitize a numeric value. The result will always
  be a `Decimal` and will be rounded *half up* by default.

  .. code-block:: python

    test = numeric()
    value = test('23')  # Decimal('23')
    value = test('24,7')  # Decimal('23')

    test = numeric(3)
    value = test('23')  # Decimal('23.000')
    value = test('24.012,209')  # Decimal('24012.209')

  :param decimals: Amount of decimals allowed.
  :param rounding: How rounding should be applied, use `decimal.ROUND_*`.
  :param at_least: Lowest allowed value.
  :param at_most: Highest allowed value.
  :param at_least_error: Error for `at_least`.
  :param at_most_error: Error for `at_most`.
  :param cast_error: Error when casting do Decimal failed.

  :type decimals: int = 0
  :type rounding: str = ROUND_HALF_UP,
  :type at_least: int = None
  :type at_most: int = None,
  :type at_least_error: str = 'Too small.',
  :type at_most_error: str = 'Too large.',
  :type cast_error: str = 'Invalid number.'

.. function:: boolean

  Turn any value to a boolean (via `str`). You can provide your own lists
  to determine True-ness or False-ness. By default this function casts
  to true when `['True', 'true', '1', 'yes', 'y', 'on']` otherwise
  the result is `False`.

  .. code-block:: python

    test = boolean()
    value = test('yes')  # True
    value = test('nope')  # False
    value = test(True)  # True

    test = boolean(is_false_when=['no', 'False', '0'])
    value = test('no')  # False
    value = test('yepper')  # True
    value = test(None)  # True

  :param is_true_when: List of `True` values.
  :param is_false_when: List of `False` values.
  :param cast_error: When `is_true_when` and `is_false_when` are not matched.
    Only applicable when you provide both lists!

  :type is_true_when: List[str] = None
  :type is_false_when: List[str] = None
  :type cast_error: str = 'Invalid boolean.'

.. function:: datetime

  Turn a value into a `datetime.datetime` value. You can provide your
  own list of formats to parse against. By default is is this list of
  formats:

  * ``'%Y-%m-%d %H:%M'``
  * ``'%d-%m-%Y %H:%M'``
  * ``'%Y-%m-%d %H:%M:%S'``
  * ``'%d-%m-%Y %H:%M:%S'``
  * ``'%Y-%m-%dT%H:%M:%S'``

  .. code-block:: python

    test = datetime()
    value = test('2001-4-23 23:01')  # datetime.datetime(2001, 4, 23, 23, 1)
    value = test('not a date')  # <Error 'Invalid datetime.'>

  :param formats: A list of formats used with `strptime`.
  :param parse_error: Error when no format is matched.

  :type formats: List[str] = None
  :type parse_error: str = 'Invalid datetime.'

.. function:: date

  Turn a value into a `datetime.date` value. You can provide your
  own list of formats to parse against. By default is is this list of
  formats:

  * ``'%Y-%m-%d'``
  * ``'%d-%m-%Y'``

  .. code-block:: python

    test = date()
    value = test('2001-4-23')  # datetime.date(2001, 4, 23)
    value = test('not a date')  # <Error 'Invalid date.'>

  :param formats: A list of formats used with `strptime`.
  :param parse_error: Error when no format is matched.

  :type formats: List[str] = None
  :type parse_error: str = 'Invalid date.'

.. function:: minutes

  Turn a value into an `int` value. It will parse (at least it
  tries) some formats people use for minutes.

  * ``'hh:mm'``, ``'hhhhh:mm'``
  * ``'hh:mm'``, ``'hh.mm'``, ``'hh,mm'``
  * ``'hhmm'``, ``'hmm'``
  * ``'mmmmm'``

  .. code-block:: python

    test = minutes()
    value = test('10:33')  # 633
    value = test('10.35')  # 635
    value = test('1028')  # 628
    value = test('not a date')  # <Error 'Invalid date.'>

  :param error: Error when no format is matched.

  :type error: str = 'Invalid format.'

.. function:: one_of

  Check if the value is one of the defined values. You can use
  the `cast` parameter to cast the value before checking, for when
  you want to check numbers or booleans.

  .. code-block:: python

    test = one_of(['a', 'b', 'c', '1', '2'], cast=string())
    value = test('b')  # 'b'
    value = test(2)  # '2'
    value = test('8')  # <Error 'Invalid value.'>

  :param values: List of values it should match to.
  :param cast: Values in the list can be cast before checking.
  :param invalid_error:

  :type values: List[Any]
  :type cast: Union[Callable, Test] = None
  :type invalid_error: str = 'Invalid value.'

.. function:: set_of

  Check if all the item in the value, which is a list, set or tuple,
  are present in the defined values. You can use the `cast` parameter
  to cast each item before checking, for when you want to check numbers
  or booleans.

  See :func:`convert_to_list` for more details.

  .. code-block:: python

    test = set_of(['a', 'b', 'c', '1', '2'], cast=string())
    value = test('b')  # ['b']
    value = test('a,2')  # ['a', '2']
    value = test(['a', 'c', 1])  # ['a', 'c', '1']
    value = test('7,1,8')  # <Error 'Invalid value(s) 7, 8.'>

  :param values: List of values it should match to.
  :param cast: Values in the list can be cast before checking.
  :param invalid_error:

  :type values: List[Any]
  :type cast: Union[Callable, Test] = None
  :type invalid_error: str = 'Invalid value.'

.. function:: list_of

  The passed value should be a list of `cast`. You can use this to
  get a list of numbers of a list of booleans, but you can also use
  this in combination with :class:`~Schema`.

  See :func:`convert_to_list` for more details.

  .. code-block:: python

    test = list_of(numeric())
    value = test(['4', '18,2'])  # [Decimal('4'), Decimal('18')]
    value = test('8,12')  # [Decimal('8'), Decimal('12')]
    value = test(['a', '13', 'c'])  #  <Errors [0, 2] Invalid item(s).>

  :param cast: Used to cast each item in the value.
  :param error: Error message when one or more casts fail.
  :param type_error: Error when an invalid value type is provided.

  :type cast: Union[Callable, Test]
  :type error: str = 'Invalid item(s) %s.'
  :type type_error: str = 'Invalid type %s.'

Others
------

.. function:: convert_to_list

  Convert a value into a list, this should be used as an helper function
  as the value it produces contains unchecked items.

  * It splits a string on ``','``, so you can pass values like ``'1,3,5'``.
  * Values that are ``int``, ``Decimal``, ``.datetime`` or ``.date`` are
    wrapped by a list.
  * Any other list type is accepted, other values throw an error.

  .. code-block:: python

    def list_of_numbers():
      return All([
        convert_to_list(),
        To(numeric()),
      ])

    test = list_of_numbers()
    value = test('1,2')  # [Decimal('1'), Decimal('2')]

.. function:: is_instance

  Verify the value is of a certain instance. You can use this to verify
  if the value is correctly converted or passed. It does not (in any way)
  sanitize the value, it only checks.

  .. code-block:: python

    def should_be_file():
      return is_instance(file)

    test = should_be_file()

    stream = open('f.txt')
    value = test(stream)  # <_io.TextIOWrapper ...>
    value.close()

  :param types: A list of types to validate against.
  :param type_error: Error if the value is not of instance.

  :type types: List[Any]
  :type type_error: str = 'Invalid type %s.'

.. function:: size

  Verify if the item is of a certain size, this function is used by
  the :func:`string` function. You could use it in conjunction with
  :func:`set_of` or :func:`list_of`, to check the size of the list.

  .. code-block:: python

    def list_of_numbers(min_len=None, max_len=None):
      return All([
        list_of(numeric()),
        size(min_len, max_len),
      ])

    test = list_of_numbers(3, 5)
    value = test('1,2,3')  # [Decimal('1'), Decimal('2'), Decimal('3')]
    value = test('1')  # <Error 'Too short.'>
    value = test('1,3,5,6,7,8')  # <Error 'Too long.'>

  :param min_len: Minimum size of the value.
  :param max_len: Maximum size of the value.
  :param min_len_error: Error for `min_len`.
  :param max_len_error: Error for `max_len`.
  :param type_error: Error for not being a string.

  :type min_len: int = None
  :type max_len: int = None
  :type min_len_error: str = 'Too short.'
  :type max_len_error: str = 'Too long.'
  :type type_error: str = 'Invalid type %s.'