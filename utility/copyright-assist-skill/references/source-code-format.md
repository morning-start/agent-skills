# 源代码格式规范

## 核心要求

依据《计算机软件著作权登记办法》：

| 要求 | 说明 |
|------|------|
| 页数 | 前30页 + 后30页，共60页 |
| 每页行数 | 不少于50行（含空行和注释） |
| 总行数 | 不少于3000行 |
| 内容 | 必须包含主程序代码（main函数或程序入口） |
| 格式 | 代码格式规范，缩进统一，注释清晰 |
| 上传格式 | 仅支持PDF |

**特殊情况**：整个程序不到60页的，应当提交整个源程序。最后1页结尾一定要是完成的功能模块。

## 提取策略

### 策略A：全量提交（代码 < 3000行）
- 提交所有可用代码
- 补充详细注释增加行数
- 确保格式规范

### 策略B：前后各30页（代码 ≥ 3000行）
- 提取前30页（从主入口文件开始）
- 提取后30页（代码末尾部分）
- 中间用分隔符隔开

## 代码文件选择

**优先选择**：
- 主入口文件（main.py、app.js、index.php等）
- 核心业务逻辑文件
- 主要功能模块文件
- 数据处理文件

**避免选择**：
- 配置文件（config.ini、.env、package.json等）
- 空文件或仅含注释的文件
- 测试文件（test_*.py、*_test.go等）
- 自动生成的代码文件
- 第三方依赖代码

## 格式标准

### 页面格式
```
每页格式：
- 页眉：文件名和行号范围
- 内容：代码内容，每行前加行号
- 页脚：页码（可选）
```

### 行号格式
行号右对齐，占4个字符位置：
```
   1: import sys
   2: import os
   3:
   4: def main():
   5:     print("Hello, World!")
```

### 文件分隔
切换到新代码文件时添加分隔注释：
```
// 文件: /path/to/file.py
// 从第 100 行开始
//
   100: def process_data(data):
   101:     result = []
   102:     for item in data:
```

### 页面分隔
```
--------------------------------------------------------------------------------
第 1 页 (前部)
--------------------------------------------------------------------------------
```

## 格式示例

### Python代码
```
--------------------------------------------------------------------------------
第 1 页 (前部)
--------------------------------------------------------------------------------

// 文件: src/main.py
// 从第 1 行开始
//
   1: #!/usr/bin/env python3
   2: # -*- coding: utf-8 -*-
   3:
   4: """
   5: 软件著作权申请示例程序
   6: """
   7:
   8: import sys
   9: import os
  10: from typing import List, Dict
  11:
  12: from config import settings
  13: from models.user import User
  14: from services.user_service import UserService
  15:
  16:
  17: class Application:
  18:     """应用程序主类"""
  19:
  20:     def __init__(self):
  21:         """初始化应用"""
  22:         self.user_service = UserService()
  23:         self.is_running = False
  24:
  25:     def run(self):
  26:         """运行应用主循环"""
  27:         self.is_running = True
  28:         print("用户管理系统启动...")
  29:
  30:         while self.is_running:
  31:             self.display_menu()
  32:             choice = input("请选择操作: ")
  33:             self.handle_choice(choice)
  34:
  35:     def display_menu(self):
  36:         """显示主菜单"""
  37:         print("\n" + "=" * 50)
  38:         print("用户管理系统")
  39:         print("=" * 50)
  40:         print("1. 添加用户")
  41:         print("2. 查询用户")
  42:         print("3. 删除用户")
  43:         print("4. 退出系统")
  44:         print("=" * 50)
  45:
  46:     def handle_choice(self, choice: str):
  47:         """处理用户选择"""
  48:         if choice == '1':
  49:             self.add_user()
  50:         elif choice == '2':
```

### Java代码
```
--------------------------------------------------------------------------------
第 2 页 (前部)
--------------------------------------------------------------------------------

// 文件: src/main/java/com/example/UserManager.java
// 从第 100 行开始
//
  100:     public List<User> findAll() {
  101:         List<User> users = new ArrayList<>();
  102:         Connection conn = null;
  103:         PreparedStatement stmt = null;
  104:         ResultSet rs = null;
  105:
  106:         try {
  107:             conn = dataSource.getConnection();
  108:             String sql = "SELECT * FROM users ORDER BY id";
  109:             stmt = conn.prepareStatement(sql);
  110:
  111:             rs = stmt.executeQuery();
  112:
  113:             while (rs.next()) {
  114:                 User user = new User();
  115:                 user.setId(rs.getInt("id"));
  116:                 user.setUsername(rs.getString("username"));
  117:                 user.setEmail(rs.getString("email"));
  118:                 users.add(user);
  119:             }
  120:
  121:         } catch (SQLException e) {
  122:             logger.error("查询用户失败", e);
  123:             throw new RuntimeException("数据库查询失败", e);
  124:
  125:         } finally {
  126:             if (rs != null) {
  127:                 try { rs.close(); } catch (SQLException e) {}
  128:             }
  129:             if (stmt != null) {
  130:                 try { stmt.close(); } catch (SQLException e) {}
  131:             }
  132:             if (conn != null) {
  133:                 try { conn.close(); } catch (SQLException e) {}
  134:             }
  135:         }
  136:
  137:         return users;
  138:     }
```

## 常见问题

### Q: 代码不足3000行怎么办？
A: 全量提交。可补充详细注释、增加空行、拆分长行。

### Q: 是否需要包含测试代码？
A: 一般不需要。测试代码不体现核心功能。

### Q: 可以删除敏感信息吗？
A: 可以。删除硬编码密码、密钥，替换为占位符。

### Q: 代码注释必须中文吗？
A: 不强制。建议主要注释中文，变量名/函数名英文。

### Q: 如何确保格式一致？
A: 使用代码格式化工具（Black、Prettier等），统一缩进和行尾字符。

### Q: 代码文件切换时注释格式？
A: `// 文件: 相对路径/文件名.扩展名` + `// 从第 N 行开始`

### Q: 最后1页有什么要求？
A: 最后1页结尾一定要是完成的功能模块。
