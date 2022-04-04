"""Use module is used for testing purposes only, do not modify."""
# pylint: disable=C0116, E0602, W0612


def some_function(arg1, arg2, arg3, arg4):  # noqa
    print("hello world!")
    int1 = arg1 * arg3 / 5 - arg4
    int2 = arg4 ** arg3
    my_list = [1, 2, 3.6, 4, 5.4, "some string"]
    my_dictionary = {
        "first": arg1,
        "second": arg2,
        "third": arg3,
        "fourth": arg4,
    }
    my_tuple = ("hello", "world")
    result = some_other_function(arg2).process_somehow()
    if not arg3 > arg2 and arg1 < arg4:
        return arg2 >> 5
    while my_list[4] > my_dictionary["first"]:
        my_variable = 54
        my_variable += arg1 / arg4
    return my_dictionary["first"] + "something here"
