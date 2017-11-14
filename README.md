# HURDAT2-for-profiling
# Nikolaus Parulian
Student group solutions for HURDAT2 that can benefit from profiling and 
selective optimizations

###solution_a:

For this solution I found that SplitStrip and get_LL take most of the time and process in the program.
However there are some things that I can improve from the code:
1. I can make a dictionary for new hurricane data that already been Splitted, therefore no need to call
the SplitStrip function over and over again
2. I found that get_LL is trying to fetch all the values in the hurricane list everytime it was getting called with complexity n2.
 Therefore I make a new function get_LL_new that will access the index directly and return the corresponding element
 
 The output for this program will be the same with the original code with runtime improvement.  

