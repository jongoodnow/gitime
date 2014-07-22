Timer
====

Start the timer, pause it, or reset it. The timer is reset automatically when you make a commit.

Usage
----

	gitime timer [-h] [--force] {start,pause,reset,status}

Details
----

The timer is reset automatically when you make a commit. You will need to start the timer again after making a commit. Using the timer is optional. You can also use the `--hours` option when committing to specify the hours yourself.

Subcommands
----

####start

Starts or restarts the timer, resuming from pause of necessary.

####pause

Stops the timer, allowing you to restart with `start`.

####reset

Stop the timer and set the time recorded to zero.

####status

Show if the timer is running, and how much time it has recorded.

Options
----

####--force, -f

The timer will not start if you do not have any invoices because it will have nowhere to record the time when you commit otherwise. If you want to start the timer anyway, use this flag to suppress that warning.

####--help, -h

Display a help message.