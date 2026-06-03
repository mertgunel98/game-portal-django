import re

with open(r'C:\Users\mertg\.gemini\antigravity\brain\b60ce355-63b5-43ea-afc7-fc36760b2050\.system_generated\steps\479\content.md', encoding='utf-8') as f:
    content = f.read()

urls = set(re.findall(r'https://[^\s"\'<>]+?\.(?:jpg|png|jpeg)', content))
for u in sorted(urls):
    if 'wikimedia' in u or 'upload' in u:
        print(u)
