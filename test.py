from validate_zimbabwe import ZimbabweValidator

def main():
    validator = ZimbabweValidator()
    
    ids = [
        "50-025544-Q-12",
        "43-165780-A-42",
        "77-040785-H-77",
        "75-341502-L-70",
        "63-751545-G-63",
        "49-008555-S-49",
        "63-1174850-T-45",
    ]

    for idno in ids:
        data = validator.extract_data(idno)
        print(data)

if __name__ == "__main__":
    main()
