class Hobby:
    def __init__(self, name, filters):
        self.name = name 
        self.filters = filters
        self.display_info = []
        self.metrics = []
        self.adjustment_filter = ""
        self.adjustment_filter_value = None
        
    def is_good_day(self, day_data):
        day_data["is_good_weather"] = day_data.apply(lambda row: all(f(row) for f in self.filters), axis=1)
        day_data = day_data[day_data["is_good_weather"] == True]
        day_data = day_data[day_data["date"].dt.hour.between(6, 18)]
        return day_data
    
    def update_adjustment_filter(self, value):
        self.adjustment_filter_value = value


class Windsurfing(Hobby): 
    def __init__(self):
        self.name = "Windsurfing"
        self.filters = [
            lambda row: row["wind_speed_10m"] > 15,
            lambda row: row["rain"] == 0
        ]
        self.display_info = ["day", "hour", "wind_speed_10m", "rain", "temperature_2m"]
        self.metrics = ["wind_speed_10m", "rain", "temperature_2m"]
        self.adjustment_function = "wind > than x km/h"
        self.adjustment_filter_value = 15

    def adjust_filter(self, wind_speed):
        self.filters[0] = lambda row: row["wind_speed_10m"] > wind_speed
        self.update_adjustment_filter(wind_speed)

    def strongest_wind_recursive(self, df, day_list=None, best_day=None, best_hours=None, max_sum=0):
        #group the DataFrame by day if this is the first call
        if day_list is None:
            grouped = df.groupby("day")
            day_list = list(grouped.groups.keys())
            return self.strongest_wind_recursive(grouped, day_list, best_day, best_hours, max_sum)

        #return if no more days to process
        if not day_list:
            return {
                "best_day": best_day,
                "best_hours": best_hours["hour"].to_list() if best_hours is not None else [],
                "windspeed": best_hours["wind_speed_10m"].to_list() if best_hours is not None else []
            }

        #get the first day
        day = day_list[0]
        group = df.get_group(day)

        #Extract wind speeds for the day
        wind_speeds = group["wind_speed_10m"].to_list()

        #find the strongest window for the current day
        current_best_hours, current_max_sum = self._find_strongest_window_(wind_speeds, group)

        #update the best day and best hours if the current day has a stronger window
        if current_max_sum > max_sum:
            best_day = day
            best_hours = current_best_hours
            max_sum = current_max_sum

        #recursive call iterate over the remaining days
        return self.strongest_wind_recursive(df, day_list[1:], best_day, best_hours, max_sum)

    def _find_strongest_window_(self, data, group, index=0, max_sum=0, best_hours=None):

        #stop and return best hour if there are less than 3 consecutive hours left
        if index > len(data) - 3:
            return best_hours, max_sum

        #calculate the sum of the current 3-hour window
        current_sum = sum(data[index:index + 3])

        #update the maximum sum and best hours if the current window is better
        if current_sum > max_sum:
            max_sum = current_sum
            best_hours = group.iloc[index:index + 3]

        #recursive call to the next window of three hours
        return self._find_strongest_window_(data, group, index + 1, max_sum, best_hours)



class Hiking(Hobby):
    def __init__(self):
        self.name = "Hiking"
        self.filters = [
            lambda row: row["temperature_2m"] > 6,
            lambda row: row["rain"] == 0
        ]
        self.display_info = ["day", "hour", "temperature_2m", "rain"]
        self.metrics = ["temperature_2m", "rain"]
        self.adjustment_function = "temperature > than x degrees"
        self.adjustment_filter_value = 6

    def adjust_filter(self, temperature):
        self.filters[0] = lambda row: row["temperature_2m"] > temperature
        self.update_adjustment_filter(temperature)

class Cycling(Hobby):
    def __init__(self):
        self.name = "Cycling"
        self.filters = [
            lambda row: row["wind_speed_10m"] < 8,
            lambda row: row["rain"] == 0
        ]
        self.display_info = ["day", "hour", "wind_speed_10m", "rain"]
        self.metrics = ["wind_speed_10m", "rain"]
        self.adjustment_functions = "wind < than x km/h"
        self.adjustment_filter_value = 8

    def adjust_filter(self, wind):
        self.filters[0] = lambda row: row["wind_speed_10m"] > wind
        self.update_adjustment_filter(wind)
    

