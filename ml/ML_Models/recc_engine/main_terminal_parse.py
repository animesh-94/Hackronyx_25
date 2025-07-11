import sys
import re
import json
from recc_engine.engine import RecommendationEngine

def parse_terminal_output(lines):
    # Example parser for the provided sample
    screen_data = {
        'topics': {},
        'content_types': {},
        'active_time': 0.0,
        'idle_time': 0.0,
        'engaged_apps': {},
        'browse_time_irrelevant': 0.0
    }
    current_app = None
    current_context = None
    idle_time = 0.0
    for line in lines:
        if 'Active App:' in line:
            current_app = line.split('Active App:')[1].strip()
            screen_data['engaged_apps'][current_app] = screen_data['engaged_apps'].get(current_app, 0) + 1
        if 'Detected Context:' in line:
            current_context = line.split('Detected Context:')[1].strip()
            if current_context:
                screen_data['topics'][current_context.capitalize()] = 1.0
        if 'Idle Time:' in line:
            match = re.search(r'Idle Time: ([\d\.]+)', line)
            if match:
                idle_time = float(match.group(1))
                screen_data['idle_time'] += idle_time
        if 'Context' in line and 'lasted' in line:
            match = re.search(r'lasted ([\d\.]+) seconds', line)
            if match:
                duration = float(match.group(1))
                if current_context == 'browsing':
                    screen_data['browse_time_irrelevant'] += duration
                elif current_context == 'programming':
                    screen_data['active_time'] += duration
    # Assume content type by context
    if 'programming' in screen_data['topics']:
        screen_data['content_types']['YouTube Video'] = 1.0
    if 'browsing' in screen_data['topics']:
        screen_data['content_types']['Blog Post'] = 1.0
    return screen_data

def main():
    engine = RecommendationEngine()
    engine.add_user("student_001")
    engine.add_content(
        title="Python Loops Tutorial",
        url="https://youtube.com/python-loops",
        content_type="YouTube Video",
        description="A beginner's guide to loops in Python.",
        transcript_or_text="Learn about loops, variables, and Python programming in this tutorial.",
        length_minutes=10
    )
    engine.add_content(
        title="Understanding Algebraic Equations",
        url="https://blog.com/algebra-equations",
        content_type="Blog Post",
        description="A blog post on solving algebraic equations.",
        transcript_or_text="This blog post discusses algebra, equations, and statistics in mathematics.",
        readability_score=70.0
    )
    print("Paste terminal output, then press Ctrl+D (or Ctrl+Z on Windows) to process:")
    lines = sys.stdin.read().splitlines()
    screen_data = parse_terminal_output(lines)
    # Always trigger recommendations, skip attentiveness threshold
    recs = engine.generate_recommendations("student_001", 0.0)
    if recs:
        engine.display_recommendations("student_001", recs)
    else:
        print("No recommendations triggered.")

if __name__ == "__main__":
    main()
