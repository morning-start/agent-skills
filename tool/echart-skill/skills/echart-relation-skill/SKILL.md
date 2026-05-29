---
name: echart-relation-skill
version: v1.0.0
author: skill-factory
parent: echart-skill
description: ECharts 关系图技能，掌握关系图、桑基图、树图、旭日图等层级和网络关系数据的可视化配置
tags: [echarts, graph, sankey, tree, sunburst, relation, network]
dependency:
  parent: echart-skill
  requires: echart-basic-skill
---

# EChart Relation Skill - 关系图技能

## 任务目标

- **本 Skill 用于**：掌握关系型数据的可视化（网络关系、层级结构、流量分布）
- **核心能力**：
  - 关系图：网络关系、组织结构
  - 桑基图：流量守恒、流向分析
  - 树图：层级归属、目录结构
  - 旭日图：多级占比、层级分布
- **触发条件**：展示网络关系、层级数据、流量数据时

## 图表类型

### 关系图 (Graph)

**展示信息**：节点间的网络关系、权重连接

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| nodes | 节点数组 | [{name, value, category, symbolSize}] |
| links/edges | 边数组 | [{source, target, value}] |
| categories | 分类数组 | 节点的分组 |
| layout | 布局算法 | 'force'/'circular'/'none' |

**变量关系**：source-target 连接关系，value 表示权重

**子类型**：
- 力引导布局图 (force)
- 笛卡尔坐标系关系图
- 环形布局图
- 自动布局关系图
- 关系图标签隐藏重叠

```javascript
option = {
  series: [{
    type: 'graph',
    layout: 'force',
    nodes: [
      { name: 'Node1', value: 10, category: 0 },
      { name: 'Node2', value: 20, category: 1 }
    ],
    links: [
      { source: 'Node1', target: 'Node2', value: 5 }
    ],
    categories: [{ name: '类目1' }, { name: '类目2' }],
    force: {
      repulsion: 100,
      edgeLength: 50
    }
  }]
};
```

### 桑基图 (Sankey)

**展示信息**：流量从起点到终点的守恒关系

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| nodes | 节点数组 | [{name}] |
| links | 边数组 | [{source, target, value}] |
| nodeAlign | 对齐方式 | 'left'/'right'/'justify' |

**变量关系**：流量守恒（流入=流出）

**子类型**：
- 水平桑基图
- 垂直桑基图
- 渐变色边桑基图
- 层级自定义样式桑基图

```javascript
option = {
  series: [{
    type: 'sankey',
    layout: 'none',
    orient: 'horizontal',
    nodeAlign: 'left',
    nodes: [
      { name: '入口1' },
      { name: '出口1' },
      { name: '出口2' }
    ],
    links: [
      { source: '入口1', target: '出口1', value: 100 },
      { source: '入口1', target: '出口2', value: 50 }
    ],
    lineStyle: { color: 'gradient' }
  }]
};
```

### 树图 (Tree)

**展示信息**：严格的父子层级关系

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| data | 树节点对象 | {name, children: [...]} |
| orient | 展开方向 | 'horizontal'/'vertical'/'radial' |
| symbol | 节点形状 | 'circle'/'rect'/'roundRect' |
| label | 标签配置 | 节点文字样式 |

**变量关系**：严格的树形父子归属关系

**子类型**：
- 从左到右树图
- 从上到下树图
- 径向树图
- 折线树图

```javascript
option = {
  series: [{
    type: 'tree',
    orient: 'horizontal',
    data: [{
      name: 'Root',
      children: [
        { name: 'Branch1', children: [{ name: 'Leaf1' }] },
        { name: 'Branch2' }
      ]
    }]
  }]
};
```

### 旭日图 (Sunburst)

**展示信息**：多层级占比数据，从内到外的包含关系

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| data | 旭日节点数组 | [{name, value, children}] |
| radius | 半径 | [内半径, 外半径] |
| label | 标签配置 | 扇区标签样式 |
| levels | 层级配置 | 每层的半径、标签设置 |

**变量关系**：从内到外的包含占比关系

**子类型**：
- 基础旭日图
- 圆角旭日图
- 单色旭日图
- 标签旋转旭日图

```javascript
option = {
  series: [{
    type: 'sunburst',
    radius: ['20%', '80%'],
    data: [{
      name: 'Root',
      value: 100,
      children: [
        { name: 'Part1', value: 60, children: [{ name: 'Detail1', value: 30 }] },
        { name: 'Part2', value: 40 }
      ]
    }],
    label: { rotate: 'radial' }
  }]
};
```

## 通用配置

### 力引导布局配置

```javascript
force: {
  initLayout: 'circular',  // 初始化布局
  repulsion: 100,           // 节点斥力
  gravity: 0.1,             // 重心引力
  edgeLength: [50, 200],    // 边的理想长度
  layoutAnimation: true     // 布局动画
}
```

### 节点样式

```javascript
itemStyle: {
  color: '#5470C6',
  borderColor: '#fff',
  borderWidth: 2,
  shadowBlur: 10,
  shadowColor: 'rgba(0,0,0,0.3)'
}
```

### 边样式

```javascript
lineStyle: {
  color: '#ccc',
  width: 1,
  curveness: 0.3,      // 弯曲度
  opacity: 0.6
}
```

## 数据转换

### 从树形数据转换

```javascript
// 树形 -> 旭日图
function treeToSunburst(data) {
  return {
    name: data.name,
    value: data.value || data.children?.reduce((sum, c) => sum + c.value, 0),
    children: data.children?.map(treeToSunburst)
  };
}
```

### 从邻接表转换

```javascript
// 邻接表 -> 关系图节点和边
function adjacencyToGraph(adjList) {
  const nodes = [];
  const links = [];
  Object.keys(adjList).forEach(source => {
    nodes.push({ name: source });
    adjList[source].forEach(target => {
      nodes.push({ name: target });
      links.push({ source, target });
    });
  });
  return { nodes, links };
}
```

## 注意事项

1. **力引导布局**：大数据量时考虑关闭布局动画或减少迭代次数
2. **桑基图**：确保流量守恒（可选中节点编辑）
3. **树图**：数据必须是严格的树形结构（无环）
4. **旭日图**：内层值应该等于外层所有子节点之和
5. **性能**：超过500节点考虑使用 canvas 渲染器

## 相关技能

- [echart-basic-skill](../echart-basic-skill/SKILL.md) - 基础图表
- [echart-multi-skill](../echart-multi-skill/SKILL.md) - 多图组合（联动）
- [echart-geo-skill](../echart-geo-skill/SKILL.md) - 地理图（关系图+地图）
