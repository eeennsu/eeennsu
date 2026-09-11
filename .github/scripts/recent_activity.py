"""events.json 의 PushEvent 에서 최근에 손댄 저장소 3개를 뽑아 README 마커 사이를 갈아끼운다."""

import json
import os
import re

OWNER = os.environ.get('OWNER', 'eeennsu')
MARKER = re.compile(r'(<!-- recent:start -->).*?(<!-- recent:end -->)', re.S)

seen = []
for event in json.load(open('events.json')):
    if event['type'] != 'PushEvent':
        continue
    full_name = event['repo']['name']  # owner/repo
    # 프로필 저장소 자신은 카드 자동 커밋 때문에 항상 최상단이라 뺀다
    if full_name.split('/')[-1] == OWNER or full_name in seen:
        continue
    seen.append(full_name)

recent = seen[:3]
if recent:
    line = ' · '.join(f'[{f.split("/")[-1]}](https://github.com/{f})' for f in recent)
    readme = open('README.md').read()
    patched = MARKER.sub(lambda m: m.group(1) + line + m.group(2), readme)
    if patched != readme:
        open('README.md', 'w').write(patched)
