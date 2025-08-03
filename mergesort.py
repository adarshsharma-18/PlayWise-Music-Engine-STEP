def merge_sort(array, key=lambda x: x, ascending=True):
    # Time: O(n log n), Space: O(n)
    if len(array) <= 1:
        return array

    mid = len(array) // 2
    left = merge_sort(array[:mid], key, ascending)
    right = merge_sort(array[mid:], key, ascending)

    return merge(left, right, key, ascending)

def merge(left, right, key, ascending):
    # Time: O(n), Space: O(n)
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        comp = key(left[i]) <= key(right[j]) if ascending else key(left[i]) >= key(right[j])
        if comp:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

