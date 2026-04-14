"""
main.py — 入口文件
"""
import threading
from pet import ClaudePet

def _init_dida(pet: ClaudePet):
    """后台线程：完成 OAuth 后激活滴答提醒"""
    try:
        from api.dida.dida_auth import get_valid_token
        from api.dida.dida_tasks import get_today_tasks
        from config.user_prefs import get_selected_project_ids

        get_valid_token()  # 首次会弹浏览器，之后静默刷新
        
        def filtered_tasks():
            return get_today_tasks(get_selected_project_ids())    
                
        pet.behavior.enable_dida(filtered_tasks)
        pet.root.after(0, lambda:                  # 回主线程显示气泡
            pet.show_bubble("滴答清单已连接！"))
        
    except Exception as e:
        print(f"[Dida] 接入失败，跳过: {e}")

if __name__ == "__main__":
    pet = ClaudePet()

    t = threading.Thread(target=_init_dida, args=(pet,), daemon=True)
    t.start()

    pet.run()