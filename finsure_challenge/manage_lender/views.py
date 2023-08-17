from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, CreateModelMixin
from .models import Lender
from .serializers import LenderSerializer
from rest_framework import generics
import io, csv, pandas as pd
from django.http import HttpResponse
from django.views.generic import TemplateView
from rest_framework.pagination import LimitOffsetPagination

class LenderView(
  APIView,
  UpdateModelMixin, 
  DestroyModelMixin, 
):
  """This class is used for Lender endpoints based on Http methods"""
  def get(self, request, id=None):
    """This method is used to get list of Lenders or specific Lender"""
    if id:
      try:
        queryset = Lender.objects.get(id=id)
      except Lender.DoesNotExist:
        return Response({'errors': 'This Lender item does not exist.'}, status=400)
      read_serializer = LenderSerializer(queryset)
    else:
      #offset= int(request.query_params["offset"],0)
      offset=int(request.GET.get('offset', 0))
      limit=5
      if offset > 0:
          offset= (limit * offset);
      queryset = Lender.objects.all().filter(is_active= True)[offset:offset + 5]
      read_serializer = LenderSerializer(queryset, many=True)
    return Response(read_serializer.data)


  def post(self, request):
    """This method is used to create new Lender"""
    create_serializer = LenderSerializer(data=request.data)
    if create_serializer.is_valid():
      Lender_item_object = create_serializer.save()
      read_serializer = LenderSerializer(Lender_item_object)
      if read_serializer.data:
          return Response({"Message": "Lender created Successfully!"}, status=200)
    return Response(create_serializer.errors, status=400)


  def put(self, request, id=None):
    """This method is used to update a Lender"""
    try:
      Lender_item = Lender.objects.get(id=id)
    except Lender.DoesNotExist:
      return Response({'errors': 'This Lender id does not exist.'}, status=400)
    update_serializer = LenderSerializer(Lender_item, data=request.data)
    if update_serializer.is_valid():
      Lender_item_object = update_serializer.save()
      read_serializer = LenderSerializer(Lender_item_object)
      if read_serializer.data:
          return Response({"Message": "Lender updated Successfully!"}, status=200)
    return Response(update_serializer.errors, status=400)


  def delete(self, request, id=None):
    """This method is used to delete a Lender"""
    try:
      Lender_item = Lender.objects.get(id=id)
    except Lender.DoesNotExist:
      return Response({'errors': 'This Lender id does not exist.'}, status=400)
    Lender_item.delete()
    return Response({"Message": "Lender deleted Successfully!"}, status=200)


class CsvUploader(TemplateView):
    """This method is used to upload Lenders csv file """
    template_name = 'csv_uploader.html'
    def post(self, request):
        context = {
            'messages':[]
        }
        csv = request.FILES['csv']
        csv_data = pd.read_csv(
            io.StringIO(
                csv.read().decode("utf-8")
            )
        )

        for record in csv_data.to_dict(orient="records"):
            try:
                Lender.objects.create(
                    name = record['name'],
                    code = record['code'],
                    upfront_comm_rate = record['upfront_comm_rate'],
                    trail_comm_rate = record['trail_comm_rate'],
                    is_active = record['is_active']
                )
            except Exception as e:
                context['exceptions_raised'] = e
                
        return render(request, self.template_name, context)

class CsvDownload(APIView):
    def get(self, request):
        """This method is used to download a csv file"""
    # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="lenders_information.csv"'},
        )

        writer = csv.writer(response)
        queryset = Lender.objects.all()
        read_serializer = LenderSerializer(queryset, many=True)
        for lender in read_serializer.data:
            writer.writerow([lender["name"],lender["code"], lender["upfront_comm_rate"], lender["trail_comm_rate"], lender["is_active"]])
        return response