#include <stdio.h>
#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif // _WIN32

#define MAX_FREQ_ARR_SIZE 20
#define CPU0_ALL_FREQS ""
#define CPU1_ALL_FREQS ""
#define CPU0_TARGET_FREQ ""
#define CPU1_TARGET_FREQ ""
#define COUNTER_FILENAME ""
#define TARGET_FILENAME "target.txt"

typedef struct {
	char* CPU_ALL_FREQS;
	char* CPU_TARGET_FREQ;
	int freq_arr[MAX_FREQ_ARR_SIZE];
	int freq_arr_size;
	int current;
} processor;

void init(processor p, char* cpu_all_freqs, char* cpu_target_freq) {
	p.CPU_ALL_FREQS = cpu_all_freqs;
	p.CPU_TARGET_FREQ = cpu_target_freq;
	read_freqs(p);
	p.current = 0;
	write_freq(p);
}

void read_freqs(processor p) {
	int value;
	FILE* fp = fopen(p.CPU_ALL_FREQS, "r");
	for(int i = 0; fscanf(fp, "%d", &value) != EOF; i++) {
		p.freq_arr[i] = value;
	}
	fclose(fp);
	p.freq_arr_size = i;
	return;
}

void write_freq(processor p) {
	FILE* fp = fopen(p.CPU_TARGET_FREQ, "w");
	fprintf(fp, "%d", get_current_freq(p));
	fclose(fp);
}

int get_current_freq(processor p) {
	return p.freq_arr[freq.current];
}

int increase(processor p) {
	p.current++;
	if (p.current >= p.freq_arr_size) {
		p.current = p.freq_arr_size - 1;
		return -1; // unable to increase
	}
	return 0; // success
}

int decrease(processor p) {
	p.current--;
	if (p.current < 0) {
		p.current = 0;
		return -1; // unable to decrease
	}
	return 0;
}

int read_counter() {
	int counter1, counter2;
	FILE* fp = fopen(COUNTER_FILENAME, "r");
	fscanf(fp, "%d", &counter1);
	fclose(fp);

	sleep(1);
	fp = fopen(COUNTER_FILENAME, "r");
	fscanf(fp, "%d", &counter2);
	fclose(fp);

	return counter2 - counter1;
}

int read_target() {
	int target;
	FILE* fp = fopen(TARGET_FILENAME, "r");
	fscanf(fp, "%d", &target);
	fclose(fp);
	return target;
}

int main() {
	processor cpu0, cpu1;
	int counter, target;
	// Init
	init(cpu0, CPU0_ALL_FREQS, CPU0_TARGET_FREQ);
	init(cpu1, CPU1_ALL_FREQS, CPU1_TARGET_FREQ);

	for(;;) {
		counter = read_counter();
		target = read_target();
		printf("Current: %d, target: %d\n", counter, target);
		if (counter > target) {
			// TODO
		} else if (counter < target) {
			// TODO
		}
	}

	return 0;
}