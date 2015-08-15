import random
from numpy.random import multinomial


def rand_floats(nb_element):
    """
    Return a dict of percentage distributed to to number of element
    :param nb_element:Number of element to distribute percent
    :return: Dict of percent
    """
    scalar = 1.0
    vector_size = nb_element
    random_vector = [random.random() for i in range(vector_size)]
    random_vector_sum = sum(random_vector)
    random_vector = [scalar * y / random_vector_sum for y in random_vector]
    return random_vector


def rand_int_vec(list_size, list_sum_value, distribution):
    """
    Return a list of random integers of length 'list_size' whose sum is 'list_sum_value'.
    :param list_size: the size of the list to return
    :param list_sum_value: The sum of list values
    :param distribution: a list of size 'list_size'
    :return: A list of random integers
    """

    returned_list = []
    if type(distribution) == list:
        distribution_size = len(distribution)
        if list_size == distribution_size or (list_size-1) == distribution_size:
            values = multinomial(list_sum_value, distribution, size=1)
            output_values = values[0]
            for val in output_values:
                returned_list.append(val)
    else:
        raise ValueError('Cannot create desired vector')
    return returned_list
