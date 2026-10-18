import os

paths = [
    r'C:\Users\anshu\.gemini\config\skills\archify\renderers\shared\atomic-output.mjs',
    r'C:\Users\anshu\.agents\skills\archify\renderers\shared\atomic-output.mjs',
    r'C:\Users\anshu\AppData\Roaming\npm\node_modules\archify\renderers\shared\atomic-output.mjs'
]

for p in paths:
    if not os.path.exists(p):
        continue
    with open(p, 'r', encoding='utf-8') as f:
        t = f.read()

    t = t.replace('beforeHandle.dev !== identity.device', "(process.platform !== 'win32' && beforeHandle.dev !== identity.device)")
    t = t.replace('afterHandle.dev !== identity.device', "(process.platform !== 'win32' && afterHandle.dev !== identity.device)")
    t = t.replace('handle.dev !== initial.dev', "(process.platform !== 'win32' && handle.dev !== initial.dev)")

    with open(p, 'w', encoding='utf-8') as f:
        f.write(t)
    print('Patched successfully:', p)
