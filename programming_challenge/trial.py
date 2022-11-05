import csv
import heapq
import math
from heapq import heappush
import merge_sort

x_list = []
y_list = []
coordinates_list = []
distance_list = []
maxHeap = []
fruits = []
with open('input.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    first_row = next(reader)
    # random coordinates
    rc = (int(first_row[0]), int(first_row[1]))
    for row in reader:
        c = (int(row[0]), int(row[1]))
        x, y = int(row[0]), int(row[1])
        distance = math.sqrt((c[0] - rc[0])**2 + (c[1] - rc[1])**2)
        maxHeap.append([distance, x, y])
    merge_sort.mergeSort(maxHeap)

dictionary = {10: [rc], 25: [rc], 63: [rc], 159: [rc], 380: [rc]}
def find_points(maxHeap, N):
    furthest = maxHeap[-1][0]
    radius = round(furthest/ N)
    min_bound = radius
    max_bound = radius * 2
    for i in range(N - 1):
        for num in maxHeap:
            if min_bound < num[0] <= max_bound:
                p = (num[1], num[2])
                dictionary[N].append(p)
                break

        min_bound += radius
        max_bound += radius

# Challenge: In the case that there is no point within the range, our approach
#            cannot find enough points. Therefore, we are thinking of reducing the
#             size of radius to solve this problem

lst = [10,25,63,159,380]
for i in lst:
    find_points(maxHeap, i)
    with open(f'{i}.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(dictionary[i])



