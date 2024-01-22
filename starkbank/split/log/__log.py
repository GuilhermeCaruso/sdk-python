from ...utils import rest
from starkcore.utils.api import from_api_json
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date
from ..__split import _resource as _split_resource


class Log(Resource):
    """# split.Log object
    Every time a Split entity is modified, a corresponding split.Log
    is generated for the entity. This log is never generated by the
    user, but it can be retrieved to check additional information
    on the Split.
    ## Attributes (return-only):
    - id [string]: unique id returned when the log is created. ex: "5656565656565656"
    - split [Split]: Split entity to which the log refers to.
    - errors [list of strings]: list of errors linked to this Split event.
    - type [string]: type of the Split event which triggered the log creation. ex: "success" or "failed"
    - created [datetime.datetime]: creation datetime for the log. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id, created, type, errors, split):
        Resource.__init__(self, id=id)

        self.created = check_datetime(created)
        self.type = type
        self.errors = errors
        self.split = from_api_json(_split_resource, split)


_resource = {"class": Log, "name": "SplitLog"}


def get(id, user=None):
    """# Retrieve a specific split.Log
    Receive a single split.Log object previously created by the Stark Bank API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - split.Log object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, types=None, split_ids=None, user=None):
    """# Retrieve split.Logs
    Receive a generator of split.Log objects previously created in the Stark Bank API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - types [list of strings, default None]: filter retrieved objects by event types. ex: "processing" or "success"
    - split_ids [list of strings, default None]: list of Split ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - generator of split.Log objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        types=types,
        split_ids=split_ids,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, types=None, split_ids=None, user=None):
    """# Retrieve paged split.Logs
    Receive a list of up to 100 split.Log objects previously created in the Stark Bank API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - types [list of strings, default None]: filter retrieved objects by event types. ex: "processing" or "success"
    - split_ids [list of strings, default None]: list of Split ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - list of split.Log objects with updated attributes
    - cursor to retrieve the next page of split.Log objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        types=types,
        split_ids=split_ids,
        user=user,
    )