#include <iostream>
#include <vector>
#include <string>

using namespace std;

#define MULTIPLY(a, b) a * b
#define HELLO "World"

int main()
{
    int* p ; 
    int a=5,b=10;

    cout << "Math: " << MULTIPLY(a + 1, 2) << endl;

    int* leak = new int[100];
    for(int i=0; i<10; i++) {
    leak[i] = i*2;
    }

    char* old_school = "Old String"; 
    string new_school = "New String";
    cout << old_school << " " << new_school << endl;

    int counter = 0;
    LOOP:
    cout << "Looping..." << counter << endl;
    counter++;
    if (counter < 3) goto LOOP;

    int x = (a > b) ? (a < 20 ? 1 : 2) : (b > 5 ? 3 : 4);
    
    vector<int> v; v.push_back(1); v.push_back(2);
    for(int i = 0; i <= v.size() - 1; i++)
    {
    cout << v[i] << endl;
    }

    return 0;
}