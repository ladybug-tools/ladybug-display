import re
pattern = re.compile(r'self.(.*)\s=\s(.*)\(')
doc_str = '        """[{}]\n\n' \
    '        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/{}' \
    '\n        """'

minimal_code = \
    """
        self.href = _str(href, 'href', True)
        self.class_ = _list_of_objs(class_, str, 'class_', True)
    """


init_code, max_code = [], []
for line in minimal_code.splitlines():
    rel_text = pattern.findall(line)
    if len(rel_text) != 0:
        var, var_type = rel_text[0]
        init_code.append('        self.{0} = {0}\n'.format(var))
        var_lines = ['    @property']
        var_lines.append('    def {}(self):'.format(var))
        var_doc = doc_str.format(var_type.strip('_').replace('_', ' '), var.replace('_', '-'))
        var_lines.append(var_doc)
        var_lines.append('        return self._{}\n'.format(var))
        var_lines.append('    @{}.setter'.format(var))
        var_lines.append('    def {}(self, value):'.format(var))
        l_split = line.split('=')
        l_split[1] = l_split[1].replace(var, 'value', 1)
        l_split[0] = l_split[0].replace(var, '_{}'.format(var), 1)
        var_lines.append('='.join(l_split))
        var_lines.append('\n')
        max_code.append('\n'.join(var_lines))

print(''.join(init_code) + '\n' + ''.join(max_code))
