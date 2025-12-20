import torch
import numpy as np
import math
import time
from agent_dqn import DQNAgent, GAMMA, BATCH_SIZE # Import Agent và các hằng số
# Giả định env.py cung cấp class Game2048
from game_2048 import Game2048 

# --- CÁC HẰNG SỐ VÀ SIÊU THAM SỐ HUẤN LUYỆN ---
NUM_EPISODES = 500000     # Số ván chơi tối đa
MEMORY_CAPACITY = 10000   # Kích thước tối đa của Replay Buffer
TARGET_UPDATE_FREQ = 2000 # Cập nhật Target Net sau X bước
PRINT_INTERVAL = 100      # In kết quả sau X episodes

# Epsilon-Greedy Scheduling
EPS_START = 1.0           # Bắt đầu chơi hoàn toàn ngẫu nhiên
EPS_END = 0.05            # Tối thiểu là 5% ngẫu nhiên
EPS_DECAY = 100000        # Số bước để epsilon giảm từ START đến END

# --- HÀM TÍNH TOÁN CUSTOM REWARD (Đã thảo luận trước đó) ---
def get_custom_reward(state, next_state, reward_goc, done):
    """
    Áp dụng chiến lược Reward Shaping.
    """
    training_reward = 0
    
    # 1. Thưởng Log2 của điểm gốc (để giảm khoảng cách giá trị)
    if reward_goc > 0:
        training_reward += math.log2(reward_goc)
        
    # 2. Thưởng cho các ô trống (khuyến khích giữ bảng thoáng)
    num_empty_tiles = (next_state == 0).sum()
    training_reward += num_empty_tiles * 0.1 
    
    # 3. Phạt nếu hành động không hợp lệ (không di chuyển được)
    if np.array_equal(state, next_state) and not done:
        training_reward -= 1
        
    # 4. Phạt nặng nếu game over
    if done:
        training_reward -= 10 
        
    return training_reward

# --- HÀM TÍNH EPSILON DỰA TRÊN SỐ BƯỚC ĐI ---
def calculate_epsilon(steps_done):
    """
    Epsilon giảm dần theo hàm mũ (Exponential Decay)
    """
    # Tính toán giá trị decay
    epsilon = EPS_END + (EPS_START - EPS_END) * \
              math.exp(-1. * steps_done / EPS_DECAY)
    return epsilon

# --- HÀM CHÍNH CHO QUÁ TRÌNH HUẤN LUYỆN ---
def train_agent():
    
    # Khởi tạo Môi trường và Agent
    env = Game2048()
    # Đầu vào 16 (4x4), Đầu ra 4 (Up, Down, Left, Right)
    agent = DQNAgent(input_dim=16, output_dim=4, capacity=MEMORY_CAPACITY)
    
    steps_done = 0
    max_tile_score = 0
    
    for episode in range(NUM_EPISODES):
        
        state = env.reset() # Bắt đầu ván mới
        done = False
        episode_reward = 0
        
        while not done:
            
            # --- 1. TÍNH TOÁN EPSILON VÀ CHỌN HÀNH ĐỘNG ---
            epsilon = calculate_epsilon(steps_done)
            action = agent.select_action(state, epsilon)
            
            # --- 2. THỰC THI HÀNH ĐỘNG ---
            next_state, reward_goc, done = env.step(action)
            
            # --- 3. REWARD SHAPING VÀ GHI NHỚ ---
            training_reward = get_custom_reward(state, next_state, reward_goc, done)
            agent.memory.push(state, action, training_reward, next_state, done)
            
            # --- 4. HỌC HỎI (TRAINING) ---
            agent.learn()
            
            # Cập nhật trạng thái và số bước
            state = next_state
            episode_reward += reward_goc
            steps_done += 1
            
            # --- 5. CẬP NHẬT MẠNG MỤC TIÊU ---
            if steps_done % TARGET_UPDATE_FREQ == 0:
                agent.update_target_net()

        # --- GHI LẠI KẾT QUẢ VÁN ĐẤU ---
        
        # Lưu điểm cao nhất đã đạt được
        max_tile = np.max(state)
        if max_tile > max_tile_score:
            max_tile_score = max_tile
            agent.save_model("best_dqn_model.pth") # Lưu model khi có điểm cao mới

        # In kết quả sau mỗi PRINT_INTERVAL
        if episode % PRINT_INTERVAL == 0:
            print(f"Episode: {episode}/{NUM_EPISODES} | "
                  f"Steps: {steps_done} | "
                  f"Max Tile: {max_tile_score} | "
                  f"Epsilon: {epsilon:.4f} | "
                  f"Total Reward: {episode_reward}")
            
    print("Huấn luyện hoàn tất!")

if __name__ == '__main__':
    train_agent()