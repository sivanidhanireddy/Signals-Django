import threading
import time
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models

# A signal receiver that logs the current thread and adds a delay
@receiver(pre_save)
def my_signal_receiver(sender, instance, **kwargs):
    print(f"Signal handler running in thread: {threading.current_thread().name}")
    time.sleep(2)  # Simulating a delay to emphasize thread behavior
    print(f"Signal handler finished in thread: {threading.current_thread().name}")

# A simple model for triggering the signal
class MyModel(models.Model):
    name = models.CharField(max_length=100)

# Triggering the signal in the main thread
if __name__ == "__main__":
    print(f"Main thread: {threading.current_thread().name}")

    # Creating an instance to trigger the signal
    obj = MyModel(name="Test")
    obj.save()  # This will trigger the pre_save signal

    print("Model save finished.")
