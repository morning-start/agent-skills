---
name: echart-geo-skill
version: v1.0.0
author: skill-factory
parent: echart-skill
description: ECharts 地理图技能，掌握地图、3D地球、航线图等地理坐标可视化，用于区域分析、人口分布和空间分布展示
tags: [echarts, map, geo, globe, flight, geographic, visualization]
dependency:
  parent: echart-skill
  requires: echart-basic-skill
---

# EChart Geo Skill - 地理图技能

## 任务目标

- **本 Skill 用于**：掌握地理坐标数据可视化（区域分析、空间分布、航线轨迹）
- **核心能力**：
  - 地图：区域数据、地理分区
  - 3D地球：全球视角、立体分布
  - 航线图：路径轨迹、连接关系
- **触发条件**：展示地理位置相关数据时

## 图表类型

### 地图 (Map)

**展示信息**：地理区域上的数据分布

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| geo | 地理坐标系 | 地图配置 |
| series.data | 数组 | [{name, value}] |
| map | 地图名称 | 对应GeoJSON |
| selectedMode | 选择模式 | 'single'/'multiple' |

**变量关系**：地理区域名称与数值的映射

**子类型**：
- 中国地图/省份地图
- 世界地图
- 等值区划图（Choropleth）
- 散点地图
- 城市气泡图
- 自定义地图投影

```javascript
// 注册地图
echarts.registerMap('china', chinaGeoJSON);

option = {
  geo: {
    map: 'china',
    roam: true,                    // 支持缩放拖拽
    label: { show: true },
    itemStyle: { areaColor: '#eee', borderColor: '#ccc' },
    emphasis: {
      itemStyle: { areaColor: '#ffd700' },
      label: { show: true }
    }
  },
  series: [{
    type: 'map',
    geoIndex: 0,
    data: [
      { name: '北京', value: 100 },
      { name: '上海', value: 80 },
      { name: '广州', value: 60 }
    ]
  }]
};
```

### 散点地图 (Scatter + Geo)

**展示信息**：地理位置上的点分布

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| geo | 地理坐标系 | 地图配置 |
| series.type | 'scatter' | 散点图 |
| series.data | 数组 | [longitude, latitude, value] |
| symbolSize | 数值/函数 | 点的大小 |

**变量关系**：经纬度确定位置，value编码大小/颜色

**子类型**：
- 基础散点地图
- 涟漪特效散点地图（effectScatter）
- 气泡大小地图
- 颜色编码地图

```javascript
option = {
  geo: { map: 'china', roam: true },
  series: [{
    type: 'effectScatter',
    coordinateSystem: 'geo',
    data: [
      { name: '北京', value: [116.46, 39.92, 100] },
      { name: '上海', value: [121.48, 31.22, 80] }
    ],
    symbolSize: function(val) { return val[2] / 10; },
    showEffectOn: 'render',
    rippleEffect: { brushType: 'stroke', scale: 3 }
  }]
};
```

### 热力地图 (Heatmap + Geo)

**展示信息**：地理区域的热力分布

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| geo | 地理坐标系 | 地图配置 |
| series.type | 'heatmap' | 热力图 |
| series.data | 数组 | [lng, lat, value] |

**变量关系**：经纬度密度分布

**子类型**：
- 城市热力分布
- 人口密度热力图

```javascript
option = {
  geo: { map: 'china', roam: true, zoom: 1.2 },
  series: [{
    type: 'heatmap',
    coordinateSystem: 'geo',
    data: [
      [116.46, 39.92, 100],
      [121.48, 31.22, 80],
      [113.23, 23.16, 60]
    ]
  }]
};
```

### 航线图 (Lines)

**展示信息**：起点到终点的路径轨迹

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| series.type | 'lines' | 路径图 |
| series.data | 数组 | [{coords: [[lng1,lat1], [lng2,lat2]], value}] |
| polyline | 布尔 | 是否为折线（false=曲线） |
| effect | 特效配置 | 动画效果 |

**变量关系**：起点到终点的弧线连接

**子类型**：
- 基础航线图
- 3D地球航线图
- 颜色渐变航线图
- 动画特效航线图

```javascript
option = {
  geo: { map: 'china', roam: true },
  series: [{
    type: 'lines',
    coordinateSystem: 'geo',
    data: [{
      name: '北京->上海',
      coords: [[116.46, 39.92], [121.48, 31.22]],
      lineStyle: { color: '#5470C6', width: 2, curveness: 0.3 },
      effect: { show: true, period: 4, trailLength: 0.3 }
    }]
  }]
};
```

### 3D地球 (Globe)

**展示信息**：全球视角的立体地理数据

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| series.type | 'globe' | 3D地球 |
| globeRadius | 数值 | 地球半径 |
| baseTexture | 纹理 | 地球表面纹理 |
| layers | 图层配置 | 大气层、光照等 |

**变量关系**：三维球面上的数据叠加

**子类型**：
- 基础3D地球
- 大气层显示
- 等值线动画地球
- 地形位移地球
- 3D柱状图地球

```javascript
option = {
  series: [{
    type: 'globe',
    globeRadius: 100,
    baseTexture: 'world.jpg',
    heightTexture: 'elevation.tif',
    shading: 'realistic',
    atmosphere: { show: true, color: '#fff', intensity: 0.5 },
    layers: [{
      type: 'scatter3D',
      coordinateSystem: 'geo3D',
      data: [[116.46, 39.92, 100]]
    }]
  }]
};
```

## 通用配置

### 地理坐标系配置

```javascript
geo: {
  map: 'world',                   // 地图名称
  roam: true,                      // 是否开启鼠标缩放和平移漫游
  zoom: 1,                         // 当前缩放级别
  center: [0, 0],                 // 中心点经纬度
  scaleLimit: { min: 1, max: 8 }, // 缩放限制
  label: {
    show: false,                   // 是否显示标签
    color: '#333'
  },
  itemStyle: {
    areaColor: '#eee',             // 区域颜色
    borderColor: '#ccc',           // 边界颜色
    borderWidth: 1
  },
  emphasis: {                      // 高亮状态
    itemStyle: { areaColor: '#ffd700' },
    label: { show: true }
  }
}
```

### 注册地图

```javascript
// 内置地图
 echarts.registerMap('china', chinaGeoJSON);
 echarts.registerMap('world', worldGeoJSON);

// 从URL加载
fetch('https://example.com/china.json')
  .then(res => res.json())
  .then(data => echarts.registerMap('china', data));
```

## 数据转换

### 经纬度数据转地图散点

```javascript
function toGeoScatter(locations) {
  return locations.map(loc => ({
    name: loc.name,
    value: [loc.lng, loc.lat, loc.value || 1]
  }));
}
```

### 行政区划数据转等值区划图

```javascript
function toChoropleth(districtData) {
  return districtData.map(d => ({
    name: d.districtName,
    value: d.value
  }));
}
```

## 注意事项

1. **地图注册**：使用前必须注册对应GeoJSON
2. **坐标系**：geo3D用于3D地球散点/柱状/航线
3. **数据格式**：经纬度顺序是 [lng, lat] 不是 [lat, lng]
4. **漫游限制**：设置scaleLimit防止过度缩放
5. **性能**：大数据量散点使用 effectScatter 而非普通 scatter

## 相关技能

- [echart-basic-skill](../echart-basic-skill/SKILL.md) - 基础图表
- [echart-3d-skill](../echart-3d-skill/SKILL.md) - 3D图表
- [echart-multi-skill](../echart-multi-skill/SKILL.md) - 多图组合（地图+散点+航线叠加）
