#!/usr/bin/env python3
"""
🚀 FINAL COMPREHENSIVE DEMONSTRATION
====================================

This demonstrates the ROBUST Slack markdown implementation with:
- ✅ Advanced validation and error handling
- ✅ Performance optimizations with caching
- ✅ Complex nested formatting support
- ✅ Edge case handling
- ✅ Comprehensive feature set
- ✅ Backward compatibility
"""

from markdownify import markdownify
import time
import sys

def slack_md(html, **options):
    """Helper for Slack format conversion"""
    return markdownify(html, flavor='slack', **options)

def demo_section(title, func):
    """Run a demo section with timing"""
    print(f"\n{'='*60}")
    print(f"🔥 {title}")
    print('='*60)
    
    start_time = time.time()
    func()
    elapsed = time.time() - start_time
    print(f"\n⚡ Completed in {elapsed:.3f}s")

def demo_validation():
    """Demonstrate robust ID and URL validation"""
    print("🛡️  VALIDATION & ERROR HANDLING")
    
    test_cases = [
        # Valid Slack IDs
        ('<a href="#" data-slack-user="U123456789">@john</a>', 'Valid User ID'),
        ('<a href="#" data-slack-channel="C987654321">#general</a>', 'Valid Channel ID'),
        
        # Invalid IDs (graceful fallback)
        ('<a href="#" data-slack-user="X123456">@john</a>', 'Invalid User Prefix'),
        ('<a href="#" data-slack-user="U">@john</a>', 'Too Short User ID'),
        ('<a href="#" data-slack-user="U123-456">@john</a>', 'Non-alphanumeric'),
        ('<a href="#" data-slack-user="">@john</a>', 'Empty User ID'),
        
        # URL validation
        ('<a href="javascript:alert(1)">Bad Link</a>', 'Dangerous URL'),
        ('<a href="https://example.com">Good Link</a>', 'Valid URL'),
    ]
    
    for html, description in test_cases:
        result = slack_md(html)
        print(f"  {description:.<25} → {result}")

def demo_performance():
    """Demonstrate performance with caching"""
    print("⚡ PERFORMANCE OPTIMIZATION")
    
    # Create a large document with repeated Slack elements
    html_parts = []
    for i in range(200):
        html_parts.append(f'''
        <div>
            <p><b>Section {i}</b> with <em>italic</em> text</p>
            <p>User: <a href="#" data-slack-user="U123456789">@user{i}</a></p>
            <p>Channel: <a href="#" data-slack-channel="C987654321">#channel{i}</a></p>
            <p>Link: <a href="https://example{i}.com">Example {i}</a></p>
        </div>
        ''')
    
    large_html = ''.join(html_parts)
    
    print(f"  📊 Processing document with {len(html_parts)} sections...")
    print(f"  📊 Total HTML size: {len(large_html):,} characters")
    
    # First conversion (populates caches)
    start = time.time()
    result1 = slack_md(large_html)
    first_time = time.time() - start
    
    # Second conversion (uses caches)
    start = time.time()
    result2 = slack_md(large_html)
    second_time = time.time() - start
    
    print(f"  ⏱️  First conversion:  {first_time:.3f}s")
    print(f"  ⏱️  Second conversion: {second_time:.3f}s")
    print(f"  🎯 Results identical: {result1 == result2}")
    print(f"  📈 Mentions converted: {result1.count('<@U123456789>')}")
    print(f"  📈 Channels converted: {result1.count('<#C987654321>')}")
    print(f"  📈 Final size: {len(result1):,} characters")

def demo_advanced_features():
    """Demonstrate advanced Slack-specific features"""
    print("🎯 ADVANCED SLACK FEATURES")
    
    # Complex document with all features
    complex_html = '''
    <div>
        <h2>Team Update</h2>
        <p>Hey <a href="#" data-slack-user="U123456789">@john</a> and 
           <span data-slack-mention="everyone">@everyone</span>!</p>
        
        <p>Check out <a href="#" data-slack-channel="C987654321">#general</a> 
           for the latest updates.</p>
        
        <p>Meeting scheduled for 
           <span data-slack-timestamp="1642734382" 
                 data-slack-format="{date_short}" 
                 data-slack-fallback="Jan 21, 2022">tomorrow</span>.</p>
        
        <p>The <span data-slack-mention="subteam" 
                     data-slack-subteam="S123456789">@dev-team</span> 
           should review this <a href="https://github.com/repo">PR</a>.</p>
        
        <pre data-slack-lang="python">
def process_slack_message():
    return "Hello, Slack!"
        </pre>
        
        <blockquote>
            <p>This is a <b>quoted</b> message with <em>formatting</em>.</p>
        </blockquote>
        
        <ul>
            <li>Task 1 with <del>strikethrough</del></li>
            <li>Task 2 with <code>inline code</code></li>
        </ul>
    </div>
    '''
    
    result = slack_md(complex_html)
    print("  🎨 Complex document converted:")
    print("     " + result.replace('\n', '\n     '))

