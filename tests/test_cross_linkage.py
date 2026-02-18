"""Tests for the cross_linkage module (issue #60)."""

from http import HTTPStatus

import pytest
import responses
from responses import matchers

import aiod
from aiod.calls.urls import server_url
from aiod.cross_linkage import RelationType


# ---------------------------------------------------------------------------
# RelationType enum
# ---------------------------------------------------------------------------


def test_relation_type_values():
    assert RelationType.proposes == "proposes"
    assert RelationType.related == "related"
    assert RelationType.uses == "uses"


def test_relation_type_is_string():
    """RelationType values can be used directly as strings."""
    assert isinstance(RelationType.proposes.value, str)


# ---------------------------------------------------------------------------
# get_publications_for_model
# ---------------------------------------------------------------------------


@responses.activate
def test_get_publications_for_model_no_filter():
    model_id = "model_abc123"
    responses.get(
        f"{server_url()}ml_models/{model_id}/publications",
        json=[{"identifier": "pub_1", "name": "Random Forests"}, {"identifier": "pub_2", "name": "Bagging"}],
        status=HTTPStatus.OK,
    )
    result = aiod.cross_linkage.get_publications_for_model(model_id, data_format="json")
    assert len(result) == 2
    assert result[0]["identifier"] == "pub_1"


@responses.activate
@pytest.mark.parametrize("relation_type", list(RelationType))
def test_get_publications_for_model_with_filter(relation_type):
    model_id = "model_abc123"
    responses.get(
        f"{server_url()}ml_models/{model_id}/publications?relation_type={relation_type.value}",
        json=[{"identifier": "pub_1", "name": "A Paper"}],
        status=HTTPStatus.OK,
    )
    result = aiod.cross_linkage.get_publications_for_model(
        model_id, relation_type=relation_type, data_format="json"
    )
    assert len(result) == 1


@responses.activate
def test_get_publications_for_model_string_relation_type():
    """Relation type can also be passed as a plain string."""
    model_id = "model_abc123"
    responses.get(
        f"{server_url()}ml_models/{model_id}/publications?relation_type=proposes",
        json=[{"identifier": "pub_1"}],
        status=HTTPStatus.OK,
    )
    result = aiod.cross_linkage.get_publications_for_model(
        model_id, relation_type="proposes", data_format="json"
    )
    assert result == [{"identifier": "pub_1"}]


@responses.activate
def test_get_publications_for_model_not_found():
    model_id = "model_unknown"
    responses.get(
        f"{server_url()}ml_models/{model_id}/publications",
        json={"detail": "ml_model not found"},
        status=HTTPStatus.NOT_FOUND,
    )
    with pytest.raises(KeyError, match=model_id):
        aiod.cross_linkage.get_publications_for_model(model_id)


@responses.activate
def test_get_publications_for_model_returns_dataframe():
    model_id = "model_abc123"
    responses.get(
        f"{server_url()}ml_models/{model_id}/publications",
        json=[{"identifier": "pub_1", "name": "A Paper"}],
        status=HTTPStatus.OK,
    )
    import pandas as pd

    result = aiod.cross_linkage.get_publications_for_model(model_id)
    assert isinstance(result, pd.DataFrame)
    assert "name" in result.columns


# ---------------------------------------------------------------------------
# get_models_for_publication
# ---------------------------------------------------------------------------


@responses.activate
def test_get_models_for_publication_no_filter():
    pub_id = "pub_xyz789"
    responses.get(
        f"{server_url()}publications/{pub_id}/ml_models",
        json=[{"identifier": "model_1", "name": "RandomForest"}, {"identifier": "model_2", "name": "ExtraTrees"}],
        status=HTTPStatus.OK,
    )
    result = aiod.cross_linkage.get_models_for_publication(pub_id, data_format="json")
    assert len(result) == 2
    assert result[0]["identifier"] == "model_1"


