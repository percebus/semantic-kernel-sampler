from hamcrest import assert_that, equal_to, is_, not_none  # type: ignore

from semantic_kernel_sampler.rest.models.request import RequestModel
from semantic_kernel_sampler.rest.models.response import ResponseModel


def test__request__message__empty():
    oRequestModel = RequestModel(message="")
    oResponseModel = ResponseModel(request=oRequestModel)
    assert_that(oResponseModel.id, equal_to(oRequestModel.id))

    assert_that(oResponseModel.request, is_(not_none()))
    assert_that(oResponseModel.id, equal_to(oResponseModel.request.id))
    assert_that(oResponseModel.request.message, equal_to(""))


def test__request__message__what_time_is_it():
    oRequestModel = RequestModel(message="What time is it?")
    oResponseModel = ResponseModel(request=oRequestModel)
    assert_that(oResponseModel.id, equal_to(oRequestModel.id))
    assert_that(oResponseModel.id, equal_to(oResponseModel.request.id))
