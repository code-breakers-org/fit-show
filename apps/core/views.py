from rest_framework import generics


class HealthView(generics.RetrieveAPIView):
    serializer_class = None
    pass