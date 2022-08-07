//
// Data Prefetching Championship Simulator 2
// Seth Pugsley, seth.h.pugsley@intel.com
//

#include <stdio.h>
#include <map>
#include <vector>
#include "../inc/prefetcher.h"

#define LIST_SIZE 65536
typedef unsigned long long address;
std::vector<address> addr_list;
size_t head;

size_t prev(size_t current) {
  if (addr_list.size() == 0)
    return 0;
  
  if (current == 0) {
    current = addr_list.size() - 1;
  }
  else
  {
    current -= 1;
  }
  return current;
}

size_t next(size_t current) {
  if (addr_list.size() == 0)
    return 0;

  current += 1;
  if (current >= addr_list.size() - 1) {
    current = 0;
  }
  return current;
}

void add(address value) {
  if (addr_list.size() < LIST_SIZE) {
    addr_list.push_back(value);
    head = addr_list.size() - 1;
  }
  else
  {
    head = next(head);
    addr_list[head] = value;
  }
}

void l2_prefetcher_initialize(int cpu_num)
{
  printf("GHB Prefetcher\n");
  // you can inspect these knob values from your code to see which configuration you're runnig in
  printf("Knobs visible from prefetcher: %d %d %d\n", knob_scramble_loads, knob_small_llc, knob_low_bandwidth);

  head = 0;
}

void add_map(std::map<address, int> *frequency, address pref_index) {
  std::map<address, int>::iterator iter = frequency->find(pref_index);
  if (iter != frequency->end()) {
    // exist
    int value = iter->second;
    value++;
    (*frequency)[pref_index] = value;
  }
  else
  {
    frequency->insert(std::make_pair(pref_index, 1));
  }
}

address find_max_pref_addr(std::map<address, int> *frequency) {
  address max_key = 0;
  int max_value = 0;
  for (std::map<address, int>::iterator iter = frequency->begin(); iter != frequency->end(); iter++) {
    if (iter->second > max_value) {
      max_value = iter->second;
      max_key = iter->first;
    }
  }
  return max_key;
}

void l2_prefetcher_operate(int cpu_num, unsigned long long int addr, unsigned long long int ip, int cache_hit)
{
  // uncomment this line to see all the information available to make prefetch decisions
  //printf("(0x%llx 0x%llx %d %d %d) ", addr, ip, cache_hit, get_l2_read_queue_occupancy(0), get_l2_mshr_occupancy(0));
  address cache = (addr >> 6) << 6;
  add(cache);
  size_t current = head;
  std::map<address, int> frequency;
  for (size_t index = prev(current); index != current; index = prev(index))
  {
    if (addr_list[index] == cache)
    {
      size_t pref_index = next(index);
      //l2_prefetch_line(0, addr, addr_list[pref_index], FILL_L2);
      add_map(&frequency, addr_list[pref_index]);
    }
  }
  address max_pref_addr = find_max_pref_addr(&frequency);
  if (max_pref_addr != 0) {
    l2_prefetch_line(0, addr, max_pref_addr, FILL_L2);
  }
  else
  {
    // not found
    //l2_prefetch_line(0, addr, ((addr>>6)+1)<<6, FILL_L2);
  }
}

void l2_cache_fill(int cpu_num, unsigned long long int addr, int set, int way, int prefetch, unsigned long long int evicted_addr)
{
  // uncomment this line to see the information available to you when there is a cache fill event
  //printf("0x%llx %d %d %d 0x%llx\n", addr, set, way, prefetch, evicted_addr);
}

void l2_prefetcher_heartbeat_stats(int cpu_num)
{
  printf("Prefetcher heartbeat stats\n");
}

void l2_prefetcher_warmup_stats(int cpu_num)
{
  printf("Prefetcher warmup complete stats\n\n");
}

void l2_prefetcher_final_stats(int cpu_num)
{
  printf("Prefetcher final stats\n");
}
