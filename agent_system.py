"""
CodeGenius Agent System - 智能代码审查与优化平台
核心Agent协作引擎
"""

import json
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
from abc import ABC, abstractmethod


class CodeQualityDimension(Enum):
    """代码质量20+维度"""
    PERFORMANCE = "performance"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"
    SCALABILITY = "scalability"
    RELIABILITY = "reliability"
    TESTABILITY = "testability"
    DOCUMENTATION = "documentation"
    CODE_SMELL = "code_smell"
    COMPLEXITY = "complexity"
    DUPLICATE_CODE = "duplicate_code"
    NAMING_CONVENTION = "naming_convention"
    ERROR_HANDLING = "error_handling"
    LOGGING = "logging"
    MEMORY_LEAK = "memory_leak"
    THREAD_SAFETY = "thread_safety"
    API_DESIGN = "api_design"
    DEPENDENCY = "dependency"
    CONFIG_HARDCODE = "config_hardcode"
    SQL_INJECTION = "sql_injection"
    XSS_VULNERABILITY = "xss_vulnerability"


@dataclass
class CodeIssue:
    """代码问题定义"""
    dimension: CodeQualityDimension
    severity: str  # critical, high, medium, low
    line: int
    description: str
    suggestion: str
    token_cost: int


@dataclass
class ReviewResult:
    """审查结果"""
    file_path: str
    total_issues: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    efficiency_score: float  # 0-100
    issues: List[CodeIssue]
    review_timestamp: str
    total_tokens_used: int


class BaseAgent(ABC):
    """Agent基类"""
    
    def __init__(self, agent_name: str, token_budget: int = 1000):
        self.agent_name = agent_name
        self.token_budget = token_budget
        self.tokens_used = 0
    
    @abstractmethod
    def analyze(self, code: str) -> List[CodeIssue]:
        """分析代码"""
        pass
    
    def _estimate_token_cost(self, content: str) -> int:
        """估计Token消耗"""
        return len(content) // 4 + 10
    
    def can_analyze(self, code: str) -> bool:
        """检查是否有足够的token预算"""
        estimated_cost = self._estimate_token_cost(code)
        return self.tokens_used + estimated_cost <= self.token_budget


class PerformanceAgent(BaseAgent):
    """性能分析Agent"""
    
    def __init__(self):
        super().__init__("PerformanceAgent", token_budget=2000)
    
    def analyze(self, code: str) -> List[CodeIssue]:
        """分析性能问题"""
        issues = []
        lines = code.split('\n')
        
        # 检测 O(n²) 嵌套循环
        for i, line in enumerate(lines):
            if 'for' in line and i < len(lines) - 1:
                if 'for' in lines[i + 1]:
                    issues.append(CodeIssue(
                        dimension=CodeQualityDimension.PERFORMANCE,
                        severity="high",
                        line=i + 1,
                        description="检测到嵌套循环，可能存在性能问题",
                        suggestion="考虑使用更优的算法或数据结构，如Hash表、二分查找等",
                        token_cost=50
                    ))
            
            # 检测 N+1 查询问题
            if 'for' in line and 'query' in line.lower():
                issues.append(CodeIssue(
                    dimension=CodeQualityDimension.PERFORMANCE,
                    severity="high",
                    line=i + 1,
                    description="循环中存在数据库查询，可能导致N+1问题",
                    suggestion="将查询操作移出循环，使用批量查询或JOIN操作",
                    token_cost=50
                ))
            
            # 检测 memory leak 风险
            if 'new ' in line and 'delete' not in code:
                issues.append(CodeIssue(
                    dimension=CodeQualityDimension.MEMORY_LEAK,
                    severity="medium",
                    line=i + 1,
                    description="未找到对应的资源释放操作",
                    suggestion="确保所有申请的资源都被正确释放",
                    token_cost=40
                ))
        
        self.tokens_used += sum(issue.token_cost for issue in issues)
        return issues


