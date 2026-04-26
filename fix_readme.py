import re

with open('README.md', 'r') as f:
    content = f.read()

# Remove trailing whitespaces specifically from these lines
content = content.replace(
    '**Signaler un bug** → [ouvrir une issue](https://github.com/nickdesi/FFBBApiClientV3/issues)  \n',
    '**Signaler un bug** → [ouvrir une issue](https://github.com/nickdesi/FFBBApiClientV3/issues)\n'
)
content = content.replace(
    '**Proposer une feature** → [discussions](https://github.com/nickdesi/FFBBApiClientV3/discussions)  \n',
    '**Proposer une feature** → [discussions](https://github.com/nickdesi/FFBBApiClientV3/discussions)\n'
)

with open('README.md', 'w') as f:
    f.write(content)
