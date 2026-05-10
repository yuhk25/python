"""
CodeGenius Agent 配置文件
"""

# Token预算配置
TOKEN_CONFIG = {
    'performance_agent': 2000,
    'security_agent': 2000,
    'maintainability_agent': 1500,
    'testability_agent': 1000,
    'total_budget': 100000  # 单次批量审查总预算
}

# 企业客户配置（支持100+客户）
CUSTOMER_CONFIG = {
    'basic': {
        'name': '基础版',
        'max_files': 100,
        'max_tokens': 10000,
        'price': '¥999/月'
    },
    'professional': {
        'name': '专业版',
        'max_files': 1000,
        'max_tokens': 100000,
        'price': '¥9999/月'
    },
    'enterprise': {
        'name': '企业版',
        'max_files': 10000,
        'max_tokens': 1000000,
        'price': '¥99999/月'
    }
}

# 代码质量维度权重
QUALITY_WEIGHTS = {
    'security': 25,      # 安全性最重要
    'performance': 20,   # 性能
    'maintainability': 20,  # 可维护性
    'testability': 15,   # 可测试性
    'reliability': 10,   # 可靠性
    'scalability': 10    # 可扩展性
}

# 问题严重程度定义
SEVERITY_LEVELS = {
    'critical': {
        'score_deduction': 20,
        'description': '严重问题，必须立即修复'
    },
    'high': {
        'score_deduction': 10,
        'description': '高风险问题，应尽快修复'
    },
    'medium': {
        'score_deduction': 5,
        'description': '中等问题，建议修复'
    },
    'low': {
        'score_deduction': 2,
        'description': '低风险问题，可选修复'
    }
}

# 效率指标
EFFICIENCY_METRICS = {
    'manual_review_cost_per_file': 500,  # 人工审查成本（元）
    'token_cost_per_unit': 0.01,  # Token成本（元/个）
    'target_efficiency_score': 85,  # 目标效率分数
}

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'codegenius.log'
}

# API限流配置
RATE_LIMIT_CONFIG = {
    'enabled': True,
    'requests_per_minute': 60,
    'burst_size': 100
}