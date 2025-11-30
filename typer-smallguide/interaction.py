import typer

app = typer.Typer()

@app.command()
def delete_user(name: str):
    """
    删除用户的危险命令。
    """
    # 1. 红色警告 (使用 typer.secho 输出彩色文本)
    typer.secho(f"警告：你即将删除用户 [{name}] ！", fg=typer.colors.RED, bold=True)
    
    # 2. 弹出确认框
    # abort=True 表示：如果用户选 No，直接终止程序，抛出 Abort 异常
    typer.confirm("你确定要继续吗？", abort=True)
    
    # 3. 如果用户选了 Yes，才会执行下面的代码
    typer.secho("正在删除...", fg=typer.colors.YELLOW)
    typer.secho(f"用户 {name} 已被彻底删除。", fg=typer.colors.GREEN)

@app.command()
def dashboard():
    typer.clear() # 瞬间清空终端
    print("欢迎来到控制面板")

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


if __name__ == "__main__":
    app()