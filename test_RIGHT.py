import logging
import numpy as np
import re
import collections
import math
import time
def twoSum_1(arr,target):
    #### 1. twoSum
    a = []
    for i in range(len(arr)-1):
       if arr[i]+arr[i+1] == target:
           a.append(i)
           a.append(i+1)
    if len(a)!=2:
        a.append('没有答案')
    return a



def addTwoNums(l1,l2): ###倒序存储很重要
    l1 = l1[::-1]
    l2 = l2[::-1]
    num_list = []
    l1_len = len(l1)
    l2_len = len(l2)
    if l1_len == 0:
        print ('ERROE L1')
    if l2_len == 0:
        print ('ERROE L2')
    max_len = max(l1_len,l2_len)
    min_len = min(l1_len, l2_len)
    i = 0
    #辅助遍历 存储加位
    guard = 0
    while i < min_len :
        add_num = float(l1[i]) + float(l2[i])
        add_num = add_num + guard
        if add_num>=10:
            guard = float(str(add_num)[0])
            num_list.append(str(add_num)[1])
        else:
            num_list.append(str(int(add_num)))
        i+=1
    if max_len > i and l1_len == max_len:
        for j in range(i,max_len):
            num_list.append(str(int(l1[j]) + int(guard)))
            guard = 0
    elif max_len > i and l2_len == max_len:
        for j in range(i,max_len):
            num_list.append(str(int(l2[j])+ int(guard)))
            guard = 0
    if guard != 0:
        num_list.append(str(int(guard)))
    num_list.reverse()
    num_list = ''.join(num_list)
    print (num_list)


def LongestSubstringWithoutRChara_3(s):
    ####动态规划   保存最大的substring max_list
    max_s = ''
    max_list = ''  #存储上一个的最长子字符串
    for i in s :
        if i in max_s:###出现重复的字母时
            if len(max_s)>=len(max_list):
                max_list = max_s
            else:
                max_list = max_list
            i_index = max_s.index(i)+1
            max_s = max_s[i_index:] + i
        elif i not in max_s:
            max_s = max_s+ i

        if len(max_s) >= len(max_list) and i==s[-1]:
            max_list = max_s
        elif len(max_s) < len(max_list) and i==s[-1]:
            max_list = max_list
    print(max_list)
    return len(max_list)


def MedianOfTwoSortedArrays_4(num1,num2):
    num1.extend(num2)
    num1.sort()
    num1_len = len(num1)
    result = 0
    if num1_len % 2 !=0:
        idx = int(num1_len/2)
        result = float(num1[idx])
    else:
        idx = int(num1_len / 2)
        idx2 = int(idx -1)
        result = float((num1[idx] + num1[idx2])/2)
    print (result)
    return result

def LongestPalindromicSubstring_5(s):  ###some probles
    #babcad
    max_s = ''
    max_list = ''
    if len(s)==0:
        max_list = 0
    for i in s:
        if i not in max_s:
            max_s = max_s + i
        elif i in max_s:
            idx = max_s.index(i)
            max_s = max_s + i
            max_s2 = max_s[idx:]
            if len(max_s2)>=len(max_list):
                max_list = max_s2
        if len(s) == 1:
            max_list = max_s
    print (max_list)
    return max_list

def longestPalindrome(s):
    if len(s)==0:
        return 0
    maxLen=1
    start=0
    for i in range(len(s)):
        if i-maxLen >=1 and s[i-maxLen-1:i+1]==s[i-maxLen-1:i+1][::-1]:
            start=i-maxLen-1
            maxLen+=2
            continue

        if i-maxLen >=0 and s[i-maxLen:i+1]==s[i-maxLen:i+1][::-1]:
            start=i-maxLen
            maxLen+=1
    print(s[start:start+maxLen])
    return s[start:start+maxLen]


def convert_6(s, numRows):
    times = time.time()
    print (times)
    s_len = len(s)
    if numRows ==1 or s_len<numRows:
        return s
    else:
        #### 正常每列numRows个
        #### 特殊的有numRows-2列
        spe_col = numRows + numRows - 2
        spe_col_num = numRows - 1
        numCols = 0  ###列数
        left = s_len % spe_col
        if left == 0:
            numCols = int((s_len / spe_col) * spe_col_num)
        elif left < spe_col:
            numCols = int(math.floor(s_len / spe_col) * spe_col_num +numRows-1)

        num_list = np.zeros((numRows, numCols))
        num_list = np.array(num_list,dtype=np.str)
        num_list = np.reshape(num_list,(numRows,numCols))
        ###(1,nrow-2)行  (1,nrow-2)* nrows
        print (num_list)
        count = 0
        for j in range(numCols):
            for i in range(numRows):
                if (j % (numRows - 1)==0) and count < s_len:
                    num_list[i][j] = s[count]
                    count = count + 1
                elif count < s_len  and i != 0 and i != numRows - 1 and (j % (numRows-1) + i == numRows - 1):#
                    num_list[i][j] = s[count]
                    print (0,i,j)
                    count = count + 1
        print (num_list)
        result = ''
        for i in range(numRows):
            for j in range(numCols):
                if num_list[i][j]!= '0.0':
                    result = result + num_list[i][j]
        print (result)
        time2 = time.time()
        cha = time2 - times
        print (cha)
        return result


