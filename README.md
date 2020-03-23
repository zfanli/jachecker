# jachecker

Java checker in customized rules.

# Before parse

Some special cases should do escape first. The targets are shown below.

Escape operation will be done by parser before parse into AST.

- \" -> JC_ESCAPED_QUOTE (String literals only)

Escaped contents will be unescaped after parsed into string.

### Dependencies

- pyPEG2
- pytest
- pytest-cov
