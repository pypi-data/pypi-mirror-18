## Unsupervised Text Segmentation

### Install

    sudo pip install uts

### Usage

```python
import uts

document = ['this is a good day', 'good day means good weather',\
            'I love computer science', 'computer science is cool']
model = uts.C99(window=2)
boundary = model.segment(document)
# output: [1, 0, 1, 0]
print(boundary)
```
