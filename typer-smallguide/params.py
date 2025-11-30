import typer

app = typer.Typer()

@app.command()
def signup(
    # 1. 必填参数 (Argument): 因为没有默认值
    username: str, 
    
    # 2. 选项 (Option): 因为有默认值 18
    # Typer 会自动将其转化为命令行选项 --age
    age: int = 18, 
    
    # 3. 标记 (Flag): 布尔值且有默认值
    # 命令行里不需要传值，只需要写 --vip 即可触发 True
    is_vip: bool = False
):
    """
    模拟用户注册流程。
    """
    print(f"正在注册用户: {username}")
    print(f"年龄: {age}")
    
    if is_vip:
        print("✨ 尊贵的 VIP 用户，欢迎！")
    else:
        print("普通用户注册成功。")

@app.command()
def login(
    username: str,
    # 使用 typer.Option 定制选项
    # "18" 是默认值
    # "--age" 和 "-a" 是别名
    # help 是显示在 --help 中的提示
    age: int = typer.Option(18, "--age", "-a", help="用户的注册年龄"),
    
    # 强制要求输入的选项 (没有默认值，设为 ...)
    # prompt=True 会让 Typer 在用户没输的时候，交互式询问
    password: str = typer.Option(..., prompt=True, hide_input=True)
):
    print(f"User {username} (Age: {age}) logged in.")
    print(f"Password: {password}")

if __name__ == "__main__":
    app()