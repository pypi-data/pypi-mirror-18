"""Returns information of the mobile phone number"""
import os
import pickle

DATAFILE = "/".join([os.path.abspath(os.path.dirname(__file__)), "mobiledb.pickle"])
DATA = None  # 0 - prefix hash
             # 1 - value [value, value ...]
             # 2 - symbols
with open(DATAFILE, 'rb') as f:
    DATA = pickle.load(f)

def get_mobile_info(number):
    """
    Returns information of the cellphone in tuple.
    cellphone should be str
    """
    prefix = number[:3]
    offset = int(number[3:7])
    prefix_index = DATA[0].get(prefix)
    if prefix_index is None:
        return None
    value_index = DATA[1][prefix_index + offset]
    value = DATA[2][value_index]
    if value is None:
        return None
    return (
        DATA[3][value[0]],  # province
        DATA[3][value[1]],  # city
        DATA[3][value[2]],  # isp
        value[3],           # code
        value[4],           # zipcode
        DATA[3][value[5]],  # type
    )


if __name__ == "__main__":
    print(get_mobile_info("13916020000"))
    print(get_mobile_info("13906900000"))
    print(get_mobile_info("13906010000"))
    print(get_mobile_info("14599990000"))
    print(get_mobile_info("11199990000"))