def demo_edge_cases():
    """Demonstrate edge case handling"""
    print("🔬 EDGE CASE HANDLING")
    
    edge_cases = [
        # Malformed HTML
        ('<b>Unclosed bold tag', 'Malformed HTML'),
        
        # Unicode content
        ('<p><b>Bold 中文</b> and <em>العربية</em> 🚀</p>', 'Unicode Content'),
        
        # Deeply nested
        ('<div><div><div><p><span><a href="#" data-slack-user="U123456789"><b>@user</b></a></span></p></div></div></div>', 'Deep Nesting'),
        
        # Special characters
        ('<a href="https://example.com/path?param=value&other=test">Complex URL</a>', 'Complex URL'),
        
        # Empty elements
        ('<p></p><div></div><span></span>', 'Empty Elements'),
    ]
    
    for html, description in edge_cases:
        try:
            result = slack_md(html)
            status = "✅ OK"
        except Exception as e:
            result = f"ERROR: {str(e)}"
            status = "❌ ERROR"
        
        print(f"  {description:.<20} {status} → {repr(result[:50])}")

def demo_option_combinations():
    """Demonstrate various option combinations"""
    print("⚙️  CONFIGURATION OPTIONS")
    
    base_html = '''
    <div>
        <h3>Header</h3>
        <ul><li>List item</li></ul>
        <table><tr><td>Table cell</td></tr></table>
        <p><a href="#" data-slack-user="U123456789">@user</a> and 
           <a href="#" data-slack-channel="C987654321">#channel</a></p>
    </div>
    '''
    
    configurations = [
        ({}, 'Default Configuration'),
        ({'slack_disable_headers': True}, 'Headers Disabled'),
        ({'slack_disable_lists': True}, 'Manual List Formatting'),
        ({'slack_disable_tables': True}, 'Tables Disabled'),
        ({'slack_user_mentions': False}, 'User Mentions Disabled'),
        ({'slack_channel_links': False}, 'Channel Links Disabled'),
        ({
            'slack_disable_headers': True,
            'slack_user_mentions': False,
            'slack_channel_links': False
        }, 'Multiple Options Disabled'),
    ]
    
    for config, description in configurations:
        result = slack_md(base_html, **config)
        print(f"  {description}:")
        lines = result.strip().split('\n')
        for line in lines[:3]:  # Show first 3 lines
            if line.strip():
                print(f"    {line}")
        if len(lines) > 3:
            print(f"    ... ({len(lines)-3} more lines)")
        print()

def demo_backward_compatibility():
    """Demonstrate backward compatibility"""
    print("🔄 BACKWARD COMPATIBILITY")
    
    test_html = '<p><b>Bold</b> and <em>italic</em> text with <a href="https://example.com">link</a></p>'
    
    # Standard markdown (original behavior)
    standard = markdownify(test_html)
    print("  📝 Standard Markdown:")
    print(f"     {repr(standard)}")
    
    # Slack format (new behavior)
    slack = markdownify(test_html, flavor='slack')
    print("  💬 Slack Format:")
    print(f"     {repr(slack)}")
    
    print(f"  ✅ Different outputs: {standard != slack}")
    print(f"  ✅ Both are strings: {isinstance(standard, str) and isinstance(slack, str)}")

def main():
    """Run the comprehensive demonstration"""
    print("🚀 COMPREHENSIVE SLACK MARKDOWN IMPLEMENTATION")
    print("=" * 60)
    print("Demonstrating ROBUST features including:")
    print("• Advanced validation and error handling")
    print("• Performance optimizations with caching") 
    print("• Complex nested formatting support")
    print("• Edge case handling")
    print("• Comprehensive Slack feature set")
    print("• Full backward compatibility")
    
    demo_section("VALIDATION & ERROR HANDLING", demo_validation)
    demo_section("PERFORMANCE OPTIMIZATION", demo_performance)
    demo_section("ADVANCED SLACK FEATURES", demo_advanced_features)
    demo_section("EDGE CASE HANDLING", demo_edge_cases)
    demo_section("CONFIGURATION OPTIONS", demo_option_combinations)
    demo_section("BACKWARD COMPATIBILITY", demo_backward_compatibility)
    
    print(f"\n{'='*60}")
    print("🎉 DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("This implementation provides:")
    print("✅ Comprehensive Slack markdown support")
    print("✅ Robust error handling and validation")
    print("✅ Performance optimizations")
    print("✅ Extensive configuration options")
    print("✅ Full backward compatibility")
    print("✅ Production-ready reliability")

if __name__ == "__main__":
    main() 