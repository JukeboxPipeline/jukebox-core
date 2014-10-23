import os

from nose.tools import eq_

from jukeboxcore import filesys, djadapter


class Test_FileElement():

    @classmethod
    def setup_class(cls):
        cls.fe = filesys.FileElement()

    def test_get_dir(self):
        assert self.fe.get_dir(object()) is None

    def test_get_chunk(self):
        assert self.fe.get_chunk(object()) is None


class Test_StaticElement():

    @classmethod
    def setup_class(cls):
        cls.se1 = filesys.StaticElement()
        cls.se2 = filesys.StaticElement(dirname='dir1')
        cls.se3 = filesys.StaticElement(chunk='chunk1')
        cls.se4 = filesys.StaticElement(dirname='2dir', chunk='2chunk')
        cls.obj = object()

    def test_get_dir(self):
        eq_(self.se1.get_dir(self.obj), None)
        eq_(self.se2.get_dir(self.obj), 'dir1')
        eq_(self.se3.get_dir(self.obj), None)
        eq_(self.se4.get_dir(self.obj), '2dir')

    def test_get_chunk(self):
        eq_(self.se1.get_chunk(self.obj), None)
        eq_(self.se2.get_chunk(self.obj), None)
        eq_(self.se3.get_chunk(self.obj), 'chunk1')
        eq_(self.se4.get_chunk(self.obj), '2chunk')


class Test_AttrElement():

    @classmethod
    def setup_class(cls):
        cls.o = type('Testobj', (object,), {})()
        cls.o.dattr1 = 'Rampage'
        cls.o.dattr2 = 'Killspree'
        cls.o.dattr3 = None
        cls.o.cattr1 = 'ram'
        cls.o.cattr2 = 'kill'
        cls.o.cattr3 = None
        cls.ae1 = filesys.AttrElement()
        cls.ae2 = filesys.AttrElement('dattr1', 'cattr1', 'Seq%s', 'seq%s')
        cls.ae3 = filesys.AttrElement('dattr2', dirformat='Shot%s', chunkformat='shot%s')
        cls.ae4 = filesys.AttrElement(chunkattr='cattr2')
        cls.ae5 = filesys.AttrElement('dattr3', 'cattr3')

    def test_get_dir(self):
        eq_(self.ae1.get_dir(self.o), None)
        eq_(self.ae2.get_dir(self.o), 'SeqRampage')
        eq_(self.ae3.get_dir(self.o), 'ShotKillspree')
        eq_(self.ae4.get_dir(self.o), None)
        eq_(self.ae5.get_dir(self.o), None)

    def test_get_chunk(self):
        eq_(self.ae1.get_chunk(self.o), None)
        eq_(self.ae2.get_chunk(self.o), 'seqram')
        eq_(self.ae3.get_chunk(self.o), None)
        eq_(self.ae4.get_chunk(self.o), 'kill')
        eq_(self.ae5.get_chunk(self.o), None)


class Test_SoftwareElement():
    @classmethod
    def setup_class(cls):
        task = djadapter.models.Task()
        cls.tfio = filesys.TaskFileInfo(task, 10, djadapter.RELEASETYPES['release'], 'mayamainscene')
        cls.se = filesys.SoftwareElement()

    def test_getdir(self):
        eq_(self.se.get_dir(self.tfio), 'Maya')


class Test_TaskGroupElement():
    @classmethod
    def setup_class(cls):
        cls.prj = djadapter.projects.create(name="Pixars Plants", short='plants', _path='plantpath', semester='SS14')
        seq = djadapter.sequences.create(name='Seq01', project=cls.prj)
        shot = djadapter.shots.create(name='Shot01', project=cls.prj, sequence=seq)
        cls.at = djadapter.atypes.create(name='matte')
        asset = djadapter.assets.create(name='background', atype=cls.at, project=cls.prj)
        cls.dep1 = djadapter.departments.create(name="Layout", short="lay", assetflag=False)
        cls.dep2 = djadapter.departments.create(name="Design", short="des", assetflag=True)
        task1 = djadapter.tasks.create(department=cls.dep1, project=cls.prj, status='New', element=shot)
        task2 = djadapter.tasks.create(department=cls.dep2, project=cls.prj, status='New', element=asset)

        cls.tfio1 = filesys.TaskFileInfo(task1, 10, djadapter.RELEASETYPES['release'], 'mayamainscene')
        cls.tfio2= filesys.TaskFileInfo(task2, 10, djadapter.RELEASETYPES['release'], 'mayamainscene')
        cls.tge = filesys.TaskGroupElement()

    @classmethod
    def teardown_class(cls):
        cls.prj.delete()
        cls.at.delete()
        cls.dep1.delete()
        cls.dep2.delete()

    def test_getdir(self):
        eq_(self.tge.get_dir(self.tfio1), os.path.normpath('shots/Seq01'))
        eq_(self.tge.get_dir(self.tfio2), os.path.normpath('assets/matte'))


