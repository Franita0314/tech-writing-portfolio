import typer
import os
import sys

app = typer.Typer()

@app.command()
def read_config(path: str):
    """
    安全地读取配置文件。
    """
    # 1. 预先检查 (Validation)
    # 不要在 try-except 里做逻辑检查，要在操作前就拦截错误
    if not os.path.exists(path):
        typer.secho(f"错误: 找不到文件 '{path}'", fg=typer.colors.RED, err=True)
        # 重点：显式抛出 Exit 异常，并指定 code=1
        # 这告诉操作系统：程序非正常退出
        raise typer.Exit(code=1)

    # 2. 业务逻辑
    typer.secho(f"正在读取 {path} ...", fg=typer.colors.GREEN)
    
    # 模拟读取过程
    # 这里即使发生未知错误，因为我们前面做了检查，概率也会大大降低
    with open(path, "r", encoding="utf-8") as f:
        print(f.read())

@app.command()
def create_user(username: str):
    """
    创建用户（带逻辑校验）。
    """
    # 场景：禁止使用 'admin' 作为用户名
    if username.lower() == "admin":
        typer.secho("错误: 禁止使用保留用户名 'admin'", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    
    print(f"用户 {username} 创建成功！")

if __name__ == "__main__":
    app()