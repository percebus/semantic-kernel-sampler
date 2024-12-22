from hamcrest import assert_that, is_


def test__true_is_true() -> None:
    assert_that(True, is_(True))
