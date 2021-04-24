def partition(array, low, high):
    pivot = array[(low + high) // 2]['created_at']
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while array[i]['created_at'] < pivot:
            i += 1

        j -= 1
        while array[j]['created_at'] > pivot:
            j -= 1

        if i >= j:
            return j

        array[i], array[j] = array[j], array[i]
    pass

def quick_sort(array):
    def _quick_sort(items, low, high):
        if low < high:
            split_index = partition(items, low, high)
            _quick_sort(items, low, split_index)
            _quick_sort(items, split_index + 1, high)

    _quick_sort(array, 0, len(array) - 1)
    pass


def sort_by_user(logs: list) -> dict:
    users_logs = dict()
    for log in logs:
        user_id = log['user_id']
        item = users_logs.get(user_id, [])
        item.append(log)
        users_logs[user_id] = item
    return users_logs
