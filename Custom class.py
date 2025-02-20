class Rectangle:
    def __init__(self, length: int, width: int):
        # Initialize the rectangle with length and width
        self.length = length
        self.width = width

    def __iter__(self):
        # Define how the Rectangle is iterated over
        yield {'length': self.length}  # Yield the length first
        yield {'width': self.width}    # Then yield the width

# Example usage
rectangle = Rectangle(10, 5)

for attribute in rectangle:
    print(attribute)
