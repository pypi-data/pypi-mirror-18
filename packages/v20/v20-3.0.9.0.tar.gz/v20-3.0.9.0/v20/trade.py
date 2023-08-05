import ujson as json
from v20.base_entity import BaseEntity
from v20.base_entity import EntityDict
from v20.request import Request
from v20 import entity_properties
from v20 import transaction
from v20 import order



class Trade(BaseEntity):
    """
    The specification of a Trade within an Account. This includes the full
    representation of the Trade's dependent Orders in addition to the IDs of
    those Orders.
    """

    #
    # Format string used when generating a summary for this object
    #
    _summary_format = "{initialUnits} of {instrument} @ {price}"

    #
    # Format string used when generating a name for this object
    #
    _name_format = "Trade {id}"

    #
    # Property metadata for this object
    #
    _properties = entity_properties.trade_Trade

    def __init__(self, **kwargs):
        """
        Create a new Trade instance
        """
        super(Trade, self).__init__()
 
        #
        # The Trade's identifier, unique within the Trade's Account.
        #
        self.id = kwargs.get("id")
 
        #
        # The Trade's Instrument.
        #
        self.instrument = kwargs.get("instrument")
 
        #
        # The execution price of the Trade.
        #
        self.price = kwargs.get("price")
 
        #
        # The date/time when the Trade was opened.
        #
        self.openTime = kwargs.get("openTime")
 
        #
        # The current state of the Trade.
        #
        self.state = kwargs.get("state")
 
        #
        # The initial size of the Trade. Negative values indicate a short
        # Trade, and positive values indicate a long Trade.
        #
        self.initialUnits = kwargs.get("initialUnits")
 
        #
        # The number of units currently open for the Trade. This value is
        # reduced to 0.0 as the Trade is closed.
        #
        self.currentUnits = kwargs.get("currentUnits")
 
        #
        # The total profit/loss realized on the closed portion of the Trade.
        #
        self.realizedPL = kwargs.get("realizedPL")
 
        #
        # The unrealized profit/loss on the open portion of the Trade.
        #
        self.unrealizedPL = kwargs.get("unrealizedPL")
 
        #
        # The IDs of the Transactions that have closed portions of this Trade.
        #
        self.closingTransactionIDs = kwargs.get("closingTransactionIDs")
 
        #
        # The financing paid/collected for this Trade.
        #
        self.financing = kwargs.get("financing")
 
        #
        # The date/time when the Trade was fully closed. Only provided for
        # Trades whose state is CLOSED.
        #
        self.closeTime = kwargs.get("closeTime")
 
        #
        # The client extensions of the Trade.
        #
        self.clientExtensions = kwargs.get("clientExtensions")
 
        #
        # Full representation of the Trade's Take Profit Order, only provided
        # if such an Order exists.
        #
        self.takeProfitOrder = kwargs.get("takeProfitOrder")
 
        #
        # Full representation of the Trade's Stop Loss Order, only provided if
        # such an Order exists.
        #
        self.stopLossOrder = kwargs.get("stopLossOrder")
 
        #
        # Full representation of the Trade's Trailing Stop Loss Order, only
        # provided if such an Order exists.
        #
        self.trailingStopLossOrder = kwargs.get("trailingStopLossOrder")

    @staticmethod
    def from_dict(data):
        """
        Instantiate a new Trade from a dict (generally from loading a JSON
        response). The data used to instantiate the Trade is a shallow copy of
        the dict passed in, with any complex child types instantiated
        appropriately.
        """

        data = data.copy()


        if data.get('clientExtensions') is not None:
            data['clientExtensions'] = \
                transaction.ClientExtensions.from_dict(
                    data['clientExtensions']
                )

        if data.get('takeProfitOrder') is not None:
            data['takeProfitOrder'] = \
                order.TakeProfitOrder.from_dict(
                    data['takeProfitOrder']
                )

        if data.get('stopLossOrder') is not None:
            data['stopLossOrder'] = \
                order.StopLossOrder.from_dict(
                    data['stopLossOrder']
                )

        if data.get('trailingStopLossOrder') is not None:
            data['trailingStopLossOrder'] = \
                order.TrailingStopLossOrder.from_dict(
                    data['trailingStopLossOrder']
                )

        return Trade(**data)


