|build| |version| |license| |downloads|

.. |build| image:: https://img.shields.io/github/actions/workflow/status/matthewwithanm/python-markdownify/python-app.yml?branch=develop
    :alt: GitHub Workflow Status
    :target: https://github.com/matthewwithanm/python-markdownify/actions/workflows/python-app.yml?query=workflow%3A%22Python+application%22

.. |version| image:: https://img.shields.io/pypi/v/markdownify
    :alt: Pypi version
    :target: https://pypi.org/project/markdownify/

.. |license| image:: https://img.shields.io/pypi/l/markdownify
    :alt: License
    :target: https://github.com/matthewwithanm/python-markdownify/blob/develop/LICENSE

.. |downloads| image:: https://pepy.tech/badge/markdownify
    :alt: Pypi Downloads
    :target: https://pepy.tech/project/markdownify

Slack Format Support
====================

The library now supports Slack's markdown format (mrkdwn) using the new **flavor** option, which provides a clean and extensible API for different markdown formats.

Flavor Option
-------------

The ``flavor`` parameter controls the overall markdown format:

* ``flavor='standard'`` (default) - GitHub/CommonMark compatible markdown
* ``flavor='slack'`` - Slack mrkdwn format

**Programmatic Usage**::

    import markdownify
    
    html = '<b>Bold</b> and <em>italic</em> text with <a href="https://example.com">a link</a>'
    
    # Standard markdown (default)
    standard = markdownify.markdownify(html)
    # Output: **Bold** and *italic* text with [a link](https://example.com)
    
    # Slack format using new flavor option
    slack = markdownify.markdownify(html, flavor='slack')
    # Output: *Bold* and _italic_ text with <https://example.com|a link>

**Command Line Usage**::

    # Standard markdown (default)
    echo '<b>Hello</b>' | markdownify
    # Output: **Hello**
    
    # Slack format using flavor option
    echo '<b>Hello</b>' | markdownify --flavor slack
    # Output: *Hello*

Key Differences from Standard Markdown
--------------------------------------

* **Bold**: Uses single asterisks ``*text*`` instead of double ``**text**``
* **Italic**: Uses underscores ``_text_`` only (no asterisks)
* **Strikethrough**: Uses single tildes ``~text~`` instead of double ``~~text~~``
* **Links**: Uses angle bracket format ``<url|text>`` instead of ``[text](url)``
* **Escaping**: Uses HTML entities (``&amp;``, ``&lt;``, ``&gt;``) for special characters

Slack-Specific Features
-----------------------

The Slack format also supports platform-specific features through special HTML attributes:

**User Mentions**::

    html = '<a href="#" data-slack-user="U123456">@john</a>'
    result = markdownify.markdownify(html, flavor='slack')
    # Output: <@U123456>

**Channel Links**::

    html = '<a href="#" data-slack-channel="C123456">#general</a>'
    result = markdownify.markdownify(html, flavor='slack')
    # Output: <#C123456>

**Special Mentions**::

    html = '<span data-slack-mention="here">@here</span>'
    result = markdownify.markdownify(html, flavor='slack')
    # Output: <!here>
    
    # Also supports: channel, everyone, and subteam mentions

**Date Formatting**::

    html = '<span data-slack-timestamp="1392734382" data-slack-format="{date}" data-slack-fallback="Feb 18, 2014">Feb 18</span>'
    result = markdownify.markdownify(html, flavor='slack')
    # Output: <!date^1392734382^{date}|Feb 18, 2014>

Configuration Options
---------------------

flavor
  Controls the overall markdown format. Options are ``'standard'`` (default) for GitHub/CommonMark 
  compatible markdown, or ``'slack'`` for Slack mrkdwn format.

slack_user_mentions
  Enable conversion of elements with ``data-slack-user`` attributes to user mentions.
  Defaults to ``True``.

slack_channel_links
  Enable conversion of elements with ``data-slack-channel`` attributes to channel links.
  Defaults to ``True``.

slack_disable_headers
  Disable header conversion for H3+ (only allow H1/H2). Defaults to ``False``.

