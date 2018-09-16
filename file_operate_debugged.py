# 文件操作模块     主要定义涉及文件IO的函数
import pickle  # 导入pickle模块
import os  # 导入os模块


# 函数login，参数：用户名，密码，用户身份，用户身份必须为'student','stuff','admin'中的一种，访问存放用户登录信息的文件，返回布尔值。

def login(user_name, key, user_identity):
    def check(user_name, key, user_identity):
        try:
            with open('data/user_info/' + str(user_identity) + '/' + str(user_name) + '.pickle', 'rb') as f:
                user = pickle.load(f)
            if user.key == key:
                return (True)
            else:
                return (False)
        except IOError and EOFError:
            return (False)  # 若文件不存在，则返回错误信息(最好也返回一个boolean值)

    response = check(user_name, key, user_identity)
    return (response)  # 最终的返回值


# 函数creat_stumenu，参数：学生订单和日期和窗口号，一个学生类，创建字典，key为学生类，value为订单列表，订单列表第1项是窗口号，用pickle保存在本地，返回新的订单


def creat_stumenu(stu, order_list, date, window):
    # 项目的日期格式均为"18-8-31"的格式，便于字符串操作
    f = 'data/order_info/' + str(window) + '/' + str(date) + '_order.pickle'
    f2 = 'data/order_now_info/' + str(window) + '/' + str(date) + '_ordernow.pickle'

    def checkfor(filen, obj):
        try:
            if os.path.getsize(filen) == 0:
                pickle.dump(obj, open(filen, 'wb'))
        except FileNotFoundError:
            with open('data/order_info/' + str(window) + '/' + str(date) + '_order.txt', 'wb') as file:
                pickle.dump(obj, file)
                file.close()
                os.rename('data/order_info/' + str(window) + '/' + str(date) + '_order.txt', filen)

    checkfor(f, [])
    checkfor(f2, test)  # 这里是为了debug，后期去除

    # 检测元素与文件是否存在，不存在就加，checkfor为string类型函数
    try:
        with open('data/order_info/' + str(window) + '/' + str(date) + '_order.pickle', 'rb') as f:
            today_stumenu = pickle.load(f)
            # today_stumenu是列表，各元素是字典，key为学生类，value为订单字典
    except IOError and EOFError as err:
        return (str(err))  # 若出错，则将错误信息返回

    order_dict = dict()
    order_list.append(window)  # 列表最后一项是窗口号
    order_dict[stu] = order_list
    today_stumenu.append(order_dict)  # 新增数据

    try:
        with open('data/order_info/' + str(window) + '/' + str(date) + '_order.pickle', 'wb') as f:
            pickle.dump(today_stumenu, f)
            # 保存更改后的文件
    except IOError and EOFError as err:
        return (str(err))
    try:
        with open('data/order_now_info/' + str(window) + '/' + str(date) + '_ordernow.pickle', 'rb') as f:
            order_now_dict = pickle.load(f)  # 字典
        for item in order_list:
            order_now_dict[item] += 1
        with open('data/order_now_info/' + str(window) + '/' + str(date) + '_ordernow.pickle', 'wb') as f:
            pickle.dump(order_now_dict, f)  # 更新订单状态
    except IOError and EOFError as err:
        return (str(err))
    return (order_dict)