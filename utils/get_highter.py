def get_highter_volume(slot_volume_dict):
        """
        Return the bigger integer in the list
        :param slot_volume_dict:
        :return:
        """
        list_volume = []
        for el in slot_volume_dict:
            list_volume.append(int(el['volume']))

        return max(list_volume)