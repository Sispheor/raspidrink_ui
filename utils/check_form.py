
def is_total_volume_exceed_20cl(cocktail_item_formset):
    """
    Check the total volume is <= 20
    :param cocktail_item_formset: the form that contain all volume
    :return: True id total volume > 20, else return False
    """
    total_volume = 0
    for form in cocktail_item_formset.forms:
        volume = form.cleaned_data['volume']
        total_volume += volume
        print "volume total: "+str(total_volume)
        if total_volume > 20:
            return True
    return False


def is_same_bootle_in_list(cocktail_item_formset):
    """
    Check if a bootle not appear more than once in the formset
    :param cocktail_item_formset: Django formset
    :return: False is a least one bootle appeared more than once
    """
    list_id = []
    for form in cocktail_item_formset.forms:
        id = form.cleaned_data['bottle'].id
        list_id.append(id)

    if len(list_id) > len(set(list_id)):
        return True
    return False
