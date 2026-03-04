"""
Practice 5 — 2.1: Python RegEx Examples
Covers: re.search, re.findall, re.split, re.sub, re.match,
        metacharacters, special sequences, quantifiers, flags
"""

import re

# ─────────────────────────────────────────────
# 1. re.search() — Find FIRST match anywhere in the string
# ─────────────────────────────────────────────
print("=" * 50)
print("1. re.search()")

text = "The rain in Spain stays mainly in the plain"
match = re.search(r"\bS\w+", text)
if match:
    print(f"  Found: '{match.group()}' at position {match.start()}-{match.end()}")

match2 = re.search(r"\d+", "Order number: 4892")
print(f"  First number: {match2.group()}")


# ─────────────────────────────────────────────
# 2. re.match() — Match only at the BEGINNING of the string
# ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("2. re.match()")

print(f"  Match 'Hello': {re.match(r'Hello', 'Hello world')}")
print(f"  Match 'world': {re.match(r'world', 'Hello world')}")  # None


# ─────────────────────────────────────────────
# 3. re.findall() — Find ALL matches, return list
# ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("3. re.findall()")

emails = "Contact us at info@example.com or support@site.org"
found = re.findall(r"[\w.]+@[\w.]+", emails)
print(f"  Emails: {found}")

numbers = re.findall(r"\d+", "I have 3 cats and 12 dogs and 1 parrot")
print(f"  Numbers: {numbers}")


# ─────────────────────────────────────────────
# 4. re.split() — Split string by pattern
# ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("4. re.split()")

result = re.split(r"[,.\s]+", "one, two. three  four")
print(f"  Split by comma/dot/space: {result}")

result2 = re.split(r"(\d+)", "abc123def456ghi")
print(f"  Split keeping delimiter:  {result2}")


# ─────────────────────────────────────────────
# 5. re.sub() — Replace matches
# ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("5. re.sub()")

cleaned = re.sub(r"[,.\s]+", ":", "one, two. three  four")
print(f"  Replace separators with colon: {cleaned}")

# Remove extra whitespace
messy = "Hello    world   Python"
clean = re.sub(r"\s+", " ", messy)
print(f"  Remove extra spaces: '{clean}'")

# Mask phone numbers
text = "Call me at +7 701 123 4567 or +7 727 999 0000"
masked = re.sub(r"\+7\s?\d{3}\s?\d{3}\s?\d{4}", "[PHONE]", text)
print(f"  Masked phones: {masked}")


# ─────────────────────────────────────────────
# 6. Metacharacters
# ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("6. Metacharacters: . ^ $ * + ? [] | ()")

s = "cat bat hat rat"
print(f"  '.at' (any char + at): {re.findall(r'.at', s)}")
print(f"  '^cat' (starts with cat): {bool(re.match(r'^cat', s))}")
print(f"  'rat$' (ends with rat): {bool(re.search(r'rat$', s))}")
print(f"  '[bh]at' (bat or hat): {re.findall(r'[bh]at', s)}")
print(f"  'cat|rat': {re.findall(r'cat|rat', s)}")


# ─────────────────────────────────────────────
# 7. Special Sequences
# ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("7. Special Sequences: \\d \\w \\s \\D \\W \\S")

sample = "Hello World 123 !@#"
digits    = re.findall(r'\d', sample)
words     = re.findall(r'\w+', sample)
spaces    = re.findall(r'\s', sample)
non_dig   = re.findall(r'\D+', sample)
non_word  = re.findall(r'\W+', sample)
boundary  = re.findall(r'\bWorld\b', sample)
print(f"  \\d  (digits):        {digits}")
print(f"  \\w  (word chars):    {words}")
print(f"  \\s  (whitespace):    {spaces}")
print(f"  \\D  (non-digits):    {non_dig}")
print(f"  \\W  (non-word):      {non_word}")
print(f"  \\b  (word boundary): {boundary}")


# ─────────────────────────────────────────────
# 8. Quantifiers: {n}, {n,}, {n,m}, *, +, ?
# ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("8. Quantifiers")

text = "color colour colouur"
print(f"  'colou{{1,2}}r' (1-2 u's): {re.findall(r'colou{1,2}r', text)}")
print(f"  'colou+r'  (1+ u's):       {re.findall(r'colou+r', text)}")
print(f"  'colou?r'  (0-1 u's):      {re.findall(r'colou?r', text)}")
four_dig = re.findall(r'\d{4}', '1234 56 7890 12')
print(f"  '\\d{{4}}'   (exactly 4 dig): {four_dig}")


# ─────────────────────────────────────────────
# 9. Flags
# ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("9. Flags: re.IGNORECASE, re.MULTILINE, re.DOTALL")

text = "Hello hello HELLO"
ig = re.findall(r'hello', text, re.IGNORECASE)
print(f"  IGNORECASE 'hello': {ig}")

multiline = "apple\nbanana\napricot"
ml = re.findall(r'^a\w+', multiline, re.MULTILINE)
print(f"  MULTILINE '^a\\w+': {ml}")

dotall = "line1\nline2\nline3"
ds = bool(re.search(r'line1.+line3', dotall, re.DOTALL))
print(f"  DOTALL 'line1.+line3': {ds}")


# ─────────────────────────────────────────────
# 10. regex.md exercises
# ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("10. regex.md Exercises")

# 1. 'a' followed by zero or more 'b's
pattern1 = re.compile(r'ab*')
print(f"  1. ab*  match 'aabbb': {pattern1.findall('aabbb ac')}")

# 2. 'a' followed by two to three 'b's
pattern2 = re.compile(r'ab{2,3}')
print(f"  2. ab{{2,3}} match 'abbb ac ab': {pattern2.findall('abbb ac ab')}")

# 3. Lowercase letters joined with underscore
pattern3 = re.compile(r'[a-z]+(_[a-z]+)+')
print(f"  3. snake_case words: {pattern3.findall('hello_world foo_bar_baz abc')}")

# 4. One uppercase followed by lowercase letters
pattern4 = re.compile(r'[A-Z][a-z]+')
print(f"  4. Capitalized words: {pattern4.findall('Hello World PYTHON camelCase')}")

# 5. 'a' followed by anything, ending in 'b'
pattern5 = re.compile(r'a.*b')
print(f"  5. a.*b in 'aXYZb': {pattern5.findall('aXYZb')}")

# 6. Replace space, comma, or dot with colon
text6 = "one two,three.four"
print(f"  6. Replace sep: {re.sub(r'[ ,.]', ':', text6)}")

# 7. snake_case to camelCase
def snake_to_camel(s):
    return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), s)
print(f"  7. snake_to_camel('hello_world_python'): {snake_to_camel('hello_world_python')}")

# 8. Split at uppercase letters
text8 = "CamelCaseString"
print(f"  8. Split at uppercase: {re.findall(r'[A-Z][a-z]*', text8)}")

# 9. Insert spaces before capitals
text9 = "CamelCaseString"
spaced = re.sub(r'(?<=[a-z])([A-Z])', r' \1', text9)
print(f"  9. Insert spaces: {spaced}")

# 10. camelCase to snake_case
def camel_to_snake(s):
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s)
    s = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', s)
    return s.lower()
print(f"  10. camel_to_snake('CamelCaseString'): {camel_to_snake('CamelCaseString')}")

print("\nDone!")
