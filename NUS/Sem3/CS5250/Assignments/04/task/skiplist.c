#include <stdio.h>
#include <stdlib.h>
#include "skiplist.h"

skiplist_layer *get_last_layer(skiplist *s)
{
	if (s->head == NULL)
		return NULL;

	skiplist_layer *last_layer;
	for (last_layer = s->head; last_layer->next != NULL; last_layer = last_layer->next)
		;
	return last_layer;
}

void add_new_layer(skiplist *s)
{
	s->height++;
	int new_layer_index = s->height - 1;
	skiplist_layer *new_layer = (skiplist_layer *)malloc(sizeof(skiplist_layer));
	new_layer->layer_index = new_layer_index;
	new_layer->head = NULL;
	new_layer->next = NULL;
	new_layer->prev = NULL;

	// add new layer to skiplist
	skiplist_layer *last_layer = get_last_layer(s);
	if (last_layer == NULL)
	{
		// first layer
		s->head = new_layer;
	}
	else
	{
		last_layer->next = new_layer;
		new_layer->prev = last_layer;
	}
}

void init_skiplist(skiplist *s)
{
	// create one layer during initialization
	s->height = 0;
	s->head = NULL;

	add_new_layer(s);
}

void free_skiplist_layer(skiplist_layer *layer)
{
	for(item *i = layer->head; i != NULL;)
	{
		item *next = i->next;
		free(i);
		i = next;
	}
	layer->head = NULL;
}

void free_skiplist(skiplist* s)
{
	for(skiplist_layer *layer = s->head; layer != NULL;)
	{
		skiplist_layer *next = layer->next;
		free_skiplist_layer(layer);
		free(layer);
		layer = next;
	}
	init_skiplist(s);
}

skiplist_layer *get_layer(skiplist *s, int layer_index)
{
	skiplist_layer *layer;
	for (layer = s->head; layer != NULL && layer->layer_index != layer_index; layer = layer->next)
		;
	return layer;
}

void print_skiplist_layer(skiplist_layer *layer)
{
	printf("Layer %d: ", layer->layer_index);
	for (item *i = layer->head; i != NULL; i = i->next)
	{
		printf("%d ", i->key);
		if (i->next == i){
			printf("ERROR\n");
			exit(1);
		}
	}
	printf("\n");
}

void print_skiplist(skiplist *s)
{
	// print from last layer to first
	printf("Skiplist:\n");
	for (skiplist_layer *layer = get_last_layer(s); layer != NULL; layer = layer->prev)
	{
		print_skiplist_layer(layer);
	}
}

item *ins_layer(skiplist_layer *layer, int k, skiplist_item_type *v)
{
	item *new_item = (item *)malloc(sizeof(item));
	new_item->key = k;
	new_item->value = v;
	new_item->next = NULL;
	new_item->prev = NULL;
	new_item->layer = layer;
	new_item->down = NULL;
	// check first item
	if (layer->head == NULL)
	{
		// first item is empty
		layer->head = new_item;
		return new_item;
	}
	else
	{
		if (layer->head->key >= k)
		{
			// insert before first item
			item *next = layer->head;
			layer->head = new_item;
			new_item->next = next;
			next->prev = new_item;
			return new_item;
		}
	}

	// otherwise, iterate over linked list
	for (item *i = layer->head; i != NULL; i = i->next)
	{
		if (i->next == NULL)
		{
			// insert to last item
			i->next = new_item;
			new_item->prev = i;
			return new_item;
		}

		if (i->next->key >= k)
		{
			// insert between i and next
			new_item->next = i->next;
			new_item->prev = i;
			i->next = new_item;
			new_item->next->prev = new_item;
			return new_item;
		}

		// continue
	}

	// should not reach here
	return NULL;
}

int generate_layer_index(int k)
{
	return k & 0xf; // last 4 bits
}

int ins_skiplist(skiplist *s, int k, skiplist_item_type *v)
{
	int layer_index = generate_layer_index(k);
	for (; s->height <= layer_index;)
		add_new_layer(s);

	item *prev = NULL;
	for (skiplist_layer *layer = get_layer(s, layer_index); layer != NULL; layer = layer->prev)
	{
		item *current = ins_layer(layer, k, v);
		if (prev != NULL)
		{
			prev->down = current;
		}
		prev = current;
	}
	return 1;
}

item *search(item *p_item, int k)
{
	if (p_item == NULL)
	{
		return NULL;
	}

	for (item *i = p_item; i != NULL && i->key <= k;)
	{
		if (i->key == k)
		{
			return i;
		}

		if (i->next == NULL)
		{
			i = i->down;
			continue;
		}

		if (i->next->key > k)
		{
			i = i->down;
			continue;
		}

		i = i->next;
	}
	return NULL;
}

item *query_skiplist(skiplist *s, int k)
{
	skiplist_layer *layer;
	item* i;
	// find layer that is not empty
	for (layer = get_last_layer(s); layer != NULL; layer = layer->prev)
	{
		if (layer->head != NULL)
		{
			i = search(layer->head, k);
			if (i != NULL)
			{
				break;
			}
		}
	}
	if (layer == NULL)
	{
		return NULL;
	}
	return i;
}

int del_skiplist(skiplist *s, int k)
{
	item* i = query_skiplist(s, k);
	if (i == NULL)
	{
		return 0;
	}

	for (; i != NULL;)
	{
		item *to_delete = i;
		if (i->prev == NULL)
		{
			// first item
			i->layer->head = i->next;
			if (i->next != NULL)
			{
				i->next->prev = NULL;
			}
		}
		else if (i->next == NULL)
		{
			// last item
			i->prev->next = NULL;
		}
		else
		{
			i->prev->next = i->next;
			i->next->prev = i->prev;
		}
		item *down = i->down;
		free(to_delete);
		i = down;
	}
	return 1;
}