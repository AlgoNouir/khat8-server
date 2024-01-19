from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from .models import BaseUser, CartItem
from Apps.Products.models import KeeperCountItem, Product

# TODO : commenting for customers

# user/




class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request):
        """
        request change user data

        TODO add latitude and longitude the location of user

        Args:
            request.data : {
                id [number] : user id
                fName [string] : new name of user
                lName [string] : new family of user
                nationalCode [string] : national code of user
                email [string] : new email of user
                address [string] : new address of user
            }
            request.user : user that send this request
        """
        data = request.data

        print(data)
        user = BaseUser.objects.get(pk=data["id"])

        user.fName = data["fName"]
        user.lName = data["lName"]
        user.nationalCode = data["nationalCode"]
        user.email = data["email"]
        user.address = data["address"]

        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


# cart/
class CartView(APIView):
    def post(self, request):
        """
        request to add, remove or change a product to an user cart

        * product id in list is unique

        Args:
            request.data : {
                'product': product id for add to cart
                'count': product count added to data
                'select': product type on keeper selected id
            }
            request.user : user that send this request
        """

        product = Product.objects.get(pk=request.data["product"])
        keeper = KeeperCountItem.objects.get(pk=request.data["select"])

        if request.data["count"] < keeper.amount and (product.countCanBuy == 0 or product.countCanBuy >= request.data["count"]):
            try:
                cartItem = CartItem.objects.get(
                    user=request.user.pk, product=product)
                if request.data["count"] == 0:
                    cartItem.delete()
                else:
                    cartItem.count = request.data["count"]
                    cartItem.select = keeper
                    cartItem.save()

            except Exception as e:
                print("in user view -> ", e)
                cartItem = CartItem(
                    user=request.user, product=product, count=request.data["count"], select=keeper
                )

                cartItem.save()

            return Response(
                {"id": cartItem.pk},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
