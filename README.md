# Timer app

> How about a simple app that times work  you do. timer start timer_name records the current time. When you do a timer stop it tells you elapsed time. You can have multiple timers. You can also have other commands like “reset” (start it at zero) or “cancel” to remove a timer.

## Design

Interface to implement with typer:

timer start name [interactive=False]
- starts timer for activity name, if interactive is True, show timer in
  foreground and user would have to cancel it manually

timer stop name
- stops the timer for name and stores a log entry in a database, raises an exception when name is not found

timer cancel name
- cancels the current name timer in transit, raises an exception when name is
  not found

timer show [name]
- show all the entries + total

timer remove name [all-entries=False]
- remove last timing for activity name, if all-entries is True it removes them
  all
