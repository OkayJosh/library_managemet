"""
Base Repository
"""
from typing import List, Union, Dict, Any


class BaseRepository:
    """
    Base repository class for handling common database operations.
    """

    def __init__(self, model_class, databases: Union[str, List[str]] = None):
        """
        Initialize the repository with a list of databases.
        :param model_class: The model class for this repository.
        :param databases: List of database identifiers or a single identifier.
        """
        if databases is None:
            databases = ['default', 'admin']
        if isinstance(databases, str):
            databases = databases.split(',')
        self.databases = databases
        self.model_class = model_class
        self.orm = model_class

    def _get_queryset(self, database):
        """
        Get the queryset for a specific database.
        :param database: Database identifier.
        :return: QuerySet for the specified database.
        """
        return self.orm.objects.using(database)

    def add(self, instance):
        """
        Add a new instance to all specified databases.
        :param instance: Instance to add.
        :return: List of results for each database operation.
        """
        results = []
        for db in self.databases:
            model_instance = self.model_class(**instance)
            result = model_instance.save(using=db)
            results.append(result)
        return results

    def remove(self, **kwargs):
        """
        Remove an instance from all specified databases.
        :param kwargs: Filters for the instance to remove.
        :return: Dictionary of results for each database operation.
        """
        results = {}
        for db in self.databases:
            try:
                instance = self._get_queryset(db).get(**kwargs)
                instance.delete()
                results[db] = True
            except self.model_class.DoesNotExist:
                results[db] = False
        return results

    def get(self, **kwargs):
        """
        Fetch an instance by its attributes from the first available database.
        :param kwargs: Filters for the instance to fetch.
        :return: Instance or None if not found.
        """
        for db in self.databases:
            try:
                return self._get_queryset(db).get(**kwargs)
            except self.model_class.DoesNotExist:
                continue
        return None

    def list(self, **filters):
        """
        List instances from all specified databases with optional filters.
        :param filters: Filters for listing instances.
        :return: List of instances from all databases.
        """
        results = []
        for db in self.databases:
            queryset = self._get_queryset(db).filter(**filters)
            results.extend(queryset)
        return results

    def update(self, filters: Dict[str, Any], updates: Dict[str, Any]):
        """
        Update instances matching the filters in all specified databases.
        :param filters: Filters for selecting instances to update.
        :param updates: Fields and values to update.
        :return: Dictionary of results for each database operation.
        """
        results = {}
        for db in self.databases:
            queryset = self._get_queryset(db).filter(**filters)
            count = queryset.update(**updates)
            results[db] = count
        return results
