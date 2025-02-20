# Signals-Django
--->Question 1<---
By default, Django signals are executed synchronously. This means that when a signal is sent, the connected receivers are executed in the same thread, one after the other, before the function that triggered the signal completes.
 consider the following example --> Question 1.py
pre_save signal: We’re using the pre_save signal to connect to the model’s save operation.
time.sleep(2) simulates a time-consuming task inside the signal handler.
When we run obj.save(), the pre_save signal is triggered, and the receiver (my_signal_receiver) is executed synchronously.
Expected Output:
  Signal received, starting long task...
  Long task done.
  Model save finished.
The key point here is that the message "Model save finished." won't print until the signal handler (with the sleep delay) finishes execution, proving the synchronous nature of signal handling.
Why does this show that signals are synchronous?
The output indicates that the my_signal_receiver runs completely before the obj.save() function proceeds further. If the signals were executed asynchronously, the "Model save finished" message would have printed before the signal handling finishes.

--->Question 2<---
Yes, by default, Django signals run in the same thread as the caller. This means that when a signal is triggered, the connected signal handlers are executed in the same thread as the code that triggered the signal (e.g., the code calling .save() on a model).

To prove this, we can use the threading module to log the current thread during signal execution. If the signal handler runs in the same thread as the caller, the thread IDs will match.
 Consider the following example --> Question 2.py
Threading: We are using threading.current_thread().name to print the current thread's name, which will show if the signal handler is running in the same thread as the caller.
Simulating Delay: The time.sleep(2) inside the signal handler ensures that the signal handler takes time to complete, allowing us to observe the thread behavior more clearly.
Key Points:
Both the "Signal handler running in thread" and "Signal handler finished in thread" messages show that the signal handler runs in the same thread (MainThread) as the caller (the main thread in this case).
If Django signals were running in a different thread (asynchronously), the thread name would not match, but since it matches, this proves that the signal handler runs in the same thread as the caller by default.
Conclusion:
By default, Django signals are executed in the same thread as the caller. The code above demonstrates this behavior by logging the current thread name during signal handling.


---> Question 3 <---
Yes, by default, Django signals run in the same database transaction as the caller. This means that when you trigger a signal (for example, pre_save or post_save), the signal handler operates within the same transaction as the code that triggered the signal. If the caller's transaction is rolled back, the signal handler's changes will also be rolled back, and vice versa.

To demonstrate this, we can use Django's database transaction management (atomic) along with a signal handler. We'll deliberately cause a transaction to fail and check if the changes from the signal handler are also rolled back.

Consider the following Code Snippet ---> Question 3.py
MyModel: A simple model with a unique constraint on the name field. This ensures that if we try to save two objects with the same name, we will hit a database integrity error.
Signal Handler: The signal handler (my_signal_receiver) is set up to simulate a failure when the object's name is "Error". It raises an IntegrityError to simulate a failure in the signal handler.
Transaction Block: The test_signal_in_transaction function wraps the save operation in a transaction.atomic() block. If any part of the transaction fails (including the signal handler), the entire transaction will be rolled back.
Error Handling: The IntegrityError is caught, and the transaction is rolled back. We check whether the object still exists in the database to verify that the transaction was indeed rolled back.
Signal Handler Rolls Back: Since the signal handler raises an IntegrityError, and the save operation is wrapped in a transaction, the whole transaction (including the signal handler's changes) is rolled back.
Database State: The object with the name "Error" does not remain in the database, demonstrating that the signal handler’s actions were part of the same transaction and were rolled back along with the rest of the transaction.
By default, Django signals run within the same database transaction as the caller. If the transaction is rolled back (e.g., due to an error in the signal handler), all changes (including those made by the signal handler) are also rolled back. The code above demonstrates this behavior conclusively.
