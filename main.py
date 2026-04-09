from parser import preprocess_regex
from postfix import regex_to_postfix

if __name__ == "__main__":
    result = preprocess_regex()
    
    if result:
        print("Processed Regex Ready for Next Step:", result)

        postfix = regex_to_postfix(result)
        print("Postfix Ready for Next Step:", postfix)