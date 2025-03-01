#include <iostream>
#include <vector>
#include <String>

using namespace std;

class Solution
{
public:
    // Encodes a list of strings to a single string.
    string encode(vector<string> &strs)
    {
        string encoded;
        for (const string &s : strs)
        {
            encoded += to_string(s.size()) + "#" + s;
        }
        return encoded;
    }

    // Decodes a single string to a list of strings.
    vector<string> decode(string s)
    {
        vector<string> decoded;
        int i = 0;

        while (i < s.size())
        {
            int j = i;
            while (s[j] != '#')
                j++; // Find the '#' delimiter

            int len = stoi(s.substr(i, j - i));  // Extract the length
            i = j + 1;                           // Move past '#'
            decoded.push_back(s.substr(i, len)); // Extract the string

            i += len; // Move to the next encoded string
        }
        return decoded;
    }
};
