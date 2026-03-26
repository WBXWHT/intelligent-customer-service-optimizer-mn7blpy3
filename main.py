import json
import random
import datetime
from typing import List, Dict, Tuple

class IntelligentCustomerService:
    """智能客服助手核心类"""
    
    def __init__(self):
        # 模拟微调后的模型知识库
        self.knowledge_base = {
            "账户问题": ["请提供您的账户ID，我将为您查询", "账户问题通常需要验证身份"],
            "支付问题": ["支付失败可能是网络问题，请重试", "检查银行卡余额和支付限额"],
            "技术故障": ["请描述具体错误信息", "尝试重启应用或清除缓存"],
            "产品咨询": ["我们提供AI助手和数据分析服务", "具体需求可以查看官网文档"]
        }
        # 对话历史记录
        self.conversation_history: List[Dict] = []
        # 纠错机制阈值
        self.error_correction_threshold = 2
        
    def simulate_llm_response(self, user_input: str) -> str:
        """模拟大模型生成回复（实际项目中会调用真实API）"""
        
        # 意图识别
        intent = self._recognize_intent(user_input)
        
        # 多轮对话纠错机制
        if self._needs_error_correction(user_input):
            return "我注意到您多次询问类似问题，让我重新梳理一下：您的主要需求是什么？"
        
        # 从知识库获取回复
        if intent in self.knowledge_base:
            responses = self.knowledge_base[intent]
            response = random.choice(responses)
        else:
            response = "这个问题我需要进一步学习，已为您转接详细文档。"
            
        # 记录对话
        self._record_conversation(user_input, response, intent)
        
        return response
    
    def _recognize_intent(self, text: str) -> str:
        """识别用户意图（简化版）"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["账户", "登录", "注册"]):
            return "账户问题"
        elif any(word in text_lower for word in ["支付", "付款", "收费"]):
            return "支付问题"
        elif any(word in text_lower for word in ["错误", "故障", "无法"]):
            return "技术故障"
        elif any(word in text_lower for word in ["功能", "服务", "产品"]):
            return "产品咨询"
        else:
            return "其他问题"
    
    def _needs_error_correction(self, current_input: str) -> bool:
        """检查是否需要触发纠错机制"""
        if len(self.conversation_history) < self.error_correction_threshold:
            return False
            
        # 检查最近几次对话是否相似
        recent_intents = [
            msg.get("intent", "") 
            for msg in self.conversation_history[-self.error_correction_threshold:]
        ]
        
        # 如果最近几次意图相同，触发纠错
        if len(set(recent_intents)) == 1:
            return True
            
        return False
    
    def _record_conversation(self, user_input: str, response: str, intent: str):
        """记录对话历史"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.conversation_history.append({
            "timestamp": timestamp,
            "user_input": user_input,
            "response": response,
            "intent": intent,
            "turn": len(self.conversation_history) + 1
        })
        
        # 保持最近10轮对话
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def get_conversation_stats(self) -> Dict:
        """获取对话统计信息"""
        if not self.conversation_history:
            return {"total_turns": 0, "resolved_rate": 0.0}
            
        # 计算问题解决率（模拟）
        resolved_turns = sum(1 for msg in self.conversation_history 
                           if msg["intent"] != "其他问题")
        total_turns = len(self.conversation_history)
        
        return {
            "total_turns": total_turns,
            "resolved_rate": round(resolved_turns / total_turns * 100, 1),
            "last_intent": self.conversation_history[-1]["intent"] if self.conversation_history else None
        }

def simulate_user_interaction():
    """模拟用户与客服的交互"""
    print("=" * 50)
    print("智能客服助手优化系统 v1.0")
    print("=" * 50)
    print("说明：输入'退出'结束对话，输入'统计'查看对话数据\n")
    
    cs = IntelligentCustomerService()
    
    # 模拟测试用例
    test_cases = [
        "我的账户登录不了",
        "还是登不上去",
        "支付功能怎么用",
        "支付失败了",
        "有什么产品服务"
    ]
    
    for i, user_input in enumerate(test_cases):
        print(f"\n[用户第{i+1}轮]: {user_input}")
        
        # 获取AI回复
        response = cs.simulate_llm_response(user_input)
        print(f"[AI助手]: {response}")
        
        # 模拟纠错机制触发
        if i == 2:  # 第三轮时显示统计
            stats = cs.get_conversation_stats()
            print(f"\n[系统提示]: 当前问题解决率 {stats['resolved_rate']}%")
    
    # 最终统计
    print("\n" + "=" * 50)
    print("对话结束，生成分析报告：")
    final_stats = cs.get_conversation_stats()
    print(f"总对话轮次: {final_stats['total_turns']}")
    print(f"问题解决率: {final_stats['resolved_rate']}%")
    
    # 模拟优化效果
    baseline_rate = 60.0  # 基线解决率
    improvement = final_stats['resolved_rate'] - baseline_rate
    print(f"相较于基线({baseline_rate}%)提升: {improvement:.1f}%")
    
    if improvement > 0:
        print("✅ 多轮对话纠错机制效果显著！")
    else:
        print("⚠️  需要进一步优化模型")

def main():
    """主函数入口"""
    print("正在启动智能客服助手优化系统...")
    simulate_user_interaction()
    print("\n系统运行完成，感谢使用！")

if __name__ == "__main__":
    main()