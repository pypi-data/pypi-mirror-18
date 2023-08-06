
Copy this code and do

    import hanging_threads

If a thread is at the same place for SECONDS_FROZEN then the stacktrace is printed.

This script prints

--------------------    Thread 6628     --------------------
  File "hanging_threads.py", line 70, in <module>
        time.sleep(3) # TEST
--------------------    Thread 6628     --------------------
  File "hanging_threads.py", line 70, in <module>
        time.sleep(3) # TEST



