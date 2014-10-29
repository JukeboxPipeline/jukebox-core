"""Module for performing arbitrary actions on objects

A :class:`FileAction` object is a collection of multiple
:class:`ActionUnit`s. When executing the :class:`FileAction` each :class:`ActionUnit` is run.
Later you can query or display the result.
"""
import traceback


class ActionStatus(object):
    """A status object that holds a status value and a short description of what
    the status means.

    So when an action is performed, the action status shows, if the action has been
    successful or failed and also shows why.

    You can query and set 3 attributes:

        :value: the status value as a string
        :message: the status message as a string
        :traceback: in case of an error, the traceback as a string

    Possible status values are :data:`ActionStatus.SUCCESS`, :data:`ActionStatus.SKIPPED`, :data:`ActionStatus.FAILURE`, :data:`ActionStatus.ERROR`
    and None. Before a action gets executed, the status is None
    """

    SUCCESS="Success"
    """Status for when the action succeded"""

    SKIPPED="Skipped"
    """Status for when the action has been skipped, because a dependency was not met"""

    FAILURE="Failure"
    "Status for when the action failed in doing what it should. But the action did not raise an error. So it is like an error that the action expected."

    ERROR="Error"
    """Status for when the action crashed and raised an error."""

    def __init__(self, value=None, msg="Not executed.", traceback=""):
        """Initialize a new action status with the given value, message and traceback

        :param value: The status value
        :type value: :class:`str`
        :param msg: The status message. A better description of the status
        :type msg: :class:`str`
        :param traceback: The traceback if an error occured during action execution.
        :type traceback: :class:`str`
        :raises: None
        """
        self.value = value
        self.message = msg
        self.traceback = traceback


class ActionUnit(object):
    """A single action to be performed on a object.

    Actions might depend on others and only get executed when the dependency
    was successful. Other actions might depend on the failure of another action
    and only get executed when the dependency failed.

    ActionUnit has the following data you can query:

        :name: the name of the action.
        :description: the description of what the action does.
        :status: the status of the action. A :class:`ActionStatus` object.

    .. Note::

       The given object must be ready to be processed. So if the object is a file, the file needs to be opened first,
       create an action that opens the file, and put it as dependency for all other actions.
       The same goes for closing or saving files.
    """

    def __init__(self, name, description, actionfunc, depsuccess=None, depfail=None):
        """Initialize a new action unit that can depends on the success of ``depsucess`` or the
        failure of ``depfail``

        :param name: The name of the action
        :type name: :class:`str`
        :param description: A short description of what the action unit does
        :type description: :class:`str`
        :param actionfunc: A function that takes an object as argument and performs a action.
                           the function should return a :class:`ActionStatus` object
        :type actionfunc: callable
        :param depsuccess: a list of action units that has to succeed first before this action can be executed
        :type depsuccess: list|None
        :param depfail: a list of action units that has to fail first before this action can be executed
        :type depfail: list|None
        :raises: None
        """
        super(ActionUnit, self).__init__()
        self.depsuccess = depsuccess
        self.depfail = depfail
        self.name = name
        self.description = description
        self.status = ActionStatus()
        self.actionfunc = actionfunc

    def run(self, obj):
        """Execute the actions on the given object.

        :param obj: The object that the action should process
        :type obj: :class:`object`
        :returns: None
        :rtype: None
        :raises: None
        """
        if self.depsuccess:
            for d in self.depsuccess:
                if d.status.value != ActionStatus.SUCCESS:
                    self.status.value = ActionStatus.SKIPPED
                    self.status.message = "Skipped because action \"%s\" did not succeed." % d.name
                    return
        if self.depfail:
            for d in self.depfail:
                if d.status.value == ActionStatus.SUCCESS:
                    self.status.value = ActionStatus.SKIPPED
                    self.status.message = "Skipped because action \"%s\" did not fail." % d.name
                    return
        try:
            self.status = self.actionfunc(f)
        except:
            self.status.value = ActionStatus.ERROR
            self.status.message = "Unexpected Error."
            self.status.traceback = traceback.format_exc()


class FileAction(object):
    """Perform a collection of :class:`ActionUnit`s on a object.

    Actions get executed in the given order.

    .. Note::

       The given object must be ready to be processed. So if the object is a file, the file needs to be opened first,
       create an action that opens the file, and put it as dependency for all other actions.
       The same goes for closing or saving files.

    You can access the action objects with these attributes:

      :actions: a list of action units.
    """

    def __init__(self, actions):
        """Initializes a FileAction object.
        The actions will be performed on a object when :meth:`FileAction.execute` is called.

        :param actions: a list of action units
        :type actions: list
        :raises: None
        """
        self.actions = actions

    def execute(self, obj):
        """Run all action units on the given object.

        :param obj: the object to be processed
        :type obj: :class:`object`
        :returns: None
        :rtype: None
        :raises: None
        """
        for a in self.actions:
            a.run(obj)

    def status(self, ):
        """The global status that summerizes all actions

        The status will be calculated in the following order:

          If any error occured, the status will be :data:`ActionStatus.ERROR`.
          If any failure occured, the status will be :data:`ActionStatus.FAILURE`.
          If all actions were successful or skipped, the status will be :data:`ActonStatus.SUCCESS`

        :returns: a status object that represents a summary of all actions
        :rtype: :class:`ActionStatus`
        :raises: None
        """
        status = ActionStatus(ActionStatus.SUCCESS, "All actions succeeded.")
        for a in self.actions:
            if a.status.value == ActionStatus.ERROR:
                status = ActionStatus(ActionStatus.ERROR, "Error: action \"%s\" raised an error!" % a.name, a.status.traceback)
                break
            if a.status.value == ActionStatus.FAILURE:
                status = ActionStatus(ActionStatus.FAILURE, "Action(s) failed!")
        return status
