#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>

using namespace std;


int main(int argc, char **argv)
{	                                 // Amount of simulations, minimum is 1
	size_t const simulations = (argc >= 2) ? stoul(argv[1]) : 1;
	                                 // If set, holds second argument
	string const arg2 = (argc >= 3) ? argv[2] : "";
	                                 // Set the random seed
	(arg2.find('r') != string::npos) ? srand(time(0)) : srand(0);

	size_t wins = 0;                 // Amount of wins
	if (arg2.find('v') != string::npos)
	{                                // If v, actually play the simulation
		for (size_t iteration = 0; iteration != simulations; ++iteration)
		{                            // Set the selected door and the price
		                             // door, and show both of them to
			size_t const selected = rand() % 3, price = rand() % 3;
			cout << "selected: " << selected << ", price behind: " << price;
			string tmp = "012";     // Set the temporary string and erase
			tmp.erase(selected, 1); // the selected door from it

			if (selected != price)   // Player wins! Remove price from tmp,
			{                        // show opened door and suggested door
			    tmp.erase(tmp.find(to_string(price)), 1);
				cout << ", opened: " << tmp[0]
				     << ", suggested: " << to_string(price);
				++wins;              // Add one to the wins
			}
			else                     // Player loses, show the randomly
			{                        // chosen opened door and suggested door
			    size_t zeroOrOne = rand() % 2;
				cout << ", opened: " << tmp[zeroOrOne] << ", suggested: "
					 << tmp.substr(0, zeroOrOne) + tmp.substr(zeroOrOne + 1);
			}
			cout << '\n';
		}
    }
    else
    {                                     // Each iteration is one simulation
		for (size_t iteration = 0; iteration != simulations; ++iteration)
		{                                 
			if (rand() % 3 != rand() % 3) // If the contestant picks 1 of the
				++wins;                   // 2 doors that are not the price
		}                                 // winning door, add one win
    }

    cout << "#iterations: " << simulations << " #hits: " << wins
         << " #hit percentage: " << static_cast<float>(wins) / simulations
         << '\n';                         // show the percentages
}