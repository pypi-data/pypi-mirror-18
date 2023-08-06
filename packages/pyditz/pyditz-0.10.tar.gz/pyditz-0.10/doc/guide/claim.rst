=================
 Claiming Issues
=================

.. highlight:: ditzsession

.. versionadded:: 0.10
   Issue-claiming commands

To avoid the situation where two or more developers inadvertently work on
the same issue at the same time, |PD| allows issues to be *claimed* by a
single developer.  When you :kbd:`claim` an issue, this marks the issue as
'yours' to other developers, and indicates that you'll be resolving it.

.. command: claim prog-1

.. prompt: >
.. reply:  You're my issue now!

.. prompt: >
.. reply:  .

.. literalinclude:: /include/claim1.txt

You can see the issues you've claimed using the :kbd:`mine` command.  It's
like the :kbd:`todo` command, but restricted to just the issues you've
claimed.

.. command: mine

.. literalinclude:: /include/claim2.txt

If another developer tries to claim an issue that's already been claimed by
someone else, |PD| will inform them of the fact, and ask if they really
want to go ahead.  Saying "yes" at that point without prior agreement from
the issue claimer (or other extenuating circumstances) is considered rude.

If you decide, for whatever reason, that you won't be resolving the issue
after all, you can :kbd:`unclaim` it again.  This reverts the issue to
having no claimer, and being up for grabs to others.

To get a summary of who has claimed what issues, you can use the
:kbd:`claimed` command.  This groups the issues by claimer:

.. command: claimed

.. literalinclude:: /include/claim3.txt

The :kbd:`unclaimed` command just lists all the issues that have no claimer
at all:

.. command: unclaimed

.. literalinclude:: /include/claim4.txt

Normally, closed issues are not shown by the :kbd:`mine`, :kbd:`claimed`
and :kbd:`unclaimed` commands.  But if you give the :kbd:`-a` (for 'all')
option, they are.