class Test_ExtElement():

    @classmethod
    def setup_class(cls):
        cls.ee = filesys.ExtElement()

    def test_raiseerrors(self):
        try:
            self.ee.get_ext(object())
            assert False, "ExtElement should raise an NotImplementedError"
        except NotImplementedError:
            pass


class Test_StaticExtElement():

    def test_get_ext(self):
        see = filesys.StaticExtElement('abc')
        eq_(see.get_ext(object()), 'abc')


class Test_TaskFileExtElement():

    def test_get_ext(self):
        tfio = filesys.TaskFileInfo(None, None, None, 'mayamainscene')
        tfee = filesys.TaskFileExtElement()
        eq_(tfee.get_ext(tfio), 'mb')


class Test_JB_File(object):

    @classmethod
    def setup_class(cls):
        Fi = type('RandomFileInfo', (object,), {})
        cls.o = Fi()
        cls.o.o2 = type('Testobj', (object,), {})()
        cls.o.attr1 = 123
        cls.o.attr2 = 'release'
        cls.o.attr3 = 'shot02'
        cls.o.o2.attr4 = 'uz'
        cls.ae1 = filesys.AttrElement('attr1', 'attr3')
        cls.ae2 = filesys.AttrElement('attr2', 'attr2')
        cls.ae3 = filesys.AttrElement('attr3', 'attr1')
        cls.ae4 = filesys.AttrElement('o2.attr4', 'o2.attr4')
        filesys.JB_File.ELEMENTPRESETS[Fi] = [cls.ae1, cls.ae2, cls.ae3, cls.ae4]
        filesys.JB_File.EXTENSIONS[Fi] = filesys.StaticExtElement('mb')

    def setup(self):
        self.jbf1 = filesys.JB_File(self.o)

    def test_get_ext(self):
        eq_(self.jbf1.get_ext(), 'mb')

    def test_get_path(self):
        eq_(self.jbf1.get_path(), os.path.normpath('123/release/shot02/uz'))

    def test_get_name(self):
        eq_(self.jbf1.get_name(), 'shot02_release_123_uz.mb')
        eq_(self.jbf1.get_name(withext=False), 'shot02_release_123_uz')

    def test_fullpath(self):
        eq_(self.jbf1.get_fullpath(), os.path.normpath('123/release/shot02/uz/shot02_release_123_uz.mb'))
        eq_(self.jbf1.get_fullpath(withext=False), os.path.normpath('123/release/shot02/uz/shot02_release_123_uz'))

    def test_get_obj(self):
        assert self.jbf1.get_obj() is self.o

    def test_set_obj(self):
        self.jbf1.set_obj('Testobj')
        eq_(self.jbf1.get_obj(), 'Testobj')


class Test_FileInfo():
    def test_raiseerrors(self):
        try:
            filesys.FileInfo.get_latest()
            assert False, "get_latest should be abstract"
        except NotImplementedError:
            pass
        try:
            filesys.FileInfo.get_next()
            assert False, "get_next should be abstract"
        except NotImplementedError:
            pass


