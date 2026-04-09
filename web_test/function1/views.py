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

def user_logout(request):
    # 建立一個跳轉回登入頁面的回應物件
    response = redirect('/login/')
    # 刪除記錄登入狀態的 Cookie
    response.delete_cookie('username')
    return response

def user_signup(request):
    error_message = None
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # 1. 檢查兩次密碼是否一致
        if pass_word != confirm_password:
            error_message = "兩次輸入的密碼不一致，請重新輸入。"
        else:
            with connection.cursor() as cursor:
                # 2. 檢查帳號是否已經存在於資料庫中
                check_sql = "SELECT id FROM users WHERE username = %s"
                cursor.execute(check_sql, [user_name])
                if cursor.fetchone():
                    error_message = "此帳號已被註冊，請使用其他帳號。"
                else:
                    # 3. 帳號不存在且密碼一致，將新資料寫入資料庫
                    insert_sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                    cursor.execute(insert_sql, [user_name, pass_word])
                    
                    # 註冊成功後，可透過 render 夾帶成功訊息回到登入頁面
                    return render(request, 'login.html', {
                        'success_message': "註冊成功！請使用新帳號登入。"
                    })

    # 如果是 GET 請求，或是發生錯誤，則渲染註冊頁面並顯示錯誤訊息
    return render(request, 'signup.html', {'error_message': error_message})