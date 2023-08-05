from ..exceptions import PyBelWarning, PyBelError


class IllegalAnnotationValueExeption(PyBelWarning):
    """Raised when an annotation has a value that does not belong to the original set of valid annotation values."""
    #:
    code = 1


class InvalidCitationException(PyBelWarning):
    """Raised when the format for a citation is wrong. It should have either {type, name, reference}; or {type, name, reference, date, authors, comments}"""
    #:
    code = 11


class NestedRelationNotSupportedException(PyBelWarning):
    """Raised when encountering a nested statement. See our wiki for an explanation of why we explicitly do not support nested statements."""
    #:
    code = 18


class IllegalNamespaceException(PyBelWarning):
    """Raised if reference made to undefined namespace"""
    #:
    code = 31


class IllegalNamespaceNameException(PyBelWarning):
    """Raised if reference to value not in namespace"""
    #:
    code = 32


class IllegalDefaultNameException(PyBelWarning):
    """Raised if reference to value not in default namespace"""
    #:
    code = 33


class PlaceholderAminoAcidException(PyBelWarning):
    """Raised for a placeholder amino acid (X)"""
    #:
    code = 15


class NakedNamespaceException(PyBelWarning):
    """Raised when there is an identifier without a namespace. Enable lenient mode to suppress"""
    #:
    code = 21


class IllegalTranslocationException(PyBelWarning):
    """Raised when there is a translocation statement without location information."""
    #:
    code = 8


class InvalidAnnotationKeyException(PyBelWarning):
    """Raised when an undefined annotation is used"""
    #:
    code = 20


class MissingAnnotationKeyException(PyBelWarning):
    """Raised when trying to unset an annotation that is not set"""
    #:
    code = 30


class LexicographyException(PyBelWarning):
    """Improper capitalization"""
    #:
    code = 34
