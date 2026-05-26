"""Base classes for API contracts and validators."""

from skbase.base import BaseObject


class BaseAPIContract(BaseObject):
    """Abstract base class for AIoD API contracts.
    
    This class implements the strategy pattern for API validation.
    """
    
    _tags = {
        "scitype_name": "contract",
        "short_descr": "Base API Contract",
        "parent_scitype": None
    }

    @classmethod
    def istypeof(cls, obj):
        """
        Cursory check: Checks if 'obj' satisfies the contract efficiently.
        
        Parameters
        ----------
        obj : object
            The object to check against the contract.
            
        Returns
        -------
        bool
            True if obj satisfies the contract, False otherwise.
        """
        raise NotImplementedError("Abstract method 'istypeof' must be implemented.")

    @classmethod
    def runtests(cls, obj):
        """
        Full check: Runs a full suite of tests on 'obj'.
        
        Parameters
        ----------
        obj : object
            The object to test.
            
        Returns
        -------
        dict
            Summary of test results.
        """
        raise NotImplementedError("Abstract method 'runtests' must be implemented.")
