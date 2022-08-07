#include <stdio.h>
#include <stdlib.h>
#include "skiplist.h"

#define TASK 2

#if TASK == 1

#define PRINT print_skiplist(&list)
#define QUERY(N)                               \
	do                                         \
	{                                          \
		if (query_skiplist(&list, (N)) == NULL)  \
		{                                      \
			printf("%d does not exist!\n", (N)); \
		}                                      \
	} while (0)
#define INSERT(N) ins_skiplist(&list, (N), NULL); QUERY((N))
#define DELETE(N) del_skiplist(&list, (N))

int main()
{
	skiplist list;
	init_skiplist(&list);
	PRINT;

	INSERT(5);
	INSERT(10);
	INSERT(100);
	INSERT(24);
	INSERT(3);
	INSERT(101);
	INSERT(99);
	INSERT(55);
	INSERT(11);
	INSERT(10);
	INSERT(7);
	PRINT;
	DELETE(5);
	PRINT;
	INSERT(7);
	DELETE(5);
	PRINT;
	free_skiplist(&list);

	return 0;
}

#elif TASK == 2

#define INPUT_FILE "input.txt"
#define RR_INTERVAL 6
#define SCALING_FACTOR 8192
#define SIM_TIMES 10
#define TO_NIFFIES(N) (N) * 1000000
#include "prio_ratio.h"

int count;

typedef skiplist_item_type process;

int calc_deadline(int current_ms, int niceness)
{
	return TO_NIFFIES(current_ms) + get_prio_ratio(niceness) * RR_INTERVAL * SCALING_FACTOR;
}

process* search_process(process* procs, int time)
{
	for (int i = 0; i < count; i++)
	{
		if (procs[i].arrival_time == time)
		{
			return &procs[i];
		}
	}
	return NULL;
}

void start_sim(process* procs, skiplist* list)
{
	item* current_item = NULL;
	for (int current_ms = 0; current_ms < 140; current_ms++)
	{
		printf("Time: %d\n", current_ms);
		process* proc_to_ins = search_process(procs, current_ms);
		if (proc_to_ins != NULL)
		{
			ins_skiplist(list, calc_deadline(current_ms, proc_to_ins->niceness), proc_to_ins);
		}
		if (current_item == NULL)
		{
			current_item = list->head->head;
		}
		if (current_item != NULL)
		{
			current_item->value->cpu_time++;
			if (current_item->value->cpu_time >= current_item->value->duration)
			{
				// remove process
				del_skiplist(list, current_item->key);
				current_item = list->head->head;
				continue;
			}

			// update deadline
			int deadline = current_item->key;
			process* value = current_item->value;
			int new_deadline = calc_deadline(current_ms, current_item->value->niceness);
			del_skiplist(list, deadline);
			ins_skiplist(list, new_deadline, value);
			current_item = query_skiplist(list, new_deadline);
			print_skiplist(list);

			if (current_ms % RR_INTERVAL == 0)
			{
				// schedule to another process
				current_item = list->head->head;
			}
		}
	}
}

int main()
{
	skiplist list;
	init_skiplist(&list);
	FILE* fp = fopen(INPUT_FILE, "r");
	fscanf(fp, "%d\n", &count);
	process* procs = (process*)malloc(sizeof(process) * count);
	for (int i = 0; i < count; i++)
	{
		fscanf(fp, "%c %d %d %d\n", &procs[i].name, &procs[i].arrival_time, &procs[i].niceness, &procs[i].duration);
		printf("%c %d %d %d\n", procs[i].name, procs[i].arrival_time, procs[i].niceness, procs[i].duration);
		procs[i].cpu_time = 0;
	}

	printf("Start\n");
	start_sim(procs, &list);
	printf("End\n");

	free(procs);
	return 0;
}

#endif