#include <iostream>
#include <vector>
#include <string>

using namespace std; // Bad practice: pollutes the global namespace

#define MULTIPLY(a, b) a * b // Dangerous macro: no parentheses
#define HELLO "World"

int main()
{
    // Cryptic variable names and uninitialized pointers
    int* p ; 
    int a=5,b=10;

    // Macro pitfall: MULTIPLY(5 + 1, 2) becomes 5 + 1 * 2 = 7, not 12
    cout << "Math: " << MULTIPLY(a + 1, 2) << endl;

    // Manual memory management with no delete (Memory Leak)
    int* leak = new int[100];
    for(int i=0; i<10; i++) {
    leak[i] = i*2;
    }

    // Mixing C-style strings and C++ strings unnecessarily
    char* old_school = "Old String"; 
    string new_school = "New String";
    cout << old_school << " " << new_school << endl;

    // Goto statement: The ultimate cardinal sin of structured programming
    int counter = 0;
    LOOP:
    cout << "Looping..." << counter << endl;
    counter++;
    if (counter < 3) goto LOOP;

    // Using magic numbers and nested ternary operators (unreadable)
    int x = (a > b) ? (a < 20 ? 1 : 2) : (b > 5 ? 3 : 4);
    
    // Manual array indexing instead of iterators or range-based loops
    vector<int> v; v.push_back(1); v.push_back(2);
    for(int i = 0; i <= v.size() - 1; i++) // Potential unsigned underflow if size is 0
    {
    cout << v[i] << endl;
    }

    return 0; // Technically optional in main, but inconsistent
}