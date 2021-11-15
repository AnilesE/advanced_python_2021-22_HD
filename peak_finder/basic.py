#
# The first version of our function!
# Write doc strings 
#
def find_peaks(list_of_intensities):
    """Find peaks

    Find local maxima for a given list of intensities or tuples
    Intensities are defined as local maxima if the
    intensities of the elements in the list before and after
    are smaller than the peak we want to determine.

    For example given a list:
        1 5 [6] 4 1 2 [3] 2

    We expect 6 and 3 to be returned.
    

    Args:
        list_of_intensities (list of floats, ints or tuple of ints): a list of
            numeric values

    Returns:
        list of floats or tuples: list of the identified local maxima

    Note:
        This is just a place holder for the TDD part :)

    """
    peaks = []
    if all([isinstance(x, tuple) for x in list_of_intensities]):
        for i in range(len(list_of_intensities)):
            list_of_intensities[i] = sum(list_of_intensities[i])
            if i==0:
                if list_of_intensities[i] > list_of_intensities[i+1]: 
                    peaks.append(list_of_intensities[i])
            elif i != 0 and i != len(list_of_intensities):
                if list_of_intensities[i-1] < list_of_intensities[i] > list_of_intensities[i+1]:
                    peaks.append(list_of_intensities[i])
            elif i==len(list_of_intensities):
                if list_of_intensities[i] > list_of_intensities[i+1]: 
                    peaks.append(list_of_intensities[i])  

    else:
        for i in range(len(list_of_intensities)):
            if isinstance(list_of_intensities[i], int) is False:
                continue
            if i==0:
                if list_of_intensities[i] > list_of_intensities[i+1]: 
                    peaks.append(list_of_intensities[i])
            elif i != 0 and i != len(list_of_intensities):
                if list_of_intensities[i-1] < list_of_intensities[i] > list_of_intensities[i+1]:
                    peaks.append(list_of_intensities[i])
            elif i==len(list_of_intensities):
                if list_of_intensities[i] > list_of_intensities[i+1]: 
                    peaks.append(list_of_intensities[i])


    return peaks