def max_water_11(height_list):
    if len(height_list)>=2:
        height = min(height_list[0], height_list[1])
        max_area = height * 2  # 存储当前最大的存水
        #简单动态规划问题
        for i in range(2,len(height_list)):
            for j in range(i,-1,-1):
                print (j)
                height = min(height_list[j], height_list[j-1])
                pass


    Max = -1
    l = 0
    r = len(height) - 1
    while l < r:
        area = (height[l] if height[l] < height[r] else height[r]) * (r - l)
        Max = Max if Max > area else area
        if height[l] < height[r]:
            k = l
            while l < r and height[l] <= height[k]: l += 1
        else:
            k = r
            while l < r and height[r] <= height[k]: r -= 1
    return Max














def searchMatrix(matrix, target):
    """
    :type matrix: List[List[int]]
    :type target: int
    :rtype: bool
    """
    ####
    ####
    # 从右上角开始, 比较target 和 matrix[i][j]的值. 如果小于target, 则该行不可能有此数,  所以i++;
    # 如果大于target, 则该列不可能有此数, 所以j--. 遇到边界则表明该矩阵不含target.
    a = False
    (m, n) = matrix.shape
    for i in range(0,m):
        for j in range(n-1,-1,-1):
            right = matrix[i,j]
            if right < target:
                i = i+1
                break
            elif right > target:
                j = j-1
                continue
            elif right == target:
                a = True
                break
    print (a)
    return a

def pow_50(x,n):
        for i in range(0,n,int(n/2)):
            if n % 2 == 0:
                x = x * x
                print ('XXXX',x)

# class Solution:
#     def getMinimumDifference(self, root):
#         nums = self.inorder(root)
#         return min(nums[i + 1] - nums[i] for i in range(len(nums) - 1))
#
#     def inorder(self, root):
#         return self.inorder(root.left) + [root.val] + self.inorder(root.right) if root else []

####看不懂
def LargestRectangleHistogram84(height):
    #height = [2,3,4,5,6,4,5,9,2,3,41,2]
    if not height:
        return 0
    res = 0
    stack = []  #存放的是索引 栈
    height.append(-1)
    for i in range(len(height)):
        current = height[i]
        while len(stack) != 0 and current <= height[stack[-1]]:
            h = height[stack.pop()]  #当前前一个的高度
            w = i if len(stack) == 0 else i - stack[-1] - 1 #
            res = max(res, h * w)
        stack.append(i)
    return res


####看不懂
def MaximalRectangle_85(matrix):
    ####不好理解
    (m, n) = matrix.shape
    count = 0
    for i in range(m):
        for j in range(n):
            if j <= n-1 and i<=m-1:
                m_1 = matrix[m,j]
                m_2 = matrix[m,j+1]
                m_3 = matrix[m+1,j]
                m_4 = matrix[m+1,j+1]
                print ((matrix[3,2]))

    pass



def WordBreak_139(s,wordDict):  #动态规划
    # 不要考虑重复项 没用
    #很棒的代码

    maxLength = getMaxLength(wordDict)
    cache = [False for i in range(len(s) + 1)]
    cache[0] = True

    for i in range(1, len(s) + 1):
        j = 1
        while j <= maxLength and j <= i:
            if not cache[i - j]:
                j += 1
                continue
            if s[i - j:i] in wordDict:
                cache[i] = True
                break
            j += 1

    return cache[len(s)]









def getMaxLength(dict):
    maxLength = 0
    for word in dict:
        maxLength = max(len(word), maxLength)
    return maxLength









def MaxAreaofIsland_695():
    pass



def PatchingArray_330(nums,n):
    ###
    ###330. Patching Array  其实是组合问题 贪心算法
    #
    '''
    Example 2:
    nums = [1, 5, 10], n = 20
    Return 2.
    The two patches can be [2, 4].
    :return:
    '''
    pass