class TradeSummary(BaseEntity):
    """
    The summary of a Trade within an Account. This representation does not
    provide the full details of the Trade's dependent Orders.
    """

    #
    # Format string used when generating a summary for this object
    #
    _summary_format = "{initialUnits} of {instrument} @ {price}"

    #
    # Format string used when generating a name for this object
    #
    _name_format = "Trade {id}"

    #
    # Property metadata for this object
    #
    _properties = entity_properties.trade_TradeSummary

    def __init__(self, **kwargs):
        """
        Create a new TradeSummary instance
        """
        super(TradeSummary, self).__init__()
 
        #
        # The Trade's identifier, unique within the Trade's Account.
        #
        self.id = kwargs.get("id")
 
        #
        # The Trade's Instrument.
        #
        self.instrument = kwargs.get("instrument")
 
        #
        # The execution price of the Trade.
        #
        self.price = kwargs.get("price")
 
        #
        # The date/time when the Trade was opened.
        #
        self.openTime = kwargs.get("openTime")
 
        #
        # The current state of the Trade.
        #
        self.state = kwargs.get("state")
 
        #
        # The initial size of the Trade. Negative values indicate a short
        # Trade, and positive values indicate a long Trade.
        #
        self.initialUnits = kwargs.get("initialUnits")
 
        #
        # The number of units currently open for the Trade. This value is
        # reduced to 0.0 as the Trade is closed.
        #
        self.currentUnits = kwargs.get("currentUnits")
 
        #
        # The total profit/loss realized on the closed portion of the Trade.
        #
        self.realizedPL = kwargs.get("realizedPL")
 
        #
        # The unrealized profit/loss on the open portion of the Trade.
        #
        self.unrealizedPL = kwargs.get("unrealizedPL")
 
        #
        # The IDs of the Transactions that have closed portions of this Trade.
        #
        self.closingTransactionIDs = kwargs.get("closingTransactionIDs")
 
        #
        # The financing paid/collected for this Trade.
        #
        self.financing = kwargs.get("financing")
 
        #
        # The date/time when the Trade was fully closed. Only provided for
        # Trades whose state is CLOSED.
        #
        self.closeTime = kwargs.get("closeTime")
 
        #
        # The client extensions of the Trade.
        #
        self.clientExtensions = kwargs.get("clientExtensions")
 
        #
        # ID of the Trade's Take Profit Order, only provided if such an Order
        # exists.
        #
        self.takeProfitOrderID = kwargs.get("takeProfitOrderID")
 
        #
        # ID of the Trade's Stop Loss Order, only provided if such an Order
        # exists.
        #
        self.stopLossOrderID = kwargs.get("stopLossOrderID")
 
        #
        # ID of the Trade's Trailing Stop Loss Order, only provided if such an
        # Order exists.
        #
        self.trailingStopLossOrderID = kwargs.get("trailingStopLossOrderID")

    @staticmethod
    def from_dict(data):
        """
        Instantiate a new TradeSummary from a dict (generally from loading a
        JSON response). The data used to instantiate the TradeSummary is a
        shallow copy of the dict passed in, with any complex child types
        instantiated appropriately.
        """

        data = data.copy()


        if data.get('clientExtensions') is not None:
            data['clientExtensions'] = \
                transaction.ClientExtensions.from_dict(
                    data['clientExtensions']
                )

        return TradeSummary(**data)


class CalculatedTradeState(BaseEntity):
    """
    The dynamic (calculated) state of an open Trade
    """

    #
    # Format string used when generating a summary for this object
    #
    _summary_format = ""

    #
    # Format string used when generating a name for this object
    #
    _name_format = ""

    #
    # Property metadata for this object
    #
    _properties = entity_properties.trade_CalculatedTradeState

    def __init__(self, **kwargs):
        """
        Create a new CalculatedTradeState instance
        """
        super(CalculatedTradeState, self).__init__()
 
        #
        # The Trade's ID.
        #
        self.id = kwargs.get("id")
 
        #
        # The Trade's unrealized profit/loss.
        #
        self.unrealizedPL = kwargs.get("unrealizedPL")

    @staticmethod
    def from_dict(data):
        """
        Instantiate a new CalculatedTradeState from a dict (generally from
        loading a JSON response). The data used to instantiate the
        CalculatedTradeState is a shallow copy of the dict passed in, with any
        complex child types instantiated appropriately.
        """

        data = data.copy()

        return CalculatedTradeState(**data)


