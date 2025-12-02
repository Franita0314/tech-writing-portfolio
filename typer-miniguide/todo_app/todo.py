import typer
import json
import os
from typing import Optional
from datetime import datetime

# 初始化应用
app = typer.Typer()

# 定义数据文件路径
DB_FILE = "todo_db.json"

# --- 辅助函数：处理数据存取 ---
def load_tasks():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

# --- 核心命令 ---

@app.command()
def add(
    task: str = typer.Argument(..., help="待办事项的具体内容"),
    priority: int = typer.Option(1, "--priority", "-p", help="优先级 (1-3)"),
):
    """添加一个新的待办事项"""
    tasks = load_tasks()
    
    new_task = {
        "content": task,
        "priority": priority,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    
    typer.secho(f"✅ 成功添加任务: {task} (优先级: {priority})", fg=typer.colors.GREEN)

@app.command()
def list(
    show_all: bool = typer.Option(False, "--all", "-a", help="显示所有任务（包括已完成的）")
):
    """列出当前的任务清单"""
    tasks = load_tasks()
    
    if not tasks:
        typer.secho("📭 目前没有待办事项。", fg=typer.colors.YELLOW)
        return

    typer.secho(f"{'ID':<4} {'优先级':<6} {'状态':<10} {'内容'}", bold=True)
    typer.echo("-" * 40)

    for idx, t in enumerate(tasks):
        # 如果不是显示全部，且任务已完成，则跳过
        if not show_all and t["status"] == "done":
            continue
            
        color = typer.colors.WHITE
        if t["status"] == "done":
            color = typer.colors.BRIGHT_BLACK # 灰色代表已完成
        elif t["priority"] >= 3:
            color = typer.colors.RED # 红色代表高优先级

        typer.secho(
            f"{idx:<4} {t['priority']:<6} {t['status']:<10} {t['content']}", 
            fg=color
        )

@app.command()
def complete(task_id: int):
    """完成某项任务 (输入 ID)"""
    tasks = load_tasks()
    
    # 错误处理：检查 ID 是否越界
    if task_id < 0 or task_id >= len(tasks):
        typer.secho(f"❌ 错误: 找不到 ID 为 {task_id} 的任务", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    
    tasks[task_id]["status"] = "done"
    save_tasks(tasks)
    typer.secho(f"🎉 任务 #{task_id} 已标记为完成！", fg=typer.colors.GREEN)

@app.command()
def clear():
    """清空所有任务 (危险操作)"""
    typer.secho("⚠️ 警告：这将删除所有数据！", fg=typer.colors.RED)
    typer.confirm("确定要继续吗？", abort=True)
    
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        typer.secho("♻️ 所有任务已清空。", fg=typer.colors.YELLOW)

if __name__ == "__main__":
    app()