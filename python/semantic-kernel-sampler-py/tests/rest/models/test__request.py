from hamcrest import assert_that, equal_to

from semantic_kernel_sampler.rest.models.request import RequestModel


def test__request__message__empty():
    oRequestModel = RequestModel(message="")
    assert_that(oRequestModel.message, equal_to(""))


def test__request__message__what_time_is_it():
    oRequestModel = RequestModel(message="What time is it?")
    assert_that(oRequestModel.message, equal_to("What time is it?"))
