#include <iostream>
#include <string>
#include <climits>

using namespace std;

int main(int argc, char **argv)
{                                    // If argc is 2 or more, put argv[1]
                                     // in input, else, put 0 in input
    int const input = (argc >= 2) ? stoi(argv[1]) : 0;

    string inputBinary;              // Holds the binary of the input
    string powerOf2Value;            // String with values 2^n where n
                                     // are the bits of input that are 1
    for (size_t index = sizeof(int) * CHAR_BIT; index--; )
    {
        if ((input >> index) & 1)    // If input bit is 1, put 1 in
        {                            // inputBinary and include decimal in
            inputBinary += '1';      // powerOf2Value string with +
            powerOf2Value += to_string(1 << index) + " + ";
        }
        else                         // If the bit is 0, put 0 in inputBinary
            inputBinary += '0';
    }
                                     // Take away redundant last plus
    powerOf2Value.resize(powerOf2Value.length() - 3);
                                     // Print to screen
    cout << input << " = " << inputBinary << " = " << powerOf2Value << '\n';
}