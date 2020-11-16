from ...utils import rest
from ...utils.checks import check_datetime, check_date
from ...utils.api import from_api_json
from ...utils.resource import Resource
from ..__invoice import _resource as _invoice_resource


class Log(Resource):
    """# invoice.Log object
    Every time an Invoice entity is updated, a corresponding invoice.Log
    is generated for the entity. This log is never generated by the
    user, but it can be retrieved to check additional information
    on the Invoice.
    ## Attributes:
    - id [string]: unique id returned when the log is created. ex: "5656565656565656"
    - invoice [Invoice]: Invoice entity to which the log refers to.
    - errors [list of strings]: list of errors linked to this Invoice event
    - type [string]: type of the Invoice event which triggered the log creation. ex: "registered" or "paid"
    - created [datetime.datetime]: creation datetime for the log. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id, created, type, errors, invoice):
        Resource.__init__(self, id=id)

        self.created = check_datetime(created)
        self.type = type
        self.errors = errors
        self.invoice = from_api_json(_invoice_resource, invoice)


_resource = {"class": Log, "name": "InvoiceLog"}


def get(id, user=None):
    """# Retrieve a specific invoice.Log
    Receive a single invoice.Log object previously created by the Stark Bank API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - invoice.Log object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, types=None, invoice_ids=None, user=None):
    """# Retrieve invoice.Log's
    Receive a generator of invoice.Log objects previously created in the Stark Bank API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - types [list of strings, default None]: filter for log event types. ex: "paid" or "registered"
    - invoice_ids [list of strings, default None]: list of Invoice ids to filter logs. ex: ["5656565656565656", "4545454545454545"]
    - user [Project object, default None]: Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - list of invoice.Log objects with updated attributes
    """
    return rest.get_list(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        types=types,
        invoice_ids=invoice_ids,
        user=user,
    )
