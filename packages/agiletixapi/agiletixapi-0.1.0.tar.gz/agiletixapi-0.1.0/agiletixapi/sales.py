
from .base import BaseAgileAPI
from .utils import method_name, strftime_agile


class AgileSalesAPI(BaseAgileAPI):
    """Interface for the Agile Sales API 

    """

    SERVICE_TYPE = 'sales'

    @method_name
    def authenticate_customer(self, username, password, **kwargs):
        response = self._make_request(
            'GET', 
            userName=username, 
            password=password, 
            **kwargs
            )
        return response

    @method_name
    def authenticate_email(self, email, password, **kwargs):
        response = self._make_request(
            'GET', 
            email=email, 
            password=password, 
            **kwargs
            )
        return response

    @method_name
    def authenticate_member(self, membership_id, member_number, password, **kwargs):
        response = self._make_request(
            'GET', 
            membershipID=membership_id, 
            memberNumber=member_number, 
            password=password, 
            **kwargs
            )
        return response

    @method_name
    def buyer_type_list(self, **kwargs):
        response = self._make_request(
            'GET', 
            **kwargs
            )
        return response        

    @method_name
    def event_list(self, start_date, end_date, **kwargs):
        response = self._make_request(
            'GET', 
            startDate=strftime_agile(start_date), 
            endDate=strftime_agile(end_date), 
            **kwargs
            )
        return response

    @method_name
    def event_get(self, event_id, **kwargs):
        response = self._make_request(
            'GET', 
            eventID=event_id,
            **kwargs
            )
        return response

    @method_name
    def event_get_description(self, event_id, **kwargs):
        response = self._make_request(
            'GET', 
            eventID=event_id,
            **kwargs
            )
        return response

    @method_name
    def event_sales_status(self, event_id, buyer_type_id, **kwargs):
        response = self._make_request(
            'GET', 
            eventID=event_id,
            buyerTypeID=buyer_type_id, 
            **kwargs
            )
        return response

    @method_name
    def event_list_prices(self, event_id, event_org_id, buyer_type_id=None, member_id=None, order_id=None, transaction_id=None, promo_code=None, **kwargs):
        response = self._make_request(
            'GET', 
            buyerTypeID=buyer_type_id, 
            eventOrgID=event_org_id,
            eventID=event_id,
            memberID=member_id,
            orderID=order_id,
            transactionID=transaction_id,
            promoCode=promo_code,
            **kwargs
            )
        return response

    @method_name
    def order_start(self, buyer_type_id, customer_id=None, member_id=None, **kwargs):
        response = self._make_request(
            'GET', 
            buyerTypeID=buyer_type_id, 
            memberID=member_id,
            customerID=customer_id,
            **kwargs
            )
        return response

    @method_name
    def order_status(self, order_id, transaction_id, include_item_summary=False, **kwargs):
        response = self._make_request(
            'GET', 
            orderID=order_id,
            transactionID=transaction_id,
            includeItemSummary=include_item_summary,
            **kwargs
            )
        return response

    @method_name
    def order_update(self, order_id, transaction_id, buyer_type_id, customer_id, include_item_summary=False, **kwargs):
        response = self._make_request(
            'GET', 
            buyer_type_id=buyer_type_id, 
            orderID=order_id,
            transactionID=transaction_id,
            customerID=customer_id,
            includeItemSummary=include_item_summary,
            **kwargs
            )
        return response

    @method_name
    def order_cancel(self, order_id, transaction_id, **kwargs):
        response = self._make_request(
            'GET', 
            orderID=order_id,
            transactionID=transaction_id,
            **kwargs
            )
        return response

    @method_name
    def order_transfer(self, order_id, transaction_id, **kwargs):
        response = self._make_request(
            'GET', 
            orderID=order_id,
            transactionID=transaction_id,
            **kwargs
            )
        return response

    @method_name
    def tickets_add(self, order_id, transaction_id, event_org_id, event_id, tier_id, ticket_types, quantities, **kwargs):
        response = self._make_request(
            'GET', 
            orderID=order_id,
            transactionID=transaction_id,
            eventOrgID=event_org_id,
            eventID=event_id,
            tierID=tier_id, # The tier ID for the prices being requested
            ticketTypes=ticket_types, # A comma separated list of ticket types for the ticket request
            quantities=quantities, # A comma separated list of quantities for the ticket request
            **kwargs
            )
        return response

