#include <iostream>
#include <vector>
#include <String>

using namespace std;

class Solution
{
public:
    string encode(vector<string> &strs)
    {

        if (strs.size() < 1)
            return " ";

        // combine string into one, place '#' between
        string encoded;
        for (string s : strs)
        {
            encoded += s + "69#";
        }
        // cout << encoded << " ";
        return encoded;
    }

    vector<string> decode(string s)
    {
        vector<string> ans;
        int i = 0;
        string temp;
        for (int i = 0; i < s.length() - 1; i++)
        {
            if (s[i] == '6')
            {
                int j = i + 1;
                if (s[j] == '9')
                {
                    j++;
                    if (s[j] == '#')
                    {
                        i = j;
                        ans.push_back(temp);
                        temp.clear();
                    }
                    else
                    {
                        temp += s[j--];
                    }
                }
                else
                {
                    temp += s[i];
                }
            }
            else
            {
                temp += s[i];
                // cout << temp << " ";
            }
        }
        return ans;
    }
};