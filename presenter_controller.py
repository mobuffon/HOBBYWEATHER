class Presenter:
    def __init__(self):
        pass

    def present_good_days(self, good_days, hobby, location):
        best_days = good_days["day"].unique()
        print(f"\nThe best days in {location} for {hobby.name} in the next 7 days are: \n{',\n'.join(best_days)}")

        # Special wind presentation if windsurfing and at least 3 good hours of wind in one day
        if hobby.name == "Windsurfing":
            best_day = hobby.strongest_wind_recursive(good_days)
            if best_day["best_day"] is not None:
                self.present_windsurfing_best_three_hours(best_day)
        
        print(f"\nWould you like to see the detailed forecast for these days? (yes = 1 / back to main menu = Press any key)")
        selection = input("\n\tPick an option: ")

        if selection == "1":
            self.present_good_days_table(good_days, hobby)
        # return to main menu
        print("\n\nReturning to main menu")
        return
        

    def present_good_days_table(self, good_days, selected_hobby):
        for day in good_days["day"].unique():
            print(f"\nForecast for {day}:")
            day_data = good_days[good_days["day"] == day]
            pivot = day_data.pivot_table(
                columns="hour",  # Columns will be days
                values=selected_hobby.metrics,  # Metrics to display
                aggfunc="first",  # Use first value (since hourly data is already specific)
            )
            print(pivot.to_string())

    def present_windsurfing_best_three_hours(self, best_day):
        print("The best day and the best three hours for windsurfing are:")
        print(f"Day: {best_day['best_day']}")
        print(f"  Strongest 3-hour period: {', '.join(map(str, best_day['best_hours']))}")
        print(f"  Windspeed: {', '.join(map(str, best_day['windspeed']))} m/s\n")