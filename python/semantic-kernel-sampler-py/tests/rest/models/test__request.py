from hamcrest import assert_that, equal_to

from src.semantic_kernel_sampler.rest.models.request import Request


def test__request__message__empty():
    oRequest = Request(message="")
    assert_that(oRequest.message, equal_to(""))


def test__request__message__what_time_is_it():
    oRequest = Request(message="What time is it?")
    assert_that(oRequest.message, equal_to("What time is it?"))
