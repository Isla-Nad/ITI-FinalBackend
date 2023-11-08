from rest_framework.decorators import api_view
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from medicalHistory.models import MedicalHistory
from medicalHistory.api.serializer import MedicalSerlizer
from rest_framework.generics import DestroyAPIView
from rest_framework import status

@api_view(['GET','POST'])
def medicalhistoryapidata(request):
    if request.method=="POST":
          information=MedicalHistory.objects.create( patient_name=request.data['patient_name'], date_of_visit=request.data['date_of_visit'],action=request.data['action'], Allergies=request.data['Allergies'], MedicalConditions=request.data['MedicalConditions'],PreviouDentalTreatments=request.data['PreviouDentalTreatments'],DentalConditions=request.data['DentalConditions'],DentalHygieneHabits=request.data['DentalHygieneHabits'],image=request.data['image'])

          information.save()
          return Response({'products':MedicalSerlizer(information).data})

    elif request.method =="GET":
         data=MedicalHistory.objects.all()
         pro_seralizer=[]
         for info in data:
             print(MedicalSerlizer(info).data)
             pro_seralizer.append(MedicalSerlizer(info).data)

         return Response({"data":pro_seralizer})
class MedicalhistoryDelete(DestroyAPIView):
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalSerlizer    
class MedicalhistoryUpdate(UpdateAPIView):
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalSerlizer   
