from pydantic import BaseSettings
from typing import Dict, List, Optional

class TestConfig(BaseSettings):
    """测试配置类"""
    
    # 测试数据路径
    TEST_DATA_DIR: str = "data/raw"
    PROCESSED_DATA_DIR: str = "data/processed"
    
    # 测试模型配置
    MODELS: Dict[str, Dict] = {
        "default": {
            "name": "default_model",
            "version": "1.0.0",
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 1000
            }
        }
    }
    
    # 测试指标配置
    METRICS: List[str] = [
        "accuracy",
        "response_time",
        "token_usage",
        "cost"
    ]
    
    # 性能测试配置
    PERFORMANCE_TEST: Dict = {
        "concurrent_users": 10,
        "duration_seconds": 300,
        "ramp_up_time": 60
    }
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/test.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True 