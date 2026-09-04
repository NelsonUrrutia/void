
class Note:

    def __enter__(self):
        """Allow `with Note() as note:`; returns this instance."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
          """Close the model when the `with` block ends, even on error."""
