# 吊耳计算器

一个基于 Streamlit 的吊耳应力校核工具，用于对吊耳的关键受力指标进行快速计算、结果展示与 Word 计算书导出。

本项目适合作为工程方案比选、参数试算和内部技术讨论辅助工具，强调轻量、直观和可快速验证。

---

## 功能特性

- 材料参数输入与自定义
- 载荷、角度、几何尺寸参数化输入
- 吊耳核心应力快速校核
- 吊耳二维几何示意图展示
- Word 格式计算书导出
- 基础输入合法性校验
- 核心计算最小回归测试

---

## 截图

### 主界面
![主界面](docs/screenshot-home.png)

### 计算结果
![计算结果](docs/screenshot-report.png)

---

## 运行环境

- Python 3.10 及以上
- Windows / macOS / Linux
- 推荐使用虚拟环境

---

## 安装依赖

```bash
python -m pip install -r requirements.txt
```

---

## 启动方式

推荐入口：

```bash
python -m streamlit run main.py
```

兼容旧入口：

```bash
python -m streamlit run app.py
```

启动后在浏览器打开：

```text
http://localhost:8501
```

---

## Windows 双击启动

本项目提供了本地脚本版的 Windows 双击启动方案。

可用入口：

- `start_app.bat`
- `launch_hidden.vbs`

脚本内部已切换为启动 `main.py`。

---

## 使用说明

### 1. 输入材料参数

在左侧栏选择材料牌号，或切换为“自定义”后手动输入：

- 材料屈服强度 `Fy`
- 材料抗拉强度 `Fu`
- 结构安全系数 `Ns`

### 2. 输入工况载荷

输入以下参数：

- 单只吊耳受力 `Fv (t)`
- 动载系数 `Kd`
- 吊索与水平面夹角 `θ`

程序会自动将吨换算为 `kN`。

### 3. 输入几何尺寸

输入或调整：

- 吊耳主板厚度 `t`
- 单侧加强板厚度 `tp`
- 销轴孔孔径 `d`
- 销轴直径 `dp`
- 孔心至边缘距离 `R`
- 圆心到底边距离 `H`
- 焊缝焊脚尺寸 `hf`
- 吊耳根部宽度 `W`

默认情况下：

- `W = 2R`

### 4. 查看结果

程序会展示：

- 综合校核结论
- 四项应力指标的通过 / 不通过状态
- 吊耳几何示意图
- 详细计算过程
- 汇总表格

### 5. 导出计算书

点击“导出 Word 报告”按钮，即可导出 `.docx` 格式计算书。

---

## 测试

运行测试：

```bash
python -m unittest discover -s tests -v
```

---

## 项目结构

```text
.
├─ app.py                         # 兼容旧入口，转发到 main.py
├─ main.py                        # 推荐 Streamlit 入口
├─ lifting_lug_calculator/
│  ├─ core/                       # 计算核心、常量与数据模型
│  ├─ reporting/                  # Word 计算书生成
│  ├─ visualization/              # 吊耳示意图绘制
│  └─ ui/                         # Streamlit 页面与展示逻辑
├─ tests/
│  ├─ test_calculate_lug_stresses.py
│  └─ test_module_exports.py
├─ docs/
├─ requirements.txt
└─ README.md
```

---

## 当前实现说明

当前版本仍采用简化工程校核逻辑，适合快速试算、尺寸敏感性分析和工程讨论中的初步校核。

如果用于正式项目，请结合适用标准、具体工况、制造要求及专业审核进行复核。

---

## 后续计划

可继续完善：

- 增加更多边界条件测试
- 补充标准依据说明
- 增加示例工况
- 优化导出报告格式

---

## 免责声明

本项目仅供学习、演示、参数试算与工程参考使用。
