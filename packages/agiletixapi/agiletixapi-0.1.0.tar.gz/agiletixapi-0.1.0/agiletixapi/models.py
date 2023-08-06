
from collections import namedtuple
from datetime import datetime

from jsonobject import *

from .utils import ms_datestring_to_datetime


SALES_STATE_TEXT = (
    (1, 'Sale has not started: On Sale: 10/20/2013 9:00 AM'),
    (2, 'On sale: Buy Tickets, Add To Cart, Purchase'),
    (3, 'Sales ended. Event pending: Check with the box office'),
    (4, 'Event passed: Event is over'),
    (5, 'Custom message: Sold Out, Rush Only, Check Back Soon'),
)
# A struct to hold Agile error codes
SALES_STATE_CODES = {
    'SALES_STATE_SALES_NOT_STARTED': 1,
    'SALES_STATE_READY': 2, 
    'SALES_STATE_SALES_ENDED': 3,
    'SALES_STATE_EVENT_PAST': 4,
    'SALES_STATE_CUSTOM': 5,
}

SalesStateStruct = namedtuple('SalesStateStruct', ' '.join(SALES_STATE_CODES.keys()))
SalesState = SalesStateStruct(**SALES_STATE_CODES)


class AgileDateTimeProperty(DateTimeProperty):
    """Custom property that converts MS date string ( Json.NET < 4.5 ) to Python date object.

    """

    _type = datetime

    def _wrap(self, value):
        try:
            return ms_datestring_to_datetime(value)
        except ValueError as e:
            raise ValueError(
                'Invalid MS Json.NET (<4.5) date/time {0!r} [{1}]'.format(value, e))


class BaseAgileJsonObject(JsonObject):
    """Adds the AgileDateTimeProperty to JsonObject classes.

    """
    
    class Meta(object):
        update_properties = {
            datetime: AgileDateTimeProperty
        }


class Member(BaseAgileJsonObject):

    member_id = IntegerProperty(name='MemberID')
    member_number = StringProperty(name='MemberNumber')
    membership_id = IntegerProperty(name='MembershipID') # The membership program ID
    membership_expiration = AgileDateTimeProperty(name='MembershipExpiration')
    valid_buyer_types = ListProperty(IntegerProperty, name='ValidBuyerTypes')


class AgileCustomer(BaseAgileJsonObject):

    authenticated = BooleanProperty(name='Authenticated')
    customer_id = IntegerProperty(name='CustomerID')
    customer_name = StringProperty(name='CustomerName')
    members = ListProperty(Member, name='Members')

    @property
    def error_message(self):
        message = None
        if hasattr(self, 'Message'):
            message = self.Message
        return message


class BuyerType(BaseAgileJsonObject):

    buyer_type_id = IntegerProperty(name='BuyerTypeID')
    org_id = IntegerProperty(name='OrgID')
    name = StringProperty(name='Name')
    restriction_level = IntegerProperty(name='RestrictionLevel') # (0 - Unrestricted price, 1-3 - Restricted prices)
    customer_required = BooleanProperty(name='CustomerRequired') # An indicator that a customer is required on an order
    group_sales = BooleanProperty(name='GroupSales')
    membership_required = BooleanProperty(name='MembershipRequired')
    season_required = BooleanProperty(name='SeasonRequired')
    display_sequence = IntegerProperty(name='DisplaySequence') # The display sequence for sorting


class ItemSummary(BaseAgileJsonObject):

    type = IntegerProperty(name='Type')
    id = IntegerProperty(name='ID')
    quantity = IntegerProperty(name='Quantity')
    description = StringProperty(name='Description')


