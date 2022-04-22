# -*- coding:utf-8 -*-
# Author: xiaohao@corp.netease.com
# Date: 2022-04-22 16:22:10
"""
ORM应用
"""


class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__, self.name)


class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')


class IntField(Field):
    def __init__(self, name):
        super(IntField, self).__init__(name, 'bigint')


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        print('Found model :%s' % name)
        mapping = {}
        for k, v in attrs.items():
            if isinstance(v, Field):
                print('Found mapping:%s ==> %s' % (k, v))
                mapping[k] = v
        for k in mapping:
            attrs.pop(k)
        attrs['__mappings__'] = mapping
        attrs['__table__'] = name
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError('Model object ha no attribute: %s' % item)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            params.append('?')
            args.append(self[k])
            # args.append(getattr(self,k,None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL:%s' % sql)
        print('ARGS: %s' % str(args))


class UserModel(Model):
    id = IntField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('pwd')


user = UserModel(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
print(dir(user))
print(user.__dict__)
print(user.id, user.name, user.email, user.password)
# user.save()
