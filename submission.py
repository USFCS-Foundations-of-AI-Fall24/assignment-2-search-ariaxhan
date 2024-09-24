import mars_planner
import routefinder

if __name__ == "__main__":
    # run mars_planner
    print("\n------------ running mars planner ------------\n")
    mars_planner.main()
    print("\n------------ running route finder ------------\n")
    # run routefinder
    start_location = "8,8"
    routefinder.run(start_location)
