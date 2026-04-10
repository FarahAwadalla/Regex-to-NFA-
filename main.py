from parser import preprocess_regex
from postfix import regex_to_postfix
from thompson import postfix_to_nfa, print_nfa

if __name__ == "__main__":
    result = preprocess_regex()
    
    if result:
        print("Processed Regex Ready for Next Step:", result)
        postfix = regex_to_postfix(result)
        print("Postfix Ready for Next Step:", postfix)
        
        nfa = postfix_to_nfa(postfix)
        print_nfa(nfa)
