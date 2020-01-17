#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    for index_1, weight in enumerate(weights):
        index_2 = hash_table_retrieve(ht, limit - weight)
        if index_2 is not None:
            return (max(index_1, index_2), min(index_1, index_2))
        else:
            hash_table_insert(ht, weight, index_1)
        
    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
