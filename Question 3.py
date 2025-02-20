from django.db import models, transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import IntegrityError

# A simple model with a unique constraint to simulate an integrity error
class MyModel(models.Model):
    name = models.CharField(max_length=100, unique=True)

# Signal handler that tries to modify a field, simulating a database change
@receiver(pre_save)
def my_signal_receiver(sender, instance, **kwargs):
    print("Signal handler running.")
    # Trying to change something in the database that will conflict
    if instance.name == "Error":
        raise IntegrityError("Simulated error during signal handling.")

# Function to test if the signal runs within the same transaction
def test_signal_in_transaction():
    try:
        # Wrapping the save operation in a transaction
        with transaction.atomic():
            print("Starting transaction.")
            # Create and save an object, which will trigger the pre_save signal
            obj = MyModel(name="Error")
            obj.save()
            print("Model saved.")
    except IntegrityError:
        print("IntegrityError caught. Rolling back transaction.")
    finally:
        # Checking if the object exists in the database
        if MyModel.objects.filter(name="Error").exists():
            print("Object still exists in the database (transaction not rolled back).")
        else:
            print("Object not found in the database (transaction rolled back).")

# Running the test
if __name__ == "__main__":
    test_signal_in_transaction()
