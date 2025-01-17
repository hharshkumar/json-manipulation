import json

# Function to read a JSON file and return its contents
def read_json_file(file_path):
    """
    Reads a JSON file from the specified file path and returns its content.
    
    Args:
        file_path (str): Path to the JSON file.
        
    Returns:
        dict: The content of the JSON file as a Python dictionary.
    """
    with open(file_path, "r") as file:
        return json.load(file)

# Function to parse taxes and calculate the total tax value
def parse_taxes(taxes_json):
    """
    Parses the given JSON string containing tax details and computes the total tax amount.
    
    Args:
        taxes_json (str): JSON string containing tax values.
        
    Returns:
        float: Total sum of all tax values.
    """
    taxes = json.loads(taxes_json)  # Convert JSON string into a Python dictionary.
    return sum(float(value) for value in taxes.values())  # Sum up all tax values.

# Function to find the cheapest room and calculate total prices
def find_and_calculate_room_prices(shown_prices, total_taxes):
    """
    Identifies the cheapest room and calculates total prices (Net price + Taxes) for all rooms.
    
    Args:
        shown_prices (dict): Dictionary of room types with their net prices.
        total_taxes (float): Total tax amount applicable to the room prices.
        
    Returns:
        tuple: Contains:
            - (str): Room type with the cheapest price.
            - (float): Cheapest price.
            - (dict): Room types with their total prices (formatted as strings with two decimal places).
    """
    cheapest_price = None  # Variable to store the cheapest price found.
    cheapest_room = None  # Variable to store the room type with the cheapest price.
    room_totals = {}  # Dictionary to store total prices for each room.

    # Loop through each room type and calculate total prices
    for room_type, price in shown_prices.items():
        price = float(price)  # Convert the string price to float.
        total_price = price + total_taxes  # Calculate total price by adding taxes.
        room_totals[room_type] = f"{total_price:.2f}"  # Format total price to two decimal places.

        # Update cheapest room and price if a lower price is found
        if cheapest_price is None or price < cheapest_price:
            cheapest_price = price
            cheapest_room = room_type

    # Return the results as a tuple
    return cheapest_room, cheapest_price, room_totals

# Function to write data to a JSON file
def write_output_to_file(output, file_path):
    """
    Writes the given data to a JSON file at the specified file path.
    
    Args:
        output (dict): Data to write to the file.
        file_path (str): Path where the output JSON file will be saved.
    """
    with open(file_path, "w") as file:
        json.dump(output, file, indent=4)

# Main function to orchestrate the process
def main():
    """
    The main function to:
    - Read JSON data.
    - Parse taxes.
    - Find the cheapest room.
    - Calculate total prices for all rooms.
    - Write results to an output file.
    """
    # Step 1: Read the input JSON file containing hotel and pricing data
    input_json_data = read_json_file("Python-task.json")

    # Step 2: Extract relevant data from the JSON structure
    assignment_results = input_json_data["assignment_results"][0]  # Get the first hotel entry.
    shown_prices = assignment_results["shown_price"]  # Retrieve room price details.
    number_of_guests = assignment_results["number_of_guests"]  # Number of guests for the booking.

    # Step 3: Parse taxes from the given JSON data and calculate the total
    total_taxes = parse_taxes(assignment_results["ext_data"]["taxes"])

    # Step 4: Find the cheapest room and calculate total prices for all rooms
    cheapest_room, cheapest_price, room_totals = find_and_calculate_room_prices(shown_prices, total_taxes)

    # Step 5: Prepare the data for the cheapest room
    cheapest_info = {
        "room_type": cheapest_room,
        "number_of_guests": number_of_guests,
        "price": f"{cheapest_price:.2f}"  # Format price to two decimal places.
    }

    # Step 6: Combine all data into a single output structure
    output = {
        "cheapest_price_info": cheapest_info,
        "room_totals": room_totals
    }

    # Step 7: Write the output data to a JSON file for submission
    write_output_to_file(output, "hotel_price_analysis_output.json")

    # Step 8: Print results to the console for debugging/verification
    print("Cheapest Price:", f"{cheapest_price:.2f}")
    print("Cheapest Price Info:", cheapest_info)
    print("Room Totals (Net Price + Taxes):", room_totals)

# Entry point of the script
if __name__ == "__main__":
    main()