class Test_TaskFileInfo():
    @classmethod
    def setup_class(cls):
        cls.prj = djadapter.projects.create(name="Pixars Plants", short='plants', _path='plantpath', semester='SS14')
        cls.seq = djadapter.sequences.create(name='Seq01', project=cls.prj)
        cls.shot = djadapter.shots.create(name='Shot01', project=cls.prj, sequence=cls.seq)
        cls.dep1 = djadapter.departments.create(name="Design", short="des", assetflag=False)
        cls.dep2 = djadapter.departments.create(name="Destruction", short="buum", assetflag=False)
        cls.task1 = djadapter.tasks.create(department=cls.dep1, project=cls.prj, status='New', element=cls.shot)
        cls.task2 = djadapter.tasks.create(department=cls.dep2, project=cls.prj, status='New', element=cls.shot)
        cls.usr = djadapter.users.create_user(username='Uz')
        cls.tf1 = djadapter.taskfiles.create(user=cls.usr, path='relpath1', task=cls.task1, version=1,
                                             releasetype=djadapter.RELEASETYPES['release'],
                                             typ=filesys.TaskFileInfo.TYPES['mayamainscene'])
        cls.tf2 = djadapter.taskfiles.create(user=cls.usr, path='relpath2', task=cls.task1, version=2,
                                             releasetype=djadapter.RELEASETYPES['release'],
                                             typ=filesys.TaskFileInfo.TYPES['mayamainscene'])
        cls.tf3 = djadapter.taskfiles.create(user=cls.usr, path='relpath3', task=cls.task1, version=3,
                                             releasetype=djadapter.RELEASETYPES['release'],
                                             typ=filesys.TaskFileInfo.TYPES['mayamainscene'])
        cls.tf4 = djadapter.taskfiles.create(user=cls.usr, path='workpath1', task=cls.task2, version=1,
                                             releasetype=djadapter.RELEASETYPES['work'], descriptor='take1',
                                             typ=filesys.TaskFileInfo.TYPES['mayamainscene'])
        cls.tf5 = djadapter.taskfiles.create(user=cls.usr, path='workpath2', task=cls.task2, version=2,
                                             releasetype=djadapter.RELEASETYPES['work'], descriptor='take1',
                                             typ=filesys.TaskFileInfo.TYPES['mayamainscene'])
        cls.tf6 = djadapter.taskfiles.create(user=cls.usr, path='workpath3', task=cls.task2, version=1,
                                             releasetype=djadapter.RELEASETYPES['work'], descriptor='take2',
                                             typ=filesys.TaskFileInfo.TYPES['mayamainscene'])
        #cls.tfio = filesys.TaskFileInfo(cls.task, 10, djadapter.RELEASETYPES['release'])

    @classmethod
    def teardown_class(cls):
        cls.prj.delete()
        cls.dep1.delete()
        cls.dep2.delete()
        cls.usr.delete()

    def test_get_latest(self):
        typ = filesys.TaskFileInfo.TYPES['mayamainscene']
        latest1 = filesys.TaskFileInfo.get_latest(self.task1, djadapter.RELEASETYPES['release'], typ)
        eq_(latest1.version, 3)
        eq_(latest1.task, self.task1)
        eq_(latest1.releasetype, djadapter.RELEASETYPES['release'])
        eq_(latest1.descriptor, None)
        eq_(latest1.typ, typ)

        latest2 = filesys.TaskFileInfo.get_latest(self.task2, djadapter.RELEASETYPES['work'], typ, descriptor='take1')
        eq_(latest2.version, 2)
        eq_(latest2.task, self.task2)
        eq_(latest2.releasetype, djadapter.RELEASETYPES['work'])
        eq_(latest2.descriptor, 'take1')
        eq_(latest2.typ, typ)

        latest3 = filesys.TaskFileInfo.get_latest(self.task2, djadapter.RELEASETYPES['work'], typ, descriptor='take2')
        eq_(latest3.version, 1)
        eq_(latest3.task, self.task2)
        eq_(latest3.releasetype, djadapter.RELEASETYPES['work'])
        eq_(latest3.descriptor, 'take2')
        eq_(latest3.typ, typ)

        assert filesys.TaskFileInfo.get_latest(self.task2, djadapter.RELEASETYPES['handoff'], typ, descriptor='take2') is None
        assert filesys.TaskFileInfo.get_latest(self.task2, djadapter.RELEASETYPES['work'], typ, descriptor='take3') is None

    def test_get_next(self):
        typ = filesys.TaskFileInfo.TYPES['mayamainscene']
        next1 = filesys.TaskFileInfo.get_next(self.task1, djadapter.RELEASETYPES['release'], typ)
        eq_(next1.version, 4)
        eq_(next1.task, self.task1)
        eq_(next1.releasetype, djadapter.RELEASETYPES['release'])
        eq_(next1.descriptor, None)
        eq_(next1.typ, typ)

        next2 = filesys.TaskFileInfo.get_next(self.task2, djadapter.RELEASETYPES['work'], typ, descriptor='take1')
        eq_(next2.version, 3)
        eq_(next2.task, self.task2)
        eq_(next2.releasetype, djadapter.RELEASETYPES['work'])
        eq_(next2.descriptor, 'take1')
        eq_(next2.typ, typ)

        next3 = filesys.TaskFileInfo.get_next(self.task2, djadapter.RELEASETYPES['work'], typ, descriptor='take2')
        eq_(next3.version, 2)
        eq_(next3.task, self.task2)
        eq_(next3.releasetype, djadapter.RELEASETYPES['work'])
        eq_(next3.descriptor, 'take2')
        eq_(next3.typ, typ)

        next4 = filesys.TaskFileInfo.get_next(self.task2, djadapter.RELEASETYPES['handoff'], typ, descriptor='take2')
        eq_(next4.version, 1)
        eq_(next4.task, self.task2)
        eq_(next4.releasetype, djadapter.RELEASETYPES['handoff'])
        eq_(next4.descriptor, 'take2')
        eq_(next4.typ, typ)

        next5 = filesys.TaskFileInfo.get_next(self.task2, djadapter.RELEASETYPES['work'], typ, descriptor='take3')
        eq_(next5.version, 1)
        eq_(next5.task, self.task2)
        eq_(next5.releasetype, djadapter.RELEASETYPES['work'])
        eq_(next5.descriptor, 'take3')
        eq_(next5.typ, typ)
