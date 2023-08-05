from __future__ import absolute_import

from functools import partial

from graphene import relay
from graphene.relay.connection import PageInfo
from graphql_relay import from_global_id
from graphql_relay import to_global_id
from graphql_relay.connection.connectiontypes import Edge

from graphene_pynamodb.relationships import RelationshipResultList
from graphene_pynamodb.utils import get_key_name


class PynamoConnectionField(relay.ConnectionField):
    def __init__(self, type, *args, **kwargs):
        super(PynamoConnectionField, self).__init__(
            type,
            *args,
            **kwargs
        )

    @property
    def model(self):
        return self.type._meta.node._meta.model

    @classmethod
    def get_query(cls, model, context, info, args):
        return model.scan

    @classmethod
    def connection_resolver(cls, resolver, connection, model, root, args, context, info):
        iterable = resolver(root, args, context, info)

        first = args.get('first')
        (_, after) = from_global_id(args.get('after')) if args.get('after') else (None, None)
        last = args.get('last')
        (_, before) = from_global_id(args.get('before')) if args.get('before') else (None, None)
        has_previous_page = bool(after)
        page_size = first if first else last if last else None
        connection_type = connection
        pageinfo_type = PageInfo

        # get a full scan query since we have no resolved iterable from relationship or resolver function
        if not iterable and not root:
            query = cls.get_query(model, context, info, args)
            iterable = query()
            if first or last or after or before:
                raise NotImplementedError(
                    "DynamoDB scan operations have no predictable sort. Arguments first, last, after " +
                    "and before will have unpredictable results")

        iterable = iterable if isinstance(iterable, list) else list(iterable) if iterable else []
        if last:
            iterable = iterable[-last:]

        (has_next, edges) = cls.get_edges_from_iterable(iterable, model, info, edge_type=connection.Edge, after=after,
                                                        page_size=page_size)

        key_name = get_key_name(model)
        try:
            start_cursor = getattr(edges[0].node, key_name)
            end_cursor = getattr(edges[-1].node, key_name)
        except IndexError:
            start_cursor = None
            end_cursor = None

        # Construct the connection
        return connection_type(
            edges=edges,
            page_info=pageinfo_type(
                start_cursor=start_cursor if start_cursor else '',
                end_cursor=end_cursor if end_cursor else '',
                has_previous_page=has_previous_page,
                has_next_page=has_next
            )
        )

    def get_resolver(self, parent_resolver):
        return partial(self.connection_resolver, parent_resolver, self.type, self.model)

    @classmethod
    def get_edges_from_iterable(cls, iterable, model, info, edge_type=Edge, after=None, page_size=None):
        has_next = False

        key_name = get_key_name(model)
        after_index = 0
        if after:
            after_index = next((i for i, item in enumerate(iterable) if str(getattr(item, key_name)) == after), None)
            if after_index is None:
                return None
            else:
                after_index += 1

        if page_size:
            has_next = len(iterable) - after_index > page_size
            iterable = iterable[after_index:after_index + page_size]
        else:
            iterable = iterable[after_index:]

        # trigger a batch get to speed up query instead of relying on lazy individual gets
        if isinstance(iterable, RelationshipResultList):
            iterable = iterable.resolve()

        edges = [edge_type(node=entity, cursor=to_global_id(model.__name__, getattr(entity, key_name)))
                 for entity in iterable]

        return [has_next, edges]
