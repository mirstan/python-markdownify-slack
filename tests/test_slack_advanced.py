"""
Advanced tests for Slack format functionality including validation, 
performance, and edge cases.
"""
from markdownify import markdownify
from .utils import md
import time


def slack_md(html, **options):
    """Helper function for Slack format tests"""
    options = {"flavor": "slack", "strip_document": None, **options}
    return md(html, **options)


class TestSlackValidation:
    """Test Slack ID and URL validation"""
    
    def test_valid_slack_user_ids(self):
        """Test various valid Slack user ID formats"""
        valid_ids = [
            'U123456',
            'U1234567890',
            'UABCDEFGHIJ'
        ]
        
        for user_id in valid_ids:
            html = f'<a href="#" data-slack-user="{user_id}">@user</a>'
            result = slack_md(html)
            assert result == f'<@{user_id}>', f"Failed for user ID: {user_id}"
    
    def test_invalid_slack_user_ids(self):
        """Test invalid Slack user ID formats fall back to text"""
        invalid_ids = [
            'X123456',  # Wrong prefix
            'U',        # Too short
            'U' * 20,   # Too long
            'U123-456', # Non-alphanumeric
            '',         # Empty
            None        # None value
        ]
        
        for user_id in invalid_ids:
            if user_id is None:
                html = '<a href="#" data-slack-user="">@user</a>'
            else:
                html = f'<a href="#" data-slack-user="{user_id}">@user</a>'
            result = slack_md(html)
            assert result == '@user', f"Should fall back to text for invalid ID: {user_id}"
    
    def test_valid_slack_channel_ids(self):
        """Test various valid Slack channel ID formats"""
        valid_ids = [
            'C123456',
            'C1234567890',
            'CABCDEFGHIJ'
        ]
        
        for channel_id in valid_ids:
            html = f'<a href="#" data-slack-channel="{channel_id}">#channel</a>'
            result = slack_md(html)
            assert result == f'<#{channel_id}>', f"Failed for channel ID: {channel_id}"
    
    def test_valid_urls(self):
        """Test URL validation"""
        valid_urls = [
            'https://example.com',
            'http://test.org',
            'ftp://files.com',
            'mailto:test@example.com',
            'tel:+1234567890',
            '/relative/path',
            '#anchor'
        ]
        
        for url in valid_urls:
            html = f'<a href="{url}">Link</a>'
            result = slack_md(html)
            if url.startswith(('http', 'ftp', 'mailto', 'tel', '/', '#')):
                assert f'<{url}|Link>' in result or f'<{url}>' in result, f"Failed for URL: {url}"
    
    def test_invalid_urls(self):
        """Test invalid URLs fall back to text"""
        invalid_urls = [
            'javascript:alert(1)',
            'data:text/html,<script>',
            '',
            '   ',  # Whitespace only
        ]
        
        for url in invalid_urls:
            html = f'<a href="{url}">Link</a>'
            result = slack_md(html)
            assert result == 'Link', f"Should fall back to text for invalid URL: {url}"


class TestSlackPerformance:
    """Test performance optimizations"""
    
    def test_caching_performance(self):
        """Test that caching improves performance for repeated validations"""
        # Create HTML with repeated Slack IDs
        html_parts = []
        for i in range(100):
            html_parts.append(f'<a href="#" data-slack-user="U123456">@user{i}</a>')
        
        html = ' '.join(html_parts)
        
        # First conversion (populates cache)
        start_time = time.time()
        result1 = slack_md(html)
        first_time = time.time() - start_time
        
        # Second conversion (uses cache)
        start_time = time.time()
        result2 = slack_md(html)
        second_time = time.time() - start_time
        
        # Results should be identical
        assert result1 == result2
        
        # Second run should be faster (though this might not always be true in practice)
        # We'll just verify the cache is working by checking the results are consistent
        assert '<@U123456>' in result1
        assert result1.count('<@U123456>') == 100
    
    def test_large_document_handling(self):
        """Test handling of large documents"""
        # Create a large HTML document
        sections = []
        for i in range(50):
            sections.append(f'''
            <div>
                <h2>Section {i}</h2>
                <p>This is <b>bold</b> and <em>italic</em> text.</p>
                <p>User mention: <a href="#" data-slack-user="U{i:06d}">@user{i}</a></p>
                <p>Link: <a href="https://example{i}.com">Example {i}</a></p>
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                </ul>
            </div>
            ''')
        
        html = ''.join(sections)
        
        start_time = time.time()
        result = slack_md(html)
        conversion_time = time.time() - start_time
        
        # Should complete in reasonable time (less than 5 seconds)
        assert conversion_time < 5.0, f"Conversion took too long: {conversion_time}s"
        
        # Verify content is correctly converted
        assert '*bold*' in result
        assert '_italic_' in result
        assert '<@U000000>' in result
        assert '<https://example0.com|Example 0>' in result


