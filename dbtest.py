import database


if __name__ == '__main__':
    # ret = database.signup('llipter', 'xxx', 'xxx')
    # print(ret)

    user = database.get_user_by_name('admin')
    print(user)