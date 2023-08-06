
# # creates a string that can be used in a $filter query
# def column_filter(key, values):

#     if isinstance(values, six.string):
#         values = "'%s'" % values

#     query = "%s eq %s" % (key, values)
#     query = paste0(query, collapse=" or ")
#     query

# def get_filter (..., filter_list=list(...)):

#     if (len(filter_list) == 0)
#         return None

#     query = sapply(names(filter_list), function(key){
#     filter = column_filter(key, filter_list[[key]])
#     paste0("(", filter, ")")
#     })

#     return " and ".join(query)