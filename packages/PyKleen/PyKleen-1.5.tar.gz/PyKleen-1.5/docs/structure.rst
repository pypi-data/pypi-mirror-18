.. _structure:

Structure
---------

You can build you own tests, validators and sanitizers using these classes.

.. class:: Test

  A test can be called and will yield a validated and/or sanitized product.
  The :class:`.Test` itself doesn't do anything.

  .. class:: One

    Given a callback, when the `One` test is ran, it runs the callback with
    the given value.

    .. code-block:: python

      test = One(lambda v: v < 10, 'Should not exceed 10.')
      value = test(6)  # 6
      value = test(23)  # <Error 'Should not exceed 10.'>

    .. py:method:: __init__(callback[, error])

      :param callback: The test that runs when called.
      :param error: Value of the error-message (`'Test failed.'`).
      :type callback: Union[Callable, Test]
      :type error: str

  .. class:: All

    Given multiple callbacks in a list, when the `All` test is ran, it runs
    the all the callbacks with the given value.

    Be aware that any sanitization must be wrapped in a :class:`To`,
    when providing a simple function the outcome is not saved. A lambda
    (or any other callback like ``str`` or ``int``) is only tested on
    truthness, when false is throws the `error`.

    .. code-block:: python

      test = All([To(int), lambda v: v < 10], 'Must be an int, less than 10.')
      value = test('6')  # 6
      value = test(23)  # <Error 'Must be an int, less than 10.'>
      value = test('aa')  # <Error 'Must be an int, less than 10.'>

    .. py:method:: __init__(callbacks[, error])

      :param callbacks: The test that runs when called.
      :param error: Value of the error-message (`'Test failed.'`).
      :type callbacks: List[Union[Callable, Test]]
      :type error: str

  .. class:: Or

    Given multiple callbacks in a list, when the `Or` test is ran, it runs
    the callbacks one by one until a success (errors are discarded). The
    successful result is returned. When no callback is successful an error
    is thrown.

    .. code-block:: python

      test = Or([date(), datetime(), numeric()], 'Requires date, datetime or timestamp (int).')
      value = test('2004-2-18')  # datetime.date(2004, 2, 18)
      value = test(1077062400)  # Decimal(1077062400)
      value = test('aa')  # <Error 'Requires date, datetime or timestamp (int).'>

    .. py:method:: __init__(callbacks[, error])

      :param callbacks: A list of callbacks.
      :param error: Error when none of the callbacks is successful.

      :type callbacks: List[Union[Callable, Test]]
      :type error: str = 'All tests failed.'

  .. class:: To

    This is a sanization helper, it simply tries to convert a value `To`
    another value. Usefull when running :class:`All`, mostly in conjunction
    with other tests.

    .. code-block:: python

      test = To(int)
      value = test('6')  # 6
      value = test(2.4)  # 2
      value = test('a')  # <Error 'Conversion failed.'>

    .. py:method:: __init__(callbacks[, error])

      :param into: Turn the value `into` this.
      :param error: Error when the conversion failed.

      :type into: Union[Callable, Test]
      :type error: str = 'Conversion failed.'

  .. class:: Yield

    Yield a fixed result when the callback over the value succeeds. There
    are not many usecases for this, but in conjunction with :class:`Or` it
    can be handy (providing default values on test-success).

    .. code-block:: python

      test = Or([
        Yield(lambda v: v in [True, False], 'boolean'),
        Yield(lambda v: v in [None], 'none'),
        Yield(One(lambda v: isinstance(v, (str, bytes))), 'string'),
        Yield(One(lambda v: isinstance(v, int)), 'number'),
      ])

      value = test(True) # 'boolean'
      test(None) # 'none'
      test('blurp') # 'string'
      test(44) # 'number'

    .. py:method:: __init__(callbacks[, error])

      :param callback: The test to run.
      :param fixed_result: Returned when the callback is truthful.
      :param error: Error when the callback was not truthful.

      :type callback: Union[Callable, Test]
      :type fixed_result: Any
      :type error: str = 'Test failed.'
