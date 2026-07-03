import random
from time import sleep

list_of_number = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# print(f"{'='*10} Queue {'='*10}")
# list_queue = list_of_number.copy()
# while len(list_queue) > 0:
#     if 0.5 <= random.random():
#         list_queue.append(list_queue[-1] + 1)
#
#     print(list_queue)
#     queue = list_queue.pop(0)
#     print(f"Turn: {queue}")
#     sleep(1)
#
#
# print(f"\n\n{'='*10} Stack {'='*10}")
# list_stack = list_of_number.copy()
# biggest = list_stack[-1]
# while len(list_stack) > 0:
#     print(list_stack)
#     stack = list_stack.pop()
#     print(f"Turn: {stack}")
#     sleep(1)
#     if 0.5 <= random.random():
#         biggest += 1
#         list_stack.append(biggest)
#
# print(f"\n\n{'='*10} Deque {'='*10}")
# list_deque = list_of_number.copy()
# biggest_number = max(list_deque)
# while len(list_deque) > 0:
#     sleep(1)
#     print(list_deque)
#
#     chance = random.random()
#     if 0.63 <= chance:
#         list_deque.pop(random.choice([0, -1]))
#     elif 0.33 <= chance:
#         list_deque[0], list_deque[-1] = list_deque[-1], list_deque[0]
#     else:
#         biggest_number += 1
#         list_deque.insert(random.choice([0, -1]), biggest_number)

# print(f"\n\n{'='*10} Lower {'='*10}")
# list_lower = list_of_number.copy()
# while len(list_lower) > 0:
#     print(list_lower)
#     lower_number = min(list_lower)
#     list_lower.remove(lower_number)
#     print(lower_number)
#     sleep(1)
#     if 0.5 <= random.random():
#         list_lower.append(random.randint(1, 9))
#

# print(f"\n\n{'='*10} Round Robin {'='*10}")
# list_robin = list_of_number.copy()
#
# while len(list_robin) > 0:
#     print(list_robin)
#     list_robin[0] -= 1
#     if 0 in list_robin:
#         list_robin.remove(0)
#         continue
#
#     if list_robin:
#         unfinished = list_robin.pop(0)
#         list_robin.append(unfinished)
#
#     sleep(1)

print(f"\n\n{'='*10} Linked List {'='*10}")
class Node:
    def __init__(self, value: list, node: 'Node' = None):
        self.value = value
        self.previous = node


    def __str__(self):
        return f"{self.value}"

node1 = Node([1, 2, 3])
Node.last_node = node1

node2 = Node([4, 5, 6], node1)
node3 = Node([4, 5, 6], node2)

print(node1)
print(node1.previous)
print(node3.previous)