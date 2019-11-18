#!/usr/bin/env python
import os
import re

for root, dirs, files in os.walk('_posts'):
  for file in list(filter(lambda file: file.endswith('.md'), files)):
    with open(os.path.join(root, file)) as rf:
      for line in rf.readlines():
        m = re.match(r'^tags\s*:\s*\[(.+)\]\s*$', line)
        if m:
          for tag in re.findall(r'\w+', m.group(1)):
            tag_path = '_tags/%s.md' % tag
            if os.path.exists(tag_path):
              print('skip:', tag)
              continue

            with open(tag_path, 'w+') as f:
              f.write('---\nname: %s\n---\n' % tag)
              print('create:', tag)
