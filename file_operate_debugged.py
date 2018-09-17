#文件操作模块     主要定义涉及文件IO的函数
import pickle       #导入pickle模块
import os       #导入os模块

#函数login，参数：用户名，密码，用户身份，用户身份必须为'student','stuff','admin'中的一种，访问存放用户登录信息的文件，返回布尔值。

def login(user_name,key,user_identity):
    try:
        with open('data/user_info/'+str(user_identity)+'/'+str(user_name)+'.pickle', 'rb') as f:
            user = pickle.load(f)
        if user.key == key:
            return(True)
        else:
            return(False)
    except IOError and EOFError:
        return(False)        #若文件不存在，则返回错误信息(最好也返回一个boolean值)


def checkfor(filen, obj):
    fileo = filen - '.pickle' + '.txt'
    try:
        if os.path.getsize(filen) == 0:
            file = open(filen, 'wb')
            pickle.dump(obj, file)
            file.close()
            return(True)
        else:
            return(False)
    except FileNotFoundError:
        with open(fileo, 'wb') as file:
            pickle.dump(obj, file)
            file.close()
            os.rename(fileo, filen)
            return(True)
#检测元素与文件是否存在，不存在就加，filen为string类型


#函数creat_stumenu，参数：学生订单和日期和窗
#口号，一个学生类，创建字典，key为学生类，value为订单列表，订单
#列表第1项是窗口号，用pickle保存在本地，返回新的订单
def creat_stumenu(stu, order_list, date, window):
    #项目的日期格式均为"18-8-31"的格式，便于字符串操作
    f = 'data/order_info/'+str(window)+'/'+str(date)+'_order.pickle'

    checkfor(f, [])

    try:
        with open('data/order_info/'+str(window)+'/'+str(date)+'_order.pickle', 'rb') as f:
            today_stumenu = pickle.load(f)
            #today_stumenu是列表，各元素是字典，key为学生类，value为订单字典
    except IOError and EOFError as err:
        return(str(err))        #若出错，则将错误信息返回

    order_dict = dict()
    order_list.insert(0, window)       #列表第一项是窗口号
    order_dict[stu] = order_list
    today_stumenu.append(order_dict)        #新增数据

    try:
        with open('data/order_info/'+str(window)+'/'+str(date)+'_order.pickle', 'wb') as f:
            pickle.dump(today_stumenu, f)
            #保存更改后的文件
    except IOError and EOFError as err:
        return(str(err))
    try:
        with open('data/order_now_info/'+str(window)+'/'+str(date)+'_ordernow.pickle', 'rb') as f:
            order_now_dict = pickle.load(f)       #字典
        for item in order_list:
            order_now_dict[item] += 1
        with open('data/order_now_info/'+str(window)+'/'+str(date)+'_ordernow.pickle', 'wb') as f:
            pickle.dump(order_now_dict, f)       #更新订单状态
    except IOError and EOFError as err:
        return(str(err))
    return(order_dict)

#函数create_menu，参数：员工创建的菜单列表和日期和窗口号，创建字典，key为日期，value为菜单列表，菜单列表第一项是窗口号，用pickle保存在本地，并返回菜单

def creat_menu(menu_list,date,window):
    menu_list.insert(0, window)        #列表第一项是窗口号，不用append
    menu_dict = dict()
    menu_dict[date] = menu_list
    f = 'data/menu_info/' + str(window) + '/' + str(date) + '_menu.pickle'
    if not checkfor(f, menu_dict):
        try:
            with open(f, 'wb') as f:
                pickle.dump(menu_dict, f)
        except IOError as err:
            return(str(err))        #若出错，则将错误信息返回
    order_now_dict = dict()       #新增订单状态
    for item in menu_list:
        order_now_dict[item] = 0
    f2 = 'data/order_now_info/'+str(window)+'/'+str(date)+'_ordernow.pickle'
    if not checkfor(f2, order_now_dict):
        try:
            with open(f2, 'wb') as f:
                pickle.dump(order_now_dict, f)       #创建订单状态字典
        except IOError as err:
            return(str(err))
    return(menu_dict)   #返回菜单


#函数get_menu，参数：日期，窗口号，返回存放菜单的列表

def get_menu(date, window):
    try:
        with open('data/menu_info/'+str(window)+'/'+str(date)+'_menu.pickle', 'rb') as f:
            menu_file = pickle.load(f)    #menu_list是菜单列表
    except IOError and EOFError and FileNotFoundError as err:
        return(str(err))        #若出错，则将错误信息返回
    return(menu_file[1:])       #列表第一项是窗口号，因此需进行切片操作

#函数delete_stumenu,参数：日期，用户名，窗口号，删除并返回该学生该日的订单,若该学生该日该窗口无订单，则返回False