class EntitySpec(object):
    """
    The trade.EntitySpec wraps the trade module's type definitions 
    and API methods so they can be easily accessed through an instance of a v20
    Context.
    """

    Trade = Trade
    TradeSummary = TradeSummary
    CalculatedTradeState = CalculatedTradeState

    def __init__(self, ctx):
        self.ctx = ctx


    def list(
        self,
        accountID,
        **kwargs
    ):
        """
        Get a list of Trades for an Account

        Args:
            accountID:
                ID of the Account to fetch Trades for.
            ids:
                List of Trade IDs to retrieve.
            state:
                The state to filter the requested Trades by.
            instrument:
                The instrument to filter the requested Trades by.
            count:
                The maximum number of Trades to return.
            beforeID:
                The maximum Trade ID to return. If not provided the most recent
                Trades in the Account are returned.

        Returns:
            v20.response.Response containing the results from submitting the
            request
        """

        request = Request(
            'GET',
            '/v3/accounts/{accountID}/trades'
        )

        request.set_path_param(
            'accountID',
            accountID
        )

        request.set_param(
            'ids',
            kwargs.get('ids')
        )

        request.set_param(
            'state',
            kwargs.get('state')
        )

        request.set_param(
            'instrument',
            kwargs.get('instrument')
        )

        request.set_param(
            'count',
            kwargs.get('count')
        )

        request.set_param(
            'beforeID',
            kwargs.get('beforeID')
        )

        response = self.ctx.request(request)


        if response.content_type is None:
            return response

        if not response.content_type.startswith("application/json"):
            return response

        jbody = json.loads(response.raw_body)

        parsed_body = {}

        #
        # Parse responses specific to the request
        #
        if str(response.status) == "200":
            if jbody.get('trades') is not None:
                parsed_body['trades'] = [
                    Trade.from_dict(d)
                    for d in jbody.get('trades')
                ]

            if jbody.get('lastTransactionID') is not None:
                parsed_body['lastTransactionID'] = \
                    jbody.get('lastTransactionID')

        #
        # Assume standard error response with errorCode and errorMessage
        #
        else:
            errorCode = jbody.get('errorCode')
            errorMessage = jbody.get('errorMessage')

            if errorCode is not None:
                parsed_body['errorCode'] = errorCode

            if errorMessage is not None:
                parsed_body['errorMessage'] = errorMessage

        response.body = parsed_body

        return response


    def list_open(
        self,
        accountID,
        **kwargs
    ):
        """
        Get the list of open Trades for an Account

        Args:
            accountID:
                ID of the Account to fetch Trades for.

        Returns:
            v20.response.Response containing the results from submitting the
            request
        """

        request = Request(
            'GET',
            '/v3/accounts/{accountID}/openTrades'
        )

        request.set_path_param(
            'accountID',
            accountID
        )

        response = self.ctx.request(request)


        if response.content_type is None:
            return response

        if not response.content_type.startswith("application/json"):
            return response

        jbody = json.loads(response.raw_body)

        parsed_body = {}

        #
        # Parse responses specific to the request
        #
        if str(response.status) == "200":
            if jbody.get('trades') is not None:
                parsed_body['trades'] = [
                    Trade.from_dict(d)
                    for d in jbody.get('trades')
                ]

            if jbody.get('lastTransactionID') is not None:
                parsed_body['lastTransactionID'] = \
                    jbody.get('lastTransactionID')

        #
        # Assume standard error response with errorCode and errorMessage
        #
        else:
            errorCode = jbody.get('errorCode')
            errorMessage = jbody.get('errorMessage')

            if errorCode is not None:
                parsed_body['errorCode'] = errorCode

            if errorMessage is not None:
                parsed_body['errorMessage'] = errorMessage

        response.body = parsed_body

        return response


    def get(
        self,
        accountID,
        tradeID,
        **kwargs
    ):
        """
        Get the details of a specific Trade in an Account

        Args:
            accountID:
                ID of the Account to fetch Trades for.
            tradeID:
                ID of the Trade to fetch

        Returns:
            v20.response.Response containing the results from submitting the
            request
        """

        request = Request(
            'GET',
            '/v3/accounts/{accountID}/trades/{tradeID}'
        )

        request.set_path_param(
            'accountID',
            accountID
        )

        request.set_path_param(
            'tradeID',
            tradeID
        )

        response = self.ctx.request(request)


        if response.content_type is None:
            return response

        if not response.content_type.startswith("application/json"):
            return response

        jbody = json.loads(response.raw_body)

        parsed_body = {}

        #
        # Parse responses specific to the request
        #
        if str(response.status) == "200":
            if jbody.get('trade') is not None:
                parsed_body['trade'] = \
                    Trade.from_dict(
                        jbody['trade']
                    )

            if jbody.get('lastTransactionID') is not None:
                parsed_body['lastTransactionID'] = \
                    jbody.get('lastTransactionID')

        #
        # Assume standard error response with errorCode and errorMessage
        #
        else:
            errorCode = jbody.get('errorCode')
            errorMessage = jbody.get('errorMessage')

            if errorCode is not None:
                parsed_body['errorCode'] = errorCode

            if errorMessage is not None:
                parsed_body['errorMessage'] = errorMessage

        response.body = parsed_body

        return response


    def close(
        self,
        accountID,
        tradeID,
        **kwargs
    ):
        """
        Close (partially or fully) a specific open Trade in an Account

        Args:
            accountID:
                ID of the Account to close a Trade in.
            tradeID:
                ID of the Trade to close.
            units:
                Indication of how much of the Trade to close. Either the string
                "ALL" (indicating that all of the Trade should be closed), or a
                DecimalNumber representing the number of units of the open
                Trade to Close using a TradeClose MarketOrder. The units
                specified must always be positive, and the magnitude of the
                value cannot exceed the magnitude of the Trade's open units.

        Returns:
            v20.response.Response containing the results from submitting the
            request
        """

        request = Request(
            'PUT',
            '/v3/accounts/{accountID}/trades/{tradeID}/close'
        )

        request.set_path_param(
            'accountID',
            accountID
        )

        request.set_path_param(
            'tradeID',
            tradeID
        )

        body = EntityDict()

        body.set('units', kwargs.get('units'))

        request.set_body_dict(body.dict)

        response = self.ctx.request(request)


        if response.content_type is None:
            return response

        if not response.content_type.startswith("application/json"):
            return response

        jbody = json.loads(response.raw_body)

        parsed_body = {}

        #
        # Parse responses specific to the request
        #
        if str(response.status) == "200":
            if jbody.get('orderCreateTransaction') is not None:
                parsed_body['orderCreateTransaction'] = \
                    transaction.MarketOrderTransaction.from_dict(
                        jbody['orderCreateTransaction']
                    )

            if jbody.get('orderFillTransaction') is not None:
                parsed_body['orderFillTransaction'] = \
                    transaction.OrderFillTransaction.from_dict(
                        jbody['orderFillTransaction']
                    )

            if jbody.get('orderCancelTransaction') is not None:
                parsed_body['orderCancelTransaction'] = \
                    transaction.OrderCancelTransaction.from_dict(
                        jbody['orderCancelTransaction']
                    )

            if jbody.get('relatedTransactionIDs') is not None:
                parsed_body['relatedTransactionIDs'] = \
                    jbody.get('relatedTransactionIDs')

            if jbody.get('lastTransactionID') is not None:
                parsed_body['lastTransactionID'] = \
                    jbody.get('lastTransactionID')

        elif str(response.status) == "400":
            if jbody.get('orderRejectTransaction') is not None:
                parsed_body['orderRejectTransaction'] = \
                    transaction.MarketOrderRejectTransaction.from_dict(
                        jbody['orderRejectTransaction']
                    )

            if jbody.get('errorCode') is not None:
                parsed_body['errorCode'] = \
                    jbody.get('errorCode')

            if jbody.get('errorMessage') is not None:
                parsed_body['errorMessage'] = \
                    jbody.get('errorMessage')

        elif str(response.status) == "404":
            if jbody.get('orderRejectTransaction') is not None:
                parsed_body['orderRejectTransaction'] = \
                    transaction.MarketOrderRejectTransaction.from_dict(
                        jbody['orderRejectTransaction']
                    )

            if jbody.get('errorCode') is not None:
                parsed_body['errorCode'] = \
                    jbody.get('errorCode')

            if jbody.get('errorMessage') is not None:
                parsed_body['errorMessage'] = \
                    jbody.get('errorMessage')

        #
        # Assume standard error response with errorCode and errorMessage
        #
        else:
            errorCode = jbody.get('errorCode')
            errorMessage = jbody.get('errorMessage')

            if errorCode is not None:
                parsed_body['errorCode'] = errorCode

            if errorMessage is not None:
                parsed_body['errorMessage'] = errorMessage

        response.body = parsed_body

        return response


    def set_client_extensions(
        self,
        accountID,
        tradeID,
        **kwargs
    ):
        """
        Update the Client Extensions for a Trade. Do not add, update, or delete
        the Client Extensions if your account is associated with MT4.

        Args:
            accountID:
                ID of the Account.
            tradeID:
                ID of the Trade to update the Client Extension of.
            clientExtensions:
                The Client Extensions to update the Trade with. Do not add,
                update, or delete the Client Extensions if your account is
                associated with MT4.

        Returns:
            v20.response.Response containing the results from submitting the
            request
        """

        request = Request(
            'PUT',
            '/v3/accounts/{accountID}/trades/{tradeID}/clientExtensions'
        )

        request.set_path_param(
            'accountID',
            accountID
        )

        request.set_path_param(
            'tradeID',
            tradeID
        )

        body = EntityDict()

        body.set('clientExtensions', kwargs.get('clientExtensions'))

        request.set_body_dict(body.dict)

        response = self.ctx.request(request)


        if response.content_type is None:
            return response

        if not response.content_type.startswith("application/json"):
            return response

        jbody = json.loads(response.raw_body)

        parsed_body = {}

        #
        # Parse responses specific to the request
        #
        if str(response.status) == "200":
            if jbody.get('tradeClientExtensionsModifyTransaction') is not None:
                parsed_body['tradeClientExtensionsModifyTransaction'] = \
                    transaction.TradeClientExtensionsModifyTransaction.from_dict(
                        jbody['tradeClientExtensionsModifyTransaction']
                    )

            if jbody.get('relatedTransactionIDs') is not None:
                parsed_body['relatedTransactionIDs'] = \
                    jbody.get('relatedTransactionIDs')

            if jbody.get('lastTransactionID') is not None:
                parsed_body['lastTransactionID'] = \
                    jbody.get('lastTransactionID')

        elif str(response.status) == "400":
            if jbody.get('tradeClientExtensionsModifyRejectTransaction') is not None:
                parsed_body['tradeClientExtensionsModifyRejectTransaction'] = \
                    transaction.TradeClientExtensionsModifyRejectTransaction.from_dict(
                        jbody['tradeClientExtensionsModifyRejectTransaction']
                    )

            if jbody.get('lastTransactionID') is not None:
                parsed_body['lastTransactionID'] = \
                    jbody.get('lastTransactionID')

            if jbody.get('errorCode') is not None:
                parsed_body['errorCode'] = \
                    jbody.get('errorCode')

            if jbody.get('errorMessage') is not None:
                parsed_body['errorMessage'] = \
                    jbody.get('errorMessage')

        #
        # Assume standard error response with errorCode and errorMessage
        #
        else:
            errorCode = jbody.get('errorCode')
            errorMessage = jbody.get('errorMessage')

            if errorCode is not None:
                parsed_body['errorCode'] = errorCode

            if errorMessage is not None:
                parsed_body['errorMessage'] = errorMessage

        response.body = parsed_body

        return response


    def set_dependent_orders(
        self,
        accountID,
        tradeID,
        **kwargs
    ):
        """
        Create, replace and cancel a Trade's dependent Orders (Take Profit,
        Stop Loss and Trailing Stop Loss) through the Trade itself

        Args:
            accountID:
                ID of the Account.
            tradeID:
                ID of the Trade to modify the dependent Orders of.
            takeProfit:
                The specification of the Take Profit to create/modify/cancel.
                If takeProfit is set to null, the Take Profit Order will be
                cancelled if it exists. If takeProfit is not provided, the
                exisiting Take Profit Order will not be modified. If a sub-
                field of takeProfit is not specified, that field will be set to
                a default value on create, and be inherited by the replacing
                order on modify.
            stopLoss:
                The specification of the Stop Loss to create/modify/cancel. If
                stopLoss is set to null, the Stop Loss Order will be cancelled
                if it exists. If stopLoss is not provided, the exisiting Stop
                Loss Order will not be modified. If a sub-field of stopLoss is
                not specified, that field will be set to a default value on
                create, and be inherited by the replacing order on modify.
            trailingStopLoss:
                The specification of the Trailing Stop Loss to
                create/modify/cancel. If trailingStopLoss is set to null, the
                Trailing Stop Loss Order will be cancelled if it exists. If
                trailingStopLoss is not provided, the exisiting Trailing Stop
                Loss Order will not be modified. If a sub-field of
                trailngStopLoss is not specified, that field will be set to a
                default value on create, and be inherited by the replacing
                order on modify.

        Returns:
            v20.response.Response containing the results from submitting the
            request
        """

        request = Request(
            'PUT',
            '/v3/accounts/{accountID}/trades/{tradeID}/orders'
        )

        request.set_path_param(
            'accountID',
            accountID
        )

        request.set_path_param(
            'tradeID',
            tradeID
        )

        body = EntityDict()

        body.set('takeProfit', kwargs.get('takeProfit'))

        body.set('stopLoss', kwargs.get('stopLoss'))

        body.set('trailingStopLoss', kwargs.get('trailingStopLoss'))

        request.set_body_dict(body.dict)

        response = self.ctx.request(request)


        if response.content_type is None:
            return response

        if not response.content_type.startswith("application/json"):
            return response

        jbody = json.loads(response.raw_body)

        parsed_body = {}

        #
        # Parse responses specific to the request
        #
        if str(response.status) == "200":
            if jbody.get('takeProfitOrderCancelTransaction') is not None:
                parsed_body['takeProfitOrderCancelTransaction'] = \
                    transaction.OrderCancelTransaction.from_dict(
                        jbody['takeProfitOrderCancelTransaction']
                    )

            if jbody.get('takeProfitOrderTransaction') is not None:
                parsed_body['takeProfitOrderTransaction'] = \
                    transaction.TakeProfitOrderTransaction.from_dict(
                        jbody['takeProfitOrderTransaction']
                    )

            if jbody.get('takeProfitOrderFillTransaction') is not None:
                parsed_body['takeProfitOrderFillTransaction'] = \
                    transaction.OrderFillTransaction.from_dict(
                        jbody['takeProfitOrderFillTransaction']
                    )

            if jbody.get('takeProfitOrderCreatedCancelTransaction') is not None:
                parsed_body['takeProfitOrderCreatedCancelTransaction'] = \
                    transaction.OrderCancelTransaction.from_dict(
                        jbody['takeProfitOrderCreatedCancelTransaction']
                    )

            if jbody.get('stopLossOrderCancelTransaction') is not None:
                parsed_body['stopLossOrderCancelTransaction'] = \
                    transaction.OrderCancelTransaction.from_dict(
                        jbody['stopLossOrderCancelTransaction']
                    )

            if jbody.get('stopLossOrderTransaction') is not None:
                parsed_body['stopLossOrderTransaction'] = \
                    transaction.StopLossOrderTransaction.from_dict(
                        jbody['stopLossOrderTransaction']
                    )

            if jbody.get('stopLossOrderFillTransaction') is not None:
                parsed_body['stopLossOrderFillTransaction'] = \
                    transaction.OrderFillTransaction.from_dict(
                        jbody['stopLossOrderFillTransaction']
                    )

            if jbody.get('stopLossOrderCreatedCancelTransaction') is not None:
                parsed_body['stopLossOrderCreatedCancelTransaction'] = \
                    transaction.OrderCancelTransaction.from_dict(
                        jbody['stopLossOrderCreatedCancelTransaction']
                    )

            if jbody.get('trailingStopLossOrderCancelTransaction') is not None:
                parsed_body['trailingStopLossOrderCancelTransaction'] = \
                    transaction.OrderCancelTransaction.from_dict(
                        jbody['trailingStopLossOrderCancelTransaction']
                    )

            if jbody.get('trailingStopLossOrderTransaction') is not None:
                parsed_body['trailingStopLossOrderTransaction'] = \
                    transaction.TrailingStopLossOrderTransaction.from_dict(
                        jbody['trailingStopLossOrderTransaction']
                    )

            if jbody.get('relatedTransactionIDs') is not None:
                parsed_body['relatedTransactionIDs'] = \
                    jbody.get('relatedTransactionIDs')

            if jbody.get('lastTransactionID') is not None:
                parsed_body['lastTransactionID'] = \
                    jbody.get('lastTransactionID')

        elif str(response.status) == "400":
            if jbody.get('takeProfitOrderCancelRejectTransaction') is not None:
                parsed_body['takeProfitOrderCancelRejectTransaction'] = \
                    transaction.OrderCancelRejectTransaction.from_dict(
                        jbody['takeProfitOrderCancelRejectTransaction']
                    )

            if jbody.get('takeProfitOrderRejectTransaction') is not None:
                parsed_body['takeProfitOrderRejectTransaction'] = \
                    transaction.TakeProfitOrderRejectTransaction.from_dict(
                        jbody['takeProfitOrderRejectTransaction']
                    )

            if jbody.get('stopLossOrderCancelRejectTransaction') is not None:
                parsed_body['stopLossOrderCancelRejectTransaction'] = \
                    transaction.OrderCancelRejectTransaction.from_dict(
                        jbody['stopLossOrderCancelRejectTransaction']
                    )

            if jbody.get('stopLossOrderRejectTransaction') is not None:
                parsed_body['stopLossOrderRejectTransaction'] = \
                    transaction.StopLossOrderRejectTransaction.from_dict(
                        jbody['stopLossOrderRejectTransaction']
                    )

            if jbody.get('trailingStopLossOrderCancelRejectTransaction') is not None:
                parsed_body['trailingStopLossOrderCancelRejectTransaction'] = \
                    transaction.OrderCancelRejectTransaction.from_dict(
                        jbody['trailingStopLossOrderCancelRejectTransaction']
                    )

            if jbody.get('trailingStopLossOrderRejectTransaction') is not None:
                parsed_body['trailingStopLossOrderRejectTransaction'] = \
                    transaction.TrailingStopLossOrderRejectTransaction.from_dict(
                        jbody['trailingStopLossOrderRejectTransaction']
                    )

            if jbody.get('lastTransactionID') is not None:
                parsed_body['lastTransactionID'] = \
                    jbody.get('lastTransactionID')

            if jbody.get('errorCode') is not None:
                parsed_body['errorCode'] = \
                    jbody.get('errorCode')

            if jbody.get('errorMessage') is not None:
                parsed_body['errorMessage'] = \
                    jbody.get('errorMessage')

        #
        # Assume standard error response with errorCode and errorMessage
        #
        else:
            errorCode = jbody.get('errorCode')
            errorMessage = jbody.get('errorMessage')

            if errorCode is not None:
                parsed_body['errorCode'] = errorCode

            if errorMessage is not None:
                parsed_body['errorMessage'] = errorMessage

        response.body = parsed_body

        return response

