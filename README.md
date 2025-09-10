# 登录校园网脚本

>[!tip]
> 
>参考了 [该仓库](https://github.com/AaronZSAM101/CampusNetworkConnection) 的内容。

## 环境依赖
- Python 3.11+（实际已在 3.13 验证构建）
- 运行库：`aiohttp`（见 requirements.txt）

## 步骤

>[!tip]
> 
> 其实有不懂的地方可以多问问 `AI` ，推荐 `ChatGPT`，一般情况下它能够解决你大部分的问题。

1. 我的 `Python` 版本为 3.11 ，估计其他版本也行。
2. 安装必要的依赖 
   
```bash
pip install -r requirements.txt
```

1. 具体的抓包步骤，可以参考[该内容](https://github.com/AaronZSAM101/CampusNetworkConnection/blob/main/README.md)。
   
2. 抓到包后，将 `config.example.json` 复制为 `config.json`，并把你的学号、加密后的密码、JSESSIONID、运营商等信息填入对应字段；`config.json` 已加入 `.gitignore`，不要把真实机密提交到仓库。

3. 当上面的脚本编写完成后，打包成 `.exe` 文件，然后将该 `.exe` 添加到计划任务里面。具体操作如下：

   要将 `.exe` 文件添加到计划任务中，可以通过 Windows 的任务计划程序实现。以下是具体操作方法：
   
   将 `.exe` 文件设置为开机启动有以下几种方法：
   
   
   ### 方法一：使用任务计划程序设置开机启动
   
   ### 方法二：使用第三方工具

## 最后

> [!tip] 
> 
>  - 确保 `.exe` 文件路径正确。
>  - 开机启动的程序需要有管理员权限，可能会弹出 UAC 提示。

**完成后，就可以开机自动连接校园网。**