def DistinctSubsequences_115(S,T):
    #时间复杂度O(n)
    ##### S是
    ##### 其实是字符串的字母的排列的一部分
    ##### 典型动态规划 - Two Sequence DP
    '''
    eg：
    给出S = "rabbbit", T ="rabbit"
    返回 3
    :return:
    '''
    ###状态cache[i][j]表示S前j位的不同子序列中有几个和T的前i位相同
    s_len = len(S)   #j
    t_len = len(T)  #i
    cache = [[0 for j in range(s_len+1)] for i in range(t_len+1)]
    for j in range(s_len+1):
        cache[0][j] = 1

    for i in range(1,t_len+1):
        for j in range(1,s_len+1):
            if S[j-1] == T[i-1]:
                cache[i][j] = cache[i][j-1] + cache[i-1][j-1]
            elif S[j-1] != T[i-1]:
                cache[i][j] = cache[i][j-1]
    return cache[t_len][s_len]


####九章算法
def countOfAtoms(formula):
    parse = re.findall(r"([A-Z][a-z]*)(\d*)|(\()|(\))(\d*)", formula)
    print('####', (parse))
    print ('####',(parse[0]))
    print('####', len(parse))
    stack = [collections.Counter()]
    print('####', stack)
    for name, m1, left_open, right_open, m2 in parse:
        print('1name', name)
        print('2m1', m1)
        print('3left_open', left_open)
        print('4right_open', right_open)
        print('5m2', m2)
        if name:
            stack[-1][name] += int(m1 or 1)
        if left_open:
            stack.append(collections.Counter())
        if right_open:
            top = stack.pop()
            for k in top:
                stack[-1][k] += top[k] * int(m2 or 1)

    return "".join(name + (str(stack[-1][name]) if stack[-1][name] > 1 else '')
                   for name in sorted(stack[-1]))


# def test():
#     import re
#
#     S = 'AA,BB,DD,EE,AA,A(B,C),CC,A(B,C)'
#     L = filter(None,re.split(r', | ', S))
#     a = [x for x in L if L.count(x) == 1]
#     print (L)
#     print(a)

if __name__ == "__main__":
    logging.basicConfig(
        format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)
    height = [2,4,5,6,7,8]
    max_water_11(height)
    # matrix = [ [1,   4,  7, 11, 15],
    #            [2,   5,  8, 12, 19],
    #            [3,   6,  9, 16, 22],
    #            [10, 13, 14, 17, 24],
    #            [18, 21, 23, 26, 30],
    #            [23, 25, 34, 37, 40]]
    # [
    # [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    # [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
    # [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
    # target = 18
    # matrix = np.mat(matrix)
    #twoSum_1(arr,target)
    #searchMatrix(matrix,target)
    #PatchingArray_330(nums, n)
    # import itertools
    #
    # list1 = [1, 5, 10]
    # n = 20
    # n_list = []
    # for i in range(1,n+1):
    #     n_list.append(i)
    # list2 = []
    # for i in range(1, len(list1) + 1):
    #     iter = itertools.combinations(list1, i)
    #     for m in iter:
    #         m_tuple = m[:]
    #         m_tuple = np.array(m_tuple)
    #         m_sum = m_tuple.sum()
    #         list2.append(m_sum)
    # print(list2)
    # # 简化版：
    # left_list = [item for item in n_list if item not in list2]
    #
    # # 方法.高级版：
    # left_list = list(set(n_list) ^ set(list2))

    #115题
    # S = 'rabbbiit' #7
    # T = 'rabbit' #6
    # num = DistinctSubsequences_115(S, T)

    # arr =    [[1, 0, 1, 0, 0],
    #           [1, 0, 1, 1, 1],
    #           [1, 1, 1, 1, 1],
    #           [1, 0, 0, 1, 0]]
    # matrix = np.mat(arr)
    # MaximalRectangle_85(matrix)
    #height = [2,1,5,6,2,3]
    #height = [2,3,4,3,2,1]
    # height = [1,2,3,4]
    # LargestRectangleHistogram84(height)
    #
    # num = countOfAtoms('(H2O2)2')
    # print ('ddddd',num)
    # s= "leetcode"
    # wordDict = ["leet","code"]
    #
    # print (WordBreak_139(s, wordDict))

    # l1 = [2,4,3]
    # l2 = [9,8,4]
    # addTwoNums(l1, l2)

    # str = 'dvdf'
    # LongestSubstringWithoutRChara_3(str)


    # num1 = [1,3]
    # num2 = [2]
    # MedianOfTwoSortedArrays_4(num1, num2)


    # s = 'a'
    # LongestPalindromicSubstring_5(s)
    #longestPalindrome(s)

    # s= 'hqwnfenpglqdqjwaumbnfvgjicrxldjswfhblwsriixauvdohedozjzjnqjawsvsze'
    #
    # convert_6(s,52)








