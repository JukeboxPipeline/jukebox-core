from datetime import datetime

import pytest
from nose.tools import eq_
from PySide import QtCore, QtGui

from jukeboxcore.gui import main


class Test_JBGui():
    @classmethod
    def setup_class(cls):
        class Foo(main.JB_Gui):
            pass

        class Bar(main.JB_Gui):
            pass

        class FooBar(Foo, Bar):
            pass

        cls.Foo = Foo
        cls.Bar = Bar
        cls.FooBar = FooBar

    def test_trackinstances(self):
        main.JB_Gui._allinstances = set()
        assert len(main.JB_Gui.allinstances()) == 0
        assert len(main.JB_Gui.instances()) == 0
        assert len(main.JB_Gui.classinstances()) == 0
        jb1 = main.JB_Gui()
        assert len(main.JB_Gui.allinstances()) == 1
        assert jb1 in main.JB_Gui.allinstances()
        assert len(main.JB_Gui.instances()) == 1
        assert jb1 in main.JB_Gui.instances()
        assert len(main.JB_Gui.classinstances()) == 1
        assert jb1 in main.JB_Gui.classinstances()
        assert len(self.Foo.allinstances()) == 1
        assert jb1 in self.Foo.allinstances()
        assert len(self.Foo.instances()) == 0
        assert len(self.Foo.classinstances()) == 0
        jb2 = main.JB_Gui()
        assert len(main.JB_Gui.allinstances()) == 2
        assert jb2 in main.JB_Gui.allinstances()
        assert len(main.JB_Gui.instances()) == 2
        assert jb2 in main.JB_Gui.instances()
        assert len(main.JB_Gui.classinstances()) == 2
        assert jb2 in main.JB_Gui.classinstances()
        assert len(self.Foo.allinstances()) == 2
        assert jb2 in self.Foo.allinstances()

        f1 = self.Foo()
        assert len(main.JB_Gui.allinstances()) == 3
        assert f1 in main.JB_Gui.allinstances()
        assert len(main.JB_Gui.instances()) == 3
        assert f1 in main.JB_Gui.instances()
        assert len(self.Foo.allinstances()) == 3
        assert f1 in self.Foo.allinstances()
        assert len(self.Foo.classinstances()) == 1
        assert f1 in self.Foo.classinstances()
        assert f1 not in main.JB_Gui.classinstances()
        f2 = self.Foo()
        assert len(main.JB_Gui.allinstances()) == 4
        assert f2 in main.JB_Gui.allinstances()
        assert len(main.JB_Gui.instances()) == 4
        assert f2 in main.JB_Gui.instances()
        assert len(self.Foo.allinstances()) == 4
        assert f2 in self.Foo.allinstances()
        assert len(self.Foo.instances()) == 2
        assert f2 in self.Foo.instances()
        assert len(self.Foo.classinstances()) == 2
        assert f2 in self.Foo.classinstances()
        assert f2 not in main.JB_Gui.classinstances()

        fb1 = self.FooBar()
        assert len(main.JB_Gui.allinstances()) == 5
        assert fb1 in main.JB_Gui.allinstances()
        assert len(main.JB_Gui.instances()) == 5
        assert fb1 in main.JB_Gui.instances()
        assert len(self.Foo.allinstances()) == 5
        assert fb1 in self.Foo.allinstances()
        assert len(self.Foo.instances()) == 3
        assert fb1 in self.Foo.instances()
        assert len(self.FooBar.allinstances()) == 5
        assert fb1 in self.FooBar.allinstances()
        assert len(self.Foo.classinstances()) == 2
        assert fb1 not in self.Foo.classinstances()
        assert len(self.FooBar.classinstances()) == 1
        assert fb1 in self.FooBar.classinstances()
        assert fb1 not in main.JB_Gui.classinstances()
        assert len(self.Bar.classinstances()) == 0
        assert fb1 not in self.Bar.classinstances()


class Test_JB_MainWindow():
    def test_inheritance(self):
        jbmw = main.JB_MainWindow(flags=QtCore.Qt.WindowStaysOnTopHint)
        assert jbmw in jbmw.instances()
        assert jbmw.windowFlags() & QtCore.Qt.WindowStaysOnTopHint == QtCore.Qt.WindowStaysOnTopHint


def test_dt_to_qdatetime():
    now = datetime.now()
    qdt = QtCore.QDateTime(QtCore.QDate(now.year, now.month, now.day),
                           QtCore.QTime(now.hour, now.minute, now.second))
    eq_(main.dt_to_qdatetime(now), qdt)


@pytest.mark.parametrize("args,expected",[((False, False), basestring),
                                          ((True, False), QtGui.QPixmap),
                                          ((False, True), QtGui.QIcon),
                                          ((True, True), QtGui.QIcon),
                                        ])
def test_get_icon(args, expected):
    name = "glyphicons_003_user.png"
    icon = main.get_icon(name, aspix=args[0], asicon=args[1])
    assert isinstance(icon, expected)
