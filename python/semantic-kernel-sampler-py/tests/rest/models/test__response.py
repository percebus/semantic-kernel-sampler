from hamcrest import assert_that, equal_to, is_, not_none  # type: ignore

from src.semantic_kernel_sampler.rest.models.request import Request
from src.semantic_kernel_sampler.rest.models.response import Response


def test__request__message__empty():
    oRequest = Request(message="")
    oResponse = Response(request=oRequest)
    assert_that(oResponse.id, equal_to(oRequest.id))

    assert_that(oResponse.request, is_(not_none()))
    assert_that(oResponse.id, equal_to(oResponse.request.id))
    assert_that(oResponse.request.message, equal_to(""))


def test__request__message__what_time_is_it():
    oRequest = Request(message="What time is it?")
    oResponse = Response(request=oRequest)
    assert_that(oResponse.id, equal_to(oRequest.id))
    assert_that(oResponse.id, equal_to(oResponse.request.id))
