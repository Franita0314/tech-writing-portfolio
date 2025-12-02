from typer.testing import CliRunner
from todo import app  # 导入我们在第六章写的 app

runner = CliRunner()

def test_help():
    """测试 1: 确保 --help 能正常显示"""
    result = runner.invoke(app, ["--help"])
    
    # 验证退出码是否为 0 (代表成功)
    assert result.exit_code == 0
    # 验证输出里是否有 "Usage" 这个词
    assert "Usage" in result.stdout

def test_add_task():
    """测试 2: 测试添加任务功能"""
    # 模拟运行: python todo.py add "测试任务" --priority 2
    result = runner.invoke(app, ["add", "测试任务", "--priority", "2"])
    
    assert result.exit_code == 0
    # 验证输出里是否包含成功的提示
    assert "成功添加任务" in result.stdout

def test_list_tasks():
    """测试 3: 测试列表查看"""
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "ID" in result.stdout
    assert "状态" in result.stdout