class SecurityAgent(BaseAgent):
    """安全分析Agent"""
    
    def __init__(self):
        super().__init__("SecurityAgent", token_budget=2000)
    
    def analyze(self, code: str) -> List[CodeIssue]:
        """分析安全问题"""
        issues = []
        lines = code.split('\n')
        
        # SQL注入检测
        for i, line in enumerate(lines):
            if 'select' in line.lower() and '+' in line:
                issues.append(CodeIssue(
                    dimension=CodeQualityDimension.SQL_INJECTION,
                    severity="critical",
                    line=i + 1,
                    description="检测到字符串拼接SQL，存在SQL注入风险",
                    suggestion="使用参数化查询或ORM框架",
                    token_cost=100
                ))
            
            # XSS检测
            if 'html' in line.lower() and 'input' in line.lower():
                issues.append(CodeIssue(
                    dimension=CodeQualityDimension.XSS_VULNERABILITY,
                    severity="critical",
                    line=i + 1,
                    description="检测到未转义的用户输入插入HTML",
                    suggestion="对用户输入进行转义或使用安全的模板引擎",
                    token_cost=100
                ))
            
            # 硬编码配置
            if 'password' in line.lower() and '=' in line and '"' in line:
                issues.append(CodeIssue(
                    dimension=CodeQualityDimension.CONFIG_HARDCODE,
                    severity="critical",
                    line=i + 1,
                    description="检测到硬编码的敏感信息（密码）",
                    suggestion="将敏感信息移至环境变量或配置管理系统",
                    token_cost=100
                ))
        
        self.tokens_used += sum(issue.token_cost for issue in issues)
        return issues


class MaintainabilityAgent(BaseAgent):
    """可维护性分析Agent"""
    
    def __init__(self):
        super().__init__("MaintainabilityAgent", token_budget=1500)
    
    def analyze(self, code: str) -> List[CodeIssue]:
        """分析可维护性问题"""
        issues = []
        lines = code.split('\n')
        
        # 检测注释不足
        comment_ratio = code.count('#') / len(lines) if lines else 0
        if comment_ratio < 0.1:
            issues.append(CodeIssue(
                dimension=CodeQualityDimension.DOCUMENTATION,
                severity="medium",
                line=1,
                description=f"注释比例过低 ({comment_ratio:.1%})",
                suggestion="添加更多的代码注释，说明复杂逻辑的意图",
                token_cost=30
            ))
        
        # 检测命名规范
        for i, line in enumerate(lines):
            if 'def ' in line or 'class ' in line:
                words = line.split()
                for word in words:
                    if '_' not in word and word.islower() and len(word) > 1:
                        if any(c.isupper() for c in word):
                            issues.append(CodeIssue(
                                dimension=CodeQualityDimension.NAMING_CONVENTION,
                                severity="low",
                                line=i + 1,
                                description="混合大小写命名不符合Python规范",
                                suggestion="使用snake_case命名方式",
                                token_cost=20
                            ))
                            break
        
        # 检测函数长度
        for i, line in enumerate(lines):
            if 'def ' in line:
                func_start = i
                func_lines = 0
                for j in range(i + 1, len(lines)):
                    if lines[j] and not lines[j][0].isspace():
                        break
                    func_lines += 1
                
                if func_lines > 50:
                    issues.append(CodeIssue(
                        dimension=CodeQualityDimension.COMPLEXITY,
                        severity="medium",
                        line=i + 1,
                        description=f"函数过长 ({func_lines} 行)",
                        suggestion="将大型函数拆分为更小的可测试单元",
                        token_cost=40
                    ))
        
        self.tokens_used += sum(issue.token_cost for issue in issues)
        return issues


