#!/usr/bin/env python3
"""
Test script to verify the snake_case conversion function.
"""

from scripts.format_to_snake_case import to_snake_case


def test_conversions():
    """Test various filename conversion cases."""
    test_cases = [
        # (input, expected_output)
        ("Clone Graph.py", "clone_graph.py"),
        ("CloneGraph.py", "clone_graph.py"),
        ("Clone-Graph.py", "clone_graph.py"),
        ("clone-graph.py", "clone_graph.py"),
        ("cloneGraph.py", "clone_graph.py"),
        ("CLONE_GRAPH.py", "clone_graph.py"),
        ("clone__graph.py", "clone_graph.py"),
        ("testFile.py", "test_file.py"),
        ("TestFile.py", "test_file.py"),
        ("XMLParser.py", "xml_parser.py"),
        ("HTMLConverter.py", "html_converter.py"),
        ("simple.py", "simple.py"),  # No change
        ("already_snake.py", "already_snake.py"),  # No change
    ]

    print("Testing filename conversions:")
    print("-" * 40)

    all_passed = True
    for input_name, expected in test_cases:
        result = to_snake_case(input_name)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{input_name}' -> '{result}' (expected: '{expected}')")

        if result != expected:
            all_passed = False

    print("-" * 40)
    if all_passed:
        print("All tests passed! ✅")
    else:
        print("Some tests failed! ❌")

    return all_passed


if __name__ == "__main__":
    test_conversions()
