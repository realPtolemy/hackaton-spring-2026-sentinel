#include <iostream>
#include <vector>
#include <cmath>
#include <string>

using namespace std;

int choice;
int n;
int i;
int j;
int temp;
int arr[100];
int size_of_array;
bool flag;
long long big_ans;

int recursive_fib(int n) {
    if (n == 0) {
        return 0;
    }
    if (n == 1) {
        return 1;
    }
    return recursive_fib(n - 1) + recursive_fib(n - 2);
}

void show_menu() {
    cout << "========================================" << endl;
    cout << "   WELCOME TO MY COMPUTER SCIENCE PROJECT" << endl;
    cout << "========================================" << endl;
    cout << "1. Calculate Fibonacci Series" << endl;
    cout << "2. Check if a number is Prime" << endl;
    cout << "3. Calculate Factorial" << endl;
    cout << "4. Sort a list of numbers (Bubble Sort)" << endl;
    cout << "5. Print a Star Triangle Pattern" << endl;
    cout << "6. Calculate Sum and Average" << endl;
    cout << "7. Exit the program" << endl;
    cout << "========================================" << endl;
    cout << "Please enter your choice here: ";
}

int main() {
    while (true) {
        show_menu();
        cin >> choice;

        if (choice == 1) {
            cout << "You selected Fibonacci." << endl;
            cout << "Enter how many numbers you want to see: ";
            cin >> n;
            cout << "Generating series... please wait..." << endl;
            
            i = 0;
            while (i < n) {
                cout << recursive_fib(i) << " ";
                i = i + 1;
            }
            cout << endl;
            cout << "Done with fibonacci." << endl;
            cout << endl;
        }
        
        else if (choice == 2) {
            cout << "You selected Prime Checker." << endl;
            cout << "Enter a number to check: ";
            cin >> n;
            
            flag = true;
            
            if (n == 0) {
                flag = false;
            }
            if (n == 1) {
                flag = false;
            }
            
            i = 2;
            while (i <= n / 2) {
                if (n % i == 0) {
                    flag = false;
                    break;
                }
                i++;
            }
            
            if (flag == true) {
                cout << n << " is a PRIME number." << endl;
            } else {
                cout << n << " is NOT a prime number." << endl;
            }
            cout << endl;
        }

        else if (choice == 3) {
            cout << "You selected Factorial." << endl;
            cout << "Enter a number: ";
            cin >> n;
            
            if (n < 0) {
                cout << "Error: Cannot do negative factorial." << endl;
            } else {
                big_ans = 1;
                i = 1;
                while (i <= n) {
                    big_ans = big_ans * i;
                    i++;
                }
                cout << "The factorial of " << n << " is: " << big_ans << endl;
            }
            cout << endl;
        }

        else if (choice == 4) {
            cout << "You selected Bubble Sort." << endl;
            cout << "How many numbers do you want to sort? (max 100): ";
            cin >> size_of_array;
            
            if (size_of_array > 100) {
                cout << "Too many numbers!" << endl;
            } else {
                cout << "Enter the numbers now:" << endl;
                for (i = 0; i < size_of_array; i++) {
                    cout << "Number " << i + 1 << ": ";
                    cin >> arr[i];
                }
                
                cout << "Unsorted array: ";
                for (i = 0; i < size_of_array; i++) {
                    cout << arr[i] << " ";
                }
                cout << endl;
                
                for (i = 0; i < size_of_array - 1; i++) {
                    for (j = 0; j < size_of_array - i - 1; j++) {
                        if (arr[j] > arr[j + 1]) {
                            temp = arr[j];
                            arr[j] = arr[j + 1];
                            arr[j + 1] = temp;
                        }
                    }
                }
                
                cout << "Sorted array is here: ";
                for (i = 0; i < size_of_array; i++) {
                    cout << arr[i] << " ";
                }
                cout << endl;
            }
            cout << endl;
        }

        else if (choice == 5) {
            cout << "You selected Star Pattern." << endl;
            cout << "Enter the number of rows: ";
            cin >> n;
            
            for (i = 1; i <= n; ++i) {
                for (j = 1; j <= i; ++j) {
                    cout << "* ";
                }
                cout << endl;
            }
            
            cout << "Do you want a reverse one too? (1 for yes, 0 for no): ";
            int sub_choice;
            cin >> sub_choice;
            if (sub_choice == 1) {
                for (i = n; i >= 1; --i) {
                    for (j = 1; j <= i; ++j) {
                        cout << "* ";
                    }
                    cout << endl;
                }
            }
            cout << endl;
        }

        else if (choice == 6) {
            cout << "Sum and Average Calculation." << endl;
            cout << "Enter amount of numbers: ";
            int amount;
            cin >> amount;
            
            double sum = 0;
            double avg = 0;
            double val = 0;
            
            int k = 0;
            while (k < amount) {
                cout << "Enter val: ";
                cin >> val;
                sum = sum + val;
                k = k + 1;
            }
            
            avg = sum / amount;
            
            cout << "The Total Sum is: " << sum << endl;
            cout << "The Average is: " << avg << endl;
            
            if (avg > 50) {
                cout << "That is a big average." << endl;
            } else {
                cout << "That is a small average." << endl;
            }
            cout << endl;
        }

        else if (choice == 7) {
            cout << "Exiting the program now..." << endl;
            cout << "Thank you for using." << endl;
            cout << "Bye bye." << endl;
            break;
        }

        else {
            cout << "Invalid Input!!!!" << endl;
            cout << "Please try again and type a number between 1 and 7." << endl;
            cout << endl;
        }
        
        cout << "Press any key and enter to continue...";
        string dummy;
        cin >> dummy;
        cout << endl;
        cout << endl;
    }

    return 0;
}


