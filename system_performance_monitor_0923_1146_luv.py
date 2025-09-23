# 代码生成时间: 2025-09-23 11:46:43
import falcon
import psutil
import json
from falcon import Request, Response

# 系统监控资源类
class SystemMonitor:
    def on_get(self, req: Request, resp: Response):
        """
        GET请求处理器，返回系统的当前性能指标。
        """
        try:
            # 收集CPU使用率
            cpu_usage = psutil.cpu_percent(interval=None)
            # 收集内存使用情况
            memory_info = psutil.virtual_memory()
            # 收集磁盘使用情况
            disk_info = psutil.disk_usage('/')
            # 收集网络信息
            net_io_info = psutil.net_io_counters()
            
            # 构建响应体
            system_data = {
                'CPU Usage': cpu_usage,
                'Memory': {
                    'Total': memory_info.total,
                    'Available': memory_info.available,
                    'Used': memory_info.used,
                    'Percentage': memory_info.percent
                },
                'Disk': {
                    'Total': disk_info.total,
                    'Available': disk_info.free,
                    'Used': disk_info.used,
                    'Percentage': disk_info.percent
                },
                'Network IO': {
                    'Bytes Sent': net_io_info.bytes_sent,
                    'Bytes Received': net_io_info.bytes_recv,
                    'Packets Sent': net_io_info.packets_sent,
                    'Packets Received': net_io_info.packets_recv
                }
            }
            
            # 设置响应体和状态码
            resp.media = system_data
            resp.status = falcon.HTTP_200
        except Exception as e:
            # 错误处理
            resp.media = {'error': str(e)}
            resp.status = falcon.HTTP_500

# 创建Falcon应用
app = falcon.App()

# 添加路由
app.add_route('/', SystemMonitor())

# 运行应用
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='System Performance Monitor')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port)