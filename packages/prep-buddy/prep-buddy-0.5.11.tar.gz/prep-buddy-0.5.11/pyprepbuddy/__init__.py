def py2java_int_array(sc, args):
    gw = sc._gateway
    result = gw.new_array(gw.jvm.int, len(args))
    for i in range(0, len(args)):
        result[i] = int(args[i])
    return result


def py2java_int_list(sc, args):
    gw = sc._gateway
    result = gw.jvm.java.util.ArrayList()
    for i in range(0, len(args)):
        result.add(int(args[i]))
    return result
