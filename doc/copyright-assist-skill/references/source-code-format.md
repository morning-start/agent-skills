# 源代码格式规范

## 目录
- [核心要求](#核心要求)
- [格式标准](#格式标准)
- [提取规则](#提取规则)
- [格式示例](#格式示例)
- [常见问题](#常见问题)

## 核心要求

### 软著申请源代码文档要求
- **页数**：通常要求提交前30页和后30页，共60页
- **每页行数**：不少于50行
- **总行数**：不少于3000行
- **内容**：必须包含主程序代码（main函数或程序入口）
- **格式**：代码格式规范，缩进统一，注释清晰

### 代码提取原则
- 选取有代表性、核心的代码文件
- 确保代码逻辑完整，能够体现软件的主要功能
- 避免选取纯配置文件、空文件、测试文件
- 保持代码的原始结构，不删除关键逻辑

## 格式标准

### 1. 页面格式
```
每页格式：
- 页眉：文件名和行号范围
- 内容：代码内容，每行前加行号
- 页脚：页码（可选）
```

### 2. 行号格式
- 行号右对齐，占4个字符位置
- 格式：`行号: 代码内容`
- 示例：
```
   1: import sys
   2: import os
   3:
   4: def main():
   5:     print("Hello, World!")
```

### 3. 文件分隔
当切换到新的代码文件时，添加文件分隔注释：
```
// 文件: /path/to/file.py
// 从第 100 行开始
//
   100: def process_data(data):
   101:     result = []
   102:     for item in data:
```

### 4. 页面分隔
每页之间添加分隔符：
```
--------------------------------------------------------------------------------
第 1 页 (前部)
--------------------------------------------------------------------------------
```

### 5. 分页标识
- 前部：前30页代码
- 后部：后30页代码
- 中间用分隔符隔开

## 提取规则

### 1. 代码文件选择
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

### 2. 提取策略
**策略A：按文件行数提取**
1. 统计所有代码文件的行数
2. 将代码文件按行数排序
3. 选择行数最多的文件优先提取
4. 确保前30页和后30页的代码都来自核心文件

**策略B：按功能模块提取**
1. 按功能模块分类代码文件
2. 每个模块选择1-2个核心文件
3. 确保覆盖主要功能模块

**策略C：按代码结构提取**
1. 从主入口文件开始
2. 按调用关系追踪依赖文件
3. 形成完整的调用链
4. 选择调用链中的关键文件

### 3. 行数计算
- 空行计入总行数
- 注释行计入总行数
- 代码行计入总行数
- 每页保证不少于50行

### 4. 代码完整性
- 确保每个代码块的开始和结束都在同一页或相邻页
- 避免在函数或类的中间断页（如果可能）
- 保持代码逻辑的连贯性

## 格式示例

### 示例1：Python代码格式
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
   6: 这是一个用户管理系统的主程序
   7: """
   8:
   9: import sys
  10: import os
  11: from typing import List, Dict
  12:
  13: from config import settings
  14: from models.user import User
  15: from services.user_service import UserService
  16:
  17:
  18: class Application:
  19:     """应用程序主类"""
  20:
  21:     def __init__(self):
  22:         """初始化应用"""
  23:         self.user_service = UserService()
  24:         self.is_running = False

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

### 示例2：Java代码格式
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
  127:                 try {
  128:                     rs.close();
  129:                 } catch (SQLException e) {
  130:                     logger.error("关闭ResultSet失败", e);
  131:                 }
  132:             }
  133:             if (stmt != null) {
  134:                 try {
  135:                     stmt.close();
  136:                 } catch (SQLException e) {
  137:                     logger.error("关闭Statement失败", e);
 138:                 }
  139:             }
  140:             if (conn != null) {
  141:                 try {
  142:                     conn.close();
  143:                 } catch (SQLException e) {
  144:                     logger.error("关闭Connection失败", e);
  145:                 }
  146:             }
  147:         }
  148:
  149:         return users;
  150:     }
```

### 示例3：JavaScript代码格式
```
--------------------------------------------------------------------------------
第 3 页 (前部)
--------------------------------------------------------------------------------

// 文件: src/services/userService.js
// 从第 200 行开始
//
  200:
  201:     /**
  202:      * 根据ID查询用户
  203:      * @param {number} userId - 用户ID
  204:      * @returns {Promise<User>} 用户对象
  205:      */
  206:     async findById(userId) {
  207:         if (!userId || userId <= 0) {
  208:             throw new Error('无效的用户ID');
  209:         }
  210:
  211:         try {
  212:             const result = await this.database.query(
  213:                 'SELECT * FROM users WHERE id = $1',
  214:                 [userId]
  215:             );
  216:
  217:             if (result.rows.length === 0) {
  218:                 return null;
  219:             }
  220:
  221:             const user = result.rows[0];
  222:             return {
  223:                 id: user.id,
  224:                 username: user.username,
  225:                 email: user.email,
  226:                 phone: user.phone,
  227:                 department: user.department,
  228:                 position: user.position,
  229:                 createdAt: new Date(user.created_at),
  230:                 updatedAt: new Date(user.updated_at)
  231:             };
  232:
  233:         } catch (error) {
  234:             console.error('查询用户失败:', error);
  235:             throw new Error('数据库查询失败');
  236:         }
  237:     }
  238:
  239:     /**
  240:      * 更新用户信息
  241:      * @param {number} userId - 用户ID
  242:      * @param {Object} data - 更新数据
  243:      * @returns {Promise<User>} 更新后的用户对象
  244:      */
  245:     async update(userId, data) {
  246:         if (!userId || userId <= 0) {
  247:             throw new Error('无效的用户ID');
 248:         }
  249:
  250:         const allowedFields = ['username', 'email', 'phone', 'department', 'position'];
  251:         const updates = [];
  252:         const values = [];
  253:         let index = 1;
```

## 常见问题

### Q1: 如果代码总行数不足3000行怎么办？
A: 如果代码总行数不足，可以：
1. 选取所有可用代码
2. 增加注释，对关键代码添加详细注释
3. 分拆长行，将一行代码拆分成多行
4. 确保代码格式规范，增加空行提高可读性

### Q2: 是否需要包含测试代码？
A: 一般不需要。测试代码通常是辅助性的，不体现软件的核心功能。但如果测试代码是软件功能的一部分（如单元测试框架），可以适当包含。

### Q3: 可以删除代码中的敏感信息吗？
A: 可以。在提交软著申请前，建议：
1. 删除硬编码的密码、密钥等敏感信息
2. 替换为占位符（如 `YOUR_API_KEY_HERE`）
3. 删除数据库连接字符串中的真实IP和端口
4. 删除真实的用户数据或测试数据

### Q4: 代码注释必须是中文吗？
A: 不强制要求。但建议：
- 主要注释使用中文，便于审查人员理解
- 变量名、函数名使用英文，符合编程规范
- 技术术语可以保留英文原文

### Q5: 如何确保代码的格式一致性？
A: 建议：
1. 使用代码格式化工具（如Black for Python、Prettier for JavaScript）
2. 统一缩进方式（4空格或2空格）
3. 统一行尾字符（使用LF而不是CRLF）
4. 删除多余的空行和尾随空格
5. 统一命名规范（驼峰命名法或下划线命名法）

### Q6: 提取的代码需要按照什么顺序排列？
A: 建议：
1. 从主入口文件开始
2. 按照调用顺序排列依赖文件
3. 同一模块的文件放在一起
4. 前部代码按逻辑顺序，后部代码按反向顺序或继续按顺序

### Q7: 代码文件切换时的注释如何添加？
A: 格式如下：
```
// 文件: 相对路径/文件名.扩展名
// 从第 N 行开始
//
```

如果文件名太长，可以简化，但建议保留相对路径以便追溯。

### Q8: 页眉和页脚是否必需？
A: 页脚（页码）不是必需的，但建议添加以便查阅。页眉（文件名和行号）是必需的，有助于审查人员定位代码位置。
