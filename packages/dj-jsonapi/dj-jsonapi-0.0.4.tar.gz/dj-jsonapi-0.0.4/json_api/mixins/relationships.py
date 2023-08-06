
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from json_api.exceptions import MethodNotAllowed


class RetrieveRelationshipMixin(object):
    def retrieve_relationship(self, request, pk, relname, *args, **kwargs):
        rel = self.get_relationship(relname)
        instance = self.get_object()
        response_data = self.build_relationship_object(rel, instance, include_linkage=True)
        return Response(response_data)


class ManageRelationshipMixin(object):
    def create_relationship(self, request, pk, relname, *args, **kwargs):
        rel = self.get_relationship(relname)
        if not rel.info.to_many:
            raise MethodNotAllowed(request.method)

        data = self.get_data(request.data)
        self.perform_relationship_create(rel, data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update_relationship(self, request, pk, relname, *args, **kwargs):
        rel = self.get_relationship(relname)
        data = self.get_data(request.data)
        self.perform_relationship_update(rel, data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy_relationship(self, request, pk, relname, *args, **kwargs):
        rel = self.get_relationship(relname)
        if not rel.info.to_many:
            raise MethodNotAllowed(request.method)

        data = self.get_data(request.data)
        self.perform_relationship_destroy(rel, data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def perform_relationship_create(self, rel, data):
        instance = self.get_object()
        related = self.get_related_from_data(rel, data)

        self.link_related(rel, instance, related)

    @transaction.atomic
    def perform_relationship_update(self, rel, data):
        instance = self.get_object()
        related = self.get_related_from_data(rel, data)

        self.set_related(rel, instance, related)

        # Only to-one relationships need to be saved
        if not rel.info.to_many:
            if rel.attname in self.model_info.reverse_relations:
                related.save()
            else:
                instance.save()

    @transaction.atomic
    def perform_relationship_destroy(self, rel, data):
        instance = self.get_object()
        related = self.get_related_from_data(rel, data)

        self.unlink_related(rel, instance, related)
