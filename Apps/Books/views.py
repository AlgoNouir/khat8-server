from rest_framework.views import APIView
from rest_framework.response import Response
from Apps.Books.models import Books
from rest_framework import status, permissions


class BookView(APIView):
    
    permission_classes=[permissions.AllowAny]
    authentication_classes = []    
    # book/
    def post(self, request):
        """
        request for add booking
        """
        
        data = request.data

        try:
            book, isCreate = Books.objects.get_or_create(
                mobNo=data['mobNo']
            )
            book.name = data['name']

        except ValueError:
            return Response("فیلد های مربوطه را به درستی وارد کنید", status=status.HTTP_400_BAD_REQUEST)

        book.save()
        
        return Response(status=status.HTTP_200_OK)
