import flet as ft
import datetime

def main(page: ft.Page):
    # --- 页面基本配置 ---
    page.title = "闪电记账"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 700
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # --- 数据存储逻辑 ---
    # 使用本地存储，刷新页面数据也不会丢
    def save_data():
        items = []
        for control in lv.controls:
            items.append(control.title.value)
        page.client_storage.set("records", items)

    def load_data():
        saved_items = page.client_storage.get("records")
        if saved_items:
            for item in saved_items:
                lv.controls.append(create_list_tile(item))
            page.update()

    def create_list_tile(text):
        return ft.ListTile(
            title=ft.Text(text),
            leading=ft.Icon(ft.icons.ACCOUNT_BALANCE_WALLET_ROUNDED, color="blue"),
            trailing=ft.IconButton(
                icon=ft.icons.DELETE_OUTLINE,
                on_click=lambda e: delete_item(text)
            )
        )

    def delete_item(text):
        # 简单的删除逻辑
        for control in lv.controls[:]:
            if control.title.value == text:
                lv.controls.remove(control)
        save_data()
        page.update()

    # --- 按钮点击事件 ---
    def add_btn_click(e):
        if not amt.value:
            amt.error_text = "请输入金额"
            page.update()
            return
        
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        record_str = f"{now} | {cat.value} : ¥{amt.value}"
        
        # 添加到列表顶部
        lv.controls.insert(0, create_list_tile(record_str))
        
        # 清空输入并保存
        amt.value = ""
        amt.error_text = None
        save_data()
        page.update()

    # --- 界面组件 ---
    amt = ft.TextField(
        label="输入金额", 
        prefix_text="¥ ", 
        keyboard_type=ft.KeyboardType.NUMBER,
        border_radius=10
    )
    
    cat = ft.Dropdown(
        label="选择分类",
        value="餐饮美食",
        options=[
            ft.dropdown.Option("餐饮美食"),
            ft.dropdown.Option("交通出行"),
            ft.dropdown.Option("购物消费"),
            ft.dropdown.Option("休闲娱乐"),
            ft.dropdown.Option("工资收入"),
        ],
        border_radius=10
    )

    lv = ft.ListView(expand=True, spacing=10)

    # --- 组装页面 ---
    page.add(
        ft.Row([
            ft.Icon(ft.icons.FLASH_ON, color="orange", size=30),
            ft.Text("闪电记账", size=28, weight="bold")
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=20, color="transparent"),
        amt,
        cat,
        ft.ElevatedButton(
            "记一笔", 
            icon=ft.icons.ADD, 
            on_click=add_btn_click,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            width=400,
            height=50,
            bgcolor="blue",
            color="white"
        ),
        ft.Divider(height=20),
        ft.Text("最近账单", size=18, weight="w500"),
        lv
    )

    # 启动时加载数据
    load_data()

# 运行 App
if __name__ == "__main__":
    ft.app(target=main)
