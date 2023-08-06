================================
COUNT Down Timer Application
================================

This is the GUI countdown timer.

Install
=======

.. code-block:: sh

  pip install CountDownApp

Usage
=====

The window will be launched when executing the following code.

.. code-block:: python

  from CountDownApp.app import CountDownTimer

  app = CountDownTimer(
    titleText="Title Text", 
    finishTime="2017-01-01 00:00:00",  # Format: YYYY-mm-DD HH:MM:SS
    footerText="Footer Text", 
    baseFontSize=100
  )

  app.run()


