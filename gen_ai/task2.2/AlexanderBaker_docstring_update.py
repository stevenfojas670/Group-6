def std(data):
    mean_of_data = mean(data)
    summation = 0
    for element in data:
        temp = element - mean_of_data
        temp = temp * temp
        summation = summation + temp
    deviation = summation/len(data)
    deviation = np.sqrt(deviation)
    return deviation