@responses.activate
@pytest.mark.parametrize("relation_type", list(RelationType))
def test_get_models_for_publication_with_filter(relation_type):
    pub_id = "pub_xyz789"
    responses.get(
        f"{server_url()}publications/{pub_id}/ml_models?relation_type={relation_type.value}",
        json=[{"identifier": "model_1"}],
        status=HTTPStatus.OK,
    )
    result = aiod.cross_linkage.get_models_for_publication(
        pub_id, relation_type=relation_type, data_format="json"
    )
    assert len(result) == 1


@responses.activate
def test_get_models_for_publication_not_found():
    pub_id = "pub_unknown"
    responses.get(
        f"{server_url()}publications/{pub_id}/ml_models",
        json={"detail": "publication not found"},
        status=HTTPStatus.NOT_FOUND,
    )
    with pytest.raises(KeyError, match=pub_id):
        aiod.cross_linkage.get_models_for_publication(pub_id)


@responses.activate
def test_get_models_for_publication_returns_dataframe():
    pub_id = "pub_xyz789"
    responses.get(
        f"{server_url()}publications/{pub_id}/ml_models",
        json=[{"identifier": "model_1", "name": "RandomForest"}],
        status=HTTPStatus.OK,
    )
    import pandas as pd

    result = aiod.cross_linkage.get_models_for_publication(pub_id)
    assert isinstance(result, pd.DataFrame)


# ---------------------------------------------------------------------------
# register_link
# ---------------------------------------------------------------------------


@responses.activate
def test_register_link(valid_refresh_token):
    model_id = "model_abc123"
    pub_id = "pub_xyz789"
    link_id = "link_aabbccdd"
    responses.post(
        f"{server_url()}ml_models/{model_id}/publications",
        match=[
            matchers.json_params_matcher(
                {"publication_identifier": pub_id, "relation_type": "proposes"}
            )
        ],
        json={"identifier": link_id},
        status=HTTPStatus.OK,
    )
    result = aiod.cross_linkage.register_link(
        model_identifier=model_id,
        publication_identifier=pub_id,
        relation_type=RelationType.proposes,
    )
    assert result == link_id


@responses.activate
def test_register_link_with_string_relation_type(valid_refresh_token):
    model_id = "model_abc123"
    pub_id = "pub_xyz789"
    link_id = "link_aabbccdd"
    responses.post(
        f"{server_url()}ml_models/{model_id}/publications",
        match=[
            matchers.json_params_matcher(
                {"publication_identifier": pub_id, "relation_type": "uses"}
            )
        ],
        json={"identifier": link_id},
        status=HTTPStatus.OK,
    )
    result = aiod.cross_linkage.register_link(
        model_identifier=model_id,
        publication_identifier=pub_id,
        relation_type="uses",
    )
    assert result == link_id


@responses.activate
def test_register_link_not_found(valid_refresh_token):
    model_id = "model_unknown"
    pub_id = "pub_unknown"
    responses.post(
        f"{server_url()}ml_models/{model_id}/publications",
        json={"detail": "not found"},
        status=HTTPStatus.NOT_FOUND,
    )
    with pytest.raises(KeyError):
        aiod.cross_linkage.register_link(
            model_identifier=model_id,
            publication_identifier=pub_id,
            relation_type=RelationType.proposes,
        )


# ---------------------------------------------------------------------------
# delete_link
# ---------------------------------------------------------------------------


@responses.activate
def test_delete_link(valid_refresh_token):
    link_id = "link_aabbccdd"
    responses.delete(
        f"{server_url()}cross_links/{link_id}",
        status=HTTPStatus.OK,
    )
    res = aiod.cross_linkage.delete_link(link_id)
    assert res.status_code == HTTPStatus.OK


@responses.activate
def test_delete_link_not_found(valid_refresh_token):
    link_id = "link_unknown"
    responses.delete(
        f"{server_url()}cross_links/{link_id}",
        json={"detail": "not found"},
        status=HTTPStatus.NOT_FOUND,
    )
    with pytest.raises(KeyError, match=link_id):
        aiod.cross_linkage.delete_link(link_id)
