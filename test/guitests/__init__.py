"""In here you can test PySide. Just add your test module to this package.

There will be a QApplication ready. Use the QTest module to test user interaction.
"""


def setup_package():
    """Make sure a QApplication is running."""
    import jukeboxcore.gui.main
    jukeboxcore.gui.main.get_qapp()
