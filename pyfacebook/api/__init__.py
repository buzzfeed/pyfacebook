from tinymodel import TinyModel


class Model(TinyModel):
    ATTACHED_ATTRIBUTES = ['_fb']

    def __init__(self, **kwargs):
        self._fb = kwargs.pop('fb', None)
        super(Model, self).__init__(**kwargs)

    def __setattr__(self, name, value):
        if name in super(TinyModel, self).__getattribute__('ATTACHED_ATTRIBUTES'):
            return super(TinyModel, self).__setattr__(name, value)
        return super(Model, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name in super(TinyModel, self).__getattribute__('ATTACHED_ATTRIBUTES'):
            return super(TinyModel, self).__getattribute__(name)
        return super(Model, self).__getattr__(name)

    @property
    def FIELDS_NAME_LIST(self):
        return [f.field_def.title for f in self.FIELDS]
