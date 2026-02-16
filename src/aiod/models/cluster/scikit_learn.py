"""Sklearn clusters."""

from aiod.models.apis import _ModelPkgCluster


class AiodPkg__SklearnClusters(_ModelPkgCluster):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "scikit-learn",
        "pkg_pypi_name": "scikit-learn",
    }

    _obj_dict ={
        'AffinityPropagation': 'sklearn.cluster._affinity_propagation.AffinityPropagation',
        'AgglomerativeClustering': 'sklearn.cluster._agglomerative.AgglomerativeClustering',
        'Birch': 'sklearn.cluster._birch.Birch',
        'BisectingKMeans': 'sklearn.cluster._bisect_k_means.BisectingKMeans',
        'DBSCAN': 'sklearn.cluster._dbscan.DBSCAN',
        'FeatureAgglomeration': 'sklearn.cluster._agglomerative.FeatureAgglomeration',
        'HDBSCAN': 'sklearn.cluster._hdbscan.hdbscan.HDBSCAN',
        'KMeans': 'sklearn.cluster._kmeans.KMeans',
        'MeanShift': 'sklearn.cluster._mean_shift.MeanShift',
        'MiniBatchKMeans': 'sklearn.cluster._kmeans.MiniBatchKMeans',
        'OPTICS': 'sklearn.cluster._optics.OPTICS',
        'SpectralClustering': 'sklearn.cluster._spectral.SpectralClustering'
    }