class TestabilityAgent(BaseAgent):
    """可测试性分析Agent"""
    
    def __init__(self):
        super().__init__("TestabilityAgent", token_budget=1000)
    
    def analyze(self, code: str) -> List[CodeIssue]:
        """分析可测试性问题"""
        issues = []
        
        # 检测错误处理
        if 'except' not in code:
            issues.append(CodeIssue(
                dimension=CodeQualityDimension.ERROR_HANDLING,
                severity="high",
                line=1,
                description="未发现异常处理代码",
                suggestion="添加try-except块处理可能的错误情况",
                token_cost=50
            ))
        
        # 检测日志
        if 'log' not in code.lower():
            issues.append(CodeIssue(
                dimension=CodeQualityDimension.LOGGING,
                severity="medium",
                line=1,
                description="缺少日志记录",
                suggestion="添加日志记录以便调试和监控",
                token_cost=30
            ))
        
        self.tokens_used += sum(issue.token_cost for issue in issues)
        return issues


class CodeReviewOrchestrator:
    """代码审查协调器 - 管理多个Agent的协作"""
    
    def __init__(self, token_plan_budget: int = 10000):
        self.agents: List[BaseAgent] = [
            PerformanceAgent(),
            SecurityAgent(),
            MaintainabilityAgent(),
            TestabilityAgent()
        ]
        self.token_plan_budget = token_plan_budget
        self.tokens_spent = 0
    
    def _optimize_token_usage(self, code: str) -> List[BaseAgent]:
        """智能Token优化 - 根据代码复杂度分配agent"""
        code_complexity = len(code) // 100
        priority_agents = []
        
        # 优先级：安全 > 性能 > 可维护性 > 可测试性
        agent_priority = {
            "SecurityAgent": 1,
            "PerformanceAgent": 2,
            "MaintainabilityAgent": 3,
            "TestabilityAgent": 4
        }
        
        sorted_agents = sorted(
            self.agents,
            key=lambda a: agent_priority.get(a.agent_name, 999)
        )
        
        remaining_budget = self.token_plan_budget - self.tokens_spent
        
        for agent in sorted_agents:
            if agent.tokens_used < agent.token_budget and remaining_budget > 0:
                priority_agents.append(agent)
                remaining_budget -= agent.token_budget // 2
        
        return priority_agents
    
    def review(self, file_path: str, code: str) -> ReviewResult:
        """执行代码审查"""
        all_issues = []
        total_tokens = 0
        
        # 获取优化后的agent列表
        active_agents = self._optimize_token_usage(code)
        
        # 并行执行多个Agent分析
        for agent in active_agents:
            if agent.can_analyze(code):
                agent_issues = agent.analyze(code)
                all_issues.extend(agent_issues)
                total_tokens += agent.tokens_used
        
        self.tokens_spent += total_tokens
        
        # 统计问题
        critical = sum(1 for issue in all_issues if issue.severity == "critical")
        high = sum(1 for issue in all_issues if issue.severity == "high")
        medium = sum(1 for issue in all_issues if issue.severity == "medium")
        low = sum(1 for issue in all_issues if issue.severity == "low")
        
        # 计算效率分数 (0-100)
        efficiency_score = max(0, 100 - (critical * 20 + high * 10 + medium * 5 + low * 2))
        
        # 对问题按严重程度排序
        all_issues.sort(key=lambda x: {
            "critical": 0,
            "high": 1,
            "medium": 2,
            "low": 3
        }.get(x.severity, 4))
        
        return ReviewResult(
            file_path=file_path,
            total_issues=len(all_issues),
            critical_count=critical,
            high_count=high,
            medium_count=medium,
            low_count=low,
            efficiency_score=efficiency_score,
            issues=all_issues,
            review_timestamp=datetime.now().isoformat(),
            total_tokens_used=total_tokens
        )


