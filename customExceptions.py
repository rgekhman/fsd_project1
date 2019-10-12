class Error(Exception):
    """ base class for other exceptions """
    pass

class CannotRemoveObject(Error):
    """ Raised when cannot remove db object """
    pass    
