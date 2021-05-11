#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
官方网址: https://palletsprojects.com/p/jinja/

模版文件语法
    {% ... %} for Statements
    {{ ... }} for Expressions to print to the template output
    {# ... #} for Comments not included in the template output
    #  ... ## for Line Statements
'''

import jinja2      #pip3 install jinja2
import sys

def temp_from_string():
    t = jinja2.Environment().from_string(
        '''
        Hello {{name}}! 
        another line     #output
        no comment line  {# not output #}
        ''')
    #t = jinja2.Template('Hello {{name}}!')
    return t
    
def temp_from_file():
    #from ./you-app-python-package/templates
    env = jinja2.Environment(
        loader = jinja2.PackageLoader('you-app-python-package', 'templates'),
    )
    t = env.get_template('mytemplate.html')
    return t


def main():
    t = temp_from_string()

    print("for small template:")
    print(t.render(name="john"))

    print("\n\nfor big template:")
    for res in t.generate(name="john"):
        print(res)

if __name__ == "__main__":
    sys.exit(main())