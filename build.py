#!/usr/bin/env python3
"""Parse the Autobiography of a Yogi text and generate the interactive HTML site."""
import re
import json

text = open('text/autobiography of a yogi.txt', encoding='utf-8').read()

# Split into frontmatter and chapters
chapters = re.split(r'(?=^CHAPTER:)', text, flags=re.MULTILINE)

# First block is frontmatter (title page, contents, preface, etc.)
frontmatter = chapters[0].strip()

# Parse chapters
chapter_data = []
for block in chapters[1:]:
    lines = block.strip().split('\n')
    # Extract chapter title from first line like "CHAPTER: 1" or "CHAPTER: 10"
    title_line = lines[0].strip()
    ch_num = re.search(r'CHAPTER:\s*(\d+)', title_line)
    if not ch_num:
        continue
    ch_num = int(ch_num.group(1))

    # Skip separator lines (---, ***, etc.) after CHAPTER: header
    i = 1
    while i < len(lines) and not lines[i].strip():
        i += 1

    # The next line(s) contain the chapter title
    title_lines = []
    while i < len(lines) and lines[i].strip() and not lines[i].startswith('CHAPTER:'):
        title_lines.append(lines[i].strip())
        i += 1
    title = ' '.join(title_lines)

    # Convert ALLCAPS titles to title case for better display
    words = title.split()
    lowercase_words = {'and', 'the', 'an', 'of', 'in', 'to', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'is', 'or', 'but', 'not', 'so', 'if', 'no', 'up', 'he', 'she', 'we', 'they', 'me', 'him', 'us', 'them', 'am', 'be', 'its', 'our', 'your', 'their', 'was', 'are'}
    title_words = []
    for idx, w in enumerate(words):
        clean = w.strip('-"\'(),.')
        if not clean:
            title_words.append(w)
            continue
        # Extract prefix/suffix punctuation
        prefix = ''
        suffix = ''
        for c in w:
            if c in '"\'(':
                prefix += c
            elif c in '),.':
                suffix = c + suffix
        # Handle single-letter words first
        if len(clean) == 1:
            if w.endswith('.'):
                title_words.append(prefix + clean.upper() + suffix)
            elif idx == 0 and clean[0] not in '"\'(':
                title_words.append(prefix + clean.upper() + suffix)
            else:
                title_words.append(prefix + clean.lower() + suffix)
            continue
        # Handle abbreviations like "J.c.." - split on dots
        if '.' in clean:
            parts = clean.split('.')
            cleaned_parts = [p for p in parts if p]
            new_clean = '.'.join(p.capitalize() for p in cleaned_parts)
            is_lower = new_clean.lower() in lowercase_words
            if idx == 0 and new_clean[0] not in '"\'(':
                is_lower = False
            if is_lower:
                title_words.append(prefix + new_clean.lower() + suffix)
            else:
                title_words.append(prefix + new_clean.capitalize() + suffix)
            continue
        is_lower = clean.lower() in lowercase_words
        # First word is always capitalized (unless it's a quote)
        if idx == 0 and clean[0] not in '"\'(':
            is_lower = False
        if is_lower:
            title_words.append(prefix + clean.lower() + suffix)
        else:
            title_words.append(prefix + clean.capitalize() + suffix)
    title = ' '.join(title_words)

    # Rest is content
    content_lines = lines[i:]
    content = '\n'.join(content_lines)

    # Clean up content: remove image references, footnote markers for now
    # Keep the text clean
    chapter_data.append({
        'number': ch_num,
        'title': title,
        'content': content
    })

# Also extract frontmatter sections
# Split frontmatter into sections
sections = re.split(r'\n\n+', frontmatter)

# Build the data structure
data = {
    'title': 'Autobiography of a Yogi',
    'author': 'Paramhansa Yogananda',
    'sections': [],
    'chapters': chapter_data
}

# Parse frontmatter sections (title page, contents, preface, acknowledgments)
current_section = None
current_title = None
current_lines = []

for line in sections:
    stripped = line.strip()
    if not stripped:
        continue

    # Detect section headers
    if 'PREFACE' in stripped and 'By' in stripped:
        if current_section:
            current_section['content'] = '\n'.join(current_lines).strip()
            data['sections'].append(current_section)
        current_section = {'title': 'Preface', 'content': ''}
        current_lines = []
        continue
    elif "AUTHOR'S ACKNOWLEDGMENTS" in stripped or "AUTHORS ACKNOWLEDGMENTS" in stripped:
        if current_section:
            current_section['content'] = '\n'.join(current_lines).strip()
            data['sections'].append(current_section)
        current_section = {'title': "Author's Acknowledgments", 'content': ''}
        current_lines = []
        continue
    elif stripped.startswith('Contents') or stripped.startswith('CONTENTS'):
        if current_section:
            current_section['content'] = '\n'.join(current_lines).strip()
            data['sections'].append(current_section)
        current_section = {'title': 'Contents', 'content': ''}
        current_lines = []
        continue
    elif stripped.startswith('ILLUSTRATIONS'):
        if current_section:
            current_section['content'] = '\n'.join(current_lines).strip()
            data['sections'].append(current_section)
        current_section = {'title': 'Illustrations', 'content': ''}
        current_lines = []
        continue

    if current_section:
        current_lines.append(line)
    else:
        # Title page stuff
        if not any(s['title'] == 'Title Page' for s in data['sections']):
            current_section = {'title': 'Title Page', 'content': ''}
            data['sections'].append(current_section)
        current_lines.append(line)

if current_section:
    current_section['content'] = '\n'.join(current_lines).strip()
    data['sections'].append(current_section)

# Write the data
with open('text/text_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Parsed {len(data['sections'])} frontmatter sections and {len(chapter_data)} chapters")
print(f"Total text size: {sum(len(c['content']) for c in chapter_data)} chars")

# --- Generate interactive HTML ---
html_template = open('index.html.template', encoding='utf-8').read()

# Embed data as JSON
data_json = json.dumps(data, ensure_ascii=False)
html = html_template.replace('/*DATA*/', data_json)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Generated index.html")
