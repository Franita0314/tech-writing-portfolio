import typer

app = typer.Typer()

@app.command()
def init():
    """初始化数据库连接池"""
    typer.echo("Initializing Database...")

@app.command()
def migrate(
    # 这里的 ctx 是 Typer 的上下文对象，里面装着主程序传来的数据
    ctx: typer.Context, 
    revision: str = typer.Argument(..., help="迁移的版本号，如 head")
):
    """
    执行数据库迁移。
    会自动读取全局配置中的环境信息。
    """
    # 从上下文(ctx.obj)中获取主程序存入的配置
    config = ctx.obj
    env = config.get("env", "dev")
    
    typer.secho(f"正在 [{env}] 环境下执行数据库迁移...", fg=typer.colors.YELLOW)
    typer.echo(f"Migrating to revision: {revision}")
    
    if env == "prod":
        typer.secho("⚠️ 警告：生产环境迁移已记录日志！", fg=typer.colors.RED)

# 注意：不要在这里写 if __name__ == "__main__"