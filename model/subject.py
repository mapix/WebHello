# coding: utf-8

from datetime import datetime


class Subject(object):

    def __init__(self, id, text, create_time=None, update_time=None):
        self.subject_id = str(id)
        self.subject_text = text
        self.create_time = create_time
        self.update_time = update_time

    @classmethod
    def new(cls, text):
        create_time = datetime.now()
        default = {}
        default.update(subject_id='2', subject_text=text,
                create_time=create_time,
                update_time=create_time)
        print default
        # TODO:存取条目

    @classmethod
    def get_by_id(cls, id):
        # TODO:查询存储系统，然后返回
        pass

    @classmethod
    def get_all_subject(cls):
        #TODO:全部返回
        pass

    def update(self, text=''):
        update = {}
        if text:
            update.update(text=text)
        if update:
            update.update(update_time=datetime.now())
        #TODO:更新存储系统里面相应条目

