#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def bubble_sort(arr):
    """
    冒泡排序算法
    :param arr: 待排序的列表
    :return: 排序后的列表
    """
    n = len(arr)
    # 遍历所有数组元素
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # 如果当前元素大于下一个元素，则交换它们
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

if __name__ == "__main__":
    # 示例用法
    sample_data = [64, 34, 25, 12, 22, 11, 90]
    print("原始数组:", sample_data)
    sorted_data = bubble_sort(sample_data.copy())
    print("排序后数组:", sorted_data)
