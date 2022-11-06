# OrderBook
## Implementation
Implemented an O(n^2) approach which is somewhat similar to insertion sort. After parsing the orders.xml each query (in the form of tags) is read from the file and processed. In AddOrder query before insterting the order in the buy or sell list, matches for the order is found and processed. If the order is perfectly matched it is not inserted in it's operation list. If no matching or partial matching is found, the order is inserted in it's operation list. Buy List is in decreasing order and Sell List is in increasing order therefore insertion in them can be made in O(n). 
Further improvements can be made if we use set data structure in which insertion, deletion and updation O(logn), therefore whole task can be done in O(nlogn). AddOrder can be done concurrently by using multi-threading. We can use lock to do order matching, so that there is no inconsistency in data.
Total execution time (including stdout) is 71 seconds.
