import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random

from .dqn_model import DQN
from .memory import ReplayBuffer 

# Các hằng số (Hyperparameters)
GAMMA = 0.99      # Hệ số chiết khấu (Discount Factor)
LR = 1e-4         # Tốc độ học (Learning Rate)
BATCH_SIZE = 64   # Kích thước lô dữ liệu học

# Khởi tạo thiết bị: GPU nếu có, không thì dùng CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class DQNAgent:
    def __init__(self, input_dim, output_dim, capacity):
        
        # 1. Khởi tạo Mạng Q (Q-Network) và Mạng Mục tiêu (Target Network)
        self.policy_net = DQN(input_dim, output_dim).to(device)
        self.target_net = DQN(input_dim, output_dim).to(device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval() # Đặt mạng mục tiêu ở chế độ đánh giá

        # 2. Khởi tạo Bộ nhớ
        self.memory = ReplayBuffer(capacity)
        
        # 3. Khởi tạo Trình tối ưu hóa và Hàm Loss
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=LR)
        self.loss_fn = nn.MSELoss() # Dùng Mean Squared Error Loss(một hàm loss)

        self.output_dim = output_dim

    # --- Phần 1: Ra Quyết Định (Action Selection) ---
    def select_action(self, state, epsilon):
        # Chuyển đổi trạng thái NumPy array -> PyTorch tensor
        state = self.preprocess_state(state)
        
        # Chiến lược Epsilon-Greedy
        if random.random() < epsilon:
            # Khám phá: Chọn hành động ngẫu nhiên
            return random.randrange(self.output_dim)
        else:
            # Khai thác: Chọn hành động có Q-value cao nhất
            with torch.no_grad(): # Không cần tính toán gradient khi ra quyết định
                q_values = self.policy_net(state)
                # Trả về chỉ số hành động có Q-value lớn nhất (0, 1, 2, hoặc 3)
                return q_values.max(1)[1].item() 
                
    # --- Phần 2: Xử Lý Dữ Liệu và Ghi nhớ ---'
    def preprocess_state(self, board_array):
        # Đảm bảo dữ liệu
        if not isinstance(board_array, np.array):
            state=np.array(state)
        #Lấy log2
        processed_state = np.where(state > 0, np.log2(state), 0.0)
        #Làm phẳng 
        processed_state=processed_state.flatten()
        #Chuyển sang tensor
        tensor_state = torch.tensor(processed_state, dtype=torch.float32)
        tensor_state = tensor_state.unsqueeze(0)##unsqueeze là thao tác thêm chiều
        return tensor_state.to(device)


    # --- Phần 3: Học Hỏi (Learning) ---
    def learn(self):
        if len(self.memory) < BATCH_SIZE:
            return # Chưa đủ dữ liệu để học

        # 1. Lấy mẫu ngẫu nhiên từ Buffer
        transitions = self.memory.sample(BATCH_SIZE)
        
        #Lấy mẫu từ states
        states = np.array([t.state for t in transitions])
        next_states = np.array([t.next_state for t in transitions])

        state_batch = torch.tensor(states, dtype=torch.float).to(device)
        next_state_batch = torch.tensor(next_states, dtype=torch.float).to(device) 
        #Lấy mẫu từ action
        actions = [t.action for t in transitions]
        action_batch = torch.tensor(actions, dtype=torch.long).unsqueeze(1).to(device)
        #Lấy mẫu từ reward
        rewards = [t.reward for t in transitions]
        reward_batch = torch.tensor(rewards, dtype=torch.float).unsqueeze(1).to(device)
        done = [t.done for t in transitions]
        done_batch = torch.tensor(done,dtype=torch.float).unsqueeze(1).to(device)
        # [KHÔNG CẦN VIẾT CHI TIẾT]

        # 2. Tính Q_current (Dự đoán hiện tại)
        q_values = self.policy_net(state_batch)#self.policy_net trả về 4 Q values cho trạng thái S
        q_current = q_values.gather(1, action_batch)#Hàm gather tạo tensor mới từ việc lựa chọn các phần tử cũ từ tensor cũ theo chỉ số
        
        # 3. Tính Q_target (Mục tiêu)
        #Lấy max Q value của state kế tiếp
        next_q_values=self.target_net(next_state_batch).detach()#Detach đảm bảo gradient không lan truyền ngược qua mạng
        max_next_q=next_q_values.max(1)[0].unsqueeze(1)
        #TÍnh target Q 
        q_target = reward_batch + (GAMMA * max_next_q * (1 - done_batch))
        # 4. Tính Loss (Sai số)
        loss = self.loss_fn(q_current, q_target)

        # 5. Cập nhật Mạng
        self.optimizer.zero_grad() # Xóa gradient cũ
        loss.backward()            # Lan truyền ngược
        self.optimizer.step()      # Cập nhật trọng số
        
    def update_target_net(self):
        #Đồng bộ hóa policy_net với target_net định kỳ
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def save_model(self, path):
        self.policy_net.save(path)
        
    def load_model(self, path):
        self.policy_net.load(path)