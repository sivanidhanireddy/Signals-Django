from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.management import call_command
import time

# Simulating a signal receiver that takes time to execute
@receiver(pre_save)
def my_signal_receiver(sender, instance, **kwargs):
    print("Signal received, starting long task...")
    time.sleep(2)  # Simulating a delay, like a long-running task
    print("Long task done.")

# A simple model for triggering the signal
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)

# In a view or shell, triggering the signal:
if __name__ == "__main__":
    # Creating an instance to trigger the signal
    obj = MyModel(name="Test")
    obj.save()  # This will trigger the pre_save signal

    print("Model save finished.")
