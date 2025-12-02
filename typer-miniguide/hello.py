import typer

# 1. 实例化一个 Typer 应用
app = typer.Typer()

# 2. 定义命令：使用 @app.command() 装饰器
@app.command()
def hello(name: str):
    """
    最简单的打招呼命令。
    """
    # Typer 会自动把 name 参数识别为命令行参数
    print(f"Hello {name}")

@app.command()
def goodbye(name: str, formal: bool = False):
    """
    道别命令。
    
    --formal: 这是一个可选的 Flag，用于切换正式语气。
    """
    if formal:
        print(f"Goodbye, Mr./Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")

# 3. 程序入口
if __name__ == "__main__":
    app()