class Event(BaseAgileJsonObject):

    id = IntegerProperty(name='EventID')
    external_event_id = StringProperty(name='ExternalEventID')

    org_id = IntegerProperty(name='OrgID')
    venue_id = IntegerProperty(name='VenueID')
    venue_name = StringProperty(name='VenueName')

    name = StringProperty(name='Name')
    description = None

    start_date = AgileDateTimeProperty(name='StartDate')
    end_date = AgileDateTimeProperty(name='EndDate')

    date_tbd = BooleanProperty(name='DateTBD')

    show_end_date = BooleanProperty(name='ShowEndDate')
    show_time = BooleanProperty(name='ShowTime')

    short_description = StringProperty(name='ShortDescription')
    short_descriptive1 = StringProperty(name='ShortDescriptive1')
    short_descriptive2 = StringProperty(name='ShortDescriptive2')
    extra_html = StringProperty(name='ExtraHTML')

    display_color = IntegerProperty(name='DisplayColor')
    event_image = StringProperty(name='EventImage')
    event_thumb_image = StringProperty(name='EventThumbImage')
    config_image = StringProperty(name='ConfigImage')
    config_thumb_image = StringProperty(name='ConfigThumbImage')

    sales_message = StringProperty(name='SalesMessage')
    sales_state = IntegerProperty(name='SalesState')


    @property  
    def sales_state_description(self):
        description = ""
        for choice in self.SALES_STATE_TEXT:
            if self.sales_state == choice[1]:
                description = choice[2]
                break
        return description


class Price(BaseAgileJsonObject):

    event_price_id = IntegerProperty(name='EventPriceID')
    tier_id = IntegerProperty(name='TierID')
    buyer_type_id = IntegerProperty(name='BuyerTypeID')
    ticket_type = StringProperty(name='TicketType')
    base_price = DecimalProperty(name='BasePrice')
    restriction_level = IntegerProperty(name='RestrictionLevel') # (0 - Unrestricted price, 1-3 - Restricted prices)
    min_per_order = IntegerProperty(name='MinPerOrder') # A value of -1 means it is not being used)
    max_per_order = IntegerProperty(name='MaxPerOrder') # A value of -1 means it is not being used)
    promo_code_required = BooleanProperty(name='PromoCodeRequired')
    display_sequence = IntegerProperty(name='DisplaySequence') # The display sequence for sorting


class EventListPrice(BaseAgileJsonObject):

    tier_id = IntegerProperty(name='TierID')
    event_id = IntegerProperty(name='EventID')
    name = StringProperty(name='Name')
    event_admission = BooleanProperty(name='EventAdmission')
    general_admission = BooleanProperty(name='GeneralAdmission')
    sales_line_type_id = IntegerProperty(name='SalesLineTypeID')
    sales_line_type_name = StringProperty(name='SalesLineTypeName')
    seat_display_color = IntegerProperty(name='SeatDisplayColor')
    available_qty = IntegerProperty(name='AvailableQty')
    show_available_qty = BooleanProperty(name='ShowAvailableQty')    
    sold_out_text = StringProperty(name='SoldOutText')
    tier_time = StringProperty(name='TierTime')
    display_sequence = IntegerProperty(name='DisplaySequence')
    prices = ListProperty(Price, name='Prices')


class EventSalesStatus(BaseAgileJsonObject):

    on_sale = BooleanProperty(name='OnSale')

    start_sales = AgileDateTimeProperty(name='StartSales')
    end_sales = AgileDateTimeProperty(name='EndSales')

    enforce_quantities = BooleanProperty(name='EnforceQuantities') # An idicator that quanties are enforced for the event and buyer type
    min_qty_per_order = IntegerProperty(name='MinQtyPerOrder')
    max_qty_per_order = IntegerProperty(name='MaxQtyPerOrder')

    display_message = BooleanProperty(name='DisplayMessage')
    message_text = StringProperty(name='MessageText') # MessageText - AvailabilityText 
    availability_text = StringProperty(name='AvailabilityText')


class Order(BaseAgileJsonObject):

    order_id = IntegerProperty(name='OrderID')
    order_number = StringProperty(name='OrderNumber')
    transaction_id = IntegerProperty(name='TransactionID')
    
    open_datetime = AgileDateTimeProperty(name='OpenDateTime')
    close_datetime = AgileDateTimeProperty(name='CloseDateTime')
    expiration_datetime = AgileDateTimeProperty(name='ExpirationDateTime')

    expired = BooleanProperty(name='Expired')
    in_process = BooleanProperty(name='InProcess') # If false, order is complete
    buyer_type_id = IntegerProperty(name='BuyerTypeID')
    customer_id = IntegerProperty(name='CustomerID')
    contact_customer_id = IntegerProperty(name='ContactCustomerID')
    subtotal = DecimalProperty(name='Subtotal')
    order_total = DecimalProperty(name='OrderTotal')
    item_count = IntegerProperty(name='ItemCount')

    item_summary = ListProperty(ItemSummary, name='ItemSummary')

