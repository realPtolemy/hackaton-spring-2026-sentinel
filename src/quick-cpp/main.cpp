#include <iostream>
#include <vector>
#include <cstring>


using namespace std; 


struct Data {
    char buffer[10]; 
};

void process_data(void* ptr) {
    
    int* val = (int*)ptr; 
    cout << "Value: " << *val << endl;
}

int main() {
    
    Data* d = new Data(); 
    sprintf(d->buffer, "User_%d", 123456789); 
    int* raw_numbers = (int*)malloc(sizeof(int) * 5); 
    raw_numbers[0] = 10;
    process_data(raw_numbers);
    return 0;
}