"""
CodeGenius Agent Web应用 - REST API服务
支持100+企业客户，提供Web界面和API接口
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from agent_system import BatchReviewManager, ReviewResult
import json
from datetime import datetime


app = Flask(__name__)
CORS(app)

# 初始化审查管理器
manager = BatchReviewManager()

# 存储客户信息
customers = {}
review_quota = {}  # 客户审查配额


# ============ Web 页面 ============

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeGenius Agent - 智能代码审查平台</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        .section h2 {
            color: #333;
            margin-bottom: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
        }
        
        textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            resize: vertical;
            min-height: 200px;
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .results {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .result-card {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 5px;
        }
        
        .result-card h3 {
            color: #333;
            margin-bottom: 15px;
        }
        
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .metric:last-child {
            border-bottom: none;
        }
        
        .metric-label {
            color: #666;
        }
        
        .metric-value {
            font-weight: bold;
            color: #667eea;
        }
        
        .critical {
            color: #ff4757;
        }
        
        .high {
            color: #ff6b35;
        }
        
        .medium {
            color: #ffa502;
        }
        
        .low {
            color: #26a745;
        }
        
        .issues-list {
            margin-top: 20px;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .issue-item {
            background: white;
            padding: 12px;
            margin-bottom: 10px;
            border-left: 3px solid;
            border-radius: 3px;
        }
        
        .issue-item.critical {
            border-left-color: #ff4757;
        }
        
        .issue-item.high {
            border-left-color: #ff6b35;
        }
        
        .issue-item.medium {
            border-left-color: #ffa502;
        }
        
        .issue-item.low {
            border-left-color: #26a745;
        }
        
        .issue-title {
            font-weight: bold;
            margin-bottom: 5px;
            font-size: 14px;
        }
        
        .issue-desc {
            font-size: 12px;
            color: #666;
            margin-bottom: 3px;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .stat-label {
            font-size: 14px;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 CodeGenius Agent</h1>
            <p>智能代码审查与优化平台 - 企业级AI驱动系统</p>
        </div>
        
        <div class="content">
            <!-- 统计数据 -->
            <div class="section">
                <h2>📊 平台统计</h2>
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-number" id="filesReviewed">0</div>
                        <div class="stat-label">已审查文件</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number" id="issuesFound">0</div>
                        <div class="stat-label">发现问题</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number" id="efficiencyRate">0%</div>
                        <div class="stat-label">平均效率分数</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number" id="costSaved">¥0</div>
                        <div class="stat-label">预估成本节省</div>
                    </div>
                </div>
            </div>
            
            <!-- 代码输入 -->
            <div class="section">
                <h2>💻 代码审查</h2>
                <div class="form-group">
                    <label for="filename">文件名:</label>
                    <input type="text" id="filename" placeholder="e.g., main.py" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                </div>
                <div class="form-group">
                    <label for="code">代码内容:</label>
                    <textarea id="code" placeholder="粘贴您的代码..."></textarea>
                </div>
                <button onclick="reviewCode()">开始审查</button>
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>AI正在分析代码...</p>
                </div>
            </div>
            
            <!-- 审查结果 -->
            <div class="section" id="resultsSection" style="display: none;">
                <h2>✅ 审查结果</h2>
                <div class="results" id="results"></div>
            </div>
        </div>
    </div>
    
    <script>
        function reviewCode() {
            const filename = document.getElementById('filename').value || 'code.py';
            const code = document.getElementById('code').value;
            
            if (!code.trim()) {
                alert('请输入代码');
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            
            fetch('/api/review', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filename: filename,
                    code: code
                })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('loading').style.display = 'none';
                displayResults(data);
                updateStats();
            })
            .catch(error => {
                document.getElementById('loading').style.display = 'none';
                alert('审查失败: ' + error);
            });
        }
        
        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';
            
            const result = data.result;
            
            let issuesHTML = '';
            result.issues.forEach(issue => {
                issuesHTML += `
                    <div class="issue-item ${issue.severity}">
                        <div class="issue-title">[${issue.line}行] ${issue.dimension} - ${issue.severity}</div>
                        <div class="issue-desc">${issue.description}</div>
                        <div class="issue-desc">💡 ${issue.suggestion}</div>
                    </div>
                `;
            });
            
            const card = document.createElement('div');
            card.className = 'result-card';
            card.innerHTML = `
                <h3>${result.file_path}</h3>
                <div class="metric">
                    <span class="metric-label">总问题数</span>
                    <span class="metric-value">${result.total_issues}</span>
                </div>
                <div class="metric">
                    <span class="metric-label critical">严重问题</span>
                    <span class="metric-value critical">${result.critical_count}</span>
                </div>
                <div class="metric">
                    <span class="metric-label high">高危问题</span>
                    <span class="metric-value high">${result.high_count}</span>
                </div>
                <div class="metric">
                    <span class="metric-label medium">中等问题</span>
                    <span class="metric-value medium">${result.medium_count}</span>
                </div>
                <div class="metric">
                    <span class="metric-label low">低风险问题</span>
                    <span class="metric-value low">${result.low_count}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">效率分数</span>
                    <span class="metric-value">${result.efficiency_score.toFixed(1)}/100</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Token消耗</span>
                    <span class="metric-value">${result.total_tokens_used}</span>
                </div>
                <div class="issues-list">
                    ${issuesHTML || '<p style="color:#999;">没有发现问题</p>'}
                </div>
            `;
            
            resultsDiv.appendChild(card);
            document.getElementById('resultsSection').style.display = 'block';
        }
        
        function updateStats() {
            fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                document.getElementById('filesReviewed').textContent = data.total_files_reviewed || 0;
                document.getElementById('issuesFound').textContent = data.total_issues_found || 0;
                document.getElementById('efficiencyRate').textContent = (data.average_efficiency_score || 0).toFixed(1) + '%';
                document.getElementById('costSaved').textContent = data.estimated_cost_saved || '¥0';
            });
        }
        
        // 初始化统计
        updateStats();
    </script>
</body>
</html>
"""