class BatchReviewManager:
    """批量审查管理器 - 支持100+企业客户"""
    
    def __init__(self):
        self.orchestrator = CodeReviewOrchestrator(token_plan_budget=100000)
        self.review_history: List[ReviewResult] = []
    
    def review_multiple_files(self, files: Dict[str, str]) -> Dict[str, ReviewResult]:
        """审查多个文件"""
        results = {}
        
        for file_path, code in files.items():
            result = self.orchestrator.review(file_path, code)
            results[file_path] = result
            self.review_history.append(result)
        
        return results
    
    def get_summary_report(self) -> Dict[str, Any]:
        """生成汇总报告"""
        if not self.review_history:
            return {}
        
        total_files = len(self.review_history)
        total_issues = sum(r.total_issues for r in self.review_history)
        total_critical = sum(r.critical_count for r in self.review_history)
        avg_efficiency = sum(r.efficiency_score for r in self.review_history) / total_files
        total_tokens = sum(r.total_tokens_used for r in self.review_history)
        
        # 计算成本节省（假设人工审查成本）
        manual_review_cost_per_file = 500  # 元
        automated_cost = total_tokens * 0.01  # Token成本
        cost_saved = (total_files * manual_review_cost_per_file - automated_cost)
        
        return {
            "total_files_reviewed": total_files,
            "total_issues_found": total_issues,
            "critical_issues": total_critical,
            "average_efficiency_score": round(avg_efficiency, 2),
            "total_tokens_used": total_tokens,
            "estimated_cost_saved": f"¥{cost_saved:,.0f}",
            "efficiency_improvement": f"{((total_files * 100 - total_critical * 5) / (total_files * 100)) * 100:.1f}%"
        }


# ============ 使用示例 ============

if __name__ == "__main__":
    # 示例代码
    sample_code = """
def process_user_data(user_id):
    for i in range(100):
        for j in range(100):
            query = "SELECT * FROM users WHERE id = " + str(user_id)
            result = db.query(query)
    
    password = "admin123"
    
    html_output = "<div>" + user_input + "</div>"
    
    new Resource()
    
    return result
"""
    
    # 创建批量审查管理器
    manager = BatchReviewManager()
    
    # 审查多个文件
    files_to_review = {
        "main.py": sample_code,
        "utils.py": "def helper():\n    pass",
        "config.py": "API_KEY = 'secret_key_12345'"
    }
    
    results = manager.review_multiple_files(files_to_review)
    
    # 输出结果
    print("=" * 80)
    print("CodeGenius Agent - 智能代码审查报告")
    print("=" * 80)
    
    for file_path, result in results.items():
        print(f"\n📄 文件: {file_path}")
        print(f"   总问题数: {result.total_issues}")
        print(f"   严重级别: {result.critical_count}个严重 | {result.high_count}个高危 | {result.medium_count}个中等 | {result.low_count}个低风险")
        print(f"   效率分数: {result.efficiency_score:.1f}/100")
        print(f"   Token消耗: {result.total_tokens_used}")
        
        if result.issues:
            print(f"   \n   问题详情:")
            for issue in result.issues[:5]:  # 显示前5个问题
                print(f"     - [行{issue.line}] {issue.dimension.value}: {issue.description}")
                print(f"       建议: {issue.suggestion}")
    
    # 输出汇总报告
    print("\n" + "=" * 80)
    print("📊 汇总报告")
    print("=" * 80)
    summary = manager.get_summary_report()
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    # 输出为JSON格式
    print("\n" + "=" * 80)
    print("JSON导出结果：")
    print("=" * 80)
    json_results = {
        file_path: {
            "file_path": result.file_path,
            "total_issues": result.total_issues,
            "critical_count": result.critical_count,
            "high_count": result.high_count,
            "medium_count": result.medium_count,
            "low_count": result.low_count,
            "efficiency_score": result.efficiency_score,
            "total_tokens_used": result.total_tokens_used,
            "review_timestamp": result.review_timestamp,
            "issues": [
                {
                    "dimension": issue.dimension.value,
                    "severity": issue.severity,
                    "line": issue.line,
                    "description": issue.description,
                    "suggestion": issue.suggestion
                }
                for issue in result.issues
            ]
        }
        for file_path, result in results.items()
    }
    print(json.dumps(json_results, indent=2, ensure_ascii=False))