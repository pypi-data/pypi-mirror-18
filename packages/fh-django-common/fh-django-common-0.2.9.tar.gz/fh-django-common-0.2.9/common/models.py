from collections import OrderedDict

from django.db import models
from django.db.models import QuerySet


class DateTimeModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')

    class Meta:
        abstract = True


def mptt_build_tree(queryset, children_key):
    '''
    :param queryset: the entire tree, or portion of tree, you're trying to construct
    :param children_key: key to store children, can't be a field name that's already on the model
    :return: QuerySet, with children (also QuerySets) properly nested to each level present
    '''
    nodes = OrderedDict()
    nodes_children = OrderedDict()

    for row in queryset:
        nodes[row.id] = row
        if nodes_children.get(row.parent_id):
            nodes_children[row.parent_id]._result_cache.append(row)
        else:
            nodes_children[row.parent_id] = QuerySet()
            nodes_children[row.parent_id]._result_cache = [row]

    for k, node in nodes.iteritems():
        # Try to find the parent so we can attach the child nodes
        setattr(node, children_key, QuerySet())
        children = getattr(node, children_key)
        children._result_cache = []
        if nodes.get(node.parent_id):
            children = getattr(nodes[node.parent_id], children_key)
            children._result_cache.append(node)

    # Build out root nodes for the base level of the list
    root_nodes = QuerySet()
    root_nodes._result_cache = []
    for node_id, node in nodes.iteritems():
        if node.parent_id is None:
            root_nodes._result_cache.append(node)

    return root_nodes


class MPTTDescendantsTreeMixin(object):

    def get_descendants_as_tree(self, children_key='children'):
        return mptt_build_tree(self.get_descendants(include_self=True), children_key=children_key)[0]
