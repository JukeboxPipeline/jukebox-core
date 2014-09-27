.. _git:

===
Git
===

Git is our version control system for the sourcecode (`<http://git-scm.com/>`_). Every computer in the CA-Pool should have an installed git version. You can use the git bash for your ordinary git workflow. If you feel more comfortable with a GUI, then you might look into Sourcetree. A good basic git tutorial can be found `here <http://git-scm.com/book>`_.

Please read this `article <http://nvie.com/posts/a-successful-git-branching-model/>`_ about the branching model we use.

Rigth now, we use a simple bare git remote repositry. To share code developers push and pull from this repo. It is currently located under ``L:\pipeline\code\global_repo``.
As a developer you want to have your code in your own sandbox, so you can work independently. Clone the global repository like this::

  git clone L:\pipeline\code\global_repo ./

This will make the current folder the cloned repo. You can edit code and push it back with::

  git push origin <branch>

When another developer updates the global repository, you have to pull the changes first::

  git pull origin <branch>

There are also two checkouts for beta and live code. These repositories hold the code, that all users use by default.
Have a look at the :ref:`Launcher <launcher>` section on how to use your sandbox code in production.
