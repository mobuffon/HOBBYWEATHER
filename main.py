from presenter_controller import Presenter
from hobbies import Windsurfing, Hiking, Cycling
from api_controller import ApiController

class Main():
    def __init__(self):
        self.hobbies = [Windsurfing(), Hiking(), Cycling()]
        self.api = ApiController()
        self.presenter = Presenter()
        self.locations = {
            "copenhagen": { "latitude": 55.68, "longitude": 12.57},
            "berlin": { "latitude": 52.52, "longitude": 13.41},
            "paris": { "latitude": 48.85, "longitude": 2.35},
            "hamburg": { "latitude": 53.55, "longitude": 9.99},
            "malaga": { "latitude": 36.72, "longitude": -4.42},
            "barcelona": { "latitude": 41.38, "longitude": 2.18},
            "texas": { "latitude": 31.00, "longitude": -100.00},
        }

    def run_loop(self):
        while True:
            print("\nPlease select a hobby:")
            for i, hobby in enumerate(self.hobbies):
                print(f"{i + 1}. {hobby.name}")
            print(f"{len(self.hobbies) + 1}. create new hobby")
            print(f"{len(self.hobbies) + 2}. exit")
            selection = input("\n\tEnter the number of the hobby you want to select: ")
            try:
                selection = int(selection)
                if selection == len(self.hobbies) + 1:
                    self.create_new_hobby()
                elif selection == len(self.hobbies) + 2:
                    print("Exiting the program")
                    print("****BYE****")
                    break
                elif selection < 1 or selection > len(self.hobbies):
                    print("Invalid selection. Please try again.")
                else:
                    hobby = self.hobbies[selection - 1]
                    self.select_location(hobby)
            except ValueError:
                print("Invalid selection. Please try again.")

    def select_location(self, hobby):
        print("\nPlease select a location or ajust the filter for the selected hobbie:")
        for i, location in enumerate(self.locations):
            print(f"{i + 1}. {location}")
        print(f"{len(self.locations) + 1}. create new location")
        print(f"{len(self.locations) + 2}. adjust the filter for {hobby.name}")
        print(f"{len(self.locations) + 3}. back to main menu")
        selection = input("\n\tEnter the number of the action you want to select: ")
        try:
            selection = int(selection)
            if selection == len(self.locations) + 1:
                location = self.create_new_location()
                self.forecast_for_hobby_at(hobby, location)
            elif selection == len(self.locations) + 2:
                self.adjust_filter(hobby)
                self.select_location(hobby)
            elif selection == len(self.locations) + 2:
                return
            elif selection < 1 or selection > len(self.locations):
                print("Invalid selection. Please try again.")
            else:
                location = list(self.locations.keys())[selection - 1]
                self.forecast_for_hobby_at(hobby, location)
        except ValueError:
            print("Invalid selection. Please try again.")

    def create_new_hobby(self):
        print("\n ********NEW FEATURE COMING SOON Function not implemented yet********")

    def adjust_filter(self, hobby):
        print(f"\nPlease type the new value for the filter '{hobby.adjustment_function}'")
        print(f"Current value: {hobby.adjustment_filter_value}")
        new_value = input("\n\tNew value: ")
        try:
            new_value = float(new_value)
        except ValueError:
            print("Invalid value. Please try again.")
            return
        hobby.adjust_filter(new_value)
        print(f"Filter for {hobby.name} adjusted to {new_value}")


    def create_new_location(self):
        #Takes an input, validates it and adds it to the locations dictionary
        print("Please type the name of the location")
        location_name = input("\n\tLocation name: ")
        print("Please type the latitude of the location between -90 and 90")
        location_latitude = input("\n\tLocation latitude: ")
        try:
            location_latitude = float(location_latitude)
            location_latitude < -90 or location_latitude > 90
        except ValueError:
            print("Invalid latitude. Please try again.")
            return
        print("Please type the longitude of the location between -180 and 180")
        location_longitude = input("\n\tLocation longitude: ")
        try:
            location_longitude = float(location_longitude)
            location_longitude < -180 or location_longitude > 180
        except ValueError:
            print("Invalid longitude. Please try again.")
            return
        self.locations[location_name] = { "latitude": location_latitude, "longitude": location_longitude}
        print(f"{location_name} added to the locations list")
        return location_name


    def forecast_for_hobby_at(self, hobby, location):
        response = self.api.retrive_data(self.locations[location])
        good_days = hobby.is_good_day(response)
        if good_days.empty:
            print(f"\nNo good days for {hobby.name} in the next 7 days in {location}")
            return
        self.presenter.present_good_days(good_days, hobby, location)