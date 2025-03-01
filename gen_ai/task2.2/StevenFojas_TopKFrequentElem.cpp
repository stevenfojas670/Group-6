#include <iostream>
#include <vector>
#include <map>
using namespace std;

/*
 * LeetCode Problem: Top K Frequent Elements
 * Problem Link: https://leetcode.com/problems/top-k-frequent-elements/
 *
 * Function: topKFrequent
 * This function finds the `k` most frequent elements in a given vector of integers.
 *
 * Approach:
 * - Use a **frequency map** to count how often each element appears.
 * - Use a **bucket sort technique** where the index represents the frequency.
 * - Elements with the same frequency are grouped together in the same bucket.
 * - Finally, collect elements from the highest frequency bucket to the lowest
 *   until we have collected exactly `k` elements.
 */

class Solution
{
public:
    vector<int> topKFrequent(vector<int> &nums, int k)
    {
        // Step 1: Frequency Count
        // Map each unique number to the number of times it appears.
        map<int, int> intCount;
        for (auto &i : nums)
        {
            intCount[i]++;
        }

        // Step 2: Bucket Sort Preparation
        // Create a vector of vectors (buckets). Each index represents a frequency count.
        // nums.size() + 1 buckets because the max frequency can be nums.size() if all elements are the same.
        vector<vector<int>> bucket(nums.size() + 1);

        // Step 3: Fill Buckets
        // Each number is placed into the bucket corresponding to its frequency.
        for (const auto &pair : intCount)
        {
            bucket[pair.second].push_back(pair.first);
        }

        // Step 4: Collect Results from Buckets
        // Start from the highest frequency bucket (at the end of the vector) and collect elements.
        vector<int> results;
        for (int i = bucket.size() - 1; i > 0; --i)
        {
            for (int n : bucket[i])
            {
                results.push_back(n);
                // Stop when we have exactly `k` elements.
                if (results.size() == k)
                {
                    return results;
                }
            }
        }

        // This return is technically unnecessary given the problem constraints (k is always valid),
        // but added for function completeness.
        return results;
    }
};
