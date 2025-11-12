from rest_framework import serializers
from adminApp.models import CandidatoOpcion, Eleccion, Votante, SesionVotacion, Terminal, Voto, Auditoria

class CandidatoOpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidatoOpcion
        fields = '__all__'