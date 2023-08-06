assertion-always-true
~~~~~~~~~~~~~~~~~~~~~
It's a mistake to write code like this::

    assert(x > 0, "x must be positive")  # wrong!

The intention was to check whether ``x > 0`` is true.
But this code checks if the tuple is true,
and it always is, regardless of the value of ``x``.
The correct code omits the parentheses::

    assert x > 0, "x must be positive"

References:

 | https://docs.python.org/2/reference/simple_stmts.html#grammar-token-assert_stmt

Severity, certainty:

 minor, certain

embedded-code-copy
~~~~~~~~~~~~~~~~~~
The source appears to include
a convenience copy of code from other software package.

References:

 | https://www.debian.org/doc/debian-policy/ch-source.html#s-embeddedfiles

Severity, certainty:

 important, possible

except-shadows-builtin
~~~~~~~~~~~~~~~~~~~~~~
It's a mistake to write code like this::

    try:
        ...
    except TypeError, ValueError:  # wrong!
        ...

The intention was to catch both ``TypeError`` and ``ValueError`` exceptions,
but this code does something different: it will catch ``TypeError``
and bind the resulting exception object to the local name ``ValueError``.
The ``ValueError`` exception will not be caught at all.
The correct code specifies a tuple of exceptions::

    try:
        ...
    except (TypeError, ValueError):
        ...

References:

 | https://docs.python.org/2/whatsnew/2.6.html#pep-3110-exception-handling-changes

Severity, certainty:

 important, possible

bare-except
~~~~~~~~~~~
It's a mistake to write code like this::

    try:
        ...
    except:  # wrong!
        ...

The ``except:`` clause catches all the exceptions,
including exceptions that the programmer never expected to happen,
potentially hiding programming errors,
or ignoring ``KeyboardInterrupt`` triggered by user's Ctrl+C.

Please catch only the exceptions you expect to be raised.

References:

 | https://docs.python.org/2/howto/doanddont.html#except

Severity, certainty:

 minor, possible

hardcoded-errno-value
~~~~~~~~~~~~~~~~~~~~~
It's a mistake to write code like this::

    try:
        ...
    except OSError as exc:
        if e.errno == 17:  # non-portable!
           ...

The code was meant to check for ``EEXIST``,
but actual value of this constant may vary with architecture.
The portable code uses constant from the ``errno`` module::

    try:
        ...
    except OSError as exc:
        if e.errno == errno.EEXIST:
           ...

References:

 | https://lists.debian.org/20100803162901.GA5419@jwilk.net
 | http://pubs.opengroup.org/onlinepubs/9699919799/functions/V2_chap02.html#tag_15_03

Severity, certainty:

 normal, possible

inconsistent-use-of-tabs-and-spaces-in-indentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The source file mixes tabs and spaces for indentation in a way that makes it
depend on the worth of a tab expressed in spaces.

You can check consistency of indentation with the following command::

    python -m tabnanny <pyfile>

References:

 | https://docs.python.org/2/reference/lexical_analysis.html#indentation

Severity, certainty:

 normal, certain

mkstemp-file-descriptor-leak
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``tempfile.mkstemp()`` returns a tuple containing
a file descriptor and the pathname.
It is responsibility of the caller to close the file descriptor
when it's no longer needed.
It's a mistake to write code like this::

    path = tempfile.mkstemp()[1]

because it leaks the file descriptor.

Please consider using a higher-level function instead,
``tempfile.TemporaryFile()`` or ``tempfile.NamedTemporaryFile()``,
which take care of file closing automatically.

References:

 | https://docs.python.org/2/library/tempfile.html#tempfile.mkstemp

Severity, certainty:

 normal, possible

obsolete-pil-import
~~~~~~~~~~~~~~~~~~~
Python Imaging Library 1.2 and Pillow (a PIL fork) no longer support this
style of imports::

    import Image

Imports from the PIL namespace should be used instead::

    from PIL import Image

References:

 | https://mail.python.org/pipermail/image-sig/2011-January/006650.html
 | https://lists.debian.org/5117D0B7.801@debian.org

Severity, certainty:

 important, possible

py3k-compat-warning
~~~~~~~~~~~~~~~~~~~
The parser encountered a syntactic construct
that is no longer supported in Python 3.

Severity, certainty:

 wishlist, certain

regexp-duplicate-range
~~~~~~~~~~~~~~~~~~~~~~
A character set in a regular expression includes
the same character range twice.
This is probably a mistake.

For example::

    [A-ZA-Z]

could be simplified to::

    [A-Z]

Severity, certainty:

 minor, possible

regexp-overlapping-ranges
~~~~~~~~~~~~~~~~~~~~~~~~~
A character set in a regular expression includes
two intersecting character ranges.
This is probably a mistake.

For example::

    [A-za-z]

is a common misspelling of::

    [A-Za-z]

Severity, certainty:

 important, possible

regexp-syntax-error
~~~~~~~~~~~~~~~~~~~
The code attempts to compile a regular expression
that is not syntactically valid.

References:

 | https://docs.python.org/2/library/re.html#regular-expression-syntax

Severity, certainty:

 important, certain

string-exception
~~~~~~~~~~~~~~~~
The code attempts to raise or catch strings exceptions.

String exceptions have been removed in Python 2.6.
Attempting to raise them causes ``TypeError``.

References:

 | https://docs.python.org/2/whatsnew/2.6.html#deprecations-and-removals

Severity, certainty:

 important, possible

string-formatting-error
~~~~~~~~~~~~~~~~~~~~~~~
The code uses string formatting (either ``%``-formatting or ``str.format()``)
in a way that always causes runtime error.

References:

 | https://docs.python.org/2/library/stdtypes.html#string-formatting-operations
 | https://docs.python.org/2/library/string.html#formatstrings

Severity, certainty:

 important, certain

syntax-error
~~~~~~~~~~~~
The parser encountered a syntax error.

Severity, certainty:

 serious, certain

syntax-warning
~~~~~~~~~~~~~~
The parser encountered a dubious syntactic construct.

Severity, certainty:

 important, possible

