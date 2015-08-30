import random
from numpy.random import multinomial
from random import randint
from django.conf import settings


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


def get_random_cocktail(bottles, number_of_bottle):
    """
    Return a list of of disct that contain volume and bottle name
    Example:
    [{'volume': 7, 'bottle_name': u'Rhum'}, {'volume': 2, 'bottle_name': u'Vodka'}]
    :param max_bottle: Max bottleis the number of bottle currently used by the system
    :return:    List of dict
    """
    # random a number of bottle from 1 to the maximum bottle available
    list_size = randint(1, number_of_bottle)
    # the sum value is the total volume. Load it from the settings
    list_sum_value = settings.MAX_VOLUME

    # get list of random number
    random_list_with_zero = rand_int_vec(list_size,
                                         list_sum_value,
                                         distribution=rand_floats(list_size))
    # remove zero in this list
    random_list = []
    for el in random_list_with_zero:
        if el != 0:
            random_list.append(el)

    number_of_bottle = len(random_list)
    print "number of bottle used: "+str(len(random_list))
    print "list volume: "+str(random_list)

    # get randomly item in the list switch the list_size
    bottles = set(bottles)
    bottles_selected = random.sample(bottles, number_of_bottle)
    print bottles_selected

    # we cannot use the Cocktail object without saving it
    bottles = []
    i = 0
    for bottle in bottles_selected:
        list_bottle_volume = {'bottle_name': bottle.name,
                              'volume': random_list[i],
                              'slot_id': bottle.slot}
        bottles.append(list_bottle_volume)
        i += 1

    return bottles

