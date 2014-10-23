from jukeboxcore import main


def test_pipeline_init():
    """ Initialize the Pipeline """
    main.init()


def test_environment_init():
    """ Initialize the environment variables """
    main.init_environment()
