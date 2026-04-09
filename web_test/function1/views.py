from django.shortcuts import render, redirect
from django.db import connection
from datetime import datetime

def user_login(request):
    error_message = None
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        
        with connection.cursor() as cursor:
            sql = "SELECT id, username FROM users WHERE username = %s AND password = %s"
            cursor.execute(sql, [user_name, pass_word])
            user = cursor.fetchone()
            
        if user:
            # 建立一個回應物件 (準備跳轉)
            response = redirect('/function1/')
            # 手動設定 Cookie，把帳號存進去 (max_age 是存活秒數，這裡設為 1 小時)
            response.set_cookie('username', user[1], max_age=3600)
            return response
        else:
            error_message = "帳號或密碼錯誤，請重新輸入。"

    return render(request, 'login.html', {'error_message': error_message})


def hello_world(request):
    # 改成從 request.COOKIES 裡面讀取資料
    username = request.COOKIES.get('username')
    
    if not username:
        # 如果 Cookie 裡面沒有帳號，代表沒登入
        return redirect('/login/')
        
    current_time = datetime.now()
    
    return render(request, 'hello.html', {
        'current_time': current_time, 
        'username': username
    })