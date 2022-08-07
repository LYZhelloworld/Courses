#ifndef __SKIPLIST_H
#define __SKIPLIST_H

typedef struct {
	char name;
	int arrival_time;
	int niceness;
	int duration;
	int cpu_time;
} skiplist_item_type;

typedef struct tag_skiplist_layer skiplist_layer;
typedef struct tag_item item;
typedef struct tag_skiplist skiplist;

typedef struct tag_item
{
	int key;
	skiplist_item_type *value;
	struct tag_item *next; // point to next item or NULL
	struct tag_item *prev; // point to previous item or NULL
	skiplist_layer *layer; // point to layer
	struct tag_item *down; // point to item with same value in previous layer
} item;

typedef struct tag_skiplist_layer
{
	int layer_index;				 // start from 0
	item *head;						 // first item or NULL if layer is empty
	struct tag_skiplist_layer *next; // point to next layer or NULL
	struct tag_skiplist_layer *prev; // point to previous layer or NULL
} skiplist_layer;

typedef struct tag_skiplist
{
	int height;			  // 0 for no layers, 1 for one layer, etc
	skiplist_layer *head; // first layer or NULL if there is no layers
} skiplist;

void init_skiplist(skiplist *);
void print_skiplist(skiplist *);
int ins_skiplist(skiplist *, int, skiplist_item_type*);
item *query_skiplist(skiplist *, int);
int del_skiplist(skiplist *, int);
void free_skiplist(skiplist *);

#endif // __SKIPLIST_H