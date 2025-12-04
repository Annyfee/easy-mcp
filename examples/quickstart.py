import asyncio
import os

from dotenv import load_dotenv
from easy_mcp.bridge import MCPToolLoader


async def main():
    load_dotenv()
    amap_key = os.getenv("AMAP_MAPS_API_KEY")
    if not amap_key:
        raise ValueError("请先在 .env 文件中设置 AMAP_MAPS_API_KEY")
    # 1. 配置MCP服务(只需修改此部分)
    MCP_SERVER_CONFIGS = [
        {
            "name": "高德地图",
            "command": "npx",
            "args": ["-y", "@amap/amap-maps-mcp-server"],
            "env": {**os.environ,"AMAP_MAPS_API_KEY":amap_key}
        }
        # {...}  之后MCP工具可随需求扩展增加
    ]

    # 2. 一行加载所有工具(自动管理子进程生命周期)
    async with MCPToolLoader(MCP_SERVER_CONFIGS) as tools:
        # 3. 找到文本搜索工具
        text_search_tool = next(t for t in tools if t.name == "maps_text_search")
        result = await text_search_tool.ainvoke({
            "keywords":"西湖"
        })
        print("🔎 查询结果:",result[:300])

if __name__ == '__main__':
    asyncio.run(main())
