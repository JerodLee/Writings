from app.utils.slug import slugify


def test_slugify_basic():
    assert slugify("Why poor people stay poor") == "why-poor-people-stay-poor"
