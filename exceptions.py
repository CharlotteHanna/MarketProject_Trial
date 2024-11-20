
from typing import Any, Callable
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi import status
from fastapi.responses import JSONResponse

class MarketPlaceException(Exception):
    """ This is the base class for all MarketPlace Exceptions """
    pass


class UserAlreadyExists(MarketPlaceException):
    """User has provided a username for a user who exists during sign up."""
    pass

class InvalidCredentials(MarketPlaceException):
    """User has provided wrong username or password during log in."""

    pass


class InsufficientPermission(MarketPlaceException):
    """User does not have the neccessary permissions to perform an action."""

    pass

class FillParameters(MarketPlaceException):
    """user should provide one parameter only."""

    pass

class UserNotFound(MarketPlaceException):
    """User Not found"""

    pass

class ProductNotFound(MarketPlaceException):
    """Product Not found"""

    pass

class ConversationNotFound(MarketPlaceException):
    """Conversation Not found"""

    pass

class MessageNotFound(MarketPlaceException):
    """Message Not found"""

    pass

class PaymentNotFound(MarketPlaceException):
    """Payment Not found"""

    pass


class CategoryNotFound(MarketPlaceException):
    """Category Not found"""

    pass

class CanNotStartConversation(MarketPlaceException):
    """Owner of product can't start a conversation about the same product """
    pass

class CanNotPayForProduct(MarketPlaceException):
    """Owner of product can't pay for the same product """
    pass



class CanNotAccessConversation(MarketPlaceException):
    """Only Participents in a conversation can access this conversation """
    pass
class CanNotAccessPayment(MarketPlaceException):
    """Only Participents in a payment can access this payment """
    pass

class CanNotDeletePayment(MarketPlaceException):
    """ Only in Progress payments can be deleted """
    pass

class CanNotDeleteConversationWithContent(MarketPlaceException):
    """Only empty conversations can be deleted"""
    pass

class CanNotPayForReservedProduct(MarketPlaceException):
    """User can not start payment for a reserved product"""
    pass




def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: MarketPlaceException):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler



def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with this username or email already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "user_not_found",
            },
        ),
    )


    app.add_exception_handler(
        ProductNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Product not found",
                "error_code": "product_not_found",
            },
        ),
    )



    app.add_exception_handler(
        CategoryNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Category not found",
                "error_code": "category_not_found",
            },
        ),
    )


    app.add_exception_handler(
        ConversationNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Conversation not found",
                "error_code": "conversation_not_found",
            },
        ),
    )



    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )
    app.add_exception_handler(
        FillParameters,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "User should provide one parameter only",
                "error_code": "one_parameter_only",
            },
        ),
    )

    app.add_exception_handler(
        CanNotStartConversation,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Owner of a product cant start conversation about a product he owns",
                "error_code": "cant_start_conversation_on_your_own_product",
            },
        ),
    )
    app.add_exception_handler(
        CanNotAccessConversation,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Only Participents in a conversation can access this conversation",
                "error_code": "not_party_of_a_conversation",
            },
        ),
    )


    app.add_exception_handler(
        CanNotDeleteConversationWithContent,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Cannot delete conversation because it contains messages",
                "error_code": "conversation_not_empty",
            },
        ),
    )

    
 
    app.add_exception_handler(
        CanNotPayForReservedProduct,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "User can not start payment for a reserved product",
                "error_code": "can_not_pay_for_this_product",
            },
        ),
    )


    app.add_exception_handler(
        CanNotPayForProduct,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Owner of product can't pay for the same product",
                "error_code": "cant_pay_for_your_own_product",
            },
        ),
    )
    app.add_exception_handler(
        CanNotAccessPayment,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Only Participents in a payment can access this payment ",
                "error_code": "not_party_of_a_payment",
            },
        ),
    )

    app.add_exception_handler(
        CanNotDeletePayment,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": " Only in Progress payments can be deleted",
                "error_code": "payment_can_not_be_deleted",
            },
        ),
    )
    
  
   
