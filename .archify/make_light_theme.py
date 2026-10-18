import re

with open(r'report/finwise_architecture.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make initial html tag data-theme="light"
html = html.replace('<html lang="en" data-theme="dark"', '<html lang="en" data-theme="light"')

# In pre-paint script, default to light
pattern_prepaint = r"if \(theme !== 'light' && theme !== 'dark'\) \{\s*theme = window\.matchMedia\('[^']+'\)\.matches \? 'light' : 'dark';\s*\}"
replace_prepaint = "if (theme !== 'light' && theme !== 'dark') {\n          theme = 'light';\n        }"
html = re.sub(pattern_prepaint, replace_prepaint, html)

# In resolveInitial, default to light
pattern_resolve = r"return window\.matchMedia\('\(prefers-color-scheme: light\)'\)\.matches \? 'light' : 'dark';"
replace_resolve = "return 'light';"
html = re.sub(pattern_resolve, replace_resolve, html)

with open(r'report/finwise_architecture_light.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Successfully created report/finwise_architecture_light.html')
