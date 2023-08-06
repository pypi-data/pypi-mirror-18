# -*- encoding=utf-8 -*-
from django import template

import re
register = template.Library()
@register.tag(name="ifequals")
def do_ifequals(parser,token):
    """
    可以传入多个对象，如果这些对象的str都是相同的，那么就显示块内的html代码
    :param parser:
    :param token:
    :return:
    """
    objs=token.split_contents()
    objs.pop(0)
    vars=[]
    for obj in objs:
        vars.append(template.Variable(obj))
    nodelist = parser.parse(('endifequals',))
    parser.delete_first_token()
    return IfEqualsNode(nodelist,vars)
class IfEqualsNode(template.Node):
    def __init__(self,nodelist,vars):
        self.nodelist=nodelist
        self.vars=vars
    def render(self,context):
        equals = True
        vars=[]
        for var in self.vars:
            if not var:
                equals=False
                break
            try:
                vars.append(var.resolve(context))
            except template.VariableDoesNotExist as e:
                print(e)
                equals = False
                break
        for i in range(len(vars)):
            if not equals: break
            for j in range(i):

                if str(vars[i]) != str(vars[j]):
                    equals = False
                    break
        if equals:
            return self.nodelist.render(context)
        else:
            return ''


class ShowNode(template.Node):
    def __init__(self, nodelist,show=True):
        self.nodelist = nodelist
        self.show=show
    def render(self, context):
        output = self.nodelist.render(context)
        return output
