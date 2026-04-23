"""Scikit-learn API Contract."""

from aiod.contracts._base import BaseAPIContract


class SklearnClassifier(BaseAPIContract):
    """Contract for scikit-learn classifiers."""
    
    _tags = {
        "scitype_name": "sklearn_classifier",
        "short_descr": "Scikit-learn Classifier Contract",
        "parent_scitype": "classifier"
    }

    @classmethod
    def istypeof(cls, obj):
        """Check if object has fit and predict methods."""
        # Standard sklearn classifiers must have fit and predict/predict_proba
        has_fit = hasattr(obj, "fit")
        has_predict = hasattr(obj, "predict")
        return has_fit and has_predict

    @classmethod
    def runtests(cls, obj):
        """Run basic compliance tests."""
        # In the future, we can wrap sklearn.utils.estimator_checks here
        results = {
            "status": "PASSED",
            "checks": []
        }
        
        if not cls.istypeof(obj):
            results["status"] = "FAILED"
            results["checks"].append("Missing 'fit' or 'predict' methods")
            return results
            
        results["checks"].append("Has 'fit' and 'predict' methods")
        return results
