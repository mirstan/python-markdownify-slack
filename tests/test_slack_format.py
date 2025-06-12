from markdownify import SLACK
from .utils import md


def slack_md(html, **options):
    """Helper function for Slack format tests"""
    options = {"flavor": "slack", "strip_document": None, **options}
    return md(html, **options)


def test_slack_bold():
    """Test Slack bold formatting uses single asterisks"""
    assert slack_md('<b>Hello</b>') == '*Hello*'
    assert slack_md('<strong>Hello</strong>') == '*Hello*'
    assert slack_md('foo <b>Hello</b> bar') == 'foo *Hello* bar'
    assert slack_md('foo<b> Hello</b> bar') == 'foo *Hello* bar'
    assert slack_md('foo <b>Hello </b>bar') == 'foo *Hello* bar'


def test_slack_italic():
    """Test Slack italic formatting uses underscores only"""
    assert slack_md('<em>Hello</em>') == '_Hello_'
    assert slack_md('<i>Hello</i>') == '_Hello_'
    assert slack_md('foo <em>Hello</em> bar') == 'foo _Hello_ bar'
    assert slack_md('foo<em> Hello</em> bar') == 'foo _Hello_ bar'
    assert slack_md('foo <em>Hello </em>bar') == 'foo _Hello_ bar'


def test_slack_strikethrough():
    """Test Slack strikethrough formatting uses single tildes"""
    assert slack_md('<del>Hello</del>') == '~Hello~'
    assert slack_md('<s>Hello</s>') == '~Hello~'
    assert slack_md('foo <del>Hello</del> bar') == 'foo ~Hello~ bar'


def test_slack_links():
    """Test Slack link formatting uses angle brackets"""
    assert slack_md('<a href="https://google.com">Google</a>') == '<https://google.com|Google>'
    assert slack_md('<a href="https://google.com">https://google.com</a>') == '<https://google.com>'
    assert slack_md('foo <a href="https://example.com">link</a> bar') == 'foo <https://example.com|link> bar'


def test_slack_user_mentions():
    """Test Slack user mentions with data-slack-user attribute"""
    html = '<a href="#" data-slack-user="U123456">@john</a>'
    assert slack_md(html) == '<@U123456>'


def test_slack_channel_links():
    """Test Slack channel links with data-slack-channel attribute"""
    html = '<a href="#" data-slack-channel="C123456">#general</a>'
    assert slack_md(html) == '<#C123456>'


def test_slack_special_mentions():
    """Test Slack special mentions"""
    assert slack_md('<span data-slack-mention="here">@here</span>') == '<!here>'
    assert slack_md('<span data-slack-mention="channel">@channel</span>') == '<!channel>'
    assert slack_md('<span data-slack-mention="everyone">@everyone</span>') == '<!everyone>'
    
    # Test subteam mention
    html = '<span data-slack-mention="subteam" data-slack-subteam="SAZ94GDB8">@devs</span>'
    assert slack_md(html) == '<!subteam^SAZ94GDB8>'


def test_slack_date_formatting():
    """Test Slack date formatting"""
    # Basic date formatting
    html = '<span data-slack-timestamp="1392734382" data-slack-format="{date}" data-slack-fallback="Feb 18, 2014">Feb 18</span>'
    assert slack_md(html) == '<!date^1392734382^{date}|Feb 18, 2014>'
    
    # Date formatting with link
    html = '<span data-slack-timestamp="1392734382" data-slack-format="{date}" data-slack-link="https://example.com" data-slack-fallback="Feb 18, 2014">Feb 18</span>'
    assert slack_md(html) == '<!date^1392734382^{date}^https://example.com|Feb 18, 2014>'


def test_slack_escaping():
    """Test Slack escaping uses HTML entities"""
    assert slack_md('<p>Hello & goodbye</p>') == '\n\nHello &amp; goodbye\n\n'
    assert slack_md('<p>Less < than > greater</p>') == '\n\nLess &lt; than &gt; greater\n\n'


def test_slack_headers_disabled():
    """Test Slack header disabling"""
    assert slack_md('<h1>Title</h1>', slack_disable_headers=True) == '\n\nTitle\n\n'
    assert slack_md('<h3>Subtitle</h3>', slack_disable_headers=True) == '\n\nSubtitle\n\n'
    assert slack_md('<h6>Small heading</h6>', slack_disable_headers=True) == '\n\nSmall heading\n\n'
    
    # H1 and H2 should still work when headers are not disabled
    assert slack_md('<h1>Title</h1>') == '\n\nTitle\n=====\n\n'
    assert slack_md('<h2>Subtitle</h2>') == '\n\nSubtitle\n--------\n\n'


def test_slack_lists_manual():
    """Test Slack manual list formatting"""
    html = '<ul><li>Item 1</li><li>Item 2</li></ul>'
    expected = '\n\n• Item 1\n• Item 2\n'
    assert slack_md(html, slack_disable_lists=True) == expected
    
    # Ordered list
    html = '<ol><li>First</li><li>Second</li></ol>'
    expected = '\n\n1. First\n2. Second\n'
    assert slack_md(html, slack_disable_lists=True) == expected


def test_slack_tables_disabled():
    """Test Slack table handling"""
    html = '<table><tr><td>Cell 1</td><td>Cell 2</td></tr></table>'
    # Should convert to simple text format
    result = slack_md(html, slack_disable_tables=True)
    assert 'Cell 1' in result and 'Cell 2' in result


def test_slack_code_blocks():
    """Test code blocks work the same in Slack format"""
    assert slack_md('<code>inline code</code>') == '`inline code`'
    assert slack_md('<pre>code block</pre>') == '\n\n```\ncode block\n```\n\n'


def test_slack_blockquotes():
    """Test blockquotes work the same in Slack format"""
    assert slack_md('<blockquote>Quote text</blockquote>') == '\n> Quote text\n\n'


def test_slack_mixed_formatting():
    """Test mixed formatting in Slack format"""
    html = '<p>This is <b>bold</b> and <em>italic</em> and <del>strikethrough</del></p>'
    expected = '\n\nThis is *bold* and _italic_ and ~strikethrough~\n\n'
    assert slack_md(html) == expected


def test_format_comparison():
    """Test differences between standard and Slack formats"""
    html = '<b>bold</b> <em>italic</em> <del>strike</del>'
    
    # Standard markdown
    standard = md(html, strip_document=None)
    assert '**bold**' in standard
    assert '*italic*' in standard  
    assert '~~strike~~' in standard
    
    # Slack format
    slack = slack_md(html)
    assert '*bold*' in slack
    assert '_italic_' in slack
    assert '~strike~' in slack


def test_slack_flavor_disabled_by_default():
    """Test that Slack flavor is disabled by default"""
    html = '<b>bold</b> <em>italic</em>'
    
    # Default behavior should be standard markdown
    result = md(html, strip_document=None)
    assert '**bold**' in result
    assert '*italic*' in result


def test_slack_mention_options():
    """Test Slack mention options can be disabled"""
    html_user = '<a href="#" data-slack-user="U123456">@john</a>'
    html_channel = '<a href="#" data-slack-channel="C123456">#general</a>'
    
    # With mentions enabled (default)
    assert slack_md(html_user) == '<@U123456>'
    assert slack_md(html_channel) == '<#C123456>'
    
    # With mentions disabled
    assert slack_md(html_user, slack_user_mentions=False) == '@john'
    assert slack_md(html_channel, slack_channel_links=False) == '#general'


def test_slack_complex_content():
    """Test complex mixed content in Slack format"""
    html = '''
    <div>
        <h2>Project Update</h2>
        <p>Hello <a href="#" data-slack-user="U123456">@john</a>!</p>
        <p>Please check <a href="https://example.com/docs">the documentation</a>.</p>
        <ul>
            <li><b>Bold item</b></li>
            <li><em>Italic item</em> with <del>strikethrough</del></li>
        </ul>
        <blockquote>Remember to test everything!</blockquote>
    </div>
    '''
    
    result = slack_md(html)
    
    # Check various formatting elements are converted correctly
    assert 'Project Update' in result
    assert '<@U123456>' in result
    assert '<https://example.com/docs|the documentation>' in result
    assert '*Bold item*' in result
    assert '_Italic item_' in result
    assert '~strikethrough~' in result
    assert '> Remember to test everything!' in result


def test_slack_span_elements():
    """Test span elements are handled correctly"""
    # Regular span should just return text
    assert slack_md('<span>regular text</span>') == 'regular text'
    
    # Span with Slack attributes should be converted
    assert slack_md('<span data-slack-mention="here">@here</span>') == '<!here>'
    
    # Nested span
    html = '<p>Text with <span data-slack-mention="channel">@channel</span> mention</p>'
    expected = '\n\nText with <!channel> mention\n\n'
    assert slack_md(html) == expected


def test_slack_edge_cases():
    """Test edge cases and error handling"""
    # Empty HTML
    assert slack_md('') == ''
    
    # Span without required data attributes
    assert slack_md('<span data-slack-mention="subteam">@team</span>') == '@team'
    
    # Date without timestamp
    assert slack_md('<span data-slack-format="{date}">today</span>') == 'today'
    
    # Invalid mention type
    assert slack_md('<span data-slack-mention="invalid">@invalid</span>') == '@invalid'


def test_flavor_option():
    """Test the new flavor option"""
    html = '<p><b>Bold</b> and <em>italic</em> text</p>'
    
    # Test flavor='standard' (default)
    result_standard = md(html, flavor='standard', strip_document=None)
    assert '**Bold**' in result_standard
    assert '*italic*' in result_standard
    
    # Test flavor='slack'
    result_slack = md(html, flavor='slack', strip_document=None)
    assert '*Bold*' in result_slack
    assert '_italic_' in result_slack
    
    # Results should be different
    assert result_standard != result_slack


 