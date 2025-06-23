# api_v1/calendar_main/controllers/calendar.py
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
# Importamos los permisos necesarios
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly

# Importa tus serializers y modelos
from calendar_main.models import Event, EventType, Department, Contact, AdditionalObservation
from calendar_main.serializers import (
    EventSerializer,
    EventTypeSerializer,
    DepartmentSerializer,
    ContactSerializer,
    AdditionalObservationSerializer,
)

# --- EventController ---
class EventController(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    # Establecemos una lista de clases de permisos.
    # Se evalúan en orden. Si la primera no permite, se intenta la siguiente.
    # Pero para este caso, crearemos una lógica personalizada dentro del método 'get_permissions'.
    # permission_classes = [IsAuthenticatedOrReadOnly] # Esto solo da acceso de escritura a cualquier autenticado

    def get_permissions(self):
        """
        Sobreescribe este método para aplicar permisos condicionalmente.
        """
        # Si la solicitud es un método "seguro" (GET, HEAD, OPTIONS),
        # permitimos el acceso a cualquier persona (incluso no autenticada).
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        # Para cualquier otro método (POST, PUT, PATCH, DELETE),
        # solo permitimos el acceso a usuarios administradores.
        return [IsAdminUser()]

# --- El resto de tus controladores (EventTypeController, DepartmentController, etc.) ---
# Estos pueden seguir con IsAdminUser si solo los administradores deben gestionarlos
# O IsAuthenticatedOrReadOnly si quieres que cualquiera pueda leerlos pero solo autenticados puedan modificarlos

class EventTypeController(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    # Aquí decidimos si cualquiera puede ver los tipos de evento o si solo los administradores
    # Por ejemplo, si solo admins pueden CRUD:
    permission_classes = [IsAdminUser] # Solo administradores pueden gestionar tipos de evento

class DepartmentController(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminUser] # Solo administradores pueden gestionar departamentos

class ContactController(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAdminUser] # Solo administradores pueden gestionar contactos

class AdditionalObservationController(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = AdditionalObservation.objects.all()
    serializer_class = AdditionalObservationSerializer
    permission_classes = [IsAdminUser] # Solo administradores pueden gestionar observaciones adicionales