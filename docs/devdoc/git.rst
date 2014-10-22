.. _git:

===
Git
===

Git is our version control system for the sourcecode (`<http://git-scm.com/>`_). Every computer in the CA-Pool should have an installed git version.
You can use the git bash for your ordinary git workflow. If you feel more comfortable with a GUI, then you might look into Sourcetree.
A good basic git tutorial can be found `here <http://git-scm.com/book>`_.

Please read this article_ about the branching model we use.
I recommend using gitflow_. Git flow is a set of commands for git, that perform high level repository operations.
It is basically an implementation of the branching model, with simpler commands.
To use it in your gitbash on windows, might be a little bit troublesome.
There is a nice tutorial_ on how to install gitflow_ on Windows.

Rigth now, we use a simple bare git remote repositry. To share code developers push and pull from this repo.
It is currently located under ``L:\pipeline\code\global_repo``.
As a developer you want to have your code in your own sandbox, so you can work independently. Clone the global repository like this::

  git clone L:\pipeline\code\global_repo ./

This will make the current folder the cloned repo. You can edit code and push it back with::

  git push origin <branch>

When another developer updates the global repository, you have to pull the changes first::

  git pull origin <branch>

--------
Git Flow
--------

Initialize your cloned repository for git flow with::

  $ git flow init

Choose ``master`` for master branches and instead of ``develop`` use ``dev``. Version prefix is ``v``.
Now you can use::

  $ git flow feature start <featurename>

and all other git flow commands. See this useful and BEATIFUL `cheatsheet <http://danielkummer.github.io/git-flow-cheatsheet/>`_ for more information.


.. _article: http://nvie.com/posts/a-successful-git-branching-model/
.. _tutorial: http://xinyustudio.wordpress.com/2012/03/26/installing-git-flow-in-windows/
.. _gitflow: https://github.com/nvie/gitflow
