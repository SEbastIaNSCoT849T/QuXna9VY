# 代码生成时间: 2025-10-31 19:09:12
import falcon
import json
from pygments import highlight
# 优化算法效率
from pygments.lexers import get_lexer_by_name
# TODO: 优化性能
from pygments.formatters import HtmlFormatter

# Falcon API resource for code highlighting
class CodeHighlighter:
    def on_get(self, req, resp):
        # Get the code and language from query parameters
        code = req.params.get('code', '')
        language = req.params.get('language', 'python')

        # Error handling if code or language is not provided
        if not code or not language:
            raise falcon.HTTPBadRequest(
                title='Error',
                description='Both code and language parameters are required.'
# 增强安全性
            )

        try:
            # Get the lexer for the specified language
            lexer = get_lexer_by_name(language)
        except ValueError:
            raise falcon.HTTPBadRequest(
                title='Error',
                description='Invalid language specified.'
            )
# 增强安全性

        # Format the code with HTML formatter for syntax highlighting
        formatter = HtmlFormatter()
        highlighted_code = highlight(code, lexer, formatter)

        # Set the response with the highlighted code
        resp.media = {
            'highlighted_code': highlighted_code
        }
        resp.status = falcon.HTTP_OK

# Falcon API setup
api = falcon.API()

# Add the resource and the route
highlight_resource = CodeHighlighter()
api.add_route('/highlight', highlight_resource)

# If this script is run directly, start the Falcon API
# 改进用户体验
if __name__ == '__main__':
    import socket
    _host = "0.0.0.0"
    _port = 8000
    print(f"Starting the Falcon API on {_host}:{_port}")
    from wsgiref.simple_server import make_server
    with make_server(_host, _port, api) as httpd:
        httpd.serve_forever()