
Data Cleaning

Merge dataset
 - merged according to month
 - added season values to missing rows
 - dropped rows with month = 6 as season is not defined
-2759 rows

Cleaning dataset
- dropped one row as it was a duplicate
	-2758 rows
-ensured that columns “start_time” and “time” matches
-sorted them according to season and then chronogically 
- fixed date values with out of range/typo mistakes
	e.g. 5/7/18  to 7/5/18 
- fixed month column values where they don’t align with the season
	e.g. month = 3 but season = 0 
	fixed to month = 3 and season = 1 

Split Dataset into seasons
-train and test data for each season
	-70% train and 30% test 