# ============ REST API 端点 ============

@app.route('/')
def index():
    """主页"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/review', methods=['POST'])
def api_review():
    """代码审查API"""
    data = request.json
    filename = data.get('filename', 'code.py')
    code = data.get('code', '')
    
    if not code:
        return jsonify({'error': '代码不能为空'}), 400
    
    # 执行审查
    result = manager.orchestrator.review(filename, code)
    
    # 转换为JSON序列化格式
    return jsonify({
        'success': True,
        'result': {
            'file_path': result.file_path,
            'total_issues': result.total_issues,
            'critical_count': result.critical_count,
            'high_count': result.high_count,
            'medium_count': result.medium_count,
            'low_count': result.low_count,
            'efficiency_score': result.efficiency_score,
            'total_tokens_used': result.total_tokens_used,
            'review_timestamp': result.review_timestamp,
            'issues': [
                {
                    'dimension': issue.dimension.value,
                    'severity': issue.severity,
                    'line': issue.line,
                    'description': issue.description,
                    'suggestion': issue.suggestion,
                    'token_cost': issue.token_cost
                }
                for issue in result.issues
            ]
        }
    })


@app.route('/api/stats', methods=['GET'])
def api_stats():
    """获取统计数据"""
    summary = manager.get_summary_report()
    
    if not summary:
        return jsonify({
            'total_files_reviewed': 0,
            'total_issues_found': 0,
            'average_efficiency_score': 0,
            'estimated_cost_saved': '¥0'
        })
    
    return jsonify(summary)


@app.route('/api/batch-review', methods=['POST'])
def api_batch_review():
    """批量审查API"""
    data = request.json
    files = data.get('files', {})
    
    if not files:
        return jsonify({'error': '文件列表不能为空'}), 400
    
    results = manager.review_multiple_files(files)
    summary = manager.get_summary_report()
    
    return jsonify({
        'success': True,
        'results': {
            file_path: {
                'file_path': result.file_path,
                'total_issues': result.total_issues,
                'critical_count': result.critical_count,
                'high_count': result.high_count,
                'medium_count': result.medium_count,
                'low_count': result.low_count,
                'efficiency_score': result.efficiency_score,
                'total_tokens_used': result.total_tokens_used
            }
            for file_path, result in results.items()
        },
        'summary': summary
    })


@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║     CodeGenius Agent - 智能代码审查平台              ║
    ║     正在启动...                                       ║
    ╚═══════════════════════════════════════════════════════╝
    
    📱 访问地址: http://localhost:5000
    🔌 API文档:
       - POST /api/review         - 审查单个文件
       - POST /api/batch-review   - 批量审查
       - GET  /api/stats          - 获取统计数据
       - GET  /api/health         - 健康检查
    
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)