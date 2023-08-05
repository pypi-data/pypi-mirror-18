Code Pretty Extension for Python Markdown
=====================================================

Adds enhenced code/syntax highlighting to standard Python-Markdown code blocks.

## Installation

```sh
pip install python-markdown-pretty
```

## Usage

To use (with caution), simply do:

```python
import markdown

code = r'''
```c
int main(int argc, char* argv[]) {
    return 0;
}
```'''

md = markdown.Markdown(extensions=['pretty'])
print md.convert(code)
```