slack_disable_tables
  Disable table conversion (Slack doesn't support markdown tables). Defaults to ``True``.

slack_disable_lists
  Use manual list formatting with bullets (•) instead of markdown lists. Defaults to ``False``.

Command Line Usage
------------------

The Slack format is also available through the command line interface::

    # Using flavor option
    markdownify --flavor slack input.html
    
    # With additional options
    markdownify --flavor slack --slack-disable-headers --slack-disable-lists input.html
    
    # Pipe usage
    echo '<b>Bold</b> text' | markdownify --flavor slack

Available CLI flags:
  * ``--flavor {standard,slack}``: Choose markdown format
  * ``--slack-disable-headers``: Disable headers beyond H2
  * ``--slack-disable-tables``: Disable table formatting
  * ``--slack-disable-lists``: Use manual list formatting
  * ``--no-slack-user-mentions``: Disable user mention conversion
  * ``--no-slack-channel-links``: Disable channel link conversion

Installation
============

``pip install markdownify``


Usage
=====

Convert some HTML to Markdown:

.. code:: python

    from markdownify import markdownify as md
    md('<b>Yay</b> <a href="http://github.com">GitHub</a>')  # > '**Yay** [GitHub](http://github.com)'

Specify tags to exclude:

.. code:: python

    from markdownify import markdownify as md
    md('<b>Yay</b> <a href="http://github.com">GitHub</a>', strip=['a'])  # > '**Yay** GitHub'

\...or specify the tags you want to include:

.. code:: python

    from markdownify import markdownify as md
    md('<b>Yay</b> <a href="http://github.com">GitHub</a>', convert=['b'])  # > '**Yay** GitHub'


Options
=======

Markdownify supports the following options:

strip
  A list of tags to strip. This option can't be used with the
  ``convert`` option.

convert
  A list of tags to convert. This option can't be used with the
  ``strip`` option.

autolinks
  A boolean indicating whether the "automatic link" style should be used when
  a ``a`` tag's contents match its href. Defaults to ``True``.

default_title
  A boolean to enable setting the title of a link to its href, if no title is
  given. Defaults to ``False``.

heading_style
  Defines how headings should be converted. Accepted values are ``ATX``,
  ``ATX_CLOSED``, ``SETEXT``, and ``UNDERLINED`` (which is an alias for
  ``SETEXT``). Defaults to ``UNDERLINED``.

bullets
  An iterable (string, list, or tuple) of bullet styles to be used. If the
  iterable only contains one item, it will be used regardless of how deeply
  lists are nested. Otherwise, the bullet will alternate based on nesting
  level. Defaults to ``'*+-'``.

strong_em_symbol
  In markdown, both ``*`` and ``_`` are used to encode **strong** or
  *emphasized* texts. Either of these symbols can be chosen by the options
  ``ASTERISK`` (default) or ``UNDERSCORE`` respectively.

sub_symbol, sup_symbol
  Define the chars that surround ``<sub>`` and ``<sup>`` text. Defaults to an
  empty string, because this is non-standard behavior. Could be something like
  ``~`` and ``^`` to result in ``~sub~`` and ``^sup^``.  If the value starts
  with ``<`` and ends with ``>``, it is treated as an HTML tag and a ``/`` is
  inserted after the ``<`` in the string used after the text; this allows
  specifying ``<sub>`` to use raw HTML in the output for subscripts, for
  example.

newline_style
  Defines the style of marking linebreaks (``<br>``) in markdown. The default
  value ``SPACES`` of this option will adopt the usual two spaces and a newline,
  while ``BACKSLASH`` will convert a linebreak to ``\\n`` (a backslash and a
  newline). While the latter convention is non-standard, it is commonly
  preferred and supported by a lot of interpreters.

code_language
  Defines the language that should be assumed for all ``<pre>`` sections.
  Useful, if all code on a page is in the same programming language and
  should be annotated with `````python`` or similar.
  Defaults to ``''`` (empty string) and can be any string.

code_language_callback
  When the HTML code contains ``pre`` tags that in some way provide the code
  language, for example as class, this callback can be used to extract the
  language from the tag and prefix it to the converted ``pre`` tag.
  The callback gets one single argument, an BeautifylSoup object, and returns
  a string containing the code language, or ``None``.
  An example to use the class name as code language could be::

    def callback(el):
        return el['class'][0] if el.has_attr('class') else None

  Defaults to ``None``.

escape_asterisks
  If set to ``False``, do not escape ``*`` to ``\*`` in text.
  Defaults to ``True``.

escape_underscores
  If set to ``False``, do not escape ``_`` to ``\_`` in text.
  Defaults to ``True``.

escape_misc
  If set to ``True``, escape miscellaneous punctuation characters
  that sometimes have Markdown significance in text.
  Defaults to ``False``.

keep_inline_images_in
  Images are converted to their alt-text when the images are located inside
  headlines or table cells. If some inline images should be converted to
  markdown images instead, this option can be set to a list of parent tags
  that should be allowed to contain inline images, for example ``['td']``.
  Defaults to an empty list.

table_infer_header
  Controls handling of tables with no header row (as indicated by ``<thead>``
  or ``<th>``). When set to ``True``, the first body row is used as the header row.
  Defaults to ``False``, which leaves the header row empty.

wrap, wrap_width
  If ``wrap`` is set to ``True``, all text paragraphs are wrapped at
  ``wrap_width`` characters. Defaults to ``False`` and ``80``.
  Use with ``newline_style=BACKSLASH`` to keep line breaks in paragraphs.
  A `wrap_width` value of `None` reflows lines to unlimited line length.

strip_document
  Controls whether leading and/or trailing separation newlines are removed from
  the final converted document. Supported values are ``LSTRIP`` (leading),
  ``RSTRIP`` (trailing), ``STRIP`` (both), and ``None`` (neither). Newlines
  within the document are unaffected.
  Defaults to ``STRIP``.

beautiful_soup_parser
  Specify the Beautiful Soup parser to be used for interpreting HTML markup. Parsers such
  as `html5lib`, `lxml` or even a custom parser as long as it is installed on the execution
  environment. Defaults to ``html.parser``.

.. _BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/

Options may be specified as kwargs to the ``markdownify`` function, or as a
nested ``Options`` class in ``MarkdownConverter`` subclasses.


Converting BeautifulSoup objects
================================

.. code:: python

    from markdownify import MarkdownConverter

    # Create shorthand method for conversion
    def md(soup, **options):
        return MarkdownConverter(**options).convert_soup(soup)


Creating Custom Converters
==========================

If you have a special usecase that calls for a special conversion, you can
always inherit from ``MarkdownConverter`` and override the method you want to
change.
The function that handles a HTML tag named ``abc`` is called
``convert_abc(self, el, text, parent_tags)`` and returns a string
containing the converted HTML tag.
The ``MarkdownConverter`` object will handle the conversion based on the
function names:

.. code:: python

    from markdownify import MarkdownConverter

    class ImageBlockConverter(MarkdownConverter):
        """
        Create a custom MarkdownConverter that adds two newlines after an image
        """
        def convert_img(self, el, text, parent_tags):
            return super().convert_img(el, text, parent_tags) + '\n\n'

    # Create shorthand method for conversion
    def md(html, **options):
        return ImageBlockConverter(**options).convert(html)

.. code:: python

    from markdownify import MarkdownConverter

    class IgnoreParagraphsConverter(MarkdownConverter):
        """
        Create a custom MarkdownConverter that ignores paragraphs
        """
        def convert_p(self, el, text, parent_tags):
            return ''

    # Create shorthand method for conversion
    def md(html, **options):
        return IgnoreParagraphsConverter(**options).convert(html)


Command Line Interface
======================

Use ``markdownify example.html > example.md`` or pipe input from stdin
(``cat example.html | markdownify > example.md``).
Call ``markdownify -h`` to see all available options.
They are the same as listed above and take the same arguments.


Development
===========

To run tests and the linter run ``pip install tox`` once, then ``tox``.
