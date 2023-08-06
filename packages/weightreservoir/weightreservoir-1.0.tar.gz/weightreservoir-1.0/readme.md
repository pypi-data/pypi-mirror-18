This module brings the effective reservoir sampling method, with or without
weight. The reservoir sampling is used when you have a very large and unknown
dataset of size N, and you want to sampling a subset of k of these N samples,
with one stream or one file reading. 

If the weight is not present, each sample will have equal chance to be selected
in the final subset; if weight is used, each sample will be selected according 
to their weights.


# to install
    pip install weightreservoir


# to use as a module in python
    from weightreservoir import reservoir

# to use uniform sampling
    uniform = reservoir.UniformSampling(size = 10)

    # to add one item into the stream and decide to sample it or not
    uniform.addOne(itemValue)

    # to add a list of items into the stream and decide to sample each of them or not
    uniform.addAll(itemValueList)    

    # to get all the current items of the sampled dataset, returned as a list
    uniform.get()

# to use weighted sampling
    weight_sample = reservoir.WeightSampling(size = 10)

    # to add one item into the stream and decide to sample it or not by its weight
    weight_sample.addOne(itemValue, itemWeight)

    # to add a list of items into the stream and decide to sample each of them or not by their weight
    weight_sample.addAll(itemValueList, itemWeightList)    

    # to get all the current items of the sampled dataset, returned as a list
    weight_sample.get()   

