import typer
import db  # 导入子模块

app = typer.Typer()

# 挂载子模块
app.add_typer(db.app, name="db", help="数据库管理命令组")

@app.callback()
def main(
    ctx: typer.Context,
    env: str = typer.Option("dev", "--env", "-e", help="运行环境 (dev/prod)")
):
    """
    DevOps 运维工具 CLI 入口。
    """
    # 这一步是灵魂：
    # 我们把 env 存入 ctx.obj，这样所有子命令（如 db migrate）都能读到它
    ctx.obj = {"env": env}
    
    if env == "prod":
        typer.secho("🚀 正在连接生产环境...", fg=typer.colors.MAGENTA)

@app.command()
def status(ctx: typer.Context):
    """
    查看当前系统状态。
    """
    env = ctx.obj.get("env")
    print(f"System Status: Online | Environment: {env}")

if __name__ == "__main__":
    app()