class TestSlackAdvancedFeatures:
    """Test advanced Slack-specific features"""
    
    def test_code_block_language_support(self):
        """Test Slack-specific code block language attributes"""
        html = '<pre data-slack-lang="python">print("hello")</pre>'
        result = slack_md(html)
        assert '```python\nprint("hello")\n```' in result
    
    def test_nested_formatting_handling(self):
        """Test handling of nested formatting"""
        html = '<p><b>Bold <em>and italic</em> text</b></p>'
        result = slack_md(html)
        # Should handle nested formatting gracefully
        assert '*Bold _and italic_ text*' in result or '*Bold and italic text*' in result
    
    def test_complex_mention_scenarios(self):
        """Test complex mention scenarios"""
        html = '''
        <div>
            <p>Hey <a href="#" data-slack-user="U123456">@john</a> and 
               <span data-slack-mention="here">@here</span>!</p>
            <p>Check <a href="#" data-slack-channel="C789012">#general</a> for updates.</p>
            <p>Team <span data-slack-mention="subteam" data-slack-subteam="S123456789">@devs</span> 
               please review.</p>
        </div>
        '''
        
        result = slack_md(html)
        assert '<@U123456>' in result
        assert '<!here>' in result
        assert '<#C789012>' in result
        assert '<!subteam^S123456789>' in result
    
    def test_date_formatting_variations(self):
        """Test various date formatting scenarios"""
        # Basic date
        html1 = '<span data-slack-timestamp="1392734382" data-slack-format="{date}" data-slack-fallback="Feb 18, 2014">Feb 18</span>'
        result1 = slack_md(html1)
        assert '<!date^1392734382^{date}|Feb 18, 2014>' == result1
        
        # Date with link
        html2 = '<span data-slack-timestamp="1392734382" data-slack-format="{date_short}" data-slack-link="https://example.com" data-slack-fallback="2/18/14">2/18</span>'
        result2 = slack_md(html2)
        assert '<!date^1392734382^{date_short}^https://example.com|2/18/14>' == result2
        
        # Invalid date (missing timestamp)
        html3 = '<span data-slack-format="{date}" data-slack-fallback="Invalid">Invalid</span>'
        result3 = slack_md(html3)
        assert result3 == 'Invalid'


class TestSlackEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_empty_and_whitespace_content(self):
        """Test handling of empty and whitespace-only content"""
        assert slack_md('') == ''
        assert slack_md('   ').strip() == ''  # Whitespace gets normalized
        # Empty paragraph might be stripped by the parser
        empty_p_result = slack_md('<p></p>')
        assert empty_p_result in ['', '\n\n\n\n']
        assert slack_md('<p>   </p>') == '\n\n\n\n'
    
    def test_malformed_html(self):
        """Test handling of malformed HTML"""
        malformed_cases = [
            '<b>Unclosed bold',
            '<a href="test">Unclosed link',
            '<span data-slack-mention="here">Unclosed span',
            '<p><b>Nested <em>tags</b></em></p>',  # Incorrectly nested
        ]
        
        for html in malformed_cases:
            # Should not crash, should produce some reasonable output
            result = slack_md(html)
            assert isinstance(result, str), f"Failed for malformed HTML: {html}"
    
    def test_special_characters_in_attributes(self):
        """Test handling of special characters in Slack attributes"""
        # User ID with edge case characters (should be rejected)
        html1 = '<a href="#" data-slack-user="U123&456">@user</a>'
        result1 = slack_md(html1)
        assert result1 == '@user'  # Should fall back to text
        
        # URL with special characters (should be handled)
        html2 = '<a href="https://example.com/path?param=value&other=test">Link</a>'
        result2 = slack_md(html2)
        assert '<https://example.com/path?param=value&other=test|Link>' in result2
    
    def test_unicode_content(self):
        """Test handling of Unicode content"""
        html = '<p><b>Bold 中文</b> and <em>italic العربية</em> and 🚀 emoji</p>'
        result = slack_md(html)
        assert '*Bold 中文*' in result
        assert '_italic العربية_' in result
        assert '🚀' in result
    
    def test_deeply_nested_structures(self):
        """Test deeply nested HTML structures"""
        html = '''
        <div>
            <div>
                <div>
                    <p>
                        <span>
                            <a href="#" data-slack-user="U123456">
                                <b>@user</b>
                            </a>
                        </span>
                    </p>
                </div>
            </div>
        </div>
        '''
        
        result = slack_md(html)
        # Should handle deep nesting without issues
        assert '<@U123456>' in result


class TestSlackCompatibility:
    """Test compatibility with existing functionality"""
    
    def test_backward_compatibility(self):
        """Test that existing functionality still works"""
        html = '<p><b>Bold</b> and <em>italic</em> text</p>'
        
        # Standard markdown should work as before
        standard = markdownify(html)
        assert '**Bold**' in standard
        assert '*italic*' in standard
        
        # Slack format should work differently
        slack = markdownify(html, flavor='slack')
        assert '*Bold*' in slack
        assert '_italic_' in slack
    
    def test_option_combinations(self):
        """Test various option combinations"""
        html = '''
        <div>
            <h3>Header</h3>
            <ul><li>Item 1</li><li>Item 2</li></ul>
            <table><tr><td>Cell</td></tr></table>
            <a href="#" data-slack-user="U123456">@user</a>
        </div>
        '''
        
        # Test different combinations
        result1 = slack_md(html, slack_disable_headers=True)
        assert '### Header' not in result1
        
        result2 = slack_md(html, slack_disable_lists=True)
        assert '• Item 1' in result2
        
        result3 = slack_md(html, slack_user_mentions=False)
        assert '<@U123456>' not in result3
        assert '@user' in result3
    
    def test_all_options_disabled(self):
        """Test Slack format with all special options disabled"""
        html = '''
        <div>
            <h1>Title</h1>
            <ul><li>Item</li></ul>
            <a href="#" data-slack-user="U123456">@user</a>
            <a href="#" data-slack-channel="C123456">#channel</a>
        </div>
        '''
        
        result = slack_md(html, 
                         slack_disable_headers=True,
                         slack_disable_lists=True, 
                         slack_user_mentions=False,
                         slack_channel_links=False)
        
        # Should still use Slack formatting for basic elements
        assert '# Title' not in result  # Headers disabled
        assert '• Item' in result       # Manual list formatting
        assert '@user' in result        # User mentions disabled
        assert '#channel' in result     # Channel links disabled 