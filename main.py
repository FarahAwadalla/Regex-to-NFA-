from parser import preprocess_regex

if __name__ == "__main__":
    result = preprocess_regex()
    
    if result:
        print("Processed Regex Ready for Next Step